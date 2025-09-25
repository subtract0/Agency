"""
Pydantic models for telemetry system
"""

from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class TelemetryEvent(BaseModel):
    """Telemetry event data"""
    event_id: str = Field(..., description="Event ID")
    event_type: str = Field(..., description="Event type")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp")
    source: str = Field(..., description="Event source")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")


class TelemetryMetrics(BaseModel):
    """Aggregated telemetry metrics"""
    total_events: int = Field(default=0, description="Total events")
    events_by_type: Dict[str, int] = Field(default_factory=dict, description="Events by type")
    events_by_source: Dict[str, int] = Field(default_factory=dict, description="Events by source")
    error_count: int = Field(default=0, description="Error count")
    success_rate: float = Field(default=0.0, description="Success rate")
    latency_metrics: Dict[str, float] = Field(default_factory=dict, description="Latency metrics")


class TelemetryReport(BaseModel):
    """Telemetry analysis report"""
    period_start: datetime = Field(..., description="Period start")
    period_end: datetime = Field(..., description="Period end")
    metrics: TelemetryMetrics = Field(..., description="Metrics")
    events: List[TelemetryEvent] = Field(default_factory=list, description="Events")
    alerts: List[str] = Field(default_factory=list, description="Alerts")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
