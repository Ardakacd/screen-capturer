"""
Tasks package - contains all CrewAI tasks for the workflow system.
"""

from tasks.url_finding_task import URLFindingTask
from tasks.workflow_execution_task import WorkflowExecutionTask

__all__ = ["URLFindingTask", "WorkflowExecutionTask"]

