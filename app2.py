from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips
import os

# Function to add a gradient background to an image
def add_gradient_background(size, color1, color2):
    base = Image.new('RGB', size, color1)
    top = Image.new('RGB', size, color2)
    mask = Image.linear_gradient('L').resize(size)
    gradient = Image.composite(base, top, mask)
    return gradient

# Function to create a promotional banner with larger text and enhanced appearance
def create_banner(product_image_path, offer_text, color_palette, theme, output_size=(1024, 512), output_file='banner.png'):
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
    draw.text((int(output_size[0] * 0.65), int(output_size[1] * 0.2)), offer_text, fill=color_palette[2],font=font_large)

    # Add theme-related text if applicable
    if theme:
        draw.text((int(output_size[0] * 0.65), int(output_size[1] * 0.6)), theme, fill=color_palette[3],font=font_medium)

    # Save the banner
    banner = banner.convert('RGB')  # Convert back to RGB before saving (to avoid saving alpha)
    banner.save(output_file)
    print(f"Banner saved as {output_file}")

# Function to create promotional videos
def create_promo_video(product_images, offer_texts, color_palette, theme, duration=5, output_file='promo_video.mp4'):
    clips = []
    
    for i, product_image_path in enumerate(product_images):
        offer_text = offer_texts[i]
        
        # Create a banner for each product image
        create_banner(product_image_path, offer_text, color_palette, theme, output_size=(1280, 720), output_file=f'banner_{i}.png')
        
        # Convert the banner to a video clip
        banner_clip = ImageClip(f'banner_{i}.png').set_duration(duration)
        clips.append(banner_clip)
    
    # Concatenate all the banner clips to make a video
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file, fps=24)
    print(f"Promotional video saved as {output_file}")

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

    # Generate a single banner (for testing)
    create_banner('product1.jpg', '50% OFF on Diwali!', color_palette, theme)

    # Generate a promotional video with multiple images
    create_promo_video(product_images, offer_texts, color_palette, theme)
