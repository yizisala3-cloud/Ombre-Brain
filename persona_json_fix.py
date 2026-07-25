"""Monkey-patch PersonaStateEngine._completion_options to enforce JSON output.

This module is imported at startup (via entrypoint) to patch the persona engine
so that deepseek-v4-pro reliably returns pure JSON without markdown wrapping.

Also patches the default model fallback from 'deepseek-chat' to 'deepseek-v4-pro'.
"""
import persona_engine

_original_completion_options = persona_engine.PersonaStateEngine._completion_options

def _patched_completion_options(self):
    options = _original_completion_options(self)
    # Force JSON output format to prevent markdown-wrapped responses
    if not self.thinking_mode:  # response_format is incompatible with thinking mode
        options["response_format"] = {"type": "json_object"}
    return options

persona_engine.PersonaStateEngine._completion_options = _patched_completion_options

# Fix default model name
# The class __init__ uses 'deepseek-chat' as default which is no longer valid
# This ensures if config somehow doesn't load, we still use a valid model
_original_init = persona_engine.PersonaStateEngine.__init__

def _patched_init(self, config, db_path=None):
    _original_init(self, config, db_path)
    if self.model == "deepseek-chat":
        self.model = "deepseek-v4-pro"

persona_engine.PersonaStateEngine.__init__ = _patched_init
