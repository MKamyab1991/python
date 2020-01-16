from click.testing import CliRunner

from danger_python.cli.main import cli
from tests.fixtures.shell import (danger_js_missing_path_fixture,
                                  danger_js_path_fixture,
                                  danger_success_fixture, subprocess_fixture)


def test_runner_discovers_danger_path():
    """
    Test that the runner discovers danger path.
    """
    runner = CliRunner()
    danger_path = "/Users/danger/.nvm/versions/node/v10.6.0/bin/danger"

    with subprocess_fixture(danger_js_path_fixture(danger_path)):
        result = runner.invoke(cli, ["run"])

    assert result.exit_code == 0
    assert result.output == "/Users/danger/.nvm/versions/node/v10.6.0/bin/danger\n"

def test_runner_errors_out_when_danger_js_is_not_found():
    """
    Test that the runner discovers danger path.
    """
    runner = CliRunner()

    with subprocess_fixture(danger_js_missing_path_fixture()):
        result = runner.invoke(cli, ["run"])

    assert result.exit_code == 1
    assert result.output == "danger-js not found in PATH\n"

def test_pr_command_invokes_danger_js_passing_arguments():
    """
    Test that pr command invokes danger_js passing correct arguments.
    """
    runner = CliRunner()
    arguments = [
        "pr",
        "https://github.com/microsoft/TypeScript/pull/34806",
        "--use-github-checks"
    ]
    danger_path = '/usr/bin/danger-js'
    danger_fixture = danger_success_fixture(danger_path, arguments, 'danger-js output')

    with subprocess_fixture(danger_js_path_fixture(danger_path), danger_fixture):
        result = runner.invoke(cli, arguments)

    assert danger_fixture.commands == [
        "/usr/bin/danger-js",
        "pr",
        "https://github.com/microsoft/TypeScript/pull/34806",
        "--use-github-checks",
        "-p",
        "danger-python",
    ]
    assert result.exit_code == 0
    assert result.output == 'danger-js output\n'
