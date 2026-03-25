import os
import re

imgs = ""
badges = sorted(os.listdir("badges"))
for badge in badges:
    print(f"Processing badge image {badge}")
    img = f"    <img src='badges/{badge}' alt='{badge}' height='90'>"
    imgs += img + "\n"

div = f"""
<div id="certifications" align="left">
{imgs}</div>
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