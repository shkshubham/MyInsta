from __future__ import absolute_import
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from posts.models import Post

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption',)
        def __init__(self, *args, **kwargs):
            super(UpdatePostForm, self).__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                'caption',
                Submit('update', 'Update', css_class='btn primary')
            )

class CreatePostForm(forms.ModelForm):
    class Meta:
        fields = ('photo', 'caption', )
        model = Post

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'photo',
            'caption',
            Submit('post', 'Post', css_class='btn primary')
        )

