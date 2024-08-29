# Equi2Cube Streamlit App

**Equi2Cube Streamlit App** is a web-based interface for converting equirectangular images to cubemaps. The app provides interactive controls for processing single images or batch-processing directories.

## Features

- **Single Image Conversion**: Upload an equirectangular image and convert it to a cubemap with customizable face size.
- **Batch Processing**: Select a source directory and process all equirectangular images within it. The output can be zipped and downloaded.
- **Automatic Naming and Folder Management**: The app organizes output folders based on the original image names and timestamps.
- **Interactive Controls**: Adjust face sizes and debug options through the Streamlit interface.

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

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. To install and run the Streamlit app:

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd equi2cube
   ```

2. Install the dependencies:

   ```bash
   poetry install
   ```

3. Run the Streamlit app:

   ```bash
   poetry run streamlit run equi2cube/app.py
   ```

## Usage

### Single Image Conversion

1. Open the Streamlit app in your browser.
2. Select the "Single Image" tab.
3. Upload an equirectangular image.
4. Adjust the face size and debug options.
5. Convert the image and download the cubemap faces.

### Batch Processing

1. Select the "Batch Processing" tab.
2. Enter the source and output directories.
3. Adjust the face size.
4. Run the batch processing and download the zipped output.

## Development

To develop or modify the app:

- Edit the `app.py` file inside the `equi2cube/` directory.
- You can test changes by running:

  ```bash
  poetry run streamlit run equi2cube/app.py
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
