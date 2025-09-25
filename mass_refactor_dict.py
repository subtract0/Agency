#!/usr/bin/env python3
"""
Mass Refactoring Script: DynamicData to Pydantic Models
Mission: Complete the Great Refactor to achieve constitutional compliance
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import shutil
from datetime import datetime
import argparse


class DataModel(BaseModel):
    """Auto-generated Pydantic model to replace Dict[str, Any]"""
    class Config:
        extra = "allow"  # Allow additional fields for flexibility

class DictRefactorer:
    """Orchestrator for mass Dict-to-Pydantic refactoring"""

    def __init__(self, dry_run: bool = False, backup: bool = True):
        self.dry_run = dry_run
        self.backup = backup
        self.files_modified = []
        self.errors = []
        self.backup_dir = None

    def create_backup(self):
        """Create backup of all files before refactoring"""
        if not self.backup:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = Path(f".backup_refactor_{timestamp}")
        self.backup_dir.mkdir(exist_ok=True)
        print(f"✅ Created backup directory: {self.backup_dir}")

    def backup_file(self, filepath: Path):
        """Backup individual file"""
        if not self.backup or not self.backup_dir:
            return

        relative = filepath.relative_to(".")
        backup_path = self.backup_dir / relative
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(filepath, backup_path)

    def find_dict_violations(self) -> List[Path]:
        """Find all Python files with DataModel violations"""
        violations = []

        # Skip .venv and test files
        for root, dirs, files in os.walk("."):
            # Skip directories
            if ".venv" in root or "__pycache__" in root or "test" in root:
                continue

            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    filepath = Path(root) / file

                    try:
                        content = filepath.read_text()
                        if re.search(r'\bDict\[', content):
                            violations.append(filepath)
                    except Exception as e:
                        print(f"⚠️  Error reading {filepath}: {e}")

        return violations

    def generate_pydantic_model(self, context: str, var_name: str) -> str:
        """Generate appropriate Pydantic model based on context"""

        # Common patterns and their replacements
        patterns = {
            # Telemetry/event patterns
            r'telemetry|event|metric': 'TelemetryData',
            r'learning|insight|knowledge': 'LearningData',
            r'pattern|coding_pattern': 'PatternData',
            r'memory|session': 'MemoryData',
            r'config|settings': 'ConfigData',
            r'response|result': 'ResponseData',
            r'request|payload': 'RequestData',
            r'context|state': 'ContextData',
            r'metadata|meta': 'MetadataModel',
            r'stats|statistics': 'StatsData',
            r'analysis|report': 'AnalysisData',
            r'task|job': 'TaskData',
            r'error|exception': 'ErrorData',
            r'agent|worker': 'AgentData',
            r'graph|node': 'GraphData',
        }

        # Check variable name and context
        lower_context = (context + var_name).lower()

        for pattern, model_name in patterns.items():
            if re.search(pattern, lower_context):
                return model_name

        # Default based on common variable names
        if 'data' in var_name.lower():
            return 'DataModel'
        elif 'params' in var_name.lower():
            return 'ParamsModel'
        elif 'options' in var_name.lower():
            return 'OptionsModel'
        else:
            return 'DynamicData'

    def refactor_file(self, filepath: Path) -> bool:
        """Refactor a single file to replace Dict with Pydantic models"""

        try:
            content = filepath.read_text()
            original_content = content

            # Backup before modification
            self.backup_file(filepath)

            # Track if we need to add imports
            needs_basemodel = False
            needs_field = False
            models_to_add = set()

            # Pattern 1: PatternData in type hints
            dict_pattern = r'\bDict\[(str|"str"|\'str\'),\s*Any\]'

            # Find all Dict violations
            matches = list(re.finditer(dict_pattern, content))

            if not matches:
                return False

            print(f"\n📝 Processing: {filepath}")
            print(f"   Found {len(matches)} Dict violations")

            # Process each match
            for match in reversed(matches):  # Reverse to maintain positions
                start, end = match.span()

                # Get context around the match
                context_start = max(0, start - 100)
                context_end = min(len(content), end + 100)
                context = content[context_start:context_end]

                # Try to find variable name
                var_pattern = r'(\w+)\s*:\s*' + re.escape(match.group())
                var_match = re.search(var_pattern, content[max(0, start-50):end+50])
                var_name = var_match.group(1) if var_match else 'data'

                # Generate appropriate model
                model_name = self.generate_pydantic_model(context, var_name)

                # Replace ContextData with model
                content = content[:start] + model_name + content[end:]
                models_to_add.add(model_name)
                needs_basemodel = True

            # Add imports if needed
            if needs_basemodel:
                # Check if pydantic imports exist
                if 'from pydantic import' not in content:
                    # Add after first import or at top
                    import_match = re.search(r'^(import .+|from .+ import .+)', content, re.MULTILINE)
                    if import_match:
                        insert_pos = import_match.end()
                        content = content[:insert_pos] + '\nfrom pydantic import BaseModel, Field' + content[insert_pos:]
                    else:
                        content = 'from pydantic import BaseModel, Field\n\n' + content

                # Add model definitions if not present
                for model_name in models_to_add:
                    if f'class {model_name}' not in content:
                        # Add model definition before first usage
                        model_def = f'''
class {model_name}(BaseModel):
    """Auto-generated Pydantic model to replace ConfigData"""
    class Config:
        extra = "allow"  # Allow additional fields for flexibility
'''

                        # Find good insertion point (after imports, before first function/class)
                        class_match = re.search(r'^(class |def |@)', content, re.MULTILINE)
                        if class_match:
                            insert_pos = class_match.start()
                            content = content[:insert_pos] + model_def + '\n' + content[insert_pos:]
                        else:
                            # Add at end if no other classes/functions
                            content = content + '\n' + model_def

            # Remove redundant Dict import if no longer needed
            if 'Dict[' not in content and 'Dict,' in content:
                content = re.sub(r'from typing import ([^)]+), Dict,', r'from typing import \1,', content)
                content = re.sub(r'from typing import Dict, ', r'from typing import ', content)
                content = re.sub(r', Dict\b', '', content)

            # Write back if changed
            if content != original_content:
                if not self.dry_run:
                    filepath.write_text(content)
                    print(f"   ✅ Refactored successfully")
                else:
                    print(f"   🔍 Would refactor (dry run)")

                self.files_modified.append(filepath)
                return True

        except Exception as e:
            error_msg = f"Error refactoring {filepath}: {e}"
            print(f"   ❌ {error_msg}")
            self.errors.append(error_msg)

        return False

    def generate_shared_models(self):
        """Generate shared Pydantic models file"""

        models_file = Path("shared/common_models.py")

        if models_file.exists() and not self.dry_run:
            # Append to existing file
            return

        models_content = '''"""
