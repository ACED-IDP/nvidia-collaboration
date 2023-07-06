#!/usr/bin/env python

import click
import pathlib
import logging
import uuid

from fhir.resources.researchstudy import ResearchStudy
from fhir.resources.researchsubject import ResearchSubject
from fhir.resources.patient import Patient
from fhir.resources.specimen import Specimen
from fhir.resources.task import Task
from fhir.resources.documentreference import DocumentReference
from fhir.resources.domainresource import DomainResource
from fhir.resources.observation import Observation

RAW_DATA_PATH = pathlib.Path('data/raw')
FHIR_DATA_PATH = pathlib.Path('data/fhir')
DIRECTORY_LISTING_PATH = RAW_DATA_PATH / 'directory-listing.txt'

BASE_PATH = '/home/exacloud/gscratch/CEDAR/cIFimaging/Cyclic_Workflow/2020_Immune/RawImages'
GENE_ID_URL = "http://www.genenames.org/geneId"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ACED_NAMESPACE = uuid.uuid3(uuid.NAMESPACE_DNS, 'aced-ipd.org')

# open file pointers
EMITTERS = {}

ALREADY_EMITTED = set()

RESEARCH_STUDY = None


def emitter(output_path: pathlib.Path, name: str):
    """Maintain a hash of open files."""
    if name not in EMITTERS:
        EMITTERS[name] = open(output_path / f"{name}.ndjson", "w")
    return EMITTERS[name]


def emit(output_path: pathlib.Path, resource: DomainResource):
    """Serialize to ndjson."""
    if resource.relative_path() not in ALREADY_EMITTED:
        emitter(output_path, resource.resource_type).write(resource.json())
        emitter(output_path, resource.resource_type).write('\n')
        ALREADY_EMITTED.add(resource.relative_path())


def close_all_emitters():
    """Close all emitters."""
    for _ in EMITTERS.values():
        _.close()


def parse_line(line: str) -> dict:
    """Parse directory listing."""
    # 'RoundNumber5_MarkerName.MarkerName.MarkerName.MarkerName_TissueID_DateOfImaging__RandomFileSpecificNumber_ChannelID'
    line = line.replace(BASE_PATH, '').rstrip()
    if line == '':
        return None
    if line.startswith('/'):
        line = line[1:]

    if '/' not in line:
        logger.debug(f"Start cell-line: {line}")
        return None

    try:
        cell_line, file_name = line.split('/')
    except ValueError:
        logger.warning(f"Un-parsable: {line}")
        return None

    if not all([cell_line, file_name]):
        logger.warning(f"Un-parsable: {line}")
        return None

    file_name = file_name.replace('__', '_')

    try:
        round_, markers, tissue, year, month, day, random_file_number, channel_id, u_ = file_name.split('_')
        markers = markers.split('.')
        date_of_imaging = f"{year}_{month}_{day}"

        if u_:
            pass

        return {
            'round': round_,
            'markers': markers,
            'tissue': tissue,
            'date_of_imaging': date_of_imaging,
            'random_file_number': random_file_number,
            'channel_id': channel_id,
            'file_name': file_name,
            'patient': cell_line,
            'path': line
        }

    except ValueError:
        logger.debug(f"Only file_name: {line}")
        return {
            'round': None,
            'markers': None,
            'tissue': None,
            'date_of_imaging': None,
            'random_file_number': None,
            'channel_id': None,
            'file_name': file_name,
            'patient': cell_line,
            'path': line
        }


def emit_research_study(output_path, project, description):
    """Creates bare-bones study."""
    global RESEARCH_STUDY
    study = {
        'title': project,
        'id': str(uuid.uuid5(ACED_NAMESPACE, project)),
        'description': description,
        'status': 'active',
        "resourceType": "ResearchStudy",
    }
    RESEARCH_STUDY = ResearchStudy.parse_obj(study)
    emit(output_path, RESEARCH_STUDY)


def _patient_id(line):
    """Mint a patient id."""
    return str(uuid.uuid5(ACED_NAMESPACE, line['patient']))


def emit_patient(output_path, line):
    """Render a patient"""
    assert 'patient' in line, line
    patient = {
        'id': _patient_id(line),
        'identifier': [
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/tissue_id',
                'value': line['tissue']
            }
        ],
        "resourceType": "Patient",
    }
    patient_ = Patient.parse_obj(patient)
    emit(output_path, patient_)


def _research_subject_id(line):
    """Mint a ResearchSubject id."""
    return str(uuid.uuid5(ACED_NAMESPACE, line['patient'] + "/ResearchSubject"))


def emit_research_subject(output_path, line):
    """Render and write."""
    global RESEARCH_STUDY
    assert 'patient' in line, line
    research_subject = {
        'id': _research_subject_id(line),
        'identifier': [
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/tissue_id',
                'value': line['tissue']
            }
        ],
        'individual': {'reference': f"Patient/{_patient_id(line)}"},
        'study': {'reference': RESEARCH_STUDY.relative_path()},
        'status': 'on-study',
        "resourceType": "ResearchSubject",
    }
    research_subject_ = ResearchSubject.parse_obj(research_subject)
    emit(output_path, research_subject_)


