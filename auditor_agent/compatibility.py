"""
Compatibility layer for transitioning from Dict to Pydantic models
Ensures backward compatibility during the healing process
"""

from typing import Dict, Any, Union
from shared.common_models import model_to_dict, dict_to_model,  BaseResponse, MetricsData, ConfigData, TaskResult, AnalysisResult

from auditor_agent.models import FileAnalysisResult, DirectoryAnalysisResult


def to_dict(analysis: Union[Dict, DirectoryAnalysisResult, FileAnalysisResult]) -> Dict[str, Any]:
    """
    Convert analysis result to dictionary format for backward compatibility.

    This is a temporary compatibility layer to help transition from Dict to Pydantic models.
    It allows existing code to continue working while we gradually update all consumers.
    """
    # If already a dict, return as-is
    if isinstance(analysis, dict):
        return analysis

    # If DirectoryAnalysisResult, convert to dict
    if isinstance(analysis, DirectoryAnalysisResult):
        return {
            "source_files": [to_dict(f) for f in analysis.source_files],
            "test_files": [to_dict(f) for f in analysis.test_files],
            "total_behaviors": analysis.total_behaviors,
            "total_test_functions": analysis.total_test_functions,
            "coverage_ratio": analysis.coverage_ratio
        }

    # If FileAnalysisResult, convert to dict
    if isinstance(analysis, FileAnalysisResult):
        return {
            "file_path": analysis.file_path,
            "is_test_file": analysis.is_test_file,
            "functions": analysis.functions,
            "classes": analysis.classes,
            "test_functions": analysis.test_functions,
            "behaviors": analysis.behaviors,
            "complexity": analysis.complexity,
            "lines_of_code": analysis.lines_of_code,
            "has_docstrings": analysis.has_docstrings,
            "imports": analysis.imports,
            "error": analysis.error
        }

    # For any other type, try to convert
    if hasattr(analysis, 'dict'):
        return analysis.dict()
    elif hasattr(analysis, '__dict__'):
        return analysis.__dict__

    # Fallback
    return {}