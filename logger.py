"""
Structured logging system for Data Alchemy pipeline.
Provides consistent logging format and centralized log management.
"""
import structlog
import sys
from datetime import datetime
from typing import Any, Dict

def configure_logger(level: str = "INFO") -> structlog.BoundLogger:
    """
    Configure structured logger with appropriate processors.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.BoundLogger,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()

# Global logger instance
logger = configure_logger()