import streamlit as st
import numpy as np
from PIL import Image
from pathlib import Path
import zipfile
import os
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

def save_individual_faces(faces, output_dir, original_name):
    output_dir.mkdir(parents=True, exist_ok=True)
    for face, img in faces:
        img.save(output_dir / f'{original_name}_{face}.jpg')
        print(f"Saved face: {original_name}_{face}.jpg")

def batch_process(input_dir, output_dir, face_size):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.is_dir():
        st.error(f"Input directory '{input_dir}' does not exist.")
        return None

    image_extensions = ['.jpg', '.jpeg', '.png']
    images = [file for file in input_path.iterdir() if file.suffix.lower() in image_extensions]

    if not images:
        st.error("No valid images found in the input directory.")
        return None

    # Use the first image's name and the current datetime for the output folder
    first_image_name = images[0].stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_output_folder = output_path / f"{first_image_name}_{timestamp}"
    batch_output_folder.mkdir(parents=True, exist_ok=True)

    for file in images:
        equirect_img = Image.open(file)
        _, labeled_faces = equirectangular_to_cubemap(equirect_img, face_size)
        save_individual_faces(labeled_faces, batch_output_folder, file.stem)

    # Zip the output directory
    zip_filename = f"{batch_output_folder}.zip"
    shutil.make_archive(batch_output_folder, 'zip', batch_output_folder)
    return zip_filename

# Streamlit app starts here
st.title("Equirectangular to Cubemap Converter")

tabs = st.tabs(["Single Image", "Batch Processing"])

with tabs[0]:
    st.header("Single Image Conversion")
    uploaded_file = st.file_uploader("Upload an Equirectangular Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Equirectangular Image", use_column_width=True)
        face_size = st.slider("Select Cube Face Size (pixels)", 256, 1024, 512)
        if st.button("Convert to Cubemap"):
            with st.spinner("Processing..."):
                cubemap_image, labeled_faces = equirectangular_to_cubemap(image, face_size)
            st.success("Conversion Complete!")
            st.image(cubemap_image, caption="Cubemap Grid", use_column_width=True)
            st.markdown("### Individual Cube Faces")
            for face, face_img in labeled_faces:
                st.image(face_img, caption=f"{face.capitalize()} Face", use_column_width=True)
                st.download_button(f"Download {face.capitalize()} Face", face_img.tobytes(), f"{face.lower()}_face.jpg", "image/jpeg")

with tabs[1]:
    st.header("Batch Processing")
    input_dir = st.text_input("Input Directory", "./src")
    output_dir = st.text_input("Output Directory", "./out")
    face_size = st.slider("Select Cube Face Size (pixels)", 256, 1024, 512, key="batch_face_size")
    
    if st.button("Run Batch Processing"):
        if input_dir and output_dir:
            with st.spinner("Processing..."):
                zip_path = batch_process(input_dir, output_dir, face_size)
            if zip_path:
                st.success(f"Batch Processing Complete! Download the results.")
                st.download_button("Download Zipped Output", open(zip_path, "rb"), zip_path.split("/")[-1])
        else:
            st.error("Please provide both input and output directories.")
