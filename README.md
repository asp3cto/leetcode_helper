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
# Dependencies
the project uses dependencies using the **poetry** tool
dependencies for auth_server in auth_server/pyproject.toml
dependencies for info_server in info_server/pyproject.toml

```bash
#add dependenc
poetry add package
#delete dependenc
poetry remove package
```