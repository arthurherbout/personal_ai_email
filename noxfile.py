"""
Shortcuts for standard codebase operations.
"""

import nox


@nox.session(name="format", python=False)
def format(session):
    """
    Run all formatting.
    """
    session.log("Formatting all files.")
    session.run("uv", "run", "--all-packages", "ruff", "format")
    session.run("uv", "run", "--all-packages", "ruff", "check", "--fix")


@nox.session(name="lint", python=False)
def lint(session):
    """
    Run lint checks only (no auto-fix).
    """
    session.log("Linting all files.")
    session.run("uv", "run", "--all-packages", "ruff", "check", ".")


@nox.session(name="test", python=False)
def test(session):
    """
    Run tests.
    """
    session.log("Running all tests.")
    session.run("uv", "run", "--all-packages", "pytest")
