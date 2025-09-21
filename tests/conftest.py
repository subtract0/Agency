import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Ensure project root is on sys.path so `agency_code_agent` can be imported
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables for tests (e.g., OPENAI_API_KEY)
load_dotenv()


@pytest.fixture(autouse=True, scope="function")
def cleanup_test_artifacts():
    """Global cleanup of test artifacts after each test."""
    yield
    # Clean up any test files that might be created
    test_files = ["fib.py", "test_fib.py", "test_file.py", "sample.py", "example.py"]
    for filename in test_files:
        if os.path.exists(filename):
            os.unlink(filename)


@pytest.fixture
def temp_workspace(tmp_path):
    """Provide a temporary workspace directory for tests."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir(exist_ok=True)
    return workspace


@pytest.fixture
def temp_file_with_content(tmp_path):
    """Provide a temporary file with default content."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello World\nThis is a test file\nWith multiple lines")
    return test_file
