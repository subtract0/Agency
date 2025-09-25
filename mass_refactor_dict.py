#!/usr/bin/env python3
"""
Mass Dict-to-Pydantic Refactoring Script
Systematically eliminates all Dict type hint violations across the codebase
"""

import ast
import os
import re
import shutil
import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional, Any
from datetime import datetime
from collections import defaultdict

# Mapping of context patterns to Pydantic models
MODEL_MAPPINGS = {
    'telemetry': ('TelemetryEvent', 'shared.telemetry_models'),
    'event': ('EventData', 'shared.common_models'),
    'analysis': ('AnalysisResult', 'shared.common_models'),
    'pattern': ('PatternData', 'shared.pattern_models'),
    'learning': ('LearningPattern', 'shared.learning_models'),
    'session': ('LearningSession', 'shared.learning_models'),
    'metrics': ('MetricsData', 'shared.common_models'),
    'config': ('ConfigData', 'shared.common_models'),
    'task': ('TaskResult', 'shared.common_models'),
    'test': ('TestResult', 'shared.common_models'),
    'validation': ('ValidationResult', 'shared.common_models'),
    'file': ('FileData', 'shared.common_models'),
    'response': ('BaseResponse', 'shared.common_models'),
}

# Files to exclude from refactoring
EXCLUDE_PATTERNS = [
    'venv/', '__pycache__/', '.git/', '.pytest_cache/',
    'node_modules/', 'dist/', 'build/', '.backups/',
    'mass_refactor_dict.py'  # Don't refactor this script itself
]


