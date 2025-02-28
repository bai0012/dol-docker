import os
import csv
import requests
from pathlib import Path
from urllib.parse import urlparse

# generate_modlist.py 的修改部分

def download_github_mods():
    mod_list = []
    with open('mods.csv') as f:
        reader = csv.reader(f)
        for row_number, row in enumerate(reader, 1):
            if len(row) < 2:
                print(f"[GitHub] 第{row_number}行格式错误，已跳过: {row}")
                continue
            repo, keyword = row[0], row[1]
            print(f"\n正在处理GitHub仓库: {repo}，关键词: {keyword}")
            try:
                repo_path = repo.replace("https://github.com/", "").strip("/")
                api_url = f"https://api.github.com/repos/{repo_path}/releases/latest"
                headers = {"Accept": "application/vnd.github.v3+json"}
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                release = response.json()
                print(f"版本 {release.get('tag_name', '未知')}")
                if 'assets' not in release:
                    print("该版本无可用资源")
                    continue
                asset = next(
                    (a for a in release['assets'] 
                    if keyword in a['name'] and a['name'].endswith('.zip')),
                    None
                )
                if asset:
                    filename = asset['name']
                    download_file(asset['browser_download_url'], filename)
                    mod_list.append(filename)
                else:
                    print(f"未找到匹配文件")
            except Exception as e:
                print(f"处理失败: {str(e)}")
    return mod_list

def download_direct_mods():
    mod_list = []
    if not Path('direct_mods.csv').exists():
        return mod_list
    with open('direct_mods.csv') as f:
        reader = csv.reader(f)
        for row_number, row in enumerate(reader, 1):
            if len(row) < 1 or not row[0].startswith('http'):
                print(f"[直链] 第{row_number}行无效链接，已跳过: {row}")
                continue
            url = row[0].strip()
            print(f"\n正在处理直链: {url}")
            try:
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path)
                if not filename:
                    filename = f"mod_{row_number}.zip"
                download_file(url, filename)
                mod_list.append(filename)
            except Exception as e:
                print(f"下载失败: {str(e)}")
    return mod_list


def download_file(url, filename):
    """通用下载函数"""
    mod_dir = Path("apps/mods")
    mod_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = mod_dir / filename
    if file_path.exists():
        print(f"文件已存在，跳过下载: {filename}")
        return
        
    print(f"开始下载: {filename}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"下载完成: {filename}")

if __name__ == "__main__":
    Path("apps/mods").mkdir(parents=True, exist_ok=True)
    github_mods = []
    direct_mods = []
    
    if Path('mods.csv').exists():
        github_mods = download_github_mods()
    else:
        print("未找到mods.csv，跳过GitHub模组下载")
    
    direct_mods = download_direct_mods()
    
    all_mods = github_mods + direct_mods
    
    with open('mod_order.txt', 'w') as f:
        for mod in all_mods:
            f.write(f"{mod}\n")