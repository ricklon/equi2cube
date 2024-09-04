import click
import numpy as np
from PIL import Image
from pathlib import Path
import shutil
from datetime import datetime

def equirectangular_to_cubemap(equirect_img, face_size, desired_faces=None, debug=False):
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
        ('front',  ( 1,  0,  0), ( 0, -1,  0), ( 0,  0,  1), (1, 1)),  # Front
        ('right',   ( 0,  0,  1), ( 0, -1,  0), (-1,  0,  0), (1, 0)),  # Left (Swapped)
        ('back',   (-1,  0,  0), ( 0, -1,  0), ( 0,  0, -1), (1, 3)),  # Back
        ('left',  ( 0,  0, -1), ( 0, -1,  0), ( 1,  0,  0), (1, 2)),  # Right (Swapped)
        ('top',    ( 0,  1,  0), ( 0,  0, -1), ( 1,  0,  0), (0, 1)),  # Top
        ('bottom', ( 0, -1,  0), ( 0,  0, -1), (-1,  0,  0), (2, 1))   # Bottom
    ]



    labeled_faces = []
    for face, forward, up, right, (row, col) in faces:
        if desired_faces and face not in desired_faces:
            continue
        y, x = np.mgrid[-1:1:face_size*1j, -1:1:face_size*1j]
        x3d = forward[0] * np.ones_like(x) + up[0] * y + right[0] * x
        y3d = forward[1] * np.ones_like(x) + up[1] * y + right[1] * x
        z3d = forward[2] * np.ones_like(x) + up[2] * y + right[2] * x
        u, v = xyz_to_equi(x3d, y3d, z3d)
        ui = np.clip(u.astype(int), 0, width - 1)
        vi = np.clip(v.astype(int), 0, height - 1)
        face_img = Image.fromarray(equi[vi, ui])
        labeled_faces.append((face, face_img))

    return labeled_faces

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
@click.option('--faces', default='front,right,back,left,top,bottom', help='Comma-separated list of faces to output.')
@click.option('--debug', is_flag=True, help='Enable debug mode with extra labels and info.')
def single(input_file, output_dir, face_size, max_size, name, faces, debug):
    """Convert a single equirectangular image to a cubemap."""
    input_path = Path(input_file)
    output_path = Path(output_dir)
    equirect_img = Image.open(input_path)

    if max_size:
        width, height = equirect_img.size
        face_size = min(width // 4, height // 3)
        print(f"Using max face size: {face_size} pixels.")

    desired_faces = faces.split(',') if faces else None
    labeled_faces = equirectangular_to_cubemap(equirect_img, face_size, desired_faces, debug)
    
    output_path.mkdir(parents=True, exist_ok=True)
    for face, img in labeled_faces:
        if img.mode == 'RGBA':
            img = img.convert('RGB')  # Convert RGBA to RGB
        img.save(output_path / f'{name if name else input_path.stem}_{face}.jpg')
        print(f"Saved face: {name if name else input_path.stem}_{face}.jpg")

    print(f"Conversion complete. Cubemap faces saved in {output_path}.")

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.option('--face-size', default=512, help='Size of each cubemap face in pixels.')
@click.option('--max-size', is_flag=True, help='Automatically use the maximum face size based on the input images.')
@click.option('--name', default=None, help='Custom name prefix for the output faces.')
@click.option('--faces', default='front,right,back,left,top,bottom', help='Comma-separated list of faces to output.')
@click.option('--debug', is_flag=True, help='Enable debug mode with extra labels and info.')
def batch(input_dir, output_dir, face_size, max_size, name, faces, debug):
    """Batch process a directory of equirectangular images to cubemaps."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    image_extensions = ['.jpg', '.jpeg', '.png']
    images = [file for file in input_path.iterdir() if file.suffix.lower() in image_extensions]

    if not images:
        print("No valid images found in the input directory.")
        return

    first_image_name = name if name else images[0].stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_output_folder = output_path / f"{first_image_name}_{timestamp}"
    batch_output_folder.mkdir(parents=True, exist_ok=True)

    desired_faces = faces.split(',') if faces else None

    for file in images:
        equirect_img = Image.open(file)
        if max_size:
            width, height = equirect_img.size
            face_size = min(width // 4, height // 3)

        labeled_faces = equirectangular_to_cubemap(equirect_img, face_size, desired_faces, debug)
        
        for face, img in labeled_faces:
            if img.mode == 'RGBA':
                img = img.convert('RGB')  # Convert RGBA to RGB
            img.save(batch_output_folder / f'{name if name else file.stem}_{face}.jpg')
            print(f"Saved face: {name if name else file.stem}_{face}.jpg")

    zip_filename = f"{batch_output_folder}.zip"
    shutil.make_archive(batch_output_folder, 'zip', batch_output_folder)
    print(f"Batch processing complete. Zipped output saved as {zip_filename}.")

cli.add_command(single)
cli.add_command(batch)

if __name__ == '__main__':
    cli()