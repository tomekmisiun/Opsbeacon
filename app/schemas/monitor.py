from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.check_result import CheckStatus
from app.services.url_validation import validate_monitor_url


class MonitorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    url: str = Field(min_length=8, max_length=2048)
    is_active: bool = True

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return validate_monitor_url(value)


class CheckResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    monitor_id: int
    status: CheckStatus
    http_status_code: int | None
    response_time_ms: int | None
    error_message: str | None
    checked_at: datetime


class MonitorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MonitorSummary(MonitorRead):
    latest_status: CheckStatus = CheckStatus.UNKNOWN
    uptime_percentage: float = 0.0
    latest_http_status_code: int | None = None
    latest_response_time_ms: int | None = None
    latest_checked_at: datetime | None = None
