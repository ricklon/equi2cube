### Installing the CLI Tool with Poetry

1. **Update `pyproject.toml` to configure the CLI entry point**:
   Add the following section under `[tool.poetry.scripts]` in `pyproject.toml`:

   ```toml
   [tool.poetry.scripts]
   equi2cube = "equi2cube.equi2cube:cli"
   ```

   This will allow you to run the CLI with `equi2cube` from anywhere after installation.

2. **Install the CLI tool**:
   Run the following command from the project’s root directory:

   ```bash
   poetry install
   ```

   This will install the CLI tool to your environment, and you can use it like this:

   ```bash
   equi2cube single src/RoomA_frame_000000.jpg out/ --max-size --name custom_prefix --debug
   ```

### Sample `README.md`

Here’s a README template for your project:

```markdown
# Equi2Cube

**Equi2Cube** is a command-line tool that converts equirectangular images into cubemaps. It supports both single image processing and batch processing with various customizable options.

## Features

- Convert equirectangular images into cubemaps.
- Supports single image and batch processing.
- Options to set face size, automatically select the max face size, and customize output naming.
- Debug mode for additional labeling and information.

## Directory Structure

```plaintext
.
├── README.md
├── equi2cube
│   ├── __init__.py
│   ├── app.py
│   └── equi2cube.py
├── out
├── poetry.lock
├── pyproject.toml
├── src
│   ├── RoomA_frame_000000.jpg
│   ├── ...
└── tests
    └── __init__.py
```

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. To install the tool:

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd equi2cube
   ```

2. Install the dependencies:

   ```bash
   poetry install
   ```

3. The CLI tool will be installed as `equi2cube` and can be run directly from the command line.

## Usage

### Single Image Conversion

Convert a single equirectangular image:

```bash
equi2cube single <input_file> <output_dir> [OPTIONS]
```

Options:
- `--face-size`: Set the size of each cubemap face (default: 512).
- `--max-size`: Automatically use the maximum face size based on the input image.
- `--name`: Set a custom name prefix for the output faces.
- `--debug`: Enable debug mode with extra labels and information.

Example:

```bash
equi2cube single src/RoomA_frame_000000.jpg out/ --max-size --name custom_prefix --debug
```

### Batch Processing

Batch process a directory of equirectangular images:

```bash
equi2cube batch <input_dir> <output_dir> [OPTIONS]
```

Options:
- `--face-size`: Set the size of each cubemap face (default: 512).
- `--max-size`: Automatically use the maximum face size based on the input images.
- `--name`: Set a custom name prefix for the output faces.
- `--debug`: Enable debug mode with extra labels and information.

Example:

```bash
equi2cube batch src/ out/ --max-size --name custom_prefix --debug
```

## Development

To run tests:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

