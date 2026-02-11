"""API Error Handling & Logging"""
import logging
import traceback
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
import json


class LoggerSetup:
    """Configure application logging"""
    
    @staticmethod
    def setup_logger(logger_name: str, log_file: str = "logs/app.log", 
                    level: int = logging.INFO) -> logging.Logger:
        """Setup logger with file and console handlers"""
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Could not create log file: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger


# Initialize global logger
logger = LoggerSetup.setup_logger(__name__)


class APIException(Exception):
    """Base API exception"""
    
    def __init__(self, message: str, status_code: int = 400, 
                 error_type: str = "APIError", details: Dict = None):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.details = details or {}
        self.timestamp = datetime.utcnow()
        
        logger.error(f"{error_type}: {message}", extra={"details": self.details})
        super().__init__(self.message)
    
    def to_dict(self) -> Dict:
        return {
            "error": self.error_type,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class ValidationException(APIException):
    """Validation error"""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, 400, "ValidationError", details)


class AuthenticationException(APIException):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401, "AuthenticationError")


class PermissionException(APIException):
    """Permission/Authorization error"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, 403, "PermissionError")


class ResourceNotFoundException(APIException):
    """Resource not found error"""
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with ID '{identifier}' not found"
        super().__init__(message, 404, "ResourceNotFound", {"resource": resource, "id": identifier})


class ConflictException(APIException):
    """Resource conflict error"""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, 409, "ConflictError", details)


class ExternalAPIException(APIException):
    """External API error"""
    def __init__(self, api_name: str, original_error: str, details: Dict = None):
        message = f"Error from {api_name}: {original_error}"
        super().__init__(message, 502, "ExternalAPIError", details or {"api": api_name})


class RateLimitException(APIException):
    """Rate limit exceeded"""
    def __init__(self, reset_after_seconds: int = 3600):
        message = f"Rate limit exceeded. Try again in {reset_after_seconds} seconds"
        super().__init__(message, 429, "RateLimitExceeded", {"reset_after": reset_after_seconds})


class DatabaseException(APIException):
    """Database error"""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, 500, "DatabaseError", details)


class ServerException(APIException):
    """Internal server error"""
    def __init__(self, message: str = "Internal server error", details: Dict = None):
        super().__init__(message, 500, "ServerError", details)


def handle_exceptions(f):
    """Decorator to handle exceptions in API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        
        except APIException as e:
            logger.error(f"API Exception in {f.__name__}: {e.message}")
            return {
                "error": True,
                "exception": e.to_dict()
            }, e.status_code
        
        except ValueError as e:
            logger.error(f"ValueError in {f.__name__}: {str(e)}")
            exc = ValidationException(f"Invalid input: {str(e)}")
            return {
                "error": True,
                "exception": exc.to_dict()
            }, 400
        
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}\n{traceback.format_exc()}")
            exc = ServerException(
                "An unexpected error occurred",
                {"original_error": str(e), "traceback": traceback.format_exc()}
            )
            return {
                "error": True,
                "exception": exc.to_dict()
            }, 500
    
    return decorated_function


class RequestLogger:
    """Log HTTP requests and responses"""
    
    @staticmethod
    def log_request(method: str, endpoint: str, params: Dict = None, 
                   user_id: Optional[int] = None):
        """Log incoming request"""
        logger.info(
            f"Request: {method} {endpoint}",
            extra={
                "method": method,
                "endpoint": endpoint,
                "params": params,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @staticmethod
    def log_response(endpoint: str, status_code: int, response_time_ms: float,
                    user_id: Optional[int] = None):
        """Log outgoing response"""
        logger.info(
            f"Response: {endpoint} -> {status_code} ({response_time_ms}ms)",
            extra={
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time_ms": response_time_ms,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @staticmethod
    def log_error(endpoint: str, error: Exception, user_id: Optional[int] = None):
        """Log error"""
        logger.error(
            f"Error in {endpoint}: {str(error)}",
            extra={
                "endpoint": endpoint,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )


class PerformanceMonitor:
    """Monitor API performance and identify bottlenecks"""
    
    def __init__(self):
        self.metrics = {}  # endpoint -> list of response times
    
    def record_metric(self, endpoint: str, response_time_ms: float):
        """Record response time for endpoint"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = []
        
        self.metrics[endpoint].append(response_time_ms)
        
        # Keep only last 100 measurements
        if len(self.metrics[endpoint]) > 100:
            self.metrics[endpoint] = self.metrics[endpoint][-100:]
    
    def get_average_response_time(self, endpoint: str) -> float:
        """Get average response time for endpoint"""
        if endpoint not in self.metrics or not self.metrics[endpoint]:
            return 0
        
        return sum(self.metrics[endpoint]) / len(self.metrics[endpoint])
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        stats = {}
        
        for endpoint, times in self.metrics.items():
            if times:
                stats[endpoint] = {
                    "count": len(times),
                    "avg_ms": sum(times) / len(times),
                    "min_ms": min(times),
                    "max_ms": max(times),
                    "p99_ms": sorted(times)[-1] if len(times) >= 1 else 0
                }
        
        return stats


# Global performance monitor
perf_monitor = PerformanceMonitor()


def log_and_monitor_request(f):
    """Decorator to log and monitor API requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        import time
        from flask import request
        
        start_time = time.time()
        endpoint = request.path
        
        try:
            # Log request
            RequestLogger.log_request(
                request.method,
                endpoint,
                request.get_json() if request.method in ['POST', 'PUT'] else request.args.to_dict()
            )
            
            # Execute handler
            result = f(*args, **kwargs)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            perf_monitor.record_metric(endpoint, response_time)
            
            # Log response
            status_code = result[1] if isinstance(result, tuple) else 200
            RequestLogger.log_response(endpoint, status_code, response_time)
            
            return result
        
        except Exception as e:
            RequestLogger.log_error(endpoint, e)
            raise
    
    return decorated_function
