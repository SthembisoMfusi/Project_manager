import pytest
import os
import json
from src.utils.template_manager import TemplateManager, TEMPLATE_FILE

@pytest.fixture
def clean_templates():
    if os.path.exists(TEMPLATE_FILE):
        os.remove(TEMPLATE_FILE)
    yield
    if os.path.exists(TEMPLATE_FILE):
        os.remove(TEMPLATE_FILE)

def test_save_and_load_template(clean_templates):
    manager = TemplateManager()
    manager.save_template("Bug Report", "Bug: ", "Steps to reproduce:")
    
    # Reload
    manager2 = TemplateManager()
    tmpl = manager2.get_template("Bug Report")
    
    assert tmpl is not None
    assert tmpl['title'] == "Bug: "
    assert tmpl['description'] == "Steps to reproduce:"

def test_delete_template(clean_templates):
    manager = TemplateManager()
    manager.save_template("Temp", "T", "D")
    
    manager.delete_template("Temp")
    
    assert manager.get_template("Temp") is None
    assert "Temp" not in manager.get_template_names()
