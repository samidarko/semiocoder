from django import forms
from datetime import datetime
from semiocoder.encoder.models import Joblist, Job, Task

class JoblistForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(JoblistForm, self).__init__(*args, **kwargs)
        self.fields['job'] = forms.ModelMultipleChoiceField(Job.objects.filter(created_by=user)) # On filtre le queryset par utilisateur
    
    class Meta:
        model = Joblist
        fields = ('name', 'description', 'job')


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('name', 'description', 'encoder', 'options', 'extension', )


class TaskForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['schedule'] = forms.DateTimeField(initial=datetime.now().strftime('%d/%m/%Y %H:%M'))
        self.fields['joblist'] = forms.ModelChoiceField(Joblist.objects.filter(created_by=user)) # On filtre le queryset par utilisateur
    
    class Meta:
        model = Task
        fields = ('joblist', 'schedule', 'source_file', 'notify')

