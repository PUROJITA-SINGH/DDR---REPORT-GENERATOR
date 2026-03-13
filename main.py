import json
import re
from extract import extract_all
from generate import generate_ddr
from build_report import build_ddr

INSPECTION_PDF = "input/Sample Report.pdf"
THERMAL_PDF    = "input/Thermal Images.pdf"
IMAGE_DIR      = "EXTRACTED_IMAGES"
OUTPUT_PATH    = "OUTPUT/DDR_Report.docx"

def main():
    print("=== DDR Report Generation System ===")
    
    # Step 1: Extract
    inspection_text, thermal_text, _, _ = extract_all(
        INSPECTION_PDF, THERMAL_PDF, IMAGE_DIR
    )

    # Step 2: Generate
    ddr_json = generate_ddr(inspection_text, thermal_text)

    if ddr_json is None:
        print("AI generation failed. Check API key and try again.")
        return

    # Step 3: Validate sections before building
    print("\n--- Section Check ---")
    for key, val in ddr_json.items():
        if isinstance(val, list):
            print(f"{key}: {len(val)} items")
        else:
            print(f"{key}: {len(str(val))} chars")

    # Step 4: Build report
    build_ddr(ddr_json, IMAGE_DIR, OUTPUT_PATH)
    print("\nDone! Open OUTPUT/DDR_Report.docx")

if __name__ == "__main__":
    main()