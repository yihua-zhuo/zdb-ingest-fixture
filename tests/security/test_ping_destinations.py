"""Caller-controlled internal destinations must never reach the ping runner."""

import subprocess
from unittest.mock import patch

import pytest

from app import app


@pytest.mark.parametrize("destination", ["127.0.0.1", "10.0.0.1", "169.254.0.1", "::1"])
def test_ping_does_not_probe_internal_destination(destination):
    commands = []

    def fake_run(command, *args, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="probe-result", stderr="")

    # Replace process execution so the regression test cannot send ICMP traffic.
    with patch("subprocess.run", side_effect=fake_run):
        app.test_client().get("/ping", query_string={"host": destination})

    for command in commands:
        arguments = command if isinstance(command, str) else " ".join(map(str, command))
        assert destination not in arguments, (
            f"Caller-selected internal destination {destination} reached process execution"
        )
