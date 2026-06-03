from django import forms

class GitHubUrlValidatorMixin:
    """Миксин для проверки того, что ссылка ведет на GitHub"""
    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url.lower():
            raise forms.ValidationError("Ссылка должна вести на GitHub")
        return url
