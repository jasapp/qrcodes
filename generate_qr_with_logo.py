import qrcode
from PIL import Image, ImageDraw
import sys

def generate_qr_with_logo(url, output_file):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Open and resize logo (25% of QR code size)
    logo = Image.open("okluma2.png").convert("RGBA")
    logo_size = int(qr_img.size[0] * 0.20)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Create a white square background for the logo (slightly larger than logo)
    white_square_size = int(logo_size * 1.2)  # 20% larger than logo
    white_square = Image.new("RGBA", (white_square_size, white_square_size), (255, 255, 255, 255))
    
    # Calculate positions
    square_pos = ((qr_img.size[0] - white_square_size) // 2, (qr_img.size[1] - white_square_size) // 2)
    logo_pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)

    # Paste white square, then logo onto QR code
    qr_img.paste(white_square, square_pos, white_square)
    qr_img.paste(logo, logo_pos, logo if logo.mode == "RGBA" else None)

    # Save the final image
    qr_img.save(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_qr_with_logo.py <URL> <output_file>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2]
    generate_qr_with_logo(url, output_file)
    print(f"QR code with logo saved as {output_file}")
