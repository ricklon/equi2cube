import click
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
import shutil
from datetime import datetime

def equirectangular_to_cubemap(equirect_img, face_size, debug=False):
    equi = np.array(equirect_img)
    height, width = equi.shape[:2]
    cubemap = np.zeros((face_size * 3, face_size * 4, 3), dtype=np.uint8)

    def xyz_to_equi(x, y, z):
        phi = np.arctan2(z, x)
        theta = np.arctan2(y, np.sqrt(x * x + z * z))
        u = (phi + np.pi) / (2 * np.pi)
        v = 1 - (theta + np.pi / 2) / np.pi
        return u * width, v * height

    faces = [
        ('front',  ( 0,  0,  1), ( 0, -1,  0), ( 1,  0,  0), (1, 1)),
        ('right',  ( 1,  0,  0), ( 0, -1,  0), ( 0,  0, -1), (1, 2)),
        ('back',   ( 0,  0, -1), ( 0, -1,  0), (-1,  0,  0), (1, 3)),
        ('left',   (-1,  0,  0), ( 0, -1,  0), ( 0,  0,  1), (1, 0)),
        ('top',    ( 0,  1,  0), ( 0,  0,  1), ( 1,  0,  0), (0, 1)),
        ('bottom', ( 0, -1,  0), ( 0,  0, -1), ( 1,  0,  0), (2, 1))
    ]

    for face, forward, up, right, (row, col) in faces:
        y, x = np.mgrid[-1:1:face_size*1j, -1:1:face_size*1j]
        x3d = forward[0] * np.ones_like(x) + up[0] * y + right[0] * x
        y3d = forward[1] * np.ones_like(x) + up[1] * y + right[1] * x
        z3d = forward[2] * np.ones_like(x) + up[2] * y + right[2] * x
        u, v = xyz_to_equi(x3d, y3d, z3d)
        ui = np.clip(u.astype(int), 0, width - 1)
        vi = np.clip(v.astype(int), 0, height - 1)
        cubemap[row*face_size:(row+1)*face_size, col*face_size:(col+1)*face_size] = equi[vi, ui]

    cubemap_image = Image.fromarray(cubemap)
    labeled_faces = []
    for face, _, _, _, (row, col) in faces:
        face_img = cubemap_image.crop((col * face_size, row * face_size, (col + 1) * face_size, (row + 1) * face_size))
        labeled_faces.append((face, face_img))

    return cubemap_image, labeled_faces

def save_individual_faces(faces, output_dir, name_prefix):
    output_dir.mkdir(parents=True, exist_ok=True)
    for face, img in faces:
        img.save(output_dir / f'{name_prefix}_{face}.jpg')
        print(f"Saved face: {name_prefix}_{face}.jpg")

def batch_process(input_dir, output_dir, face_size, name_prefix):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.is_dir():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return None

    image_extensions = ['.jpg', '.jpeg', '.png']
    images = [file for file in input_path.iterdir() if file.suffix.lower() in image_extensions]

    if not images:
        print("No valid images found in the input directory.")
        return None

    # Use the first image's name and the current datetime for the output folder
    first_image_name = name_prefix if name_prefix else images[0].stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_output_folder = output_path / f"{first_image_name}_{timestamp}"
    batch_output_folder.mkdir(parents=True, exist_ok=True)

    for file in images:
        equirect_img = Image.open(file)
        _, labeled_faces = equirectangular_to_cubemap(equirect_img, face_size)
        save_individual_faces(labeled_faces, batch_output_folder, file.stem if not name_prefix else name_prefix)

    # Zip the output directory
    zip_filename = f"{batch_output_folder}.zip"
    shutil.make_archive(batch_output_folder, 'zip', batch_output_folder)
    return zip_filename

@click.group()
def cli():
    """equi2cube.py: Convert equirectangular images to cubemap images."""
    pass

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.option('--face-size', default=512, help='Size of each cubemap face in pixels.')
@click.option('--max-size', is_flag=True, help='Automatically use the maximum face size based on the input image.')
@click.option('--name', default=None, help='Custom name prefix for the output faces.')
@click.option('--debug', is_flag=True, help='Enable debug mode with extra labels and info.')
def single(input_file, output_dir, face_size, max_size, name, debug):
    """Convert a single equirectangular image to a cubemap."""
    input_path = Path(input_file)
    output_path = Path(output_dir)
    equirect_img = Image.open(input_path)

    if max_size:
        width, height = equirect_img.size
        face_size = min(width // 4, height // 3)
        print(f"Using max face size: {face_size} pixels.")

    _, labeled_faces = equirectangular_to_cubemap(equirect_img, face_size, debug)
    save_individual_faces(labeled_faces, output_path, name if name else input_path.stem)
    print(f"Conversion complete. Cubemap faces saved in {output_path}.")

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.option('--face-size', default=512, help='Size of each cubemap face in pixels.')
@click.option('--max-size', is_flag=True, help='Automatically use the maximum face size based on the input images.')
@click.option('--name', default=None, help='Custom name prefix for the output faces.')
@click.option('--debug', is_flag=True, help='Enable debug mode with extra labels and info.')
def batch(input_dir, output_dir, face_size, max_size, name, debug):
    """Batch process a directory of equirectangular images to cubemaps."""
    first_image_path = next(Path(input_dir).iterdir())
    if max_size:
        equirect_img = Image.open(first_image_path)
        width, height = equirect_img.size
        face_size = min(width // 4, height // 3)
        print(f"Using max face size: {face_size} pixels.")

    zip_filename = batch_process(input_dir, output_dir, face_size, name)
    if zip_filename:
        print(f"Batch processing complete. Zipped output saved as {zip_filename}.")

cli.add_command(single)
cli.add_command(batch)

if __name__ == '__main__':
    cli()
