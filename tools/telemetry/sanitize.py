from __future__ import annotations
from pydantic import BaseModel, Field

import copy
import re
from typing import Any, Dict

# Patterns for secret-like values
_SECRET_VALUE_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{10,}"),        # OpenAI-style keys
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),       # GitHub PAT (min 20 chars)
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), # Slack tokens
    re.compile(r"AIza[0-9A-Za-z\-_]{15,}"),    # Google API key
]

# Keys that should always be redacted when present
_SENSITIVE_KEYS = {
    "api_key",
    "apikey",
    "authorization",
    "auth",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "client_secret",
    "password",
    "passwd",
}

_REPLACEMENT = "[REDACTED]"



class TelemetryData(BaseModel):
    """Auto-generated Pydantic model to replace Dict[str, Any]"""
    class Config:
        extra = "allow"  # Allow additional fields for flexibility

def _redact_str(s: str) -> str:
    out = s
    for pat in _SECRET_VALUE_PATTERNS:
        out = pat.sub(_REPLACEMENT, out)
    return out


def _redact_any(val: Any) -> Any:
    if isinstance(val, str):
        return _redact_str(val)
    if isinstance(val, dict):
        return {k: _redact_any(v) for k, v in val.items()}
    if isinstance(val, list):
        return [_redact_any(v) for v in val]
    return val


def redact_event(event: TelemetryData) -> TelemetryData:
    """Redact sensitive material from a telemetry event.

    Rules:
    - For known sensitive keys (case-insensitive), replace value with [REDACTED]
    - For string values, mask known secret-like patterns (OpenAI, GH PAT, Slack, Google)
    - Keep structure intact; avoid removing non-secret fields
    """
    if not isinstance(event, dict):
        return event
    safe = copy.deepcopy(event)

    def _walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            new: TelemetryData = {}
            for k, v in obj.items():
                if k.lower() in _SENSITIVE_KEYS:
                    new[k] = _REPLACEMENT
                else:
                    new[k] = _walk(v)
            return new
        if isinstance(obj, list):
            return [_walk(v) for v in obj]
        if isinstance(obj, str):
            return _redact_str(obj)
        return obj

    return _walk(safe)
