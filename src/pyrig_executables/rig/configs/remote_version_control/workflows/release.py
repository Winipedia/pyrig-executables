"""Workflow configuration for automated GitHub release creation."""

from pyrig.rig.configs.remote_version_control.workflows.release import (
    ReleaseWorkflowConfigFile as BaseReleaseWorkflowConfigFile,
)


class ReleaseWorkflowConfigFile(BaseReleaseWorkflowConfigFile):
    """You can override methods from the base class to customize behavior."""
