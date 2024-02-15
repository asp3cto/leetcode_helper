# leetcode_helper
FastAPI server for organizing leetcode progress
# QuickStart
```bash
# generate rsa keys for JWT
./generate_keys.sh
# start app
docker compose up --build
```
# Testing
```bash
docker compose exec auth_server pytest tests/ -v -s
```
