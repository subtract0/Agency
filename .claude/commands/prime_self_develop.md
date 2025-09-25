---
description: Enable autonomous self-development mode for the Agency codebase
---

# Prime Self-Develop

## Mission: Autonomous Self-Development

You are now in self-development mode, focused on analyzing and improving the Agency codebase itself. Your goal is to enhance the system's capabilities, fix issues, and optimize performance while maintaining constitutional compliance.

### Workflow

1. **Self-Analysis**: Run comprehensive analysis of the Agency codebase
2. **Pattern Extraction**: Learn from successful operations and patterns
3. **Improvement Planning**: Generate prioritized improvement plan
4. **Implementation**: Apply improvements with proper testing
5. **Verification**: Ensure 100% test success (Article II)
6. **Learning**: Store successful improvements as patterns

### Initial Context Loading

Read these critical files to understand the system:
- `agency.py` - Main entry point and agent orchestration
- `CLAUDE.md` - Constitution and development guidelines
- `project-overview.md` - System architecture overview
- `agency_self_improve.py` - Self-improvement capabilities

### Available Self-Development Commands

```bash
# Analyze the codebase for improvements
python agency_self_improve.py analyze

# Generate improvement plan
python agency_self_improve.py plan --output improvement_plan.md

# Apply improvements (with dry-run first)
python agency_self_improve.py improve --dry-run

# Full self-analysis report
python agency_self_improve.py report
```

### Self-Development Tools

Use these specialized tools for self-improvement:
- **agency_self_improve.py**: Autonomous codebase analysis
- **pattern_intelligence/**: Extract and apply successful patterns
- **learning_agent**: Learn from past operations
- **toolsmith_agent**: Create new tools from patterns
- **quality_enforcer_agent**: Ensure constitutional compliance

### Focus Areas

Prioritize improvements in these areas:
1. **Performance Optimization**: Identify and fix bottlenecks
2. **Code Quality**: Reduce complexity, improve readability
3. **Test Coverage**: Ensure comprehensive testing
4. **Documentation**: Maintain clear, up-to-date docs
5. **Architecture**: Improve system design and modularity
6. **Memory Management**: Optimize resource usage
7. **Agent Communication**: Streamline inter-agent messaging
8. **Tool Generation**: Create tools from repeated patterns

### Constitutional Compliance

All self-improvements must adhere to the Five Articles:
1. **Complete Context**: Understand before modifying
2. **100% Verification**: All tests must pass
3. **Automated Enforcement**: Quality standards enforced
4. **Continuous Learning**: Learn from each change
5. **Spec-Driven**: Document changes properly

### Self-Improvement Patterns

Common patterns for autonomous improvement:
- **Refactoring**: Break down complex functions
- **Extraction**: Move duplicated code to utilities
- **Optimization**: Replace inefficient patterns
- **Testing**: Add missing test coverage
- **Documentation**: Generate from code analysis
- **Tooling**: Create tools from manual processes

### Telemetry and Monitoring

Track self-improvement metrics:
```python
from core.telemetry import SimpleTelemetry

telemetry = SimpleTelemetry()
telemetry.emit("self_improvement_started", {
    "focus_areas": ["performance", "testing"],
    "health_score": 0.85
})
```

### Example Self-Development Session

```python
# 1. Analyze current state
from agency_self_improve import AgencySelfImprover

improver = AgencySelfImprover()
report = improver.analyze_self(focus_areas=["performance", "testing"])

# 2. Review health score and issues
print(f"Health Score: {report.health_score:.1%}")
print(f"Critical Issues: {len([o for o in report.opportunities_found if o.severity == 'critical'])}")

# 3. Generate improvement plan
plan = improver.generate_improvement_plan(report)

# 4. Apply high-priority improvements
high_priority = [o for o in report.opportunities_found if o.severity in ["critical", "high"]]
results = improver.apply_improvements(high_priority, dry_run=False)

# 5. Verify with tests
import subprocess
result = subprocess.run(["python", "run_tests.py", "--fast"], capture_output=True)
assert result.returncode == 0, "Tests must pass after improvements"

# 6. Store successful patterns
from pattern_intelligence import CodingPattern, PatternStore

store = PatternStore(namespace="self_improvements")
for improvement in results["applied"]:
    pattern = CodingPattern(
        pattern_type="self_improvement",
        pattern_id=improvement.id,
        description=improvement.description,
        confidence=0.9
    )
    store.store_pattern(pattern)
```

### Continuous Self-Improvement Loop

The Agency should continuously improve itself:
1. **Monitor**: Watch for performance issues and errors
2. **Analyze**: Regular self-analysis (daily/weekly)
3. **Plan**: Generate improvement plans
4. **Execute**: Apply improvements incrementally
5. **Learn**: Store successful improvements
6. **Iterate**: Repeat the cycle

### Safety Mechanisms

Self-development includes safety features:
- **Dry-run mode**: Test changes before applying
- **Automatic rollback**: Revert on test failures
- **Constitutional checks**: Verify compliance
- **Gradual rollout**: Apply improvements incrementally
- **Human oversight**: Critical changes require approval

### Success Metrics

Track self-improvement success:
- Health score improvement (target: >90%)
- Test coverage increase (target: >80%)
- Performance metrics (response time, memory usage)
- Code quality metrics (complexity, duplication)
- Documentation coverage (target: >70%)
- Pattern application success rate

### Start Self-Development

Begin with:
```bash
# Run self-analysis
./agency_cli improve

# Or use Python directly
python agency_self_improve.py analyze --focus architecture performance

# Review and apply improvements
python agency_self_improve.py plan --output self_improvement_plan.md
```

Remember: The Agency's ability to improve itself is its greatest strength. Each improvement makes the system more capable of future improvements, creating exponential growth in capabilities.