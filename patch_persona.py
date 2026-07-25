"""Pre-startup patcher for persona_engine.py.

Run this before server.py / gateway.py to fix:
1. Default model fallback 'deepseek-chat' -> 'deepseek-v4-pro'
2. Add response_format json_object
3. Explicitly disable thinking to prevent <think> blocks in output
4. Strip <think> blocks in _parse_json as safety net
"""
import re
import sys

FILE = "persona_engine.py"

with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

changes = 0

# 1. Fix default model
old_default = 'self.persona_cfg.get("model", "deepseek-chat")'
new_default = 'self.persona_cfg.get("model", "deepseek-v4-pro")'
if old_default in code:
    code = code.replace(old_default, new_default)
    changes += 1
    print(f"[patch] Fixed default model to deepseek-v4-pro")

# 2. Replace _completion_options to add response_format + force disable thinking
old_completion = '''    def _completion_options(self) -> dict[str, Any]:
        options: dict[str, Any] = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.thinking_mode:
            options["extra_body"] = {"thinking": {"type": self.thinking_mode}}
        return options'''

new_completion = '''    def _completion_options(self) -> dict[str, Any]:
        options: dict[str, Any] = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"},
        }
        if self.thinking_mode:
            options["extra_body"] = {"thinking": {"type": self.thinking_mode}}
        else:
            # Explicitly disable thinking to prevent <think> blocks in output
            options["extra_body"] = {"thinking": {"type": "disabled"}}
        return options'''

if old_completion in code:
    code = code.replace(old_completion, new_completion)
    changes += 1
    print(f"[patch] Updated _completion_options: +response_format, +thinking disabled")

# 3. Enhance _parse_json to strip <think> blocks
old_parse_start = '''    def _parse_json(self, raw: str) -> dict | None:
        text = raw.strip()
        if not text:
            return None'''

new_parse_start = '''    def _parse_json(self, raw: str) -> dict | None:
        text = raw.strip()
        if not text:
            return None
        # Strip thinking blocks that some models include
        text = re.sub(r"<think>[\\s\\S]*?</think>", "", text).strip()
        if not text:
            return None'''

if old_parse_start in code:
    code = code.replace(old_parse_start, new_parse_start)
    changes += 1
    print(f"[patch] Enhanced _parse_json to strip <think> blocks")

if changes > 0:
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[patch] Applied {changes} patches to {FILE}")
else:
    print(f"[patch] No patches needed (already applied or code changed)")

sys.exit(0)
