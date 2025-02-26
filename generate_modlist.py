import os
import csv
import requests
from pathlib import Path

def download_mods():
    mod_dir = Path("apps/mods")
    mod_dir.mkdir(parents=True, exist_ok=True)
    
    with open('mods.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            repo, keyword = row
            api_url = f"https://api.github.com/repos{repo.split('github.com')[-1]}/releases/latest"
            response = requests.get(api_url)
            release = response.json()
            
            asset = next(
                (a for a in release['assets'] 
                if keyword in a['name'] and a['name'].endswith('.zip')),
                None
            )
            
            if asset:
                download_url = asset['browser_download_url']
                file_path = mod_dir / asset['name']
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

if __name__ == "__main__":
    download_mods()
