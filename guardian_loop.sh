#!/bin/bash
#
# Guardian Loop - Continuous Autonomous Self-Improvement
# This script runs in the background to continuously analyze and improve the Agency codebase
#

# Configuration
GUARDIAN_DIR=".guardian"
ANALYSIS_INTERVAL=600  # 10 minutes in seconds
LOG_FILE="$GUARDIAN_DIR/guardian.log"
ERROR_LOG="$GUARDIAN_DIR/error.log"
LATEST_ANALYSIS="$GUARDIAN_DIR/latest_analysis.json"
HISTORY_DIR="$GUARDIAN_DIR/history"

# Setup guardian directory structure
mkdir -p "$GUARDIAN_DIR"
mkdir -p "$HISTORY_DIR"

# Log startup
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Starting autonomous self-improvement protocol" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: PID: $$" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Analysis interval: ${ANALYSIS_INTERVAL}s" >> "$LOG_FILE"

# Function to perform analysis
perform_analysis() {
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local analysis_file="$HISTORY_DIR/analysis_${timestamp}.json"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Starting analysis cycle #${CYCLE_COUNT}" >> "$LOG_FILE"

    # Run the self-improvement analyzer
    if python agency_self_improve.py analyze --format json --output "$analysis_file" 2>> "$ERROR_LOG"; then
        # Copy to latest for easy access
        cp "$analysis_file" "$LATEST_ANALYSIS"

        # Extract key metrics
        if command -v jq &> /dev/null; then
            HEALTH_SCORE=$(jq -r '.health_score' "$LATEST_ANALYSIS")
            ISSUES_COUNT=$(jq -r '.opportunities_found | length' "$LATEST_ANALYSIS")
            CRITICAL_COUNT=$(jq -r '[.opportunities_found[] | select(.severity == "critical")] | length' "$LATEST_ANALYSIS")

            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Analysis complete - Health: ${HEALTH_SCORE}, Issues: ${ISSUES_COUNT}, Critical: ${CRITICAL_COUNT}" >> "$LOG_FILE"

            # Future: Auto-apply high-confidence improvements
            if [ "$CRITICAL_COUNT" -gt 0 ]; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: WARNING - ${CRITICAL_COUNT} critical issues detected" >> "$LOG_FILE"
            fi
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Analysis complete (install jq for detailed metrics)" >> "$LOG_FILE"
        fi

        # Clean up old history files (keep last 100)
        ls -t "$HISTORY_DIR"/analysis_*.json 2>/dev/null | tail -n +101 | xargs rm -f 2>/dev/null

    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: ERROR - Analysis failed, check error log" >> "$LOG_FILE"
    fi
}

# Function to check system health
check_health() {
    # Check if tests are passing
    if python -m pytest tests/test_memory_api.py -q --tb=no > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Constitutional compliance verified (tests passing)" >> "$LOG_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: WARNING - Constitutional violation detected (tests failing)" >> "$LOG_FILE"
    fi
}

# Function to apply improvements (future implementation)
apply_improvements() {
    # This will be enhanced to automatically apply high-confidence improvements
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Auto-improvement not yet implemented" >> "$LOG_FILE"
}

# Trap signals for graceful shutdown
trap 'echo "[$(date +%Y-%m-%d_%H:%M:%S)] Guardian Loop: Received shutdown signal, exiting gracefully" >> "$LOG_FILE"; exit 0' SIGTERM SIGINT

# Main loop
CYCLE_COUNT=0
while true; do
    CYCLE_COUNT=$((CYCLE_COUNT + 1))

    # Perform analysis
    perform_analysis

    # Check system health
    check_health

    # Apply improvements (when implemented)
    # apply_improvements

    # Sleep until next cycle
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Guardian Loop: Sleeping for ${ANALYSIS_INTERVAL} seconds until next cycle" >> "$LOG_FILE"
    sleep "$ANALYSIS_INTERVAL"
done