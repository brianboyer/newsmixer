# Copyright 2008 Brian Boyer, Ryan Mark, Angela Nitzke, Joshua Pollock,
# Stuart Tiffen, Kayla Webley and the Medill School of Journalism, Northwestern
# University.
#
# This file is part of Crunchberry Pie.
#
# Crunchberry Pie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Crunchberry Pie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Crunchberry Pie.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from pressroom.models import Article
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

VERB_CHOICES = (
    ('thinks', 'Thinks'),
    ('feels', 'Feels'),
    ('wonders', 'Wonders'),
    ('agrees', 'Agrees'),
    ('disagrees', 'Disagrees'),
    ('hates', 'Hates'),
    ('loves', 'Loves'),
)

class Quip(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)
    verb = models.CharField(max_length=20, choices=VERB_CHOICES, default='says')
    message = models.CharField(max_length=200)
    notify = models.BooleanField()
    offensive = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
            
    def get_absolute_url(self):
        return "%s#quip-%i" % (self.article.get_absolute_url(),self.id)
        
class QuipForm(ModelForm):
    article = forms.CharField(widget=forms.HiddenInput)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    
    class Meta:
        model = Quip
        exclude = ('user')
        
    def clean_article(self):
        value = self.cleaned_data['article']
        try:
            return Article.objects.get(id=value)
        except Article.DoesNotExist:
            raise forms.util.ValidationError('Article %s does not exist' % value)
