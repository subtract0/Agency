#!/usr/bin/env python3
"""Fix missing BaseModel imports after refactoring"""

import os
import re
from pathlib import Path

def fix_file(filepath):
    """Fix missing BaseModel import in a file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Check if BaseModel is used but not imported
        if '(BaseModel)' in content and 'from pydantic import' in content:
            # Find the pydantic import line
            import_match = re.search(r'from pydantic import ([^)\n]+)', content)
            if import_match:
                imports = import_match.group(1)
                if 'BaseModel' not in imports:
                    # Add BaseModel to imports
                    if imports.strip():
                        new_imports = 'BaseModel, ' + imports
                    else:
                        new_imports = 'BaseModel'

                    content = content.replace(
                        f'from pydantic import {imports}',
                        f'from pydantic import {new_imports}'
                    )

                    with open(filepath, 'w') as f:
                        f.write(content)

                    print(f"✅ Fixed: {filepath}")
                    return True
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")

    return False

def main():
    files_to_fix = [
        './mass_refactor_dict.py',
        './tools/apply_and_verify_patch.py',
        './chief_architect_agent/tools/architecture_loop.py',
        './learning_agent/tools/telemetry_pattern_analyzer.py',
        './learning_agent/tools/analyze_session.py',
        './learning_agent/tools/store_knowledge.py',
        './learning_agent/tools/self_healing_pattern_extractor.py',
        './learning_agent/tools/cross_session_learner.py',
        './learning_agent/tools/consolidate_learning.py',
        './learning_agent/tools/extract_insights.py',
    ]

    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_file(filepath):
                fixed_count += 1

    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()