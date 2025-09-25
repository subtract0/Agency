"""
Pydantic models for pattern intelligence system
"""

from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class PatternContext(BaseModel):
    """Pattern context information"""
    domain: str = Field(..., description="Domain")
    tags: List[str] = Field(default_factory=list, description="Tags")
    source_files: List[str] = Field(default_factory=list, description="Source files")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies")


class PatternOutcome(BaseModel):
    """Pattern application outcome"""
    success: bool = Field(..., description="Success status")
    impact: float = Field(default=0.0, description="Impact score")
    errors: List[str] = Field(default_factory=list, description="Errors")
    warnings: List[str] = Field(default_factory=list, description="Warnings")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Outcome metrics")


class CodingPattern(BaseModel):
    """Coding pattern definition"""
    pattern_id: str = Field(..., description="Pattern ID")
    name: str = Field(..., description="Pattern name")
    description: str = Field(..., description="Description")
    context: PatternContext = Field(..., description="Context")
    template: str = Field(..., description="Pattern template")
    examples: List[str] = Field(default_factory=list, description="Examples")
    outcome: Optional[PatternOutcome] = Field(None, description="Outcome")
    confidence: float = Field(default=0.0, description="Confidence")
    usage_count: int = Field(default=0, description="Usage count")


class PatternAnalysis(BaseModel):
    """Pattern analysis results"""
    patterns_found: List[CodingPattern] = Field(default_factory=list, description="Patterns found")
    pattern_frequency: Dict[str, int] = Field(default_factory=dict, description="Pattern frequency")
    effectiveness_scores: Dict[str, float] = Field(default_factory=dict, description="Effectiveness scores")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


class MetaLearningData(BaseModel):
    """Meta-learning analysis data"""
    learning_rate: float = Field(default=0.0, description="Learning rate")
    pattern_discovery_rate: float = Field(default=0.0, description="Discovery rate")
    adaptation_speed: float = Field(default=0.0, description="Adaptation speed")
    knowledge_retention: float = Field(default=0.0, description="Retention rate")
    cross_domain_transfer: float = Field(default=0.0, description="Transfer rate")
    optimization_suggestions: List[str] = Field(default_factory=list, description="Suggestions")


class PatternData(BaseModel):
    """Generic pattern data container"""
    pattern_id: str = Field(default="", description="Pattern identifier")
    pattern_type: str = Field(default="", description="Type of pattern")
    content: Any = Field(default=None, description="Pattern content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    confidence: float = Field(default=0.0, description="Confidence score")
    occurrences: int = Field(default=0, description="Number of occurrences")
