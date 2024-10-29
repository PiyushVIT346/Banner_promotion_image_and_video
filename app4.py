import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips

UNSPLASH_API_KEY = 'RPGfuYb22dl2-O2Obm3Vye1XG_4EMve-IAHjfNL1LJM'  # Replace with your Unsplash API Key

# Function to fetch product images from Unsplash API
def fetch_product_images_from_unsplash(query, num_images=3):
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page={num_images}"
    headers = {'Authorization': f'Client-ID {UNSPLASH_API_KEY}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        image_urls = [result['urls']['regular'] for result in data['results']]
        return image_urls
    else:
        print(f"Error fetching images: {response.status_code}")
        return []

# Function to create a banner using Lorem Picsum with text overlay
def create_banner_with_placeholder(product_image_url, offer_text, theme_text, output_file='banner.png'):
    # Fetch product image
    response = requests.get(product_image_url)
    product_image = Image.open(BytesIO(response.content)).convert("RGBA")

    # Fetch a random placeholder image from Lorem Picsum
    placeholder_url = 'https://picsum.photos/1280/720'
    response = requests.get(placeholder_url)
    placeholder = Image.open(BytesIO(response.content)).convert("RGBA")

    # Resize product image and placeholder
    product_image = product_image.resize((400, 400))
    placeholder = placeholder.resize((1280, 720))

    # Add product image onto placeholder
    placeholder.paste(product_image, (50, 160), product_image)

    # Create a draw object
    draw = ImageDraw.Draw(placeholder)
    font = ImageFont.load_default()

    # Add offer text and theme text
    draw.text((500, 100), offer_text, font=font, fill="white")
    draw.text((500, 600), theme_text, font=font, fill="white")

    # Save the banner
    placeholder.save(output_file)
    print(f"Banner saved as {output_file}")
    return output_file

# Function to create a promotional video from banners
def create_promo_video_with_banners(banner_files, duration=5, output_file='promo_video.mp4'):
    clips = []

    for banner_file in banner_files:
        # Convert the banner to a video clip
        banner_clip = ImageClip(banner_file).set_duration(duration)
        clips.append(banner_clip)

    # Concatenate all the banner clips to make a video
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file, fps=24)
    print(f"Promotional video saved as {output_file}")

# Example usage
if __name__ == "__main__":
    # Fetch product images from Unsplash
    product_images = fetch_product_images_from_unsplash("sale items", num_images=3)

    # Example promotional offers and theme
    offer_texts = ["50% OFF on Diwali!", "Buy 1 Get 1 Free!", "Flash Sale: Limited Stock!"]
    theme_text = "Diwali Festive Sale"

    # Create dynamic banners using fetched images and text
    banner_files = []
    for i, product_image_url in enumerate(product_images):
        banner_file = f'banner_{i}.png'
        create_banner_with_placeholder(product_image_url, offer_texts[i], theme_text, banner_file)
        banner_files.append(banner_file)

    # Generate a promotional video using the created banners
    create_promo_video_with_banners(banner_files, duration=5)
