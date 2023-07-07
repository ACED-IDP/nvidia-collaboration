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

### Retrieve directory listing

See `data/raw/README.md`, download directory-listing.txt


## Run the import with `--plugin_path` 

```
gen3_util meta  import dir INPUT_PATH OUTPUT_PATH --project_id aced-nvidia --plugin_path {plugin_path}
```

### expected results

```
data
├── fhir
│   ├── DocumentReference.ndjson
│   ├── Patient.ndjson
│   ├── ResearchStudy.ndjson
│   ├── ResearchSubject.ndjson
│   ├── Specimen.ndjson
│   └── Task.ndjson


```

## Run the tests

```
pytest  tests/
```

