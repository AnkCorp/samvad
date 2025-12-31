# samvad (संवाद)

The goal of this project is simple, create an open source toolkit that will help to train a model to convert Indian Sign Language (or any other sign language) into English.

## Getting Started

You should have the following tools installed:
- [Git](https://git-scm.com/downloads)
- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- Python >=3.12

## Installation

### Clone the Repository:
```sh
git clone https://github.com/AnkCorp/samvad.git
cd samvad
```

### Install Dependencies:
```sh
uv sync
```

### Run the Application:
```sh
uv run samvad
```

## Notebooks

Notebooks are powered by marimo. All the notebooks are located in the `notebooks` directory. To run a notebook in edit mode, you can use the following command:
```sh
uv run marimo edit notebooks/<notebook_name>.py
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
