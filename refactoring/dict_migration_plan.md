# The Great Refactor: Dict to Pydantic Migration Plan

## Overview
- **Total Files Affected**: 54
- **Total Dict Violations**: 315
- **Health Score Impact**: Expected improvement from 16.7% to ~25%

## Phase 1: Core Models Creation

### Priority 1: High-Impact Files (26+ violations)
1. **pattern_intelligence/meta_learning.py** (26 violations)
   - Create `MetaLearningModels` with pattern analysis types

### Priority 2: Learning System (20+ violations each)
2. **learning_agent/tools/cross_session_learner.py** (22)
3. **tools/learning_dashboard.py** (20)
   - Create unified `LearningModels` module

### Priority 3: Telemetry & Memory (10+ violations)
4. **tools/telemetry/enhanced_aggregator.py** (16)
5. **learning_loop/pattern_extraction.py** (14)
6. **agency_memory/memory_v2.py** (13)
7. **meta_learning/agent_registry.py** (13)

## Phase 2: Systematic Migration

### Strategy
1. Create domain-specific model modules:
   - `common_models.py` - Shared models across all modules
   - `telemetry_models.py` - Telemetry-specific types
   - `learning_models.py` - Learning system types
   - `memory_models.py` - Memory system types
   - `pattern_models.py` - Pattern intelligence types

2. Apply compatibility layer pattern from healing_patterns/dict_to_pydantic_pattern.py

3. Use automated refactoring script to:
   - Replace Dict imports
   - Update function signatures
   - Add model imports
   - Insert compatibility wrappers where needed

## Phase 3: Test Stabilization

### Current Failures (4 tests)
- Investigate timeout issues in test suite
- Fix any breakage from refactoring
- Ensure 100% test pass rate

## Automation Script

Create `refactor_dict_to_pydantic.py` to automate the migration process.