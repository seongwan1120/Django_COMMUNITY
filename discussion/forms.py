from django import forms
from .models import Posting, Comment, Reply

class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        # fields = '__all__'
        exclude = ('author', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ('content', )

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        # fields = '__all__'
        fields = ('content', )