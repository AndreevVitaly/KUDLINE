from django.test import TestCase
from .models import Project

class ProjectApiTests(TestCase):
    def test_unpublished_project_is_hidden(self):
        Project.objects.create(title="Черновик", slug="draft", published=False)
        self.assertEqual(self.client.get("/api/projects/").json(), [])
        self.assertEqual(self.client.get("/api/projects/draft/").status_code, 404)

