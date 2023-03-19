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


## Run the transform

```
nvidia_collab_etl directory
```

## Run the tests

```
pytest  tests/
```

