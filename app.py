from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips
import os

# Function to create a promotional banner
def create_banner(product_image_path, offer_text, color_palette, theme, output_size=(1024, 512), output_file='banner.png'):
    # Load the product image
    product_image = Image.open(product_image_path)
    product_image = product_image.resize((int(output_size[0] * 0.7), int(output_size[1] * 0.7)))

    # Create a blank banner image with the desired size
    banner = Image.new('RGB', output_size, color=color_palette[0])
    
    # Create draw object
    draw = ImageDraw.Draw(banner)
    
    # Add the product image to the banner
    banner.paste(product_image, (int(output_size[0] * 0.15), int(output_size[1] * 0.15)))

    # Load font
    font = ImageFont.load_default()

    # Add offer text with a different color from the palette
    draw.text((int(output_size[0] * 0.75), int(output_size[1] * 0.1)), offer_text, fill=color_palette[1], font=font)

    # Add theme-related text if applicable
    if theme:
        draw.text((int(output_size[0] * 0.75), int(output_size[1] * 0.5)), theme, fill=color_palette[2], font=font)

    # Save the banner
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

    # Color palette for consistency (background, text, theme)
    color_palette = ['#FFD700', '#FF4500', '#FFFFFF']  # Golden, Red, White

    # Example theme
    theme = 'Diwali Sale'

    # Generate a single banner (for testing)
    create_banner('product1.jpg', '50% OFF on Diwali!', color_palette, theme)

    # Generate a promotional video with multiple images
    create_promo_video(product_images, offer_texts, color_palette, theme)
