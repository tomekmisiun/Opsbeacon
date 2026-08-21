from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitor import Monitor
from app.schemas.monitor import CheckResultRead, MonitorCreate, MonitorRead, MonitorSummary
from app.services.monitoring import run_http_check
from app.services.monitors import monitor_or_none, recent_results, summarize_monitor

router = APIRouter(prefix="/api/v1")


@router.get("/monitors", response_model=list[MonitorSummary])
def list_monitors(db: Session = Depends(get_db)) -> list[MonitorSummary]:
    monitors = list(db.scalars(select(Monitor).order_by(Monitor.created_at.desc())))
    for monitor in monitors:
        monitor.check_results = recent_results(db, monitor.id, 100)
    return [summarize_monitor(monitor) for monitor in monitors]


@router.post("/monitors", response_model=MonitorRead, status_code=status.HTTP_201_CREATED)
def create_monitor(payload: MonitorCreate, db: Session = Depends(get_db)) -> Monitor:
    monitor = Monitor(name=payload.name, url=payload.url, is_active=payload.is_active)
    db.add(monitor)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Monitor URL already exists") from exc
    db.refresh(monitor)
    return monitor


@router.get("/monitors/{monitor_id}", response_model=MonitorRead)
def get_monitor(monitor_id: int, db: Session = Depends(get_db)) -> Monitor:
    monitor = monitor_or_none(db, monitor_id)
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return monitor


@router.delete("/monitors/{monitor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_monitor(monitor_id: int, db: Session = Depends(get_db)) -> Response:
    monitor = monitor_or_none(db, monitor_id)
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    db.delete(monitor)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/monitors/{monitor_id}/check", response_model=CheckResultRead)
def check_monitor(monitor_id: int, db: Session = Depends(get_db)) -> CheckResultRead:
    monitor = monitor_or_none(db, monitor_id)
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return run_http_check(db, monitor)


@router.get("/monitors/{monitor_id}/history", response_model=list[CheckResultRead])
def monitor_history(monitor_id: int, db: Session = Depends(get_db)) -> list[CheckResultRead]:
    if monitor_or_none(db, monitor_id) is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return recent_results(db, monitor_id)
