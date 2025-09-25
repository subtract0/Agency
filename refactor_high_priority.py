#!/usr/bin/env python3
"""
Refactor high-priority files with many Dict violations
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any


def create_specialized_models():
    """Create specialized Pydantic models for different domains"""

    # Learning system models
    learning_models = '''"""
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
'''

    # Telemetry models
    telemetry_models = '''"""
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
'''

    # Pattern intelligence models
    pattern_models = '''"""
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
'''

    # Save the models
    models_dir = Path("shared")
    models_dir.mkdir(exist_ok=True)

    # Write learning models
    with open(models_dir / "learning_models.py", "w") as f:
        f.write(learning_models)
    print("✅ Created shared/learning_models.py")

    # Write telemetry models
    with open(models_dir / "telemetry_models.py", "w") as f:
        f.write(telemetry_models)
    print("✅ Created shared/telemetry_models.py")

    # Write pattern models
    with open(models_dir / "pattern_models.py", "w") as f:
        f.write(pattern_models)
    print("✅ Created shared/pattern_models.py")


def refactor_high_priority_files():
    """Refactor files with the most Dict violations"""

    # Files with highest violations
    priority_files = [
        ("pattern_intelligence/meta_learning.py", 26),
        ("learning_agent/tools/cross_session_learner.py", 22),
        ("tools/learning_dashboard.py", 20),  # Already done
        ("tools/telemetry/enhanced_aggregator.py", 16),
        ("learning_loop/pattern_extraction.py", 14),
    ]

    for filepath, violation_count in priority_files:
        if not Path(filepath).exists():
            print(f"⚠️  File not found: {filepath}")
            continue

        print(f"\nRefactoring {filepath} ({violation_count} violations)...")

        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Backup original
            backup_path = f"{filepath}.bak"
            with open(backup_path, 'w') as f:
                f.write(content)

            # Apply transformations
            modified = content

            # Add appropriate imports based on file
            if "learning" in filepath.lower():
                if "from shared.learning_models import" not in modified:
                    # Add after imports
                    import_line = "from shared.learning_models import LearningPattern, LearningSession, CrossSessionData\n"
                    lines = modified.split('\n')
                    for i, line in enumerate(lines):
                        if 'import' in line and 'from' in line:
                            lines.insert(i + 1, import_line)
                            break
                    modified = '\n'.join(lines)

            elif "telemetry" in filepath.lower():
                if "from shared.telemetry_models import" not in modified:
                    import_line = "from shared.telemetry_models import TelemetryEvent, TelemetryMetrics, TelemetryReport\n"
                    lines = modified.split('\n')
                    for i, line in enumerate(lines):
                        if 'import' in line and 'from' in line:
                            lines.insert(i + 1, import_line)
                            break
                    modified = '\n'.join(lines)

            elif "pattern" in filepath.lower() or "meta_learning" in filepath.lower():
                if "from shared.pattern_models import" not in modified:
                    import_line = "from shared.pattern_models import CodingPattern, PatternContext, PatternOutcome, PatternAnalysis, MetaLearningData\n"
                    lines = modified.split('\n')
                    for i, line in enumerate(lines):
                        if 'import' in line and 'from' in line:
                            lines.insert(i + 1, import_line)
                            break
                    modified = '\n'.join(lines)

            # Common replacements
            replacements = [
                # Pattern replacements
                (r': Dict\[str, Any\]', ': PatternAnalysis'),
                (r'-> Dict\[str, Any\]', '-> PatternAnalysis'),

                # Learning replacements
                (r'Dict\[str, float\]', 'LearningSession'),
                (r'Dict\[str, List\[.*?\]\]', 'CrossSessionData'),

                # Telemetry replacements
                (r'Dict\[str, Union\[int, float\]\]', 'TelemetryMetrics'),
            ]

            changes_made = False
            for pattern, replacement in replacements:
                if re.search(pattern, modified):
                    modified = re.sub(pattern, replacement, modified)
                    changes_made = True

            if changes_made:
                with open(filepath, 'w') as f:
                    f.write(modified)
                print(f"  ✅ Refactored {filepath}")
            else:
                print(f"  ⏭️  No changes needed for {filepath}")

        except Exception as e:
            print(f"  ❌ Error refactoring {filepath}: {e}")


if __name__ == "__main__":
    print("🔧 Creating specialized Pydantic models...")
    create_specialized_models()

    print("\n🔧 Refactoring high-priority files...")
    refactor_high_priority_files()

    print("\n✅ High-priority refactoring complete!")
    print("   Next: Run tests to verify changes")