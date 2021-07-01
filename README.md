<center><h2>Rules Engine</h2></center>

  Basic Rules Engine API designed to be part of an event driven solution architecture.

  This is designed for NoSQL data but will be configurable to multiple backends

Goals:
  -   To be better than SQL for deeply nested data
  -   To offer logic on temporary abstractions without large latency overhead

## First Steps

TODO

## Prerequisites
- Python 3.8+ ([pyenv](https://github.com/pyenv/pyenv) is the best way to install/manage)
- [pdm](https://pdm.fming.dev/)
- [Pre-commit](https://pre-commit.com/)

Install the pre-commit hook
```bash
pre-commit install
```

## First Steps

### Package Management using Poetry
All python development should be done in a virtual environment and package managers such as Poetry and Pipenv make this simple. Currently Poetry is the best package manager for Python development\* and it saves a lot of time using this from the start with your project.

```bash
# Installing initial dependencies
poetry install

# Running hello.py
poetry run python main/hello.py

# Running test_hello.py
poetry run python tests/test_hello.py

```

<strong>For scenarios where you need a `requirements.txt`</strong>  
Some situations require a `requirements.txt` (think Airflow or Cloud Functions). In this case, still use Poetry and you can export to `requirement.txt` using
```
poetry export -f requirements.txt > requirements.txt
```
As the file is generally required to be in a bucket, you can add this and a `gsutil` as part of your CD process as having both Poetry and a`requirements.txt` in a repo becomes a messy two versions of the truth situation.


\* The one time I'd use Pipenv over Poetry is when doing Tensorflow development. For some reason, that package and Poetry aren't friends...

### Pre-commit
Pre-commit is amazing and should be used on every project you do!  

For python I've found using [Black](https://github.com/psf/black) and [Flake8](https://flake8.pycqa.org/en/latest/) together creates a very nice automated linter which follows Python best practises. For more information on why you should use these tools, [this](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/) article does a great job explaining (with pretty diagrams). Both will be automatically installed when setting up poetry in the above section.

## Development

### Folder Structure

This is generally personal preference and Python has never layed out a set structure to follow.  
I've found for POCs and small projects, a structure such as:
```bash
main/
  {funtionality}.py

tests/
  test_{functionality}.py
```
keeps the project readable but again, personal preference.

For larger projects, the folder structure should be set to compliment the functionality of that individual project.

\* For anyone used to Python development (<3.5), you no longer need `__init__.py` files and hence these should be no more as just add codebase bloat. The only thing which is required is to add the project to `PYTHONPATH`. The file `.envrc` does this automatically and can be used by simply installing [direnv](https://direnv.net/) 

## Testing

Here we're using a combination of `pytest`/`unittest`/`coverage` to achieve a nice testing framework. 

```bash
# Run individual test file (test_hello.py)
pdm run python tests/test_base_rules.py

# Run all tests
pdm run pytest --cov=main tests/

```

## CI/CD

CI on this project is setup to enforce best practises with testing and pre-commit. 

There are three stages:
  - pre-commit
  - test
  - coverage

Currently the coverage stage has been set to fail with coverage less than 100%.  
<strong>Your project will be better if you can keep this up!</strong>  
If you do need to reduce, go to `.coveragerc` and update `fail_under` to what is required for your project.

The current image `python:buster` was chosen to cater for the most general use case. This can be optimised for your individual repo if need be.

CD will be specific to each individual project but don't hesitate to contact [me](simon.butt@datatonic.com) if you require help/advice setting up with best practises :)