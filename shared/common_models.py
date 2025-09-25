"""
Common Pydantic Models for Agency
Auto-generated to replace Dict[str, Any] violations
"""

from typing import Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class DynamicData(BaseModel):
    """Flexible data model that accepts any fields"""
    class Config:
        extra = "allow"


class TelemetryData(BaseModel):
    """Telemetry and metrics data"""
    event_type: str = Field(..., description="Type of telemetry event")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        extra = "allow"


class LearningData(BaseModel):
    """Learning and insight data"""
    insight_type: str = Field(..., description="Type of learning insight")
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    class Config:
        extra = "allow"


class PatternData(BaseModel):
    """Pattern recognition data"""
    pattern_id: str = Field(..., description="Unique pattern identifier")
    pattern_type: str = Field(..., description="Type of pattern")
    class Config:
        extra = "allow"


class MemoryData(BaseModel):
    """Memory and session data"""
    session_id: str = Field(..., description="Session identifier")
    class Config:
        extra = "allow"


class ConfigData(BaseModel):
    """Configuration data"""
    class Config:
        extra = "allow"


class ResponseData(BaseModel):
    """API response data"""
    success: bool = Field(True, description="Operation success status")
    class Config:
        extra = "allow"


class RequestData(BaseModel):
    """API request data"""
    class Config:
        extra = "allow"


class ContextData(BaseModel):
    """Context and state data"""
    class Config:
        extra = "allow"


class MetadataModel(BaseModel):
    """Metadata model"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    class Config:
        extra = "allow"


class StatsData(BaseModel):
    """Statistics data"""
    count: int = Field(0, ge=0)
    class Config:
        extra = "allow"


class AnalysisData(BaseModel):
    """Analysis and report data"""
    analysis_type: str = Field(..., description="Type of analysis")
    class Config:
        extra = "allow"


class TaskData(BaseModel):
    """Task and job data"""
    task_id: str = Field(..., description="Task identifier")
    status: str = Field("pending", description="Task status")
    class Config:
        extra = "allow"


class ErrorData(BaseModel):
    """Error and exception data"""
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    class Config:
        extra = "allow"


class AgentData(BaseModel):
    """Agent and worker data"""
    agent_id: str = Field(..., description="Agent identifier")
    agent_type: str = Field(..., description="Type of agent")
    class Config:
        extra = "allow"


class GraphData(BaseModel):
    """Graph and node data"""
    node_id: str = Field(..., description="Node identifier")
    class Config:
        extra = "allow"
