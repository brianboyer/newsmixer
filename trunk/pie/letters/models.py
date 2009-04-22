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

from datetime import datetime
from django.db import models
from bartender.models import Article
from django.contrib.auth.models import User
from django.forms import ModelForm
import search

class Letter(models.Model):
    """Letters to the Editor"""
    user = models.ForeignKey(User,verbose_name="Author")
    article = models.ForeignKey(Article,null=True,blank=True,verbose_name='In reply to article')
    letter = models.ForeignKey('Letter',null=True,blank=True,related_name='replies',verbose_name='In reply to letter')
    title = models.CharField(max_length=100)
    body = models.TextField()
    offensive = models.BooleanField(default=False)
    notify = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/letters/%i/" % self.id
    
    def __unicode__(self):
        return u"%s" % (self.title)
search.register(Letter,fields=[{"field_name":"title","is_title":True},{"field_name":"body"}])

class LetterForm(ModelForm):
    """Form for the Letters"""
    class Meta:
        model=Letter
        exclude = ('created','offensive','user','article','letter','editor_pick')


class EditorPickManager(models.Manager):
    def get_published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now)
    def get_top_two_published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now).order_by("-pub_date")[:2]

class EditorPick(models.Model):
    """A letter picked by an editor"""
    letter = models.ForeignKey(Letter,related_name="editor_pick")
    pub_date = models.DateTimeField("Publish date", default=datetime.now)
    publish = models.BooleanField("Publish on site", default=True,
                                  help_text='Editors picks will not appear on the site until their "publish date".')
 
    objects = EditorPickManager()                   
 
    def __unicode__(self):
        return u"'%s'" % (self.letter.title)
