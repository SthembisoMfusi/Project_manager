import pytest
from unittest.mock import MagicMock
from src.api.data_fetcher import DataFetcher

@pytest.fixture
def mock_client():
    client = MagicMock()
    client.gl = MagicMock()
    return client

def test_fetch_projects(mock_client):
    fetcher = DataFetcher(mock_client)
    
    # Mock response
    mock_project = MagicMock()
    mock_project.name = "Test Project"
    mock_client.gl.projects.list.return_value = [mock_project]
    
    projects = fetcher.fetch_projects(search="Test", page=1)
    
    assert len(projects) == 1
    assert projects[0].name == "Test Project"
    mock_client.gl.projects.list.assert_called_once()
    
    # Check call args
    call_kwargs = mock_client.gl.projects.list.call_args.kwargs
    assert call_kwargs['search'] == "Test"
    assert call_kwargs['page'] == 1

def test_create_issue(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    mock_issue = MagicMock()
    mock_issue.title = "New Issue"
    mock_project.issues.create.return_value = mock_issue
    
    success, issue = fetcher.create_issue(1, "New Issue", "Desc", assignee_id=10, labels=["bug"])
    
    assert success is True
    assert issue.title == "New Issue"
    
    mock_project.issues.create.assert_called_once()
    call_args = mock_project.issues.create.call_args[0][0]
    assert call_args['title'] == "New Issue"
    assert call_args['assignee_ids'] == [10]
    assert call_args['labels'] == ["bug"]

def test_update_issue(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    mock_issue = MagicMock()
    mock_project.issues.get.return_value = mock_issue
    
    success, issue = fetcher.update_issue(1, 100, title="Updated Title", labels=["feature"])
    
    assert success is True
    assert mock_issue.title == "Updated Title"
    assert mock_issue.labels == ["feature"]
    mock_issue.save.assert_called_once()

def test_create_label(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    mock_label = MagicMock()
    mock_label.name = "Test Label"
    mock_project.labels.create.return_value = mock_label
    
    success, label = fetcher.create_label(1, "Test Label", "#FF0000", "A test label")
    
    assert success is True
    assert label.name == "Test Label"
    mock_project.labels.create.assert_called_with({'name': "Test Label", 'color': "#FF0000", 'description': "A test label"})

def test_update_label(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    mock_label = MagicMock()
    mock_label.name = "Old Name"
    mock_project.labels.get.return_value = mock_label
    
    success, label = fetcher.update_label(1, "Old Name", new_name="New Name", new_description="New Desc")
    
    assert success is True
    assert mock_label.new_name == "New Name"
    assert mock_label.description == "New Desc"
    mock_label.save.assert_called_once()

def test_delete_label(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    
    success, _ = fetcher.delete_label(1, "Test Label")
    
    assert success is True
    mock_project.labels.delete.assert_called_with("Test Label")

def test_create_milestone(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    mock_milestone = MagicMock()
    mock_milestone.title = "v1.0"
    mock_project.milestones.create.return_value = mock_milestone
    
    success, milestone = fetcher.create_milestone(1, "v1.0", "2024-12-31")
    
    assert success is True
    assert milestone.title == "v1.0"
    mock_project.milestones.create.assert_called_with({'title': "v1.0", 'due_date': "2024-12-31"})

def test_delete_milestone(mock_client):
    fetcher = DataFetcher(mock_client)
    
    mock_project = MagicMock()
    mock_client.gl.projects.get.return_value = mock_project
    
    success, _ = fetcher.delete_milestone(1, 123)
    
    assert success is True
    mock_project.milestones.delete.assert_called_with(123)
