"""Custom exceptions for Atlassian integration."""


class AtlassianError(Exception):
    """Base exception for Atlassian-related errors."""
    pass


class AuthenticationError(AtlassianError):
    """Raised when authentication fails."""
    pass


class ConfigurationError(AtlassianError):
    """Raised when configuration is invalid."""
    pass


class APIError(AtlassianError):
    """Raised when API calls fail."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data