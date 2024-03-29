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

## Run meta import with --plugin_path

The input directory:

```
tests/fixtures-new/
├── HandE
├── RegisteredImages
│   ├── 17633-6-Scene-001
│   ├── 18538-6-Scene-001
│   ├── 19142-6-Scene-001
│   ├── 24952-6-Scene-001
│   ├── 30411-6-Scene-001
│   ├── 31022-6-Scene-001
│   ├── 31480-6-Scene-001
│   ├── 33548-6-Scene-001
│   ├── 38592-6-Scene-001
│   ├── 48411-6-Scene-001
│   ├── 54774-4-Scene-001
│   ├── 57494-6-Scene-001
│   └── 57658-6-Scene-001
└── annotations

```

will produce:

```
gen3_util meta  import dir tests/fixtures/ tmp/output --project_id aced-nvidia --plugin_path gen3_util_plugin_nvidia --remove_path_prefix tests/fixtures/
summary:
  ResearchStudy:
    count: 1
  ResearchSubject:
    count: 13
  Patient:
    count: 13
  Specimen:
    count: 13
  DocumentReference:
    count: 738
    size: 74437
msg: OK


```

### expected results

Output files:

```
tmp/output
├── DocumentReference.ndjson
├── Patient.ndjson
├── ResearchStudy.ndjson
├── ResearchSubject.ndjson
└── Specimen.ndjson
```

Identifiers:

```
$ cat tmp/output/*.ndjson | jq -rc '. as $r | .identifier[]? | [$r.resourceType, .value]'
["Patient","P1"]
["Specimen","T1"]
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
