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
Project uses dependencies via the **poetry** tool
dependencies for auth_server in auth_server/pyproject.toml
dependencies for info_server in info_server/pyproject.toml

```bash
# add dependency
poetry add package
# delete dependency
poetry remove package
```

# Linting
```bash
pip install ruff
ruff check .
```

# if elastic-search not working
Add in file /etc/sysctl.conf:
```bash
vm.max_map_count=262144
```
and then:
```bash
sysctl -w vm.max_map_count=262144
```
