# nvidia-collaboration
OHSU CEDAR Cyclic IF and H&amp;E images

## Getting started

### Setup python environment

```commandline
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt  
python3 -m pip install -e .
```

## Run the import with `--plugin_path` 

```
gen3_util meta  import dir tests/fixtures/ tmp/output --project_id aced-nvidia --plugin_path gen3_util_plugin_nvidia --remove_path_prefix tests/fixtures/
summary:
  ResearchStudy:
    count: 1
  ResearchSubject:
    count: 1
  Patient:
    count: 1
  Specimen:
    count: 1
  DocumentReference:
    count: 1
    size: 4
msg: OK

```

### expected results

```
tmp/output
├── DocumentReference.ndjson
├── Patient.ndjson
├── ResearchStudy.ndjson
├── ResearchSubject.ndjson
└── Specimen.ndjson



```

## Run the tests

```
pytest  tests/
```
## Distribution

- PyPi

```
# update pypi

# pypi credentials - see https://twine.readthedocs.io/en/stable/#environment-variables

export TWINE_USERNAME=  #  the username to use for authentication to the repository.
export TWINE_PASSWORD=  # the password to use for authentication to the repository.

# this could be maintained as so: export $(cat .env | xargs)

rm -r dist/
python3  setup.py sdist bdist_wheel
twine upload dist/*
```
