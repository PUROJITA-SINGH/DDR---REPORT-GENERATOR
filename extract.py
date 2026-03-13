import fitz  # PyMuPDF
import os

def extract_from_pdf(pdf_path, image_output_dir, prefix):
    doc = fitz.open(pdf_path)
    full_text = ""
    image_paths = []

    os.makedirs(image_output_dir, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Extract text
        full_text += f"\n--- Page {page_num + 1} ---\n"
        full_text += page.get_text()

        # Extract images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            filename = f"{prefix}_page{page_num+1}_img{img_index+1}.{ext}"
            filepath = os.path.join(image_output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            image_paths.append(filepath)

    return full_text, image_paths


def extract_all(inspection_pdf, thermal_pdf, image_dir):
    print("Extracting inspection report...")
    inspection_text, inspection_images = extract_from_pdf(
        inspection_pdf, image_dir, "inspection"
    )

    print("Extracting thermal report...")
    thermal_text, thermal_images = extract_from_pdf(
        thermal_pdf, image_dir, "thermal"
    )

    print(f"Images extracted: {len(inspection_images)} inspection, {len(thermal_images)} thermal")

    return inspection_text, thermal_text, inspection_images, thermal_images


if __name__ == "__main__":
    i_text, t_text, i_imgs, t_imgs = extract_all(
        "input/Sample Report.pdf",
        "input/Thermal Images.pdf",
        "EXTRACTED_IMAGES"
    )
    print("\n--- INSPECTION TEXT SAMPLE ---")
    print(i_text[:500])
    print("\n--- THERMAL TEXT SAMPLE ---")
    print(t_text[:500])
    print("\nImage files:", i_imgs + t_imgs)