---
description: Start the Guardian Loop background process for continuous self-improvement
---

# Start Guardian Loop

## Background Command: Start Guardian Loop

You will now execute the continuous self-improvement loop as a detached background process.

### Workflow
1. **Construct the Command:** Create a shell command that will run indefinitely. This command will:
   a. Create a `.guardian` directory for logging if it doesn't exist.
   b. Sleep for a 10-minute interval (600 seconds) to ensure low-intensity operation.
   c. Wake up and run the self-improvement analyzer in CI mode, outputting results to `.guardian/latest_analysis.json`.
   d. Log all actions with timestamps to `.guardian/guardian.log`.
   e. **(Future Objective)** This script should be enhanced later to parse the JSON output and trigger `plan_and_execute` workflows for high-confidence improvements.

2. **Execute in Background:** Use the `/background` tool to execute this infinite loop. The `prompt` for the background tool will be the shell command you construct.

3. **Report to User:** Output the PID and the location of the log file so the operator can monitor your progress.

### Shell Command for Background Execution:
```bash
#!/bin/bash
mkdir -p .guardian
while true; do
  echo "[$(date)] - Guardian Loop: Waking up. Analyzing codebase..." >> .guardian/guardian.log
  ./agency_cli improve --ci --json > .guardian/latest_analysis.json 2>> .guardian/error.log
  echo "[$(date)] - Guardian Loop: Analysis complete. Sleeping for 10 minutes." >> .guardian/guardian.log
  sleep 600
done
```

### Enhanced Guardian Loop (Future Implementation):
```bash
#!/bin/bash
mkdir -p .guardian

while true; do
  echo "[$(date)] - Guardian Loop: Starting analysis cycle" >> .guardian/guardian.log

  # Run analysis
  python agency_self_improve.py analyze --output .guardian/latest_analysis.json 2>> .guardian/error.log

  # Check if analysis succeeded
  if [ $? -eq 0 ]; then
    echo "[$(date)] - Analysis completed successfully" >> .guardian/guardian.log

    # Parse high-confidence improvements (future)
    # python -c "
    # import json
    # with open('.guardian/latest_analysis.json') as f:
    #     data = json.load(f)
    #     high_conf = [o for o in data['opportunities_found']
    #                  if o['confidence'] > 0.9 and o['severity'] != 'critical']
    #     if high_conf:
    #         # Trigger improvement workflow
    #         pass
    # "
  else
    echo "[$(date)] - Analysis failed, check error log" >> .guardian/guardian.log
  fi

  # Report metrics
  echo "[$(date)] - Guardian Loop: Sleeping for 10 minutes" >> .guardian/guardian.log
  sleep 600
done
```

### Monitoring Commands

After starting the Guardian Loop, use these commands to monitor:

```bash
# View latest log entries
tail -f .guardian/guardian.log

# Check latest analysis
cat .guardian/latest_analysis.json | jq .health_score

# Monitor errors
tail -f .guardian/error.log

# Check if Guardian is running
ps aux | grep -E "guardian|agency_cli improve"
```

### Safety Features

The Guardian Loop includes:
- **Rate Limiting:** 10-minute intervals prevent resource exhaustion
- **Error Isolation:** Separate error log for debugging
- **JSON Output:** Structured data for automated processing
- **Non-Blocking:** Runs in background without interfering with main session
- **Graceful Degradation:** Continues running even if individual analyses fail

### Integration Points

The Guardian Loop integrates with:
- `agency_self_improve.py` - Core analysis engine
- `.guardian/` directory - Persistent state storage
- Telemetry system - Performance tracking
- Memory store - Learning from improvements
- Pattern intelligence - Extracting successful patterns

### Future Enhancements

Planned improvements for the Guardian Loop:
1. **Auto-Apply:** Automatically apply high-confidence improvements
2. **Pattern Learning:** Extract patterns from successful improvements
3. **Adaptive Timing:** Adjust analysis frequency based on activity
4. **Notification System:** Alert on critical issues
5. **Web Dashboard:** Visual monitoring interface
6. **Distributed Analysis:** Parallelize analysis across modules
7. **Rollback Capability:** Automatic reversion of failed improvements

Remember: The Guardian Loop is the Agency's commitment to continuous self-improvement, operating autonomously to maintain and enhance system quality.