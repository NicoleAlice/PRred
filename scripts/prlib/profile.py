"""Reader for .pr-ready/profile.md (tolerant: bad input yields defaults + warnings)."""
from __future__ import annotations

import re
from pathlib import Path

DEFAULT_BUDGET = 500

POLICY_VALUES = {
    "ai_description": ("allowed", "forbidden", "unclear"),
    "ai_disclosure": ("none", "required-in-description", "required-in-trailer",
                      "forbidden-trailer", "unclear"),
    "prior_approval": ("required", "not-required", "unclear"),
}


def _section(heading):
    h = heading.strip().lower()
    if h == "generated files":
        return "generated"
    if h == "risk paths":
        return "risk"
    if h == "budget":
        return "budget"
    if h == "project rules":
        return "rules"
    return None


def read_profile(cwd):
    profile = {
        "found": False,
        "generated": [],
        "risk_paths": [],
        "budget": DEFAULT_BUDGET,
        "policy": dict((k, "unclear") for k in POLICY_VALUES),
        "warnings": [],
    }
    path = Path(str(cwd)) / ".pr-ready" / "profile.md"
    try:
        with open(str(path), encoding="utf-8", newline="") as fh:
            text = fh.read()
    except FileNotFoundError:
        return profile
    except (OSError, UnicodeDecodeError) as exc:
        profile["warnings"].append("cannot read .pr-ready/profile.md: %s" % exc)
        return profile

    profile["found"] = True
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#"):
            if line.startswith("##") and not line.startswith("###"):
                section = _section(line.lstrip("#"))
            continue
        if section in ("generated", "risk"):
            m = re.match(r"^[-*]\s+`([^`]+)`", line)
            if m:
                key = "generated" if section == "generated" else "risk_paths"
                profile[key].append(m.group(1).strip())
        elif section == "budget":
            m = re.match(r"^(?:[-*]\s+)?max_lines\s*:\s*(.*)$", line)
            if m:
                value = m.group(1).strip().strip("`")
                if re.fullmatch(r"\d+", value) and int(value) > 0:
                    profile["budget"] = int(value)
                else:
                    profile["warnings"].append(
                        "invalid max_lines %r; using %d" % (value, DEFAULT_BUDGET))
        elif section == "rules":
            m = re.match(r"^[-*]\s+(\w+)\s*:\s*([\w-]+)", line)
            if m and m.group(1) in POLICY_VALUES:
                key, value = m.group(1), m.group(2)
                if value in POLICY_VALUES[key]:
                    profile["policy"][key] = value
                else:
                    profile["warnings"].append(
                        "invalid %s value %r; using unclear" % (key, value))
    return profile
