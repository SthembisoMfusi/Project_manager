import json
import os

TEMPLATE_FILE = "templates.json"

class TemplateManager:
    def __init__(self):
        self.templates = self.load_templates()

    def load_templates(self):
        defaults = {
            "Bug Report": {
                "title": "Bug: ",
                "description": "## Description\nDescribe the bug here.\n\n## Steps to Reproduce\n1. \n2. \n3. \n\n## Expected Behavior\n\n## Actual Behavior\n"
            },
            "Feature Request": {
                "title": "Feature: ",
                "description": "## Problem\nDescribe the problem you are trying to solve.\n\n## Proposed Solution\nDescribe your solution.\n"
            }
        }
        
        if not os.path.exists(TEMPLATE_FILE):
            return defaults
        try:
            with open(TEMPLATE_FILE, 'r') as f:
                data = json.load(f)
                # Merge defaults with loaded data (loaded takes precedence, but ensure defaults exist if not deleted)
                # Actually, simple way: if file exists, use it. If user deleted defaults, so be it.
                # But user asked for defaults to be available.
                # Let's just return defaults if file is empty or invalid.
                if not data: return defaults
                return data
        except:
            return defaults

    def save_template(self, name, title, description):
        self.templates[name] = {'title': title, 'description': description}
        self._persist()

    def delete_template(self, name):
        if name in self.templates:
            del self.templates[name]
            self._persist()

    def _persist(self):
        with open(TEMPLATE_FILE, 'w') as f:
            json.dump(self.templates, f, indent=4)
            
    def get_template_names(self):
        return list(self.templates.keys())
        
    def get_template(self, name):
        return self.templates.get(name)
