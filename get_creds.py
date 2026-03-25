import os
import requests
from PIL import Image

def fetch_org_badges(username):
    """Fetch all Credly-hosted badges (filtering applied in process_username)."""
    badges = []
    page = 1
    while True:
        url = f'https://www.credly.com/users/{username}/badges.json?page={page}&per_page=100'
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        page_badges = data.get('data', [])
        if not page_badges:
            break
        badges.extend(page_badges)
        page += 1
        if page > 20:
            break
    return badges

def download_badge_image(badge):
    """Download badge image and return local path."""
    image_url = badge["badge_template"]["image_url"]
    badge_name = badge["badge_template"]["name"].lower().replace(" ", "_").replace(":", "")
    issuer_name = badge["issuer"]["entities"][0]["entity"]["name"].lower().replace(" ", "_").replace(":", "")
    
    if not image_url:
        print(f"No image URL for badge {badge["badge_template"]["name"]}")
        return None
    resp = requests.get(image_url, timeout=10)
    resp.raise_for_status()
    filename = f"badges/{issuer_name}_{badge_name}.png"
    with open(filename, 'wb') as f:
        f.write(resp.content)
    return filename

def change_image_size(image_path, size=(256, 256)):
    """Resize image to specified size."""
    with Image.open(image_path) as img:
        img = img.resize(size)
        img.save(image_path)
        
username="evan_allen"
badges=fetch_org_badges(username)
print(badges[0])
os.makedirs("badges", exist_ok=True)
for badge in badges:
    image_path = download_badge_image(badge)
    if image_path:
        print(f"Downloaded badge image to {image_path}")
        change_image_size(image_path)