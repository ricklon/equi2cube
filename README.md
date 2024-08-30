# equi2cube

**equi2cube** is a command-line tool that converts equirectangular images into cubemaps. It supports both single image processing and batch processing with various customizable options.

## Features

- Convert equirectangular images into cubemaps.
- Supports single image and batch processing.
- Options to set face size, automatically select the max face size, and customize output naming.
- Debug mode for additional labeling and information.

## Installation

### Using pip

You can install `equi2cube` directly from PyPI:

```bash
pip install equi2cube
```

### Using Poetry

If you're using Poetry:

```bash
poetry add equi2cube
```

After installation, you can use the `equi2cube` command directly from your terminal:

```bash
equi2cube --help
```

### Installing from source

If you want to install from source or contribute to the project:

1. Clone the repository:

   ```bash
   git clone https://github.com/ricklon/equi2cube.git
   cd equi2cube
   ```

2. Install the dependencies:

   ```bash
   poetry install
   ```

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

## Usage

Both the `single` and `batch` commands now support a `--faces` option to specify which cubemap faces to output:

```bash
equi2cube single <input_file> <output_dir> [OPTIONS]
equi2cube batch <input_dir> <output_dir> [OPTIONS]
```

New option:
- `--faces`: Comma-separated list of faces to output (default: front,right,back,left,top,bottom)

Example:
```bash
equi2cube single input.jpg output/ --faces front,top,bottom
```

This will only output the front, top, and bottom faces of the cubemap.

## Development

To set up the project for development:

1. Clone the repository:

   ```bash
   git clone https://github.com/ricklon/equi2cube.git
   cd equi2cube
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

To run tests (if implemented):

```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.