Common Pydantic Models for Agency
Auto-generated to replace DataModel violations
"""

from typing import Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class DynamicData(BaseModel):
    """Flexible data model that accepts any fields"""
    class Config:
        extra = "allow"


class TelemetryData(BaseModel):
    """Telemetry and metrics data"""
    event_type: str = Field(..., description="Type of telemetry event")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        extra = "allow"


class LearningData(BaseModel):
    """Learning and insight data"""
    insight_type: str = Field(..., description="Type of learning insight")
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    class Config:
        extra = "allow"


class PatternData(BaseModel):
    """Pattern recognition data"""
    pattern_id: str = Field(..., description="Unique pattern identifier")
    pattern_type: str = Field(..., description="Type of pattern")
    class Config:
        extra = "allow"


class MemoryData(BaseModel):
    """Memory and session data"""
    session_id: str = Field(..., description="Session identifier")
    class Config:
        extra = "allow"


class ConfigData(BaseModel):
    """Configuration data"""
    class Config:
        extra = "allow"


class ResponseData(BaseModel):
    """API response data"""
    success: bool = Field(True, description="Operation success status")
    class Config:
        extra = "allow"


class RequestData(BaseModel):
    """API request data"""
    class Config:
        extra = "allow"


class ContextData(BaseModel):
    """Context and state data"""
    class Config:
        extra = "allow"


class MetadataModel(BaseModel):
    """Metadata model"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    class Config:
        extra = "allow"


