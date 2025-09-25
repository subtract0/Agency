#!/usr/bin/env python3
"""
Fix PatternAnalysis references that were incorrectly replaced
"""

import re
from pathlib import Path

# Files to fix
files_to_fix = [
    "pattern_intelligence/meta_learning.py",
    "learning_agent/tools/cross_session_learner.py",
    "learning_loop/pattern_extraction.py",
    "tools/telemetry/enhanced_aggregator.py"
]

def fix_file(filepath: str):
    """Fix PatternAnalysis references in a file"""

    path = Path(filepath)
    if not path.exists():
        print(f"⚠️  File not found: {filepath}")
        return

    with open(path, 'r') as f:
        content = f.read()

    original = content

    # Replace incorrectly replaced PatternAnalysis with Dict[str, Any]
    # These are the ones that were meant to be type aliases for Dict
    patterns_to_fix = [
        # Method signatures that should return Dict
        (r': PatternAnalysis:', ': Dict[str, Any]:'),
        (r'-> PatternAnalysis:', '-> Dict[str, Any]:'),
        (r'\) -> PatternAnalysis', ') -> Dict[str, Any]'),

        # Parameters that should be Dict
        (r': PatternAnalysis\)', ': Dict[str, Any])'),
        (r': PatternAnalysis =', ': Dict[str, Any] ='),

        # Variable type hints
        (r': PatternAnalysis =', ': Dict[str, Any] ='),
    ]

    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)

    # Make sure we have the Dict import
    if 'Dict[str, Any]' in content and 'from typing import' in content:
        # Check if Dict is imported
        if 'from typing import' in content and 'Dict' not in content.split('from typing import')[1].split('\n')[0]:
            # Add Dict to imports
            content = re.sub(
                r'from typing import ([^\\n]+)',
                r'from typing import Dict, \1',
                content,
                count=1
            )

    if content != original:
        # Backup and save
        backup_path = f"{filepath}.fix_bak"
        with open(backup_path, 'w') as f:
            f.write(original)

        with open(path, 'w') as f:
            f.write(content)

        print(f"✅ Fixed {filepath}")
        return True
    else:
        print(f"⏭️  No changes needed for {filepath}")
        return False

def main():
    print("🔧 Fixing PatternAnalysis references...")

    fixed_count = 0
    for filepath in files_to_fix:
        if fix_file(filepath):
            fixed_count += 1

    print(f"\n✅ Fixed {fixed_count} files")

    # Additional manual fixes for specific cases
    print("\n📝 Additional manual fixes may be needed for:")
    print("  - Type aliases that were meant to reference an actual PatternAnalysis class")
    print("  - Import statements that need PatternAnalysis from shared.pattern_models")

if __name__ == "__main__":
    main()