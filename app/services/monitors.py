from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.check_result import CheckResult, CheckStatus
from app.models.monitor import Monitor
from app.schemas.monitor import MonitorSummary
from app.services.stats import uptime_percentage


def monitor_or_none(db: Session, monitor_id: int) -> Monitor | None:
    return db.get(Monitor, monitor_id)


def recent_results(db: Session, monitor_id: int, limit: int = 20) -> list[CheckResult]:
    return list(
        db.scalars(
            select(CheckResult)
            .where(CheckResult.monitor_id == monitor_id)
            .order_by(CheckResult.checked_at.desc())
            .limit(limit)
        )
    )


def list_monitors_with_results(db: Session) -> list[Monitor]:
    return list(
        db.scalars(
            select(Monitor)
            .options(selectinload(Monitor.check_results))
            .order_by(Monitor.created_at.desc())
        )
    )


def summarize_monitor(monitor: Monitor) -> MonitorSummary:
    results = sorted(monitor.check_results, key=lambda item: item.checked_at, reverse=True)
    latest = results[0] if results else None
    return MonitorSummary(
        id=monitor.id,
        name=monitor.name,
        url=monitor.url,
        is_active=monitor.is_active,
        created_at=monitor.created_at,
        updated_at=monitor.updated_at,
        latest_status=latest.status if latest else CheckStatus.UNKNOWN,
        uptime_percentage=uptime_percentage(results),
        latest_http_status_code=latest.http_status_code if latest else None,
        latest_response_time_ms=latest.response_time_ms if latest else None,
        latest_checked_at=latest.checked_at if latest else None,
    )
