# Equi2Cube

Equi2Cube is a command-line tool that converts equirectangular images into cubemaps. It supports both single image processing and batch processing with various customizable options.

## Features

- Convert equirectangular images into cubemaps
- Support for single image and batch processing
- Options to set face size, automatically select the max face size, and customize output naming
- Ability to specify which cubemap faces to output
- Debug mode for additional labeling and information

## Installation

### From GitHub

You can install `equi2cube` directly from the GitHub repository:

```bash
pip install git+https://github.com/ricklon/equi2cube.git
```

If you're using Poetry:

```bash
poetry add git+https://github.com/ricklon/equi2cube.git
```

### From Releases

You can find pre-built releases of this package on the [Releases page](https://github.com/ricklon/equi2cube/releases) of this repository. Each release includes a `equi2cube-x.y.z.tar.gz` file that can be installed with pip:

```bash
pip install https://github.com/ricklon/equi2cube/releases/download/vx.y.z/equi2cube-x.y.z.tar.gz
```

Replace `x.y.z` with the version number you want to install.

## Usage

After installation, you can use the `equi2cube` command directly from your terminal:

```bash
equi2cube --help
```

### Single Image Conversion

Convert a single equirectangular image:

```bash
equi2cube single <input_file> <output_dir> [OPTIONS]
```

Options:
- `--face-size`: Set the size of each cubemap face in pixels (default: 512)
- `--max-size`: Automatically use the maximum face size based on the input image
- `--name`: Set a custom name prefix for the output faces
- `--faces`: Comma-separated list of faces to output (default: front,right,back,left,top,bottom)
- `--debug`: Enable debug mode with extra labels and information

Example:

```bash
equi2cube single src/RoomA_frame_000000.jpg out/ --max-size --name custom_prefix --faces front,top,bottom --debug
```

### Batch Processing

Batch process a directory of equirectangular images:

```bash
equi2cube batch <input_dir> <output_dir> [OPTIONS]
```

Options are the same as for single image conversion.

Example:

```bash
equi2cube batch src/ out/ --max-size --name batch_prefix --faces front,right,left --debug
```

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

## Creating a New Release

This project uses GitHub Actions to automatically create new releases when a version tag is pushed. Here's how to create a new release:

1. Ensure all your changes are committed and pushed to the main branch.

2. Use Poetry's version bump command to update the version. Choose one of the following based on the nature of your changes:
   ```bash
   poetry version patch  # for bug fixes and minor changes
   poetry version minor  # for new features
   poetry version major  # for major changes
   ```
   You can also specify a specific version:
   ```bash
   poetry version x.y.z
   ```

3. Commit the version change:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to $(poetry version -s)"
   ```

4. Create and push a new tag:
   ```bash
   git tag v$(poetry version -s)
   git push origin v$(poetry version -s)
   ```

5. Push the commit:
   ```bash
   git push
   ```

6. The GitHub Action will automatically run, creating a new release with the built package attached.

You can find the new release on the [Releases page](https://github.com/ricklon/equi2cube/releases) of the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.