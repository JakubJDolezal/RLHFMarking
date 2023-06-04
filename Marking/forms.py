from django import forms

class ScoreForm(forms.Form):
    score = forms.IntegerField(min_value=0, max_value=10)

class QuestionForm(forms.Form):
    question = forms.CharField(max_length=255)
    num_responses = forms.IntegerField(label='Number of Responses', min_value=1)
