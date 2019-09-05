from django.forms import ModelForm, Textarea
from ratings.models import Rating

class ReviewForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']