"""
Centralized logging configuration for the RAG Chatbot API
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from ..config.settings import settings
from datetime import datetime
import os

def setup_logging():
    """
    Configure logging for the application
    """
    # Set up the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # Clear any existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Create a custom JSON formatter
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
    )
    
    # Create a standard formatter for console
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler for development
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.debug:
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setFormatter(json_formatter)
        console_handler.setLevel(logging.INFO)
    
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if settings.log_level.lower() in ['debug', 'info']:
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        file_handler = logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setFormatter(json_formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
    
    # Update the level of the root logger based on the configured level
    if settings.log_level.lower() == 'debug':
        root_logger.setLevel(logging.DEBUG)
    elif settings.log_level.lower() == 'info':
        root_logger.setLevel(logging.INFO)
    elif settings.log_level.lower() == 'warning':
        root_logger.setLevel(logging.WARNING)
    elif settings.log_level.lower() == 'error':
        root_logger.setLevel(logging.ERROR)
    else:
        root_logger.setLevel(logging.INFO)

# Initialize logging when this module is imported
setup_logging()

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    """
    return logging.getLogger(name)