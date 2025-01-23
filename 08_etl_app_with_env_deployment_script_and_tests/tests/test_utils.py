
import pytest
import json
from src.utils import read_config, load_schema

def test_read_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_content = "key: value"
    config_path.write_text(config_content)

    config = read_config(str(config_path))
    assert config["key"] == "value"

def test_load_schema(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_content = json.dumps({
        "fields": [
            {"name": "id", "type": "int", "nullable": False},
            {"name": "name", "type": "string", "nullable": True}
        ]
    })
    schema_path.write_text(schema_content)

    schema = load_schema(str(schema_path))
    assert schema.fieldNames() == ["id", "name"]
