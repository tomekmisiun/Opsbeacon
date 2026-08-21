from app.models.check_result import CheckResult, CheckStatus


def uptime_percentage(results: list[CheckResult]) -> float:
    if not results:
        return 0.0
    up = sum(1 for result in results if result.status == CheckStatus.UP)
    return round((up / len(results)) * 100, 2)


def average_response_time_ms(results: list[CheckResult]) -> int | None:
    values = [result.response_time_ms for result in results if result.response_time_ms is not None]
    return round(sum(values) / len(values)) if values else None
