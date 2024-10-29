import requests
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips
import os
from io import BytesIO

# Function to fetch icons from Flaticon API (or any other API)
def fetch_icon_from_api(query, api_key):
    url = f"https://api.flaticon.com/v3/search/icons?q={query}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Get the first icon URL from the results
        icon_url = data['data'][0]['images']['png'][128]  # Get 128x128 PNG
        return icon_url
    else:
        print("Error fetching icon:", response.status_code)
        return None

# Function to download image from a URL
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    return img

# Function to add a gradient background to an image
def add_gradient_background(size, color1, color2):
    base = Image.new('RGB', size, color1)
    top = Image.new('RGB', size, color2)
    mask = Image.linear_gradient('L').resize(size)
    gradient = Image.composite(base, top, mask)
    return gradient

# Function to overlay an icon onto the banner
def add_icon(banner, icon, position, icon_size):
    icon = icon.resize(icon_size, Image.ANTIALIAS)  # Resize the icon to fit nicely on the banner
    banner.paste(icon, position, icon)  # Paste icon at specified position with transparency
    return banner

# Function to create a promotional banner with larger text, enhanced appearance, and API-fetched icons
def create_banner(product_image_path, offer_text, color_palette, theme, api_key, output_size=(1024, 512), output_file='banner.png'):
    # Load the product image
    product_image = Image.open(product_image_path).convert('RGBA')  # Convert to RGBA to handle transparency
    product_image = product_image.resize((int(output_size[0] * 0.5), int(output_size[1] * 0.5)))

    # Create a gradient background image
    banner = add_gradient_background(output_size, color_palette[0], color_palette[1])
    
    # Convert banner to RGBA to allow transparent overlays
    banner = banner.convert('RGBA')
    
    # Create draw object
    draw = ImageDraw.Draw(banner)

    # Add the product image to the banner
    banner.paste(product_image, (int(output_size[0] * 0.1), int(output_size[1] * 0.25)), product_image)

    # Load font and set size
    font_path = "C:/Windows/Fonts/arial.ttf"  # Replace with the path to your preferred font
    font_large = ImageFont.truetype(font_path, 60)
    font_medium = ImageFont.truetype(font_path, 40)

    # Add offer text with a different color from the palette
    draw.text((int(output_size[0] * 0.65), int(output_size[1] * 0.2)), offer_text, fill=color_palette[2], font=font_large)

    # Add theme-related text if applicable
    if theme:
        draw.text((int(output_size[0] * 0.65), int(output_size[1] * 0.6)), theme, fill=color_palette[3], font=font_medium)

    # Fetch icons related to the theme from the API
    diwali_lamp_url = fetch_icon_from_api("diwali lamp", api_key)
    fireworks_url = fetch_icon_from_api("fireworks", api_key)

    if diwali_lamp_url and fireworks_url:
        # Download icons
        diwali_lamp_icon = download_image(diwali_lamp_url)
        fireworks_icon = download_image(fireworks_url)

        # Add icons to the banner
        banner = add_icon(banner, diwali_lamp_icon, (int(output_size[0] * 0.05), int(output_size[1] * 0.75)), (80, 80))
        banner = add_icon(banner, fireworks_icon, (int(output_size[0] * 0.85), int(output_size[1] * 0.05)), (120, 120))

    # Save the banner
    banner = banner.convert('RGB')  # Convert back to RGB before saving (to avoid saving alpha)
    banner.save(output_file)
    print(f"Banner saved as {output_file}")

# Example usage
if __name__ == "__main__":
    # Example product images
    product_images = ['product1.jpg', 'product2.jpg', 'product3.jpg']

    # Example promotional offers
    offer_texts = ['50% OFF on Diwali!', 'Buy 1 Get 1 Free!', 'Flash Sale: Limited Stock!']

    # Color palette for consistency (gradient start, gradient end, text, theme)
    color_palette = ['#FFD700', '#FF6347', '#FFFFFF', '#FF4500']  # Golden, Tomato, White, Red

    # Example theme
    theme = 'Diwali Sale'

    # API Key for Flaticon or other icon services
    api_key = 'FPSX81490e22114843d892bcd4325df4bfc5'

    # Generate a single banner (for testing)
    create_banner('product1.jpg', '50% OFF on Diwali!', color_palette, theme, api_key)

