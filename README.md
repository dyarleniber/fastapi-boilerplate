# FastAPI Boilerplate

Starter template for building RESTful APIs using [FastAPI](https://fastapi.tiangolo.com/). It includes pre-configured settings and dependencies to help you kickstart your project development.

## Features

- [FastAPI](https://fastapi.tiangolo.com/) framework for building high-performance APIs.
- Testing with [pytest](https://docs.pytest.org/).
- Dependency management with [Poetry](https://python-poetry.org/).
- Code formatting with [Black](https://pypi.org/project/black/) and [isort](https://pycqa.github.io/isort/).

> **Note:** This project is still under development. More features will be added in the future.

## Getting Started

To clone and run this project, you'll need to have Git, Python 3, and Poetry installed on your computer.

From your command line:

- Clone this repository
```bash
git clone https://github.com/dyarleniber/fastapi-boilerplate.git
```

- Go into the repository folder
```bash
cd fastapi-boilerplate
```

- Install the project dependencies
```bash
poetry install
```

- Activate the virtual environment (in order to ensure that subsequent commands refer to the correct dependencies)
```bash
poetry shell
```

> To deactivate the virtual environment and exit the shell, run `exit`.

- Start the development server (in watch mode)
```bash
poetry run task dev
```

> The API will be available at `http://127.0.0.1:8000/` by default.

### Testing and Code Formatting

- Use the following command to run the tests:
```bash
poetry run task test
```

- Use the following command to format the code:
```bash
poetry run task lint
```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the terms of the MIT license.
