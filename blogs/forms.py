from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
                'placeholder': 'Enter post title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
                'rows': 6,
                'placeholder': 'Write your content here...',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
            }),
        }

