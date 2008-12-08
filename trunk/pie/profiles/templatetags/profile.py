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

from django.contrib.auth.models import User
from django import template
from pie.letters.models import Letter
from pie.bumbles.models import Bumble
from pie.questions.models import Question,Answer

register = template.Library()

def show_comment(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, comment_obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return CommentNode(comment_obj)

class CommentNode(template.Node):
    def __init__(self, comment_obj):
        self.comment_obj = comment_obj
    def render(self, context):
        if isinstance(context[self.comment_obj],Bumble):
            template_name = "bumbles/profile_feed_bumble.html"
            context.update({'bumble':context[self.comment_obj]})
        elif isinstance(context[self.comment_obj],Answer):
            template_name = "questions/profile_feed_answer.html"
            context.update({'answer':context[self.comment_obj]})
        elif isinstance(context[self.comment_obj],Question):
            template_name = "questions/profile_feed_question.html"
            context.update({'question':context[self.comment_obj]})
        elif isinstance(context[self.comment_obj],Letter):
            template_name = "letters/profile_feed_letter.html"
            context.update({'letter':context[self.comment_obj]})
        else:
            template_name = "profiles/profile_feed_comment.html"
        t = template.loader.get_template(template_name)
        return t.render(context)

register.tag('show_comment',show_comment)

@register.inclusion_tag("profiles/follow_form.html",takes_context=True)
def show_follow_link(context,profile_to_follow):
    """shows a link for following or unfollowing"""
    try:
        if profile_to_follow == context['user'].get_profile():
            template_dict = {
                'display':'none',
                'profile':profile_to_follow,
            }
        elif profile_to_follow in context['user'].get_profile().following.all():
            template_dict = {
                'display':'unfollow',
                'profile':profile_to_follow,
            }
        elif profile_to_follow in context['user'].get_profile().get_friends_profiles():
            template_dict = {
                'display':'friend',
                'profile':profile_to_follow,
            }
        else:
            template_dict = {
                'display':'follow',
                'profile':profile_to_follow,
            }
    except (KeyError,AttributeError):
        template_dict = {
            'display':'none',
            'profile':profile_to_follow,
        }

    return template_dict

@register.inclusion_tag("profiles/medium_profile.html",takes_context=True)
def show_medium_profile(context,profile=None):
    if not profile:
        profile = context['user'].get_profile()
    context.update({'profile':profile})
    return context
