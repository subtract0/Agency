"""
Pydantic models for auditor agent
Ensures type safety and constitutional compliance
"""

from typing import List, Optional, Any
from pydantic import BaseModel, Field


class FileAnalysisResult(BaseModel):
    """Result of analyzing a single Python file"""
    file_path: str = Field(..., description="Path to the analyzed file")
    is_test_file: bool = Field(default=False, description="Whether this is a test file")
    functions: List[str] = Field(default_factory=list, description="List of function names")
    classes: List[str] = Field(default_factory=list, description="List of class names")
    test_functions: List[str] = Field(default_factory=list, description="List of test function names")
    behaviors: int = Field(default=0, description="Number of behaviors/functions")
    complexity: float = Field(default=0.0, description="Complexity metric")
    lines_of_code: int = Field(default=0, description="Number of lines in file")
    has_docstrings: bool = Field(default=False, description="Whether file has docstrings")
    imports: List[str] = Field(default_factory=list, description="List of imports")
    error: Optional[str] = Field(None, description="Error message if analysis failed")


class DirectoryAnalysisResult(BaseModel):
    """Result of analyzing a directory of Python files"""
    source_files: List[FileAnalysisResult] = Field(
        default_factory=list,
        description="Analysis results for source files"
    )
    test_files: List[FileAnalysisResult] = Field(
        default_factory=list,
        description="Analysis results for test files"
    )
    total_behaviors: int = Field(default=0, description="Total number of behaviors across all files")
    total_test_functions: int = Field(default=0, description="Total number of test functions")
    coverage_ratio: float = Field(default=0.0, description="Test coverage ratio")


class ComplexityMetrics(BaseModel):
    """Complexity metrics for code analysis"""
    cyclomatic_complexity: int = Field(default=0, description="Cyclomatic complexity")
    cognitive_complexity: int = Field(default=0, description="Cognitive complexity")
    max_nesting_depth: int = Field(default=0, description="Maximum nesting depth")
    function_count: int = Field(default=0, description="Number of functions")
    class_count: int = Field(default=0, description="Number of classes")


class QualityReport(BaseModel):
    """Overall code quality report"""
    file_analyses: List[FileAnalysisResult] = Field(
        default_factory=list,
        description="Individual file analysis results"
    )
    overall_complexity: ComplexityMetrics = Field(
        default_factory=ComplexityMetrics,
        description="Overall complexity metrics"
    )
    quality_score: float = Field(default=0.0, description="Overall quality score (0-100)")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Quality improvement recommendations"
    )
    violations: List[str] = Field(
        default_factory=list,
        description="Constitutional or quality violations found"
    )