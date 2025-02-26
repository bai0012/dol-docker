import os
import csv
import requests
from pathlib import Path

def download_mods():
    mod_dir = Path("apps/mods")
    mod_dir.mkdir(parents=True, exist_ok=True)
    
    with open('mods.csv') as f:
        reader = csv.reader(f)
        for row_number, row in enumerate(reader, 1):
            # 格式校验
            if len(row) < 2:
                print(f"Row {row_number} 格式错误，已跳过: {row}")
                continue
                
            repo, keyword = row[0], row[1]
            print(f"正在处理仓库: {repo}，关键词: {keyword}")
            
            try:
                # 转换仓库地址格式（支持两种输入格式）
                repo_path = repo.replace("https://github.com/", "").strip("/")
                api_url = f"https://api.github.com/repos/{repo_path}/releases/latest"
                
                # 添加API请求头
                headers = {"Accept": "application/vnd.github.v3+json"}
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()  # 检查HTTP错误
                
                release = response.json()
                print(f"仓库 {repo} 最新版本: {release.get('tag_name', '未知')}")
                
                # 检查assets是否存在
                if 'assets' not in release:
                    print(f"仓库 {repo} 无可用资源，已跳过")
                    continue
                    
                # 查找匹配的asset
                asset = next(
                    (a for a in release['assets'] 
                    if keyword in a['name'] and a['name'].endswith('.zip')),
                    None
                )
                
                if asset:
                    print(f"找到匹配资源: {asset['name']}")
                    download_url = asset['browser_download_url']
                    file_path = mod_dir / asset['name']
                    
                    # 下载文件
                    with requests.get(download_url, stream=True) as r:
                        r.raise_for_status()
                        with open(file_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    print(f"成功下载: {asset['name']}")
                else:
                    print(f"未找到匹配关键词 {keyword} 的zip文件")
                    
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {str(e)}")
            except Exception as e:
                print(f"处理异常: {str(e)}")

if __name__ == "__main__":
    download_mods()
