import pytest
from unittest.mock import patch, mock_open
import json
from src.utils.config import save_app_state, load_app_state, SETTINGS_FILE

def test_save_app_state():
    with patch("builtins.open", mock_open()) as mock_file:
        # Mock json.dump to not actually write but we verify open is called
        with patch("json.dump") as mock_dump:
            # Mock loading existing state as empty
            with patch("src.utils.config.os.path.exists", return_value=False):
                save_app_state("test_key", "test_value")
                
                mock_file.assert_called_with(SETTINGS_FILE, 'w')
                # Verify json.dump was called with correct data
                args, _ = mock_dump.call_args
                assert args[0] == {"test_key": "test_value"}

def test_load_app_state():
    mock_data = json.dumps({"test_key": "test_value"})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("src.utils.config.os.path.exists", return_value=True):
            val = load_app_state("test_key")
            assert val == "test_value"
            
            val_none = load_app_state("non_existent")
            assert val_none is None
