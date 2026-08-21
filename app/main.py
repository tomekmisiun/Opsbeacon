from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.v1 import router as api_router
from app.core.config import get_settings
from app.db.session import get_db
from app.models.monitor import Monitor
from app.schemas.monitor import MonitorCreate
from app.services.monitoring import run_http_check
from app.services.monitors import (
    list_monitors_with_results,
    monitor_or_none,
    recent_results,
    summarize_monitor,
)
from app.services.stats import average_response_time_ms, uptime_percentage

app = FastAPI(title="OpsBeacon", version=get_settings().app_version)
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
def health(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        db.execute(text("select 1"))
    except SQLAlchemyError:
        return JSONResponse(status_code=503, content={"status": "unhealthy"})
    return JSONResponse({"status": "healthy"})


@app.get("/version")
def version() -> dict[str, str]:
    settings = get_settings()
    return {
        "version": settings.app_version,
        "commit": settings.git_commit,
        "environment": settings.app_env,
    }


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    summaries = [summarize_monitor(monitor) for monitor in list_monitors_with_results(db)]
    return templates.TemplateResponse("index.html", {"request": request, "monitors": summaries})


@app.post("/monitors")
def create_monitor_form(
    name: str = Form(..., min_length=1, max_length=120),
    url: str = Form(..., min_length=8, max_length=2048),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    payload = MonitorCreate(name=name, url=url)
    db.add(Monitor(name=payload.name, url=payload.url, is_active=payload.is_active))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/monitors/{monitor_id}/check")
def check_monitor_form(monitor_id: int, db: Session = Depends(get_db)) -> RedirectResponse:
    monitor = monitor_or_none(db, monitor_id)
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    run_http_check(db, monitor)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/monitors/{monitor_id}", response_class=HTMLResponse)
def monitor_detail(
    monitor_id: int, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    monitor = monitor_or_none(db, monitor_id)
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    results = recent_results(db, monitor_id, 50)
    monitor.check_results = results
    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "monitor": monitor,
            "summary": summarize_monitor(monitor),
            "results": results,
            "uptime": uptime_percentage(results),
            "avg_response": average_response_time_ms(results),
        },
    )
