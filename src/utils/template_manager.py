import json
import os

TEMPLATE_FILE = "templates.json"

class TemplateManager:
    def __init__(self):
        self.templates = self.load_templates()

    def load_templates(self):
        if not os.path.exists(TEMPLATE_FILE):
            return {}
        try:
            with open(TEMPLATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

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
