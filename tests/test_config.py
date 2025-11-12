# test_config.py
from src.utils import load_config

config = load_config()

print("PostgreSQL Host:", config.get('database.postgres.host'))
print("NEX Root:", config.nex_root_path)
print("✅ Config loaded successfully!")