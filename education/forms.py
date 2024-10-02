from django.forms import ModelForm
from .models import TeacherProfile, ParentProfile, Users


class TeacherProfileForm(ModelForm):
    class Meta:
        model = TeacherProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Users.objects.filter(role='teacher')


class ParentProfileForm(ModelForm):
    class Meta:
        model = ParentProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Users.objects.filter(role='parent')
