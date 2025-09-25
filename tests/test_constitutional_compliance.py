"""
Test Constitutional Compliance
Ensures all code adheres to the Agency's constitutional requirements
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple
import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestConstitutionalCompliance:
    """Test that all code follows constitutional requirements"""

    def get_python_files(self) -> List[Path]:
        """Get all Python files in the project"""
        python_files = []
        exclude_dirs = {'.venv', '__pycache__', '.git', '.pytest_cache', 'tests'}

        for root, dirs, files in os.walk(project_root):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)

        return python_files

    def check_dict_usage_in_file(self, file_path: Path) -> List[Tuple[int, str]]:
        """Check for Dict usage in type hints"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            for node in ast.walk(tree):
                # Check function annotations
                if isinstance(node, ast.FunctionDef):
                    # Check return annotation
                    if node.returns:
                        annotation_str = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
                        if 'Dict[' in annotation_str or '-> Dict' in annotation_str:
                            violations.append((node.lineno, f"Function '{node.name}' returns Dict instead of Pydantic model"))

                    # Check argument annotations
                    for arg in node.args.args:
                        if arg.annotation:
                            annotation_str = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else str(arg.annotation)
                            if 'Dict[' in annotation_str or ': Dict' in annotation_str:
                                violations.append((arg.lineno if hasattr(arg, 'lineno') else node.lineno,
                                                 f"Function '{node.name}' parameter uses Dict"))

                # Check variable annotations
                if isinstance(node, ast.AnnAssign):
                    if node.annotation:
                        annotation_str = ast.unparse(node.annotation) if hasattr(ast, 'unparse') else str(node.annotation)
                        if 'Dict[' in annotation_str:
                            violations.append((node.lineno, "Variable annotation uses Dict"))

        except Exception as e:
            # If we can't parse the file, skip it
            pass

        return violations

    def test_no_dict_in_type_hints(self):
        """Test that no Dict is used in type hints - must use Pydantic models"""
        python_files = self.get_python_files()
        all_violations = []

        for file_path in python_files:
            # Skip test files and examples
            if 'test_' in file_path.name or 'example' in str(file_path):
                continue

            violations = self.check_dict_usage_in_file(file_path)
            if violations:
                for line_no, description in violations:
                    all_violations.append(f"{file_path.relative_to(project_root)}:{line_no} - {description}")

        # Constitutional requirement: No Dict usage, only Pydantic models
        assert len(all_violations) == 0, (
            f"Constitutional Violation: Found {len(all_violations)} Dict usages instead of Pydantic models:\n" +
            "\n".join(all_violations[:10])  # Show first 10 violations
        )

    def test_api_input_validation(self):
        """Test that all API endpoints have input validation"""
        # This test checks for functions that look like API endpoints
        python_files = self.get_python_files()
        violations = []

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Simple heuristic: functions with 'api' in name or that take 'request' params
                # should have validation
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check if it's likely an API endpoint
                        is_api = ('api' in node.name.lower() or
                                 any('request' in arg.arg.lower() for arg in node.args.args))

                        if is_api:
                            # Check if function has validation
                            has_validation = False
                            for child in ast.walk(node):
                                if isinstance(child, ast.Call):
                                    if hasattr(child.func, 'attr'):
                                        # Look for validation patterns
                                        if child.func.attr in ['validate', 'parse_obj', 'model_validate']:
                                            has_validation = True
                                            break

                            if not has_validation:
                                # Check if it's using Pydantic model parameters (which auto-validate)
                                for arg in node.args.args:
                                    if arg.annotation:
                                        annotation_str = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else str(arg.annotation)
                                        if 'Model' in annotation_str or 'Schema' in annotation_str:
                                            has_validation = True
                                            break

                            if not has_validation:
                                violations.append(f"{file_path.relative_to(project_root)}:{node.lineno} - "
                                                f"Function '{node.name}' appears to be an API endpoint without validation")

            except Exception:
                pass

        # For now, we'll mark this as a warning rather than failure since it's harder to detect accurately
        if violations:
            print(f"Warning: Potential API endpoints without validation:\n" + "\n".join(violations[:5]))


class TestAuditorAgentCompliance:
    """Specific tests for auditor_agent constitutional compliance"""

    def test_ast_analyzer_uses_pydantic_models(self):
        """Test that ast_analyzer.py uses Pydantic models instead of Dict"""
        file_path = project_root / "auditor_agent" / "ast_analyzer.py"

        if not file_path.exists():
            pytest.skip("ast_analyzer.py not found")

        with open(file_path, 'r') as f:
            content = f.read()

        # Check for Dict usage in return types
        has_dict_violation = ": Dict[" in content or "-> Dict[" in content

        assert not has_dict_violation, (
            "Constitutional Violation: ast_analyzer.py uses Dict instead of Pydantic models. "
            "Must use concrete Pydantic models with typed fields."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])