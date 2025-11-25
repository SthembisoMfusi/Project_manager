import gitlab

class GitLabClient:
    def __init__(self, token=None, url='https://gitlab.wethinkco.de'):
        self.url = url
        self.token = token
        self.gl = None
        self.user = None

        if token:
            self.connect(token)

    def connect(self, token):
        """Initializes the GitLab connection."""
        self.token = token
        self.gl = gitlab.Gitlab(self.url, private_token=token)

    def authenticate(self):
        """Verifies the token by attempting to fetch the current user."""
        if not self.gl:
            return False, "No connection initialized."
        
        try:
            self.gl.auth()
            self.user = self.gl.user
            return True, f"Connected as {self.user.username}"
        except gitlab.exceptions.GitlabAuthenticationError:
            return False, "Authentication failed. Invalid token."
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def get_projects(self):
        """Fetches projects owned by the user."""
        if not self.gl:
            return []
        try:
            return self.gl.projects.list(owned=True, per_page=20)
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []
