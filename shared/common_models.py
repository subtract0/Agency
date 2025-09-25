"""
Common Pydantic models for the Agency codebase
Replaces Dict usage to ensure constitutional compliance with strict typing
"""

from typing import List, Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field


# Base models for common patterns

class BaseResponse(BaseModel):
    """Base response model for all API-like interactions"""
    success: bool = Field(default=True, description="Whether the operation succeeded")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class MetricsData(BaseModel):
    """Common metrics data structure"""
    total: int = Field(default=0, description="Total count")
    success: int = Field(default=0, description="Success count")
    failed: int = Field(default=0, description="Failed count")
    rate: float = Field(default=0.0, description="Success rate")
    metadata: Optional[Any] = Field(default=None, description="Additional metadata")


class ConfigData(BaseModel):
    """Configuration data model"""
    key: str = Field(..., description="Configuration key")
    value: Any = Field(..., description="Configuration value")
    description: Optional[str] = Field(None, description="Configuration description")
    is_required: bool = Field(default=False, description="Whether config is required")


class FileData(BaseModel):
    """File information model"""
    path: str = Field(..., description="File path")
    content: Optional[str] = Field(None, description="File content")
    size: Optional[int] = Field(None, description="File size in bytes")
    modified: Optional[datetime] = Field(None, description="Last modified time")
    metadata: Optional[Any] = Field(default=None, description="Additional file metadata")


class TaskResult(BaseModel):
    """Result of a task execution"""
    task_id: str = Field(..., description="Unique task identifier")
    status: str = Field(..., description="Task status (pending, running, completed, failed)")
    result: Optional[Any] = Field(None, description="Task result data")
    error: Optional[str] = Field(None, description="Error message if failed")
    started_at: Optional[datetime] = Field(None, description="Task start time")
    completed_at: Optional[datetime] = Field(None, description="Task completion time")
    duration_seconds: Optional[float] = Field(None, description="Task duration")


class ValidationResult(BaseModel):
    """Result of a validation check"""
    is_valid: bool = Field(..., description="Whether validation passed")
    violations: List[str] = Field(default_factory=list, description="List of violations found")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")
    score: float = Field(default=0.0, description="Validation score (0-1)")


class AnalysisResult(BaseModel):
    """Generic analysis result"""
    target: str = Field(..., description="What was analyzed")
    findings: List[Any] = Field(default_factory=list, description="Analysis findings")
    metrics: Optional[MetricsData] = Field(None, description="Analysis metrics")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    confidence: float = Field(default=0.0, description="Confidence level (0-1)")


class EventData(BaseModel):
    """Event/telemetry data model"""
    event_type: str = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    source: Optional[str] = Field(None, description="Event source")
    data: Optional[Any] = Field(None, description="Event data payload")
    metadata: Optional[Any] = Field(default=None, description="Event metadata")


class PatternData(BaseModel):
    """Pattern/template data model"""
    pattern_id: str = Field(..., description="Unique pattern identifier")
    pattern_type: str = Field(..., description="Type of pattern")
    description: str = Field(..., description="Pattern description")
    content: Any = Field(..., description="Pattern content")
    confidence: float = Field(default=0.0, description="Pattern confidence")
    usage_count: int = Field(default=0, description="Times pattern has been used")
    success_rate: float = Field(default=0.0, description="Pattern success rate")


class MemoryData(BaseModel):
    """Memory/storage data model"""
    key: str = Field(..., description="Memory key")
    value: Any = Field(..., description="Memory value")
    tags: List[str] = Field(default_factory=list, description="Memory tags")
    timestamp: datetime = Field(default_factory=datetime.now, description="Storage timestamp")
    ttl_seconds: Optional[int] = Field(None, description="Time to live in seconds")


class AgentMessage(BaseModel):
    """Message between agents"""
    from_agent: str = Field(..., description="Source agent")
    to_agent: str = Field(..., description="Target agent")
    message_type: str = Field(..., description="Type of message")
    content: Any = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    correlation_id: Optional[str] = Field(None, description="Correlation ID for tracking")


class CodeAnalysis(BaseModel):
    """Code analysis result"""
    file_path: str = Field(..., description="Analyzed file path")
    language: str = Field(default="python", description="Programming language")
    metrics: MetricsData = Field(default_factory=MetricsData, description="Code metrics")
    issues: List[str] = Field(default_factory=list, description="Issues found")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    complexity: float = Field(default=0.0, description="Code complexity score")


class TestResult(BaseModel):
    """Test execution result"""
    test_name: str = Field(..., description="Test name")
    status: str = Field(..., description="Test status (passed, failed, skipped)")
    duration_seconds: float = Field(default=0.0, description="Test duration")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    stack_trace: Optional[str] = Field(None, description="Stack trace if failed")


# Compatibility helpers

def dict_to_model(data: dict, model_class: type[BaseModel]) -> BaseModel:
    """Convert dictionary to Pydantic model"""
    return model_class(**data)


def model_to_dict(model: BaseModel) -> dict:
    """Convert Pydantic model to dictionary"""
    return model.model_dump()


# Type aliases for common patterns
ConfigDict = dict  # Deprecated - use ConfigData instead
MetricsDict = dict  # Deprecated - use MetricsData instead
ResultDict = dict  # Deprecated - use TaskResult or BaseResponse instead