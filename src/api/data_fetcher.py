import gitlab

class DataFetcher:
    def __init__(self, gl_client):
        self.gl_client = gl_client
        self.gl = gl_client.gl

    def fetch_projects(self):
        """Fetches projects that the user is a member of."""
        if not self.gl:
            return []
        
        try:
            # Fetch projects with membership=True to get all projects user has access to
            # simple=True returns lighter objects (faster)
            # order_by='updated_at' to show recently active projects first
            return self.gl.projects.list(membership=True, simple=True, order_by='updated_at', per_page=50)
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []
