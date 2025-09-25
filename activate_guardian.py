#!/usr/bin/env python3
"""
Guardian Loop Activation Script
Starts the autonomous self-improvement guardian in the background
"""

import os
import subprocess
import sys
import time
from pathlib import Path

def activate_guardian():
    """Activate the Guardian Loop protocol"""

    print("🔮 GUARDIAN LOOP PROTOCOL ACTIVATION")
    print("=" * 50)
    print("Initiating autonomous self-improvement system...")
    print()

    # Check if guardian is already running
    result = subprocess.run(
        ["pgrep", "-f", "guardian_loop.sh"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("⚠️  Guardian Loop already running with PID:", result.stdout.strip())
        print("   To stop: kill", result.stdout.strip())
        return

    # Start the Guardian Loop
    print("🚀 Starting Guardian Loop...")

    # Make sure the script is executable
    guardian_script = Path(__file__).parent / "guardian_loop.sh"
    guardian_script.chmod(0o755)

    # Start in background using nohup
    process = subprocess.Popen(
        ["nohup", str(guardian_script)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    time.sleep(2)  # Give it time to start

    # Check if it's running
    check = subprocess.run(
        ["pgrep", "-f", "guardian_loop.sh"],
        capture_output=True,
        text=True
    )

    if check.returncode == 0:
        pid = check.stdout.strip()
        print(f"✅ Guardian Loop activated successfully")
        print(f"   Process ID: {pid}")
        print(f"   Log file: .guardian/guardian.log")
        print(f"   Analysis output: .guardian/latest_analysis.json")
        print()
        print("📊 Guardian Loop will:")
        print("   • Analyze codebase every 10 minutes")
        print("   • Generate improvement reports")
        print("   • Monitor system health")
        print("   • Ensure constitutional compliance")
        print()
        print("📁 Monitor progress:")
        print("   tail -f .guardian/guardian.log")
        print()
        print("🛑 To deactivate:")
        print(f"   kill {pid}")
    else:
        print("❌ Failed to start Guardian Loop")
        print("   Check .guardian/error.log for details")

    print()
    print("=" * 50)
    print("The Agency now operates with continuous self-improvement")
    print("Guardian Loop ensures optimal performance and quality")


if __name__ == "__main__":
    activate_guardian()