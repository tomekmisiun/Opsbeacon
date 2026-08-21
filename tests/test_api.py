import httpx
import pytest
from fastapi import HTTPException
from pydantic_core import ValidationError

from app.api.v1 import check_monitor, create_monitor, list_monitors, monitor_history
from app.main import health
from app.models.monitor import Monitor
from app.schemas.monitor import MonitorCreate
from app.services.monitoring import run_http_check
from app.services.stats import uptime_percentage


def test_health(db):
    response = health(db)
    assert response.status_code == 200
    assert response.body == b'{"status":"healthy"}'


def test_create_and_list_monitor(db):
    monitor = create_monitor(MonitorCreate(name="Example", url="https://example.com"), db)
    assert monitor.id is not None

    listing = list_monitors(db)
    assert listing[0].url == "https://example.com"


def test_rejects_unsafe_urls():
    bad_urls = ["ftp://example.com", "http://localhost", "http://127.0.0.1"]
    for url in bad_urls:
        with pytest.raises(ValidationError):
            MonitorCreate(name="Bad", url=url)


def test_manual_check_success(db):
    monitor = Monitor(name="Example", url="https://example.com")
    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    transport = httpx.MockTransport(lambda request: httpx.Response(204))
    with httpx.Client(transport=transport) as http:
        result = run_http_check(db, monitor, client=http)

    assert result.status.value == "UP"
    assert result.http_status_code == 204
    assert result.response_time_ms is not None


def test_manual_check_error(db):
    monitor = Monitor(name="Example", url="https://example.com")
    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    def raise_timeout(request):
        raise httpx.TimeoutException("too slow")

    transport = httpx.MockTransport(raise_timeout)
    with httpx.Client(transport=transport) as http:
        result = run_http_check(db, monitor, client=http)

    assert result.status.value == "DOWN"
    assert result.http_status_code is None
    assert result.error_message == "too slow"


def test_api_manual_check_and_history(db, monkeypatch):
    monitor = create_monitor(MonitorCreate(name="Example", url="https://example.com"), db)

    def fake_check(db, monitor):
        transport = httpx.MockTransport(lambda request: httpx.Response(200))
        with httpx.Client(transport=transport) as http:
            return run_http_check(db, monitor, client=http)

    monkeypatch.setattr("app.api.v1.run_http_check", fake_check)
    response = check_monitor(monitor.id, db)
    assert response.status.value == "UP"

    history = monitor_history(monitor.id, db)
    assert len(history) == 1


def test_missing_monitor_raises_404(db):
    with pytest.raises(HTTPException) as exc:
        check_monitor(999, db)
    assert exc.value.status_code == 404


def test_uptime_calculation(db):
    monitor = Monitor(name="Example", url="https://example.com")
    db.add(monitor)
    db.commit()
    db.refresh(monitor)
    up = httpx.MockTransport(lambda request: httpx.Response(200))
    down = httpx.MockTransport(
        lambda request: (_ for _ in ()).throw(httpx.ConnectError("nope"))
    )
    with httpx.Client(transport=up) as http:
        run_http_check(db, monitor, client=http)
    with httpx.Client(transport=down) as http:
        run_http_check(db, monitor, client=http)

    assert uptime_percentage(monitor.check_results) == 50.0
