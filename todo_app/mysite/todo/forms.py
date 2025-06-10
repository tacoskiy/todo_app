from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=200,
            widget=forms.TextInput(
            attrs={'placeholder':'タイトル', 'class':'form_title',}))
    due = forms.DateTimeField(
            widget=forms.DateTimeInput(
            attrs={'class':'form_due', 'type': 'datetime-local'}),
            input_formats=['%Y-%m-%dT%H:%M'],
            required=False,)
    isStared = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form_bool'}), 
        required=False,
    )
    class Meta:
        model = Task
        fields = ('title','due','isStared',)