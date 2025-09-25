"""
Pydantic models for learning system
"""

from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class LearningPattern(BaseModel):
    """Learning pattern data"""
    pattern_id: str = Field(..., description="Pattern ID")
    pattern_type: str = Field(..., description="Pattern type")
    content: Any = Field(..., description="Pattern content")
    confidence: float = Field(default=0.0, description="Confidence level")
    usage_count: int = Field(default=0, description="Usage count")
    success_rate: float = Field(default=0.0, description="Success rate")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")


class LearningSession(BaseModel):
    """Learning session data"""
    session_id: str = Field(..., description="Session ID")
    start_time: datetime = Field(default_factory=datetime.now, description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")
    patterns_learned: List[LearningPattern] = Field(default_factory=list, description="Patterns learned")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Session metrics")


class CrossSessionData(BaseModel):
    """Cross-session learning data"""
    sessions: List[LearningSession] = Field(default_factory=list, description="All sessions")
    aggregated_patterns: List[LearningPattern] = Field(default_factory=list, description="Aggregated patterns")
    global_metrics: Dict[str, float] = Field(default_factory=dict, description="Global metrics")
    insights: List[str] = Field(default_factory=list, description="Cross-session insights")
