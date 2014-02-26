from django import forms

METHOD_CHOICES = (
    ("GET", "GET"),
    ("POST", "POST")
)

class ApiCallForm(forms.Form):
    method = forms.ChoiceField(choices=METHOD_CHOICES, initial="GET")
    path = forms.CharField(initial="/api/myself/")
    data = forms.CharField(widget=forms.Textarea, required=False)
