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
            # get_all=False to suppress pagination warning (we are setting per_page)
            return self.gl.projects.list(membership=True, simple=True, order_by='updated_at', per_page=50, get_all=False)
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []

    def fetch_issues(self, project_id):
        """Fetches open issues for a specific project."""
        if not self.gl:
            return []
        
        try:
            project = self.gl.projects.get(project_id)
            return project.issues.list(state='opened', order_by='updated_at', per_page=50, get_all=False)
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return []

    def create_issue(self, project_id, title, description):
        """Creates a new issue in the specified project."""
        if not self.gl:
            return False, "Not connected"
        
        try:
            project = self.gl.projects.get(project_id)
            issue = project.issues.create({'title': title, 'description': description})
            return True, issue
        except Exception as e:
            return False, str(e)
