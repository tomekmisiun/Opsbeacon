from time import perf_counter

import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.check_result import CheckResult, CheckStatus
from app.models.monitor import Monitor
from app.services.url_validation import validate_monitor_url


def run_http_check(
    db: Session,
    monitor: Monitor,
    client: httpx.Client | None = None,
) -> CheckResult:
    validate_monitor_url(monitor.url)
    owns_client = client is None
    client = client or httpx.Client(
        timeout=get_settings().http_timeout_seconds, follow_redirects=False
    )
    started = perf_counter()
    try:
        response = client.get(monitor.url)
        result = CheckResult(
            monitor_id=monitor.id,
            status=CheckStatus.UP if response.status_code < 400 else CheckStatus.DOWN,
            http_status_code=response.status_code,
            response_time_ms=round((perf_counter() - started) * 1000),
        )
    except (httpx.TimeoutException, httpx.TransportError) as exc:
        result = CheckResult(
            monitor_id=monitor.id,
            status=CheckStatus.DOWN,
            response_time_ms=round((perf_counter() - started) * 1000),
            error_message=str(exc)[:500],
        )
    finally:
        if owns_client:
            client.close()
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
