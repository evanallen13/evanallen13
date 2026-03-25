import os
import re
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
        
def set_creds(size=(90,90)):
    """Update README.md with badge images."""
    imgs = ""
    badges = sorted(os.listdir("badges"))
    for badge in badges:
        image_path = f"badges/{badge}"
        change_image_size(image_path, size)
        img = f"    <img src='badges/{badge}' alt='{badge}'>"
        imgs += img + "\n"

    div = f"""
    <div id="certifications" align="left">\n{imgs}</div>
    """

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    pattern = r'<div id="certifications" align="left">[\s\S]*?</div>'
    updated_readme, replacements = re.subn(pattern, div.strip(), readme, count=1)

    if replacements == 0:
        print("No certifications div found. Appending to README.md")
        updated_readme = readme.rstrip() + "\n\n" + div.strip() + "\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
def get_creds(username, size):
    """Fetch badges, download images, and resize them."""
    os.makedirs("badges", exist_ok=True)
    badges = fetch_org_badges(username)
    for badge in badges:
        download_badge_image(badge)

if __name__ == "__main__":      
    username="evan_allen"
    size=100
    get_creds(username, (size, size))
    set_creds()