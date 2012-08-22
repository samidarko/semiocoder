# -*- coding: utf-8 -*-
"""
.. module:: forms
   :platform: Unix, Windows
   :synopsis: Module des formulaires de l'encodeur

.. moduleauthor:: Samuel Darko <samidarko@gmail.com>

"""
from django import forms
from datetime import datetime, timedelta
from semiocoder.encoder.models import Joblist, Job, Task, Encoder, Extension

class JoblistForm(forms.ModelForm):
    """Classe formulaire de l'objet Joblist
    """
    
    def __init__(self, user, *args, **kwargs):
        """Formulaire qui filtre le champs job en fonction des objets Job dont l'utilisateur est propriétaire
    
        :param user: utilisateur propriétaire des objets Job
        :type user: User

        """
        super(JoblistForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label='Nom * ')
        self.fields['job'] = forms.ModelMultipleChoiceField(Job.objects.filter(owner=user), label='Jobs * ') # On filtre le queryset par utilisateur
    
    class Meta:
        model = Joblist
        fields = ('name', 'description', 'job')


class JobForm(forms.ModelForm):
    """Classe formulaire de l'objet Job
    """

    name = forms.CharField(label='Nom * ')
    encoder = forms.ModelChoiceField(Encoder.objects.all(), label='Encodeur * ') #, empty_label="------")
    options = forms.CharField(label='Options * ')
    extension = forms.ModelChoiceField(Extension.objects.all(), label='Extension * ') #, empty_label="------")

    class Meta:
        model = Job
        fields = ('name', 'description', 'encoder', 'options', 'extension', )
        

class TaskForm(forms.ModelForm):
    """Classe formulaire de l'objet Task
    """
    
    def __init__(self, user, *args, **kwargs):
        """Formulaire qui filtre le champs joblist en fonction des objets Joblist dont l'utilisateur est propriétaire
    
        :param user: utilisateur propriétaire des objets Joblist
        :type user: User

        """
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['joblist'] = forms.ModelChoiceField(Joblist.objects.filter(owner=user), label='Joblists * ') # On filtre le queryset par utilisateur
        self.fields['schedule'] = forms.DateTimeField(initial=(datetime.now()+timedelta(minutes=10)).strftime('%d/%m/%Y %H:%M'), label='Planification * ')
        self.fields['source_file'] = forms.FileField(label='Fichier source * ',)
        self.fields['notify'] = forms.BooleanField(label='Notification',help_text=' - Cocher pour activer')

    class Meta:
        model = Task
        fields = ('joblist', 'schedule', 'source_file', 'notify')
        
    def clean(self):
        cleaned_data = self.cleaned_data
        schedule = cleaned_data.get("schedule")
        
        if datetime.now() > schedule:
            self._errors["schedule"] = self.error_class(['Merci de ne pas planifier pour hier'])

        # Always return the full collection of cleaned data.
        return cleaned_data

