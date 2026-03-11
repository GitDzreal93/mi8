"""Custom application exceptions."""


class MI8Exception(Exception):
    """Base exception for MI8 application."""

    def __init__(self, message: str, code: str = "internal_error"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DatabaseException(MI8Exception):
    """Database related exceptions."""

    def __init__(self, message: str):
        super().__init__(message, code="database_error")


class SourceException(MI8Exception):
    """Data source related exceptions."""

    def __init__(self, message: str, source: str = ""):
        self.source = source
        super().__init__(message, code="source_error")


class QuotaException(MI8Exception):
    """Quota related exceptions."""

    def __init__(self, message: str, source: str = ""):
        self.source = source
        super().__init__(message, code="quota_exceeded")


class LLMException(MI8Exception):
    """LLM service related exceptions."""

    def __init__(self, message: str):
        super().__init__(message, code="llm_error")


class AlertException(MI8Exception):
    """Alert system related exceptions."""

    def __init__(self, message: str):
        super().__init__(message, code="alert_error")
