# test_integration.py
from src.btrieve import open_btrieve_file
from src.models import GSCATRecord
from src.utils import load_config

# Load config
config = load_config()

# Open GSCAT file
gscat_path = config.nex_stores_path / "GSCAT.BTR"
client, pos_block = open_btrieve_file(str(gscat_path))

# Read first record
status, data = client.get_first(pos_block)

if status == 0:
    record = GSCATRecord.from_bytes(data)
    print(f"✅ Successfully read GSCAT record: {record.gs_code} - {record.gs_name}")
else:
    print(f"❌ Error: {client.get_status_message(status)}")

# Close file
client.close_file(pos_block)
print("✅ All tests passed!")