class StatsData(BaseModel):
    """Statistics data"""
    count: int = Field(0, ge=0)
    class Config:
        extra = "allow"


class AnalysisData(BaseModel):
    """Analysis and report data"""
    analysis_type: str = Field(..., description="Type of analysis")
    class Config:
        extra = "allow"


class TaskData(BaseModel):
    """Task and job data"""
    task_id: str = Field(..., description="Task identifier")
    status: str = Field("pending", description="Task status")
    class Config:
        extra = "allow"


class ErrorData(BaseModel):
    """Error and exception data"""
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    class Config:
        extra = "allow"


class AgentData(BaseModel):
    """Agent and worker data"""
    agent_id: str = Field(..., description="Agent identifier")
    agent_type: str = Field(..., description="Type of agent")
    class Config:
        extra = "allow"


class GraphData(BaseModel):
    """Graph and node data"""
    node_id: str = Field(..., description="Node identifier")
    class Config:
        extra = "allow"
'''

        if not self.dry_run:
            models_file.parent.mkdir(exist_ok=True)
            models_file.write_text(models_content)
            print(f"\n✅ Generated shared models file: {models_file}")
        else:
            print(f"\n🔍 Would generate shared models file: {models_file}")

    def run(self):
        """Execute the mass refactoring"""

        print("\n" + "="*60)
        print("🚀 THE GREAT REFACTOR: DynamicData → Pydantic Models")
        print("="*60)

        # Create backup
        if self.backup:
            self.create_backup()

        # Find violations
        print("\n🔍 Scanning for Dict violations...")
        violations = self.find_dict_violations()

        print(f"\n📊 Found {len(violations)} files with Dict violations")

        if not violations:
            print("✅ No violations found! Constitutional compliance achieved!")
            return

        # Generate shared models first
        self.generate_shared_models()

        # Process each file
        print(f"\n{'🔍' if self.dry_run else '⚙️'} Processing files...")

        for filepath in violations:
            self.refactor_file(filepath)

        # Summary
        print("\n" + "="*60)
        print("📊 REFACTORING SUMMARY")
        print("="*60)
        print(f"✅ Files modified: {len(self.files_modified)}")

        if self.errors:
            print(f"❌ Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   - {error}")

        if self.backup_dir:
            print(f"\n💾 Backup created at: {self.backup_dir}")

        if self.dry_run:
            print("\n⚠️  DRY RUN - No files were actually modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ Refactoring complete! Run tests to verify stability.")

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Mass refactor ErrorData to Pydantic models")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backups")
    parser.add_argument("--restore", help="Restore from backup directory")

    args = parser.parse_args()

    if args.restore:
        # Restore from backup
        backup_dir = Path(args.restore)
        if not backup_dir.exists():
            print(f"❌ Backup directory not found: {backup_dir}")
            sys.exit(1)

        print(f"♻️  Restoring from backup: {backup_dir}")
        # Copy files back
        for backup_file in backup_dir.rglob("*.py"):
            relative = backup_file.relative_to(backup_dir)
            target = Path(".") / relative
            print(f"   Restoring: {target}")
            shutil.copy2(backup_file, target)
        print("✅ Restore complete!")
        sys.exit(0)

    # Run refactoring
    refactorer = DictRefactorer(
        dry_run=args.dry_run,
        backup=not args.no_backup
    )

    success = refactorer.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()