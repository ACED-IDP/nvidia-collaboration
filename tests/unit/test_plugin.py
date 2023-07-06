import pytest

from nvidia_plugin import NVIDIAPathParser


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
