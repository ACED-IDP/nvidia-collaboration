import pathlib

import pytest

from gen3_util_plugin_nvidia import parse_path
import gen3_util_plugin_nvidia

# add some arbitrary do not include paths
gen3_util_plugin_nvidia.BLACKLIST = [
    'HandE/2020_08_13__8667_31480.tif',
    'HandE_annotations/HandE/tifs.tar.gz',
    'annotations/2020_08_13__8675_57658.json',
    '.DS_Store',
]


def test_expected_paths(fixtures_path, expected_paths):
    """Ensure that the expected paths are present in the test fixtures."""
    assert len(expected_paths) > 0, "expected_paths should not be empty"
    for expected_path in expected_paths:
        assert pathlib.Path(fixtures_path, expected_path).exists(), f"expected_path should exist {expected_path}"


def test_parse_paths_good(fixtures_path, expected_paths):
    """Ensure that the (non blacklisted ) paths are parsed correctly."""
    expected_no_patient_count = 1
    actual_no_patient_count = 0
    for expected_path in expected_paths:
        if expected_path in gen3_util_plugin_nvidia.BLACKLIST:
            continue
        _ = parse_path(expected_path)
        if not _['patient']:
            actual_no_patient_count += 1
    assert actual_no_patient_count == expected_no_patient_count, f"actual_no_patient_count should be {expected_no_patient_count} {actual_no_patient_count}"


def test_parse_paths_bad(fixtures_path, expected_paths):
    """Ensure that the (blacklisted ) paths are not included"""
    with pytest.raises(ValueError):
        for expected_path in expected_paths:
            _ = parse_path(expected_path)


def test_plugin_good(fixtures_path, expected_paths):
    """Ensure that the plugin is loaded and the patient_id and specimen_id are extracted from expected_paths."""
    parser = gen3_util_plugin_nvidia.NVIDIAPathParser()
    expected_no_patient_count = 1
    actual_no_patient_count = 0

    for expected_path in expected_paths:
        if expected_path in gen3_util_plugin_nvidia.BLACKLIST:
            continue
        expected_path = fixtures_path / expected_path
        patient_id = parser.extract_patient_identifier(str(expected_path))
        if not patient_id:
            actual_no_patient_count += 1
    assert actual_no_patient_count == expected_no_patient_count, f"actual_no_patient_count should be {expected_no_patient_count} {actual_no_patient_count}"

        # assert patient_id.value in expected_patients, f"patient_id should be in expected_patients {patient_id} {expected_path}"
        # specimen_id = parser.extract_specimen_identifier(expected_path)
        # if specimen_id:
        #     assert specimen_id.value in expected_tissues, f"specimen_id should be in expected_tissues {specimen_id} {expected_path}"
