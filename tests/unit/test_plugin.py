import pytest

from plugins.gen3_util_plugin_nvidia import NVIDIAPathParser, parse_path


def test_plugin(expected_paths, expected_tissues, expected_patients):
    """Ensure that the plugin is loaded and the patient_id and specimen_id are extracted from expected_paths."""
    assert len(expected_paths) > 0, "expected_paths should not be empty"
    parser = NVIDIAPathParser()
    for expected_path in expected_paths:
        patient_id = parser.extract_patient_identifier(expected_path)
        assert patient_id, f"patient_id should be extracted {patient_id} {expected_path}"
        assert patient_id.value in expected_patients, f"patient_id should be in expected_patients {patient_id} {expected_path}"
        specimen_id = parser.extract_specimen_identifier(expected_path)
        if specimen_id:
            assert specimen_id.value in expected_tissues, f"specimen_id should be in expected_tissues {specimen_id} {expected_path}"


def test_fixture():
    path = 'P1/R1_A.B.C_T1_2023_01_01_RAND1_1_test.txt'
    _ = parse_path(path)
    print(_)
    assert _['round'] == 'R1'
    assert _['markers'] == ['A', 'B', 'C']
    assert _['tissue'] == 'T1'
    assert _['date_of_imaging'] == '2023-01-01T00:00:00'
    assert _['random_file_number'] == 'RAND1'
    assert _['channel_id'] == '1'
    assert _['file_name'] == 'R1_A.B.C_T1_2023_01_01_RAND1_1_test.txt'
