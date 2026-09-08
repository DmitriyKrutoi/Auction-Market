class DomainError(Exception):
    """Базовое доменное исключение."""

    status_code = 400  # HTTP статус по умолчанию

    def __init__(self, message: str, code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(DomainError):
    """Ошибка валидации данных."""

    status_code = 422

    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class NotFoundError(DomainError):
    """Объект не найден."""

    status_code = 404

    def __init__(self, message: str):
        super().__init__(message, code="not_found")


class InsufficientFundsError(DomainError):
    """Недостаточно средств."""

    status_code = 400

    def __init__(self, message: str = "Недостаточно средств"):
        super().__init__(message, code="insufficient_funds")


class MarketClosedError(DomainError):
    """Рынок закрыт."""

    status_code = 400

    def __init__(self, message: str = "Рынок закрыт"):
        super().__init__(message, code="market_closed")


class EventNotOpenError(DomainError):
    """Событие не открыто."""

    status_code = 400

    def __init__(self, message: str = "Событие не открыто"):
        super().__init__(message, code="event_not_open")


class AlreadyExistsError(DomainError):
    """Объект уже существует."""

    status_code = 409

    def __init__(self, message: str):
        super().__init__(message, code="already_exists")


class InvalidOperationError(DomainError):
    """Недопустимая операция."""

    status_code = 400

    def __init__(self, message: str):
        super().__init__(message, code="invalid_operation")


class UnauthorizedError(DomainError):
    """Не авторизован."""

    status_code = 401

    def __init__(self, message: str = "Не авторизован"):
        super().__init__(message, code="unauthorized")


class ForbiddenError(DomainError):
    """Доступ запрещён."""

    status_code = 403

    def __init__(self, message: str = "Доступ запрещён"):
        super().__init__(message, code="forbidden")


class RateLimitExceededError(DomainError):
    """Превышен лимит запросов."""

    status_code = 429

    def __init__(self, message: str = "Превышен лимит запросов"):
        super().__init__(message, code="rate_limit_exceeded")
