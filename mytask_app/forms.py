from django import forms
from .models import Task, Tag, Remainder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



#form validations for all form inputs
class SearchTag(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tag']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.filter(owner=self.user)


class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'piority_level', 'tag']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.filter(owner=self.user)

    def clean(self):
        super(AddTask, self).clean()
        task_name = self.cleaned_data.get('task_name')

        if len(task_name) >= 24:
            raise forms.ValidationError('Task name too long')
            
        if Task.objects.filter(
            owner=self.user,
            task_name__iexact=task_name
            ).exists():
            raise forms.ValidationError(f'{task_name} task already exist.')

        # for instance in Task.objects.filter(owner=self.user):
        #     if instance.task_name.lower() == task_name.lower():
        #         raise forms.ValidationError(f'{task_name} task already created by a user.')

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """set the validations of all tags to be created in this form"""
        super(TagForm, self).clean()
        tag_name = self.cleaned_data.get('tag_name')
        
        if not tag_name:#if it is empty or equals to an empty string
            raise forms.ValidationError("Must Input a name for the TAG")
            
        if len(tag_name) <= 3:
            self._errors['tag_name'] = self.error_class([
                "minimum of 4 inputs"])

        if Tag.objects.filter(
            owner=self.user,
            tag_name__iexact=tag_name).exists():
                raise forms.ValidationError(f'{tag_name} already exist.')




class RemainderForm(forms.ModelForm):
    class Meta:
        model = Remainder
        fields = ['task_name', 'date', 'time']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)#defining the user attributes 
        super().__init__(*args, **kwargs)

    date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Select date'
        }),
        input_formats=['%Y-%m-%d']
    )

    time = forms.TimeField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control timepicker',
            'placeholder': 'Select time'
        }),
        input_formats=['%H:%M']
    )



class RegisterForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']






