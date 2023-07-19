import json
import pathlib
from collections import defaultdict

from click.testing import CliRunner

from gen3_util.cli.cli import cli

# TODO - add tests for expected_tissues, expected_patients, expected_markers, etc.

def test_meta_plugin(expected_paths):
    """
    This test is to test the plugin functionality of the meta command.

    """
    plugin_path = './gen3_util_plugin_nvidia '
    params = f'--format json meta  import dir tests/fixtures/ tmp/foometa --project_id aced-foometa --plugin_path {plugin_path} --remove_path_prefix tests/fixtures/'.split()
    print(' '.join(params))
    runner = CliRunner()
    result = runner.invoke(cli, params)
    print(result.output)
    assert result.exit_code == 0
    _ = json.loads(result.output)
    assert _['summary']['DocumentReference']['size']  >  0, "DocumentReference size is not > 0"
    assert _['summary']['DocumentReference']['count'] == 736, "DocumentReference count is not 736 (738 - 2 blacklisted)"
    assert _['summary']['Specimen']['count'] == 13, "Specimen count is not 13"
    assert _['summary']['Patient']['count'] == 13, "Patient count is not 13"

