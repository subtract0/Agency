"""
Shared Pydantic Models for Agency OS
Constitutional Law #2: Strict typing enforcement
"""

from .memory import (
    MemoryRecord,
    MemoryPriority,
    MemoryMetadata,
    MemorySearchResult,
)
from .learning import (
    LearningConsolidation,
    LearningInsight,
    LearningMetric,
    PatternAnalysis,
    ContentTypeBreakdown,
    TimeDistribution,
)
from .telemetry import (
    TelemetryEvent,
    TelemetryMetrics,
    AgentMetrics,
    SystemHealth,
)
from .dashboard import (
    DashboardSummary,
    SessionSummary,
    AgentActivity,
)
from .context import (
    AgentContextData,
    SessionMetadata,
    AgentState,
)
from .patterns import (
    SessionInsight,
    HealingPattern,
    CrossSessionData,
    PatternExtraction,
    ToolExecutionResult,
    ValidationOutcome,
    TemporalPattern,
    ContextFeatures,
    PatternMatch,
    LearningRecommendation,
    ApplicationRecord,
    LearningEffectiveness,
    SelfHealingEvent,
    DataCollectionSummary,
    LearningObject,
    PatternMatchSummary,
    PatternType,
    ValidationStatus,
    ApplicationPriority,
    EventStatus,
)

__all__ = [
    # Memory models
    "MemoryRecord",
    "MemoryPriority",
    "MemoryMetadata",
    "MemorySearchResult",
    # Learning models
    "LearningConsolidation",
    "LearningInsight",
    "LearningMetric",
    "PatternAnalysis",
    "ContentTypeBreakdown",
    "TimeDistribution",
    # Telemetry models
    "TelemetryEvent",
    "TelemetryMetrics",
    "AgentMetrics",
    "SystemHealth",
    # Dashboard models
    "DashboardSummary",
    "SessionSummary",
    "AgentActivity",
    # Context models
    "AgentContextData",
    "SessionMetadata",
    "AgentState",
    # Pattern models
    "SessionInsight",
    "HealingPattern",
    "CrossSessionData",
    "PatternExtraction",
    "ToolExecutionResult",
    "ValidationOutcome",
    "TemporalPattern",
    "ContextFeatures",
    "PatternMatch",
    "LearningRecommendation",
    "ApplicationRecord",
    "LearningEffectiveness",
    "SelfHealingEvent",
    "DataCollectionSummary",
    "LearningObject",
    "PatternMatchSummary",
    "PatternType",
    "ValidationStatus",
    "ApplicationPriority",
    "EventStatus",
]