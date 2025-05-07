# DoL Docker Auto-Deploy

[![Build and Deploy](https://github.com/bai0012/dol-docker/actions/workflows/build.yml/badge.svg)](https://github.com/bai0012/dol-docker/actions/workflows/build.yml)
[![Docker Image](https://img.shields.io/badge/dynamic/json?url=https://github.com/bai0012/dol-docker/pkgs/container/dol-docker&label=Docker%20Image&query=$.name&color=blue)](https://github.com/bai0012/dol-docker/pkgs/container/dol-docker)

Automated deployment system for DoL ModLoader with modular extension support, featuring GitHub Actions CI/CD and Docker packaging.

Base on [Lyra Repack](https://github.com/DoL-Lyra/Lyra)

## Features

- **Automated Mod Management**
  - Download ModLoader from official source
  - Install mods from multiple sources:
    - GitHub repository releases
    - Direct download links
    - Local mod files
    - Bootstrap packages
- **Smart Dependency Handling**
  - Priority-based loading system
  - Automatic conflict resolution (last-write wins)
- **Secure Deployment**
  - Auto-generated Docker images
  - SSL encryption support
  - Basic authentication protection
- **CI/CD Pipeline**
  - Automatic rebuild on:
    - Source code changes
    - New mod releases
    - Manual triggers

## Quick Start

### Prerequisites
- GitHub account
- Docker installed (for local testing)
- OpenSSL (for certificate generation)

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/bai0012/dol-docker
   cd dol-docker
   ```

2. **Configure Mod Sources**
   - `mods.csv` - GitHub-hosted mods
     ```csv
     Owner/Repo,Keyword
     Lyoko-Jeremie/DoLModLoaderBuild,DoL-ModLoader
     ```
   - `direct_mods.csv` - Direct download links
     ```csv
     https://example.com/path/to/mod.zip
     ```

3. **Set Up Secrets**
   ```bash
   # Generate SSL certificates
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
   
   # Create htpasswd file
   htpasswd -c auth.conf username
   ```

## GitHub Actions Setup

1. Add repository secrets:
   - `GHCR_TOKEN`: GitHub Personal Access Token with `write:packages` permission

2. Workflow triggers automatically on:
   - Push to `main` branch
   - New release creation
   - Manual workflow dispatch

## Deployment

### Docker Run
```bash
docker run -d \
  -p 8443:8443 \
  -v /path/to/ssl:/etc/nginx/ssl \
  -v /path/to/auth:/etc/nginx/auth \
  ghcr.io/bai0012/dol-docker:main
```

### Runtime Requirements
| Volume Mount         | Description                     |
|----------------------|---------------------------------|
| `/etc/nginx/ssl`     | SSL certificate directory       |
| `/etc/nginx/auth`    | Basic authentication credentials|

## Mod Loading Order
Priority-based loading system ensures consistent mod initialization:
1. GitHub-sourced mods (`mods.csv`)
2. Direct download mods (`direct_mods.csv`)
3. Local mods (`mods/` directory)

## Configuration Files

### `nginx.conf`
```nginx
server {
    listen 8443 ssl;
    server_name dol-modloader;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    auth_basic "Admin Access";
    auth_basic_user_file /etc/nginx/auth/auth.conf;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## Troubleshooting

### Common Issues
**Q: Mods not loading in correct order**  
A: Verify CSV file formatting and check `modList.json` generation logs

**Q: SSL certificate errors**  
A: Ensure certificate files are mounted at:
```bash
/etc/nginx/ssl/cert.pem
/etc/nginx/ssl/key.pem
```

**Q: Authentication failures**  
A: Verify htpasswd file creation:
```bash
htpasswd -v auth.conf username
```

## License
MIT License - See [LICENSE](LICENSE) for details
