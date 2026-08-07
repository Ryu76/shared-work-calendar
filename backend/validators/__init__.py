"""Input-validation boundaries.

Pydantic request schemas remain the authoritative API validators; upload validation
is injected into the task service to retain the established MIME/signature rules.
"""
