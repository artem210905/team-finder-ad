from django import forms

from team_finder.mixins import GitHubUrlValidatorMixin
from .models import Project


class ProjectForm(GitHubUrlValidatorMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
