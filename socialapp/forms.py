from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc', 'image']  # Specify the fields you want in the form

        # Optionally, you can customize widgets or labels here
        widgets = {
            'desc': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
        labels = {
            'title': 'Post Title',
            'desc': 'Post Description',
            'image': 'Add Image',
        }