def _specimen_id(line):
    """Mint a Specimen id."""
    return str(uuid.uuid5(ACED_NAMESPACE, line['tissue'] + "/Specimen"))


def emit_specimen(output_path, line):
    assert 'patient' in line, line
    if not line['tissue']:
        return

    specimen = {
        'id': _specimen_id(line),
        'identifier': [
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/tissue_id',
                'value': line['tissue']
            }
        ],
        'subject': {'reference': f"Patient/{_patient_id(line)}"},
        "resourceType": "Specimen",
    }
    specimen_ = Specimen.parse_obj(specimen)
    emit(output_path, specimen_)


def _task_id(line):
    """Mint a Task id."""
    return str(uuid.uuid5(ACED_NAMESPACE, line['patient'] + '/' + line['round'] + '/' + line['channel_id'] + "/Task"))


def emit_task(output_path, line):
    assert 'patient' in line, line
    if not line['tissue']:
        return

    task = {
        'id': _task_id(line),
        'identifier': [
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/tissue_id',
                'value': line['tissue']
            },
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/channel_id',
                'value': line['channel_id']
            },
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/round',
                'value': line['round']
            }
        ],
        'for': {'reference': f"Patient/{_patient_id(line)}"},
        'focus': {'reference': f"Specimen/{_specimen_id(line)}"},
        "resourceType": "Task",
        "intent": "unknown",
        "status": "completed",
        "lastModified": line['date_of_imaging'],
        "input": [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/",
                            "code": "Specimen",
                        }
                    ]
                },
                "valueReference": {'reference': f"Specimen/{_specimen_id(line)}"}
            }
        ],
        "output": [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/",
                            "code": "DocumentReference",
                        }
                    ]
                },
                "valueReference": {'reference': f"DocumentReference/{_document_reference_id(line)}"}
            }
        ]
    }
    task_ = Task.parse_obj(task)
    emit(output_path, task_)


def _document_reference_id(line):
    """Mint a DocumentReference id."""
    return str(uuid.uuid5(ACED_NAMESPACE, line['file_name'] + "/DocumentReference"))


def emit_document_reference(output_path, line):
    assert 'patient' in line, line
    has_task = True
    if not line['tissue']:
        has_task = False

    document_reference = {
        'id': _document_reference_id(line),
        'identifier': [
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/tissue_id',
                'value': line['patient'] + "/" + line['file_name']
            }
        ],
        'subject': {'reference': f"Patient/{_patient_id(line)}"},
        "resourceType": "DocumentReference",
        "status": "current",
        "content": [
            {'attachment': {
                'url': f"file://{line['path']}"
            }}
        ]
    }
    document_reference_ = DocumentReference.parse_obj(document_reference)
    emit(output_path, document_reference_)


def _observation_id(line):
    """Mint an Observation id."""
    _specimen_id(line)
    return str(uuid.uuid5(ACED_NAMESPACE, _specimen_id(line) + "/Observation"))


def emit_observation(output_path, line):
    assert 'patient' in line, line
    if not line['tissue']:
        return

    coding = [{"system": GENE_ID_URL, "code": _, "display":_ } for _ in line['markers']]
    coding.append({
        "system": "http://hl7.org/fhir/uv/genomics-reporting/CodeSystem/tbd-codes-cs",
        "code": "diagnostic-implication",
        "display": "diagnostic-implication"
    })
    observation = {
        'id': _observation_id(line),
        'identifier': [
            {
                'system': 'https://aced-idp.org/nvidia-collaboration/tissue_id',
                'value': line['patient']
            }
        ],
        'code': {
            'coding': coding
        },
        'subject': {'reference': f"Patient/{_patient_id(line)}"},
        "resourceType": "Observation",
        "status": "final"
    }
    observation_ = Observation.parse_obj(observation)
    emit(output_path, observation_)


@click.group()
def transform():
    """Transform data from exacloud."""
    pass


@transform.command('directory')
@click.argument('directory_listing_path', default=DIRECTORY_LISTING_PATH)
@click.argument('output_path', default=FHIR_DATA_PATH)
@click.option('--project_id', required=True,
              default='aced-nvidiaCollab',
              show_default=True,
              help='program-project'
              )
def transform_directory(directory_listing_path, output_path, project_id):
    """Transform directory listing."""
    directory_listing_path = pathlib.Path(directory_listing_path)
    output_path = pathlib.Path(output_path)
    assert directory_listing_path.is_file(), f"{directory_listing_path} does not exist."
    assert output_path.is_dir(), f"{output_path} does not exist or is not a directory."

    program, project = project_id.split('-')

    emit_research_study(output_path, project, f"A study with files from {directory_listing_path}.")

    with open(directory_listing_path, "rt") as fp:
        for line in fp.readlines():
            line = parse_line(line)
            if not line:
                continue
            emit_resources(line, output_path)

    close_all_emitters()


def emit_resources(line, output_path):
    """Emit all FHIR resources for this line."""
    emit_patient(output_path, line)
    emit_research_subject(output_path, line)
    emit_specimen(output_path, line)
    emit_task(output_path, line)
    emit_document_reference(output_path, line)
    emit_observation(output_path, line)


if __name__ == '__main__':
    transform()
