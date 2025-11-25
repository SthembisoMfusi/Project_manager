import gitlab

class DataFetcher:
    def __init__(self, gl_client):
        self.gl_client = gl_client
        self.gl = gl_client.gl

    def fetch_projects(self, search=None, page=1, per_page=20):
        """Fetches projects that the user is a member of."""
        if not self.gl:
            return []
        
        try:
            # Fetch projects with membership=True to get all projects user has access to
            # simple=True returns lighter objects (faster)
            # order_by='updated_at' to show recently active projects first
            # get_all=False to suppress pagination warning (we are setting per_page)
            kwargs = {
                'membership': True, 
                'simple': True, 
                'order_by': 'updated_at', 
                'per_page': per_page, 
                'page': page,
                'get_all': False
            }
            if search:
                kwargs['search'] = search
                
            return self.gl.projects.list(**kwargs)
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

    def create_issue(self, project_id, title, description, assignee_id=None, labels=None, milestone_id=None):
        """Creates a new issue in the specified project."""
        if not self.gl:
            return False, "Not connected"
        
        try:
            project = self.gl.projects.get(project_id)
            data = {'title': title, 'description': description}
            if assignee_id:
                data['assignee_ids'] = [assignee_id]
            if labels:
                data['labels'] = labels
            if milestone_id:
                data['milestone_id'] = milestone_id
                
            issue = project.issues.create(data)
            return True, issue
        except Exception as e:
            return False, str(e)

    def update_issue(self, project_id, issue_iid, **kwargs):
        """Updates an existing issue."""
        if not self.gl:
            return False, "Not connected"
        
        try:
            project = self.gl.projects.get(project_id)
            issue = project.issues.get(issue_iid)
            
            for key, value in kwargs.items():
                if key == 'assignee_id':
                    issue.assignee_ids = [value] if value else []
                elif key == 'labels':
                    issue.labels = value
                elif key == 'milestone_id':
                    issue.milestone_id = value
                else:
                    setattr(issue, key, value)
            
            issue.save()
            return True, issue
        except Exception as e:
            return False, str(e)

    def fetch_members(self, project_id):
        """Fetches members of the project."""
        if not self.gl: return []
        try:
            project = self.gl.projects.get(project_id)
            return project.members.list(all=True)
        except: return []

    def fetch_labels(self, project_id):
        """Fetches labels of the project."""
        if not self.gl: return []
        try:
            project = self.gl.projects.get(project_id)
            return project.labels.list(all=True)
        except: return []

    def fetch_milestones(self, project_id):
        """Fetches milestones of the project."""
        if not self.gl: return []
        try:
            project = self.gl.projects.get(project_id)
            return project.milestones.list(state='active', all=True)
        except: return []

    def create_label(self, project_id, name, color):
        """Creates a new label."""
        if not self.gl: return False, "Not connected"
        try:
            project = self.gl.projects.get(project_id)
            label = project.labels.create({'name': name, 'color': color})
            return True, label
        except Exception as e:
            return False, str(e)

    def delete_label(self, project_id, label_name):
        """Deletes a label."""
        if not self.gl: return False, "Not connected"
        try:
            project = self.gl.projects.get(project_id)
            project.labels.delete(label_name)
            return True, None
        except Exception as e:
            return False, str(e)

    def create_milestone(self, project_id, title, due_date=None):
        """Creates a new milestone."""
        if not self.gl: return False, "Not connected"
        try:
            project = self.gl.projects.get(project_id)
            data = {'title': title}
            if due_date: data['due_date'] = due_date
            milestone = project.milestones.create(data)
            return True, milestone
        except Exception as e:
            return False, str(e)

    def delete_milestone(self, project_id, milestone_id):
        """Deletes a milestone."""
        if not self.gl: return False, "Not connected"
        try:
            project = self.gl.projects.get(project_id)
            project.milestones.delete(milestone_id)
            return True, None
        except Exception as e:
            return False, str(e)
