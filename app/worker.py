import logging
import time

from sqlalchemy import select

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.monitor import Monitor
from app.services.monitoring import run_http_check

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("opsbeacon.worker")


def run_once() -> None:
    with SessionLocal() as db:
        monitors = list(db.scalars(select(Monitor).where(Monitor.is_active.is_(True))))
        for monitor in monitors:
            try:
                result = run_http_check(db, monitor)
                logger.info("%s %s %sms", monitor.url, result.status.value, result.response_time_ms)
            except Exception:
                logger.exception("check failed for monitor_id=%s", monitor.id)


def main() -> None:
    interval = get_settings().worker_interval_seconds
    while True:
        run_once()
        time.sleep(interval)


if __name__ == "__main__":
    main()
