#!/usr/bin/env python3
"""
Automated Dict to Pydantic refactoring script
Part of The Great Refactor mission
"""

import os
import re
import ast
from pathlib import Path
from typing import List, Tuple, Set
import argparse


class DictRefactorer:
    """Automated refactoring tool for Dict to Pydantic migration"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.files_processed = 0
        self.violations_fixed = 0
        self.errors = []

    def find_dict_violations(self, root_dir: str = ".") -> List[Path]:
        """Find all Python files with Dict violations"""
        violations = []
        exclude_dirs = {'.venv', '__pycache__', '.git', '.pytest_cache', 'node_modules', '.tox'}

        for root, dirs, files in os.walk(root_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    filepath = Path(root) / file

                    # Skip test files and this script
                    if 'test_' in file or file == 'refactor_dict_to_pydantic.py':
                        continue

                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        if self._has_dict_violation(content):
                            violations.append(filepath)
                    except Exception as e:
                        self.errors.append(f"Error reading {filepath}: {e}")

        return violations

    def _has_dict_violation(self, content: str) -> bool:
        """Check if content has Dict type hint violations"""
        # Look for Dict in type hints
        patterns = [
            r': Dict\[',
            r'-> Dict\[',
            r': typing\.Dict\[',
            r'-> typing\.Dict\[',
        ]

        for pattern in patterns:
            if re.search(pattern, content):
                return True

        return False

    def refactor_file(self, filepath: Path) -> bool:
        """Refactor a single file to replace Dict with Pydantic models"""

        print(f"Processing: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Parse the file to understand its structure
            try:
                tree = ast.parse(original_content)
            except SyntaxError as e:
                self.errors.append(f"Syntax error in {filepath}: {e}")
                return False

            # Apply transformations
            modified_content = self._apply_transformations(original_content, tree, filepath)

            if modified_content != original_content:
                if not self.dry_run:
                    # Create backup
                    backup_path = filepath.with_suffix('.py.bak')
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)

                    # Write modified content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

                    print(f"  ✅ Refactored (backup: {backup_path})")
                else:
                    print(f"  🔍 Would refactor (dry run)")

                self.files_processed += 1
                return True
            else:
                print(f"  ⏭️  No changes needed")
                return False

        except Exception as e:
            self.errors.append(f"Error processing {filepath}: {e}")
            return False

    def _apply_transformations(self, content: str, tree: ast.AST, filepath: Path) -> str:
        """Apply transformations to replace Dict with appropriate models"""

        modified = content

        # Step 1: Add common_models import if Dict is used
        if 'from typing import Dict' in modified or 'import typing' in modified:
            if 'from shared.common_models import' not in modified:
                # Add import after typing imports
                import_line = "from shared.common_models import BaseResponse, MetricsData, ConfigData, TaskResult, AnalysisResult\n"

                # Find the right place to insert
                lines = modified.split('\n')
                insert_index = 0

                for i, line in enumerate(lines):
                    if 'from typing import' in line or 'import typing' in line:
                        insert_index = i + 1
                        break

                if insert_index > 0:
                    lines.insert(insert_index, import_line)
                    modified = '\n'.join(lines)

        # Step 2: Replace common Dict patterns with models
        replacements = [
            # Common return type patterns
            (r'-> Dict\[str, Any\]:', '-> BaseResponse:'),
            (r'-> Dict\[str, Any\]', '-> BaseResponse'),
            (r': Dict\[str, Any\] =', ': BaseResponse ='),

            # Metrics patterns
            (r'Dict\[str, Union\[int, float\]\]', 'MetricsData'),
            (r'Dict\[str, int\]', 'MetricsData'),

            # Config patterns
            (r'Dict\[str, str\]', 'ConfigData'),

            # Keep generic Dict for now (will need manual review)
            # These will be marked for manual intervention
        ]

        for pattern, replacement in replacements:
            if re.search(pattern, modified):
                modified = re.sub(pattern, replacement, modified)
                self.violations_fixed += 1

        # Step 3: Add compatibility wrapper for functions that were changed
        if modified != content:
            # Check if we need to add the compatibility import
            if 'from shared.common_models import' in modified and 'model_to_dict' not in modified:
                # Add compatibility helpers
                modified = modified.replace(
                    'from shared.common_models import',
                    'from shared.common_models import model_to_dict, dict_to_model, '
                )

        return modified

    def generate_report(self) -> str:
        """Generate a refactoring report"""

        report = []
        report.append("=" * 60)
        report.append("Dict to Pydantic Refactoring Report")
        report.append("=" * 60)
        report.append(f"Mode: {'DRY RUN' if self.dry_run else 'APPLIED'}")
        report.append(f"Files processed: {self.files_processed}")
        report.append(f"Violations fixed: {self.violations_fixed}")

        if self.errors:
            report.append(f"\nErrors encountered: {len(self.errors)}")
            for error in self.errors[:10]:  # Show first 10 errors
                report.append(f"  - {error}")

        report.append("\nNext steps:")
        if self.dry_run:
            report.append("  1. Review the changes that would be made")
            report.append("  2. Run with --apply to apply changes")
        else:
            report.append("  1. Run tests to verify no breakage")
            report.append("  2. Review and adjust model usage as needed")
            report.append("  3. Remove backup files after verification")

        return "\n".join(report)


def main():
    """Main entry point for the refactoring script"""

    parser = argparse.ArgumentParser(description="Refactor Dict to Pydantic models")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (default is dry run)"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Root path to scan (default: current directory)"
    )
    parser.add_argument(
        "--file",
        help="Refactor a specific file only"
    )

    args = parser.parse_args()

    refactorer = DictRefactorer(dry_run=not args.apply)

    print("🔧 Starting Dict to Pydantic refactoring...")
    print(f"Mode: {'APPLYING CHANGES' if args.apply else 'DRY RUN'}\n")

    if args.file:
        # Refactor single file
        filepath = Path(args.file)
        if filepath.exists():
            refactorer.refactor_file(filepath)
        else:
            print(f"File not found: {args.file}")
    else:
        # Find and refactor all violations
        violations = refactorer.find_dict_violations(args.path)

        print(f"Found {len(violations)} files with Dict violations\n")

        # Process files in batches
        for i, filepath in enumerate(violations, 1):
            print(f"\n[{i}/{len(violations)}]", end=" ")
            refactorer.refactor_file(filepath)

            # Safety check - limit to first 10 files in initial run
            if i >= 10 and not args.file:
                print("\n\n⚠️  Limiting to first 10 files for safety")
                print("    Review changes and run again to continue")
                break

    # Generate and print report
    print("\n" + refactorer.generate_report())


if __name__ == "__main__":
    main()