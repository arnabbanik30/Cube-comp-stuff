import sys
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def usage():
    print(
        "Usage: python add_logo.py <input.pdf> <logo.png> <output.pdf> [logo_width_mm] [logo_height_mm] [margin_mm]"
    )
    print("Example: python add_logo.py input.pdf logo.png output.pdf 15 15 5")
    sys.exit(1)


def main():
    if len(sys.argv) < 4:
        usage()

    INPUT_PDF = sys.argv[1]
    LOGO_FILE = sys.argv[2]
    OUTPUT_PDF = sys.argv[3]
    LOGO_W = float(sys.argv[4]) * mm if len(sys.argv) > 4 else 15 * mm
    MARGIN = float(sys.argv[6]) * mm if len(sys.argv) > 6 else 15 * mm
    LOGO_H = float(sys.argv[5]) * mm if len(sys.argv) > 5 else 15 * mm

    A4_W = 210 * mm
    A4_H = 297 * mm
    A6_W = 105 * mm
    A6_H = 148.5 * mm

    a6_corners = [
        (A6_W, A4_H),
        (A4_W, A4_H),
        (A6_W, A6_H),
        (A4_W, A6_H),
    ]

    def make_logo_overlay(page_width, page_height):
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=(page_width, page_height))
        for corner_x, corner_y in a6_corners:
            x = corner_x - LOGO_W - MARGIN
            y = corner_y - LOGO_H - MARGIN
            c.drawImage(
                LOGO_FILE,
                x,
                y,
                width=LOGO_W,
                height=LOGO_H,
                mask="auto",
                preserveAspectRatio=True,
            )
        c.save()
        buf.seek(0)
        return PdfReader(buf).pages[0]

    reader = PdfReader(INPUT_PDF)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        overlay = make_logo_overlay(w, h)
        page.merge_page(overlay)
        writer.add_page(page)
        print(f"Added logo overlay in page-{i + 1}")

    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)

    print(f"Done all {len(reader.pages)} pages! Saved to {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
