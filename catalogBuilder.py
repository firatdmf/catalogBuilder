# we will make a pdf of 2 columns and 2 rows, displaying 4 SKUs per page.
from reportlab.lib.pagesizes import letter  # this is for us letter size
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from PIL import Image

def convert_webp(image_path):
    # Convert .webp to .jpeg or .png using Pillow
    img = Image.open(image_path)
    output_path = image_path.rsplit(".", 1)[0] + ".jpeg"  # Convert to .jpeg format
    img.convert("RGB").save(output_path, "JPEG")
    return output_path


def generate_catalog_pdf(image_folder, output_path):

    image_paths = []
    for filename in os.listdir(image_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            image_paths.append(os.path.join(image_folder, filename))
        elif filename.endswith(".webp"):
            # Convert .webp to .jpeg and add the converted path
            webp_path = os.path.join(image_folder, filename)
            converted_path = convert_webp(webp_path)
            image_paths.append(converted_path)

    # create a new pdf file using us letter size
    pdf = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # now let's set the marging:
    margin_left = 0.5 * inch
    margin_top = 0.5 * inch
    margin_right = 0.5 * inch
    margin_bottom = 0.5 * inch
    image_spacing = 0.5 * inch  # Space between images


    # Calculate available space for images
    available_width = width - margin_left - margin_right
    available_height = height - margin_top - margin_bottom

    images_per_page = 4
    # image_size = (available_width // 2, available_height // 2)
    image_width = (available_width - image_spacing) // 2  # Adjust image width with spacing
    image_height = (available_height - image_spacing) // 2  # Adjust image height with spacing

    # Center offset
    center_offset_x = (available_width - (image_width * 2 + image_spacing)) / 2 + margin_left
    center_offset_y = (available_height - (image_height * 2 + image_spacing)) / 2 + margin_bottom

    for i, image_path in enumerate(image_paths):
        row = i % 2
        col = (i // 2) % 2
        x = center_offset_x + col * (image_width + image_spacing)
        y = center_offset_y + (1 - row) * (image_height + image_spacing)  # Flip Y to have first image on top

        # Now let's add the image
        try:
            pdf.drawImage(image_path, x, y, width=image_width, height=image_height)
        except Exception as e:
            print(f"Error with image {image_path} : {e}")

        # After 4 images, start a new page
        if (i + 1) % images_per_page == 0:
            pdf.showPage()

    # Save the file
    pdf.save()


# Example usage

image_folder = "images"
output_pdf_path = "product_catalog.pdf"
generate_catalog_pdf(image_folder, output_pdf_path)


# now let's compress the pdf

