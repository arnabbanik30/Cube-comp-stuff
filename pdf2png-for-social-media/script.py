import sys
import pymupdf


def pdf_to_png(pdf_path, output_path):
    doc = pymupdf.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        pix.save(f"{output_path}_{i}.png")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <pdf_file_path>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    pdf_file_name = pdf_file_path.split(".")[0]
    output_file_path = f"{pdf_file_name}.png"

    pdf_to_png(pdf_file_path, output_file_path)
    print(f"PDF converted to PNG: {output_file_path}")

