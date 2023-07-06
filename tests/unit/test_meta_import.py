import json
import pathlib
from collections import defaultdict

from click.testing import CliRunner

from gen3_util.cli.cli import cli

def test_meta_plugin(expected_paths):
    """
    This test is to test the plugin functionality of the meta command.

    """
    # plugin_path = pathlib.Path('./plugins').absolute()
    # print(plugin_path)
    plugin_path = './plugins'
    params = f'--format json meta  import dir tests/fixtures/ tmp/foometa --project_id aced-foometa --plugin_path {plugin_path} --remove_path_prefix tests/fixtures/'.split()
    runner = CliRunner()
    result = runner.invoke(cli, params)
    print(result.output)
    assert result.exit_code == 0
    _ = json.loads(result.output)
    assert _['summary']['DocumentReference']['size']  >  0, "DocumentReference size is not > 0"
    assert _['summary']['DocumentReference']['count'] == 1, "DocumentReference count is not 1"
    assert _['summary']['Specimen']['count'] == 1, "Specimen count is not 1"
    assert _['summary']['Patient']['count'] == 1, "Patient count is not 1"

