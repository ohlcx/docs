#!/usr/bin/env python3
"""Build docs/mcp/tools/reference.md from the OHLCX MCP server's own files.

Usage:
    python3 scripts/build_mcp_reference.py /path/to/trading-app/src/Mcp          # write the page
    python3 scripts/build_mcp_reference.py /path/to/trading-app/src/Mcp --check  # fail if the page is stale

What comes from where:
    tool names and their order   descriptors/index.json (also copied to docs/mcp/tools/index.json)
    arguments                    descriptors/<tool>.json
    kind and availability        the tool classes (annotations and registration rules)
    areas and one-line summaries scripts/mcp_tool_areas.json (hand-written, in this repository)

The script stops when a tool of the index has no summary, a summary names a tool the index
does not have, or docs/mcp/tools/index.json is not the server's current index. Standard library only.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PAGE = os.path.join(REPO, "docs", "mcp", "tools", "reference.md")
PUBLIC_INDEX = os.path.join(REPO, "docs", "mcp", "tools", "index.json")
AREAS = os.path.join(HERE, "mcp_tool_areas.json")

AVAILABILITY = {
    "open": "Everyone",
    "user": "Signed in",
    "pro": "Signed in, OHLCX Pro",
    "backtests": "Signed in, server backtests on",
    "tickets": "Signed in, support desk connected",
    "admin": "Admin",
}


def fail(message: str) -> None:
    sys.stderr.write("build_mcp_reference: " + message + "\n")
    sys.exit(1)


def read_tool_classes(mcp: str) -> dict[str, dict[str, str]]:
    """Kind and availability of each tool, read from its class."""
    tools: dict[str, dict[str, str]] = {}
    for path in glob.glob(os.path.join(mcp, "Tools", "*", "*Tool.php")):
        source = open(path, encoding="utf-8").read()
        name = re.search(r"#\[Name\('([^']+)'\)\]", source)
        if not name:
            continue

        if re.search(r"#\[IsReadOnly\(true\)\]", source):
            kind = "Read"
        elif re.search(r"#\[IsDestructive\(true\)\]", source):
            kind = "Write, destructive"
        elif re.search(r"#\[IsDestructive\(false\)\]", source):
            kind = "Write"
        else:
            kind = "Write, no hint"

        traits = set(re.findall(r"^\s+use \\?(?:[\w\\]+\\)?(Registers\w+);", source, re.M))
        own_rule = "function shouldRegister" in source
        if "RegistersWhenBacktestServerRuns" in traits:
            availability = "backtests"
        elif "RegistersWhenSupportTicketsConfigured" in traits:
            availability = "tickets"
        elif own_rule and "StrategyRouting::available()" in source:
            availability = "pro"
        elif "RegistersWhenAdmin" in traits and not own_rule:
            availability = "admin"
        elif traits or own_rule:
            availability = "user"
        else:
            availability = "open"

        tools[name.group(1)] = {"kind": kind, "availability": AVAILABILITY[availability]}
    return tools


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def type_of(prop: dict) -> str:
    kind = prop.get("type", "any")
    if isinstance(kind, list):
        return " or ".join(kind)
    if kind == "array" and isinstance(prop.get("items"), dict) and prop["items"].get("type"):
        return "array of " + str(prop["items"]["type"])
    return str(kind)


def values_of(prop: dict) -> str:
    values = prop.get("enum")
    if not values and isinstance(prop.get("items"), dict):
        values = prop["items"].get("enum")
    return ", ".join("`" + str(v) + "`" for v in values) if values else ""


def arguments(descriptor: dict) -> list[str]:
    schema = descriptor.get("arguments") or descriptor.get("inputSchema") or {}
    props = schema.get("properties") or {}
    if not props:
        return ["No arguments.", ""]
    required = set(schema.get("required") or [])
    lines = ["| Argument | Type | Required | Description |", "|---|---|---|---|"]
    for name, prop in props.items():
        description = cell(prop.get("description", ""))
        allowed = values_of(prop)
        if allowed:
            description = (description + " " if description else "") + "Allowed: " + allowed + "."
        lines.append("| `%s` | %s | %s | %s |" % (name, type_of(prop), "yes" if name in required else "no", description))
    lines.append("")
    return lines


def build(mcp: str) -> str:
    index_path = os.path.join(mcp, "descriptors", "index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    if open(index_path, encoding="utf-8").read() != open(PUBLIC_INDEX, encoding="utf-8").read():
        fail("docs/mcp/tools/index.json is not the server's descriptors/index.json. Copy it first (scripts/sync-public-docs.sh in trading-app does).")

    order = [tool["name"] for tool in index["tools"]]
    files = {tool["name"]: tool["descriptor"] for tool in index["tools"]}
    classes = read_tool_classes(mcp)
    areas = json.load(open(AREAS, encoding="utf-8"))["areas"]

    placed = [name for area in areas for name, _ in area["tools"]]
    missing = [name for name in order if name not in placed]
    unknown = [name for name in placed if name not in files]
    twice = sorted({name for name in placed if placed.count(name) > 1})
    unread = [name for name in order if name not in classes]
    if missing or unknown or twice or unread:
        fail("areas file out of step. No summary: %s. Not in the index: %s. Twice: %s. No tool class: %s." % (missing, unknown, twice, unread))

    counts: dict[str, int] = {}
    for name in order:
        counts[classes[name]["availability"]] = counts.get(classes[name]["availability"], 0) + 1

    out = [
        "# Tool reference",
        "",
        "<!-- Generated by scripts/build_mcp_reference.py. Do not edit this page by hand: edit scripts/mcp_tool_areas.json or the server's descriptors and build it again. -->",
        "",
        "Every tool of the OHLCX MCP server (version %s), grouped by area: %d tools. Each tool has one line here and its arguments below. Tool names, argument names, types and argument descriptions are the server's own." % (index["server"].get("version", ""), len(order)),
        "",
        "For what the server can and cannot do, start with the [overview](../overview.md). The same list in the server's own order is the [generated tool list](README.md); the machine-readable index is [index.json](index.json).",
        "",
        "## How to read this page",
        "",
        "**Kind** is the hint the server sends with the tool, which MCP clients use to decide when to ask the user:",
        "",
        "| Kind | Meaning |",
        "|---|---|",
        "| Read | Marked read-only. It changes nothing. |",
        "| Write | Changes something. Marked not destructive. |",
        "| Write, destructive | Changes or deletes something, or changes what a strategy does. Marked destructive: clients should ask the user first. |",
        "| Write, no hint | Changes something and carries no hint. Treat it as a write and ask the user first. |",
        "",
        "**Availability** says who is offered the tool. A tool you are not offered is not in the tool list at all.",
        "",
        "| Availability | Tools | Listed when |",
        "|---|---|---|",
        "| Everyone | %d | Always, also without a signed-in user. |" % counts.get(AVAILABILITY["open"], 0),
        "| Signed in | %d | The request has a signed-in user. |" % counts.get(AVAILABILITY["user"], 0),
        "| Signed in, OHLCX Pro | %d | Signed in, on OHLCX Pro, where orders are routed for the signed-in user. |" % counts.get(AVAILABILITY["pro"], 0),
        "| Signed in, server backtests on | %d | Signed in, and the app has server backtests switched on. |" % counts.get(AVAILABILITY["backtests"], 0),
        "| Signed in, support desk connected | %d | Signed in, and the app is connected to the support desk. |" % counts.get(AVAILABILITY["tickets"], 0),
        "| Admin | %d | The signed-in user is an admin. |" % counts.get(AVAILABILITY["admin"], 0),
        "",
        "## Areas",
        "",
        "| Area | Tools |",
        "|---|---|",
    ]
    for area in areas:
        anchor = re.sub(r"[^a-z0-9 -]", "", area["title"].lower()).replace(" ", "-")
        out.append("| [%s](#%s) | %d |" % (area["title"], anchor, len(area["tools"])))
    out.append("")

    for area in areas:
        out += ["## " + area["title"], ""]
        if area.get("intro"):
            out += [area["intro"], ""]
        out += ["| Tool | What it does | Kind | Availability |", "|---|---|---|---|"]
        for name, summary in area["tools"]:
            out.append("| [`%s`](#%s) | %s | %s | %s |" % (name, name, cell(summary), classes[name]["kind"], classes[name]["availability"]))
        out.append("")
        for name, summary in area["tools"]:
            descriptor = json.load(open(os.path.join(mcp, "descriptors", files[name]), encoding="utf-8"))
            out += ["### `" + name + "`", "", summary, "", "%s. %s." % (classes[name]["kind"], classes[name]["availability"]), ""]
            out += arguments(descriptor)

    return "\n".join(out).rstrip("\n") + "\n"


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--check"]
    if len(args) != 1 or not os.path.isdir(os.path.join(args[0], "descriptors")):
        fail("give the path of the server's src/Mcp folder (the one that holds descriptors/ and Tools/).")
    page = build(args[0])
    if "--check" in sys.argv:
        current = open(PAGE, encoding="utf-8").read() if os.path.exists(PAGE) else ""
        if current != page:
            fail("docs/mcp/tools/reference.md is stale. Build it again.")
        print("reference.md is current.")
        return
    with open(PAGE, "w", encoding="utf-8") as handle:
        handle.write(page)
    print("Wrote %s" % os.path.relpath(PAGE, REPO))


if __name__ == "__main__":
    main()