class DictRefactorer:
    """Main refactoring engine for Dict to Pydantic conversion"""

    def __init__(self, backup_dir: str = '.backups', dry_run: bool = False,
                 test_after: bool = False, verbose: bool = False):
        self.backup_dir = Path(backup_dir)
        self.dry_run = dry_run
        self.test_after = test_after
        self.verbose = verbose
        self.changes_made = []
        self.errors = []
        self.stats = defaultdict(int)

    def setup_backup_dir(self):
        """Create backup directory with timestamp"""
        if not self.dry_run:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.backup_path = self.backup_dir / f'refactor_{timestamp}'
            self.backup_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Backup directory: {self.backup_path}")

    def should_exclude(self, file_path: Path) -> bool:
        """Check if file should be excluded from refactoring"""
        str_path = str(file_path)
        for pattern in EXCLUDE_PATTERNS:
            if pattern in str_path:
                return True
        return False

    def detect_context(self, node: ast.AST, file_content: str) -> Optional[str]:
        """Detect the context of a Dict usage from surrounding code"""
        # Get the line content
        if hasattr(node, 'lineno'):
            lines = file_content.split('\n')
            if 0 <= node.lineno - 1 < len(lines):
                line = lines[node.lineno - 1].lower()

                # Check for context keywords
                for context, (model, _) in MODEL_MAPPINGS.items():
                    if context in line:
                        return context

        # Check function/variable name if it's a FunctionDef
        if isinstance(node, ast.FunctionDef):
            func_name = node.name.lower()
            for context in MODEL_MAPPINGS:
                if context in func_name:
                    return context

        return None

    def get_model_for_context(self, context: Optional[str]) -> Tuple[str, str]:
        """Get appropriate Pydantic model for the detected context"""
        if context and context in MODEL_MAPPINGS:
            return MODEL_MAPPINGS[context]
        # Default fallback
        return ('Any', 'typing')

    def refactor_file(self, file_path: Path) -> bool:
        """Refactor a single Python file"""
        if self.should_exclude(file_path):
            return False

        try:
            with open(file_path, 'r') as f:
                original_content = f.read()

            # Parse the AST
            tree = ast.parse(original_content)

            # Track required imports
            required_imports = set()
            modifications = []

            # Find all Dict usages
            for node in ast.walk(tree):
                context = self.detect_context(node, original_content)
                model_name, import_from = self.get_model_for_context(context)

                # Handle function return types
                if isinstance(node, ast.FunctionDef) and node.returns:
                    if self._is_dict_annotation(node.returns):
                        modifications.append({
                            'type': 'return',
                            'node': node,
                            'model': model_name,
                            'line': node.lineno
                        })
                        if import_from != 'typing':
                            required_imports.add((import_from, model_name))

                # Handle function parameters
                if isinstance(node, ast.FunctionDef):
                    for arg in node.args.args:
                        if arg.annotation and self._is_dict_annotation(arg.annotation):
                            modifications.append({
                                'type': 'param',
                                'node': node,
                                'arg': arg,
                                'model': model_name,
                                'line': node.lineno
                            })
                            if import_from != 'typing':
                                required_imports.add((import_from, model_name))

                # Handle variable annotations
                if isinstance(node, ast.AnnAssign) and self._is_dict_annotation(node.annotation):
                    modifications.append({
                        'type': 'variable',
                        'node': node,
                        'model': model_name,
                        'line': node.lineno
                    })
                    if import_from != 'typing':
                        required_imports.add((import_from, model_name))

            if not modifications:
                return False

            # Apply modifications
            new_content = self._apply_modifications(
                original_content, modifications, required_imports
            )

            if new_content == original_content:
                return False

            # Backup original file
            if not self.dry_run:
                backup_path = self.backup_path / file_path.relative_to('.')
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_path)

            # Write modified content
            if self.dry_run:
                print(f"🔍 Would modify: {file_path}")
                if self.verbose:
                    print(f"  Changes: {len(modifications)} Dict replacements")
                    for mod in modifications[:3]:  # Show first 3
                        print(f"    Line {mod['line']}: Dict → {mod['model']}")
            else:
                with open(file_path, 'w') as f:
                    f.write(new_content)
                print(f"✅ Modified: {file_path} ({len(modifications)} changes)")

            self.stats['files_modified'] += 1
            self.stats['total_changes'] += len(modifications)
            self.changes_made.append((file_path, len(modifications)))

            # Run tests if requested
            if self.test_after and not self.dry_run:
                if not self._run_file_tests(file_path):
                    # Rollback on test failure
                    shutil.copy2(backup_path, file_path)
                    self.errors.append(f"Test failed for {file_path}, rolled back")
                    return False

            return True

        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")
            return False

    def _is_dict_annotation(self, annotation: ast.AST) -> bool:
        """Check if an annotation is a Dict type"""
        if isinstance(annotation, ast.Name) and annotation.id == 'Dict':
            return True
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name) and annotation.value.id == 'Dict':
                return True
        return False

    def _apply_modifications(self, content: str, modifications: List[dict],
                           required_imports: set) -> str:
        """Apply all modifications to the file content"""
        lines = content.split('\n')

        # Sort modifications by line number (reverse order to maintain line numbers)
        modifications.sort(key=lambda x: x['line'], reverse=True)

        # Apply each modification using regex
        for mod in modifications:
            line_idx = mod['line'] - 1
            if 0 <= line_idx < len(lines):
                line = lines[line_idx]
                model = mod['model']

                # Replace Dict patterns
                line = re.sub(r'\bDict\[str,\s*Any\]', model, line)
                line = re.sub(r'\bDict\[Any,\s*Any\]', model, line)
                line = re.sub(r'\bDict\b(?!\[)', model, line)

                lines[line_idx] = line

        # Add imports at the top
        if required_imports:
            import_lines = []
            for module, name in sorted(required_imports):
                import_lines.append(f"from {module} import {name}")

            # Find where to insert imports (after existing imports)
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    insert_idx = i + 1
                elif insert_idx > 0 and not line.strip():
                    break

            # Insert new imports
            for import_line in reversed(import_lines):
                # Check if import already exists
                if import_line not in content:
                    lines.insert(insert_idx, import_line)

        return '\n'.join(lines)

    def _run_file_tests(self, file_path: Path) -> bool:
        """Run tests for a specific file"""
        test_file = Path('tests') / f"test_{file_path.stem}.py"
        if test_file.exists():
            try:
                result = subprocess.run(
                    ['python', '-m', 'pytest', str(test_file), '-xvs'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.returncode == 0
            except:
                return False
        return True  # No test file, assume OK

    def run(self, target_patterns: List[str] = None):
        """Run the refactoring process"""
        self.setup_backup_dir()

        # Find all Python files
        if target_patterns:
            files = []
            for pattern in target_patterns:
                files.extend(Path('.').glob(pattern))
        else:
            files = list(Path('.').rglob('*.py'))

        # Filter and sort by violation count
        files_with_violations = []
        for file_path in files:
            if not self.should_exclude(file_path):
                count = self._count_dict_violations(file_path)
                if count > 0:
                    files_with_violations.append((file_path, count))

        # Sort by violation count (highest first)
        files_with_violations.sort(key=lambda x: x[1], reverse=True)

        print(f"\n🎯 Found {len(files_with_violations)} files with Dict violations")
        print(f"📊 Total violations to fix: {sum(c for _, c in files_with_violations)}\n")

        # Process files
        for file_path, violation_count in files_with_violations:
            print(f"Processing {file_path} ({violation_count} violations)...")
            self.refactor_file(file_path)

        # Print summary
        self.print_summary()

    def _count_dict_violations(self, file_path: Path) -> int:
        """Count Dict violations in a file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content.count('Dict[') + content.count('Dict ')
        except:
            return 0

    def print_summary(self):
        """Print refactoring summary"""
        print("\n" + "="*60)
        print("📊 REFACTORING SUMMARY")
        print("="*60)
        print(f"✅ Files modified: {self.stats['files_modified']}")
        print(f"🔧 Total changes: {self.stats['total_changes']}")

        if self.changes_made:
            print(f"\n📝 Top refactored files:")
            for file_path, count in sorted(self.changes_made, key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {file_path}: {count} changes")

        if self.errors:
            print(f"\n❌ Errors encountered:")
            for error in self.errors[:5]:
                print(f"  {error}")

        if self.dry_run:
            print(f"\n⚠️  DRY RUN - No files were actually modified")
            print(f"   Run without --dry-run to apply changes")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Mass refactor Dict type hints to Pydantic models'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--backup-dir', default='.backups',
        help='Directory to store backups (default: .backups)'
    )
    parser.add_argument(
        '--test-after', action='store_true',
        help='Run tests after each file modification'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        'targets', nargs='*',
        help='Specific file patterns to refactor (e.g., "tools/*.py")'
    )

    args = parser.parse_args()

    # Create refactorer instance
    refactorer = DictRefactorer(
        backup_dir=args.backup_dir,
        dry_run=args.dry_run,
        test_after=args.test_after,
        verbose=args.verbose
    )

    # Run refactoring
    refactorer.run(args.targets)

    return 0 if not refactorer.errors else 1


if __name__ == '__main__':
    sys.exit(main())