class DevilsAdvocateException(Exception):
    """Base exception for Devil's Advocate Panel."""
    def __init__(self, message: str = "Devil's Advocate internal error occurred"):
        self.message = message
        super().__init__(self.message)


class ModelInferenceError(DevilsAdvocateException):
    """Raised when LLM model inference fails."""
    def __init__(self, message: str = "Model inference failed across all fallback providers"):
        super().__init__(message)


class PersistenceError(DevilsAdvocateException):
    """Raised when database storage or retrieval fails."""
    def __init__(self, message: str = "Database persistence operation failed"):
        super().__init__(message)


class MCPToolExecutionError(DevilsAdvocateException):
    """Raised when an MCP connector tool execution fails."""
    def __init__(self, message: str = "MCP tool execution failed"):
        super().__init__(message)
