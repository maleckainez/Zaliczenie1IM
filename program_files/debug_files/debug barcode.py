import code128
import io
from PIL import Image, ImageDraw, ImageFont
import webbrowser
import datetime
# Get barcode value
barcode_param = '1234567890-12345678'
dpi_value = 2400  # Dots per inch
# Create barcode image
barcode_image = code128.image(barcode_param, height=100)

# Create empty image for barcode + text
top_bott_margin = 70
l_r_margin = 10
new_height = barcode_image.height + (2 * top_bott_margin)
new_width = barcode_image.width + (2 * l_r_margin)
new_image = Image.new( 'RGB', (new_width, new_height), (255, 255, 255))

# object to draw text
draw = ImageDraw.Draw(new_image)

# Define custom text size and font
h1_size = 20
h2_size = 20
h3_size = 16
footer_size = 21

h1_font = ImageFont.truetype("DejaVuSans-Bold.ttf", h1_size)
h2_font = ImageFont.truetype("Ubuntu-Th.ttf", h2_size)
h3_font = ImageFont.truetype("Ubuntu-Th.ttf", h3_size)
footer_font = ImageFont.truetype("arial.ttf", footer_size)

# Define custom text
company_name = 'PRI Kępno ZUP-K'
id1 = datetime.datetime.now().strftime("%d/%m/%Y")
user = "Inez Małecka"
license_num = f"Wygenerowano przez użytkownika {user}"


center_barcode_value = (barcode_image.width/2) - len(barcode_param) * 6.5
top_bott_margin = 20
# Draw text on picture
draw.text( (l_r_margin, 0), company_name, fill=(0, 0, 0), font=h1_font)
draw.text( (l_r_margin, h1_size), id1, fill=(0, 0, 0), font=h2_font)
draw.text( (l_r_margin + 2, (h1_size + h2_size + 5)), license_num, fill=(0, 0, 0), font=h3_font)
draw.text( (center_barcode_value, (new_height - footer_size - 15)), barcode_param, fill=(0, 0, 0), font=h1_font)

# paste barcode image onto new image
new_image.paste(barcode_image, (0, 80))

# save in file
new_image.save('barcode_image.png', 'PNG',dpi=(dpi_value, dpi_value))
