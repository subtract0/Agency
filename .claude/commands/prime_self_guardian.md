---
description: Activate the Autonomous Guardian Protocol for continuous self-improvement
---

# Prime Self-Guardian

## Mission: Activate Autonomous Guardian Protocol

Your primary objective is to initiate and oversee the continuous, autonomous self-improvement of the Agency codebase. You will act as the "Guardian," ensuring the system's health, performance, and constitutional compliance without direct, constant supervision.

Your sole task upon activation is to start the Guardian Loop in the background.

### Workflow
1. **Initiate Guardian Loop:** Immediately call the `/start_guardian_loop` command to begin the autonomous process.
2. **Report & Detach:** Report the process ID (PID) of the background task to the user and confirm that the Guardian Loop is active. Your primary task is then complete.

### Start Command
- `/start_guardian_loop`

### Guardian Loop Responsibilities

Once activated, the Guardian Loop will:
- Analyze the codebase every 10 minutes
- Identify improvement opportunities
- Generate reports in `.guardian/` directory
- Maintain logs of all activities
- Ensure constitutional compliance
- (Future) Auto-apply high-confidence improvements

### Monitoring

After activation, monitor the Guardian Loop via:
- Log files: `.guardian/guardian.log`
- Latest analysis: `.guardian/latest_analysis.json`
- Error tracking: `.guardian/error.log`

### Safety Mechanisms

The Guardian Loop includes:
- Low-intensity operation (10-minute intervals)
- JSON output for structured analysis
- Error logging for debugging
- Non-blocking background execution
- Graceful failure handling

### Success Indicators

The Guardian Loop is successful when:
- Background process is running continuously
- Regular analysis reports are generated
- No critical errors in error log
- System health score improves over time
- Constitutional compliance maintained

### Deactivation

To stop the Guardian Loop if needed:
```bash
# Find the process
ps aux | grep guardian

# Kill the process
kill <PID>
```

Remember: The Guardian Loop represents the Agency's commitment to continuous self-improvement, operating silently in the background to ensure optimal performance and quality.