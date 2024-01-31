# leetcode_helper
FastAPI server for organizing leetcode progress
# QuickStart
```bash
# generate rsa keys for JWT
./generate_keys.sh
# start app
docker compose up --build
```
If error occurs when binding port 80 for Traefik, it means that Apache is already launched on it:
```bash
sudo service apache2 stop
```
