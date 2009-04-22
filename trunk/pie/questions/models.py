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
from django import forms
from django.forms import ModelForm

# Create your models here.
class Question(models.Model):
    article = models.ForeignKey(Article)
    block = models.IntegerField(blank=True,default=-1)
    user = models.ForeignKey(User)
    text = models.TextField("Ask a question.")
    notify = models.BooleanField()
    offensive = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.offensive:
            return "Question #"+str(self.id)+" on '"+self.article.headline+"' (offensive)"
        else:
            return "Question #"+str(self.id)+" on '"+self.article.headline+"'"
            
    def get_absolute_url(self):
        return "%s#question-%s-%s" % (self.article.get_absolute_url(),self.block,self.id)

    
class QuestionForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    class Meta:
        model = Question
        exclude = ('article', 'block', 'user', 'offensive')
    
class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField("Answer the question.")
    reference = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Answer #"+str(self.id)+" to question #"+str(self.question.id)+" on '"+self.question.article.headline+"'"
    
    def get_absolute_url(self):
        return "%s#answer-%s-%s" % (self.question.article.get_absolute_url(),self.question.block,self.id)
    
class AnswerForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    class Meta:
        model = Answer
        exclude = ('question', 'user', 'offensive')
