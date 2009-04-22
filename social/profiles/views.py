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

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from profiles.helpers import get_comments

@login_required
def personal(request):
    """show the dashboard or personal profile screen to a logged in user"""
    me = request.user.get_profile()
    
    comments = []
    
    friends = me.get_friends_profiles()
    comments = get_comments(friends)
    
    for fg in me.following.all():
        if not fg in friends:
            comments.extend(fg.get_recent_comments())

    comments.sort(key=lambda x: x.created)
    comments.reverse()
    
    content = """
        <fb:name uid="%s" firstnameonly="true" shownetwork="false"/>
        wants to invite you to join the conversation.
        <fb:req-choice url="%s" label="Check out News Mixer!"/>
        """ % (me.facebook_id, request.facebook.get_add_url())
    from cgi import escape 
    content = escape(content, True) 
    #exclude_ids = ','.join([str(f.facebook_id) for f in friends])
    facebook_uid = request.facebook.uid
    fql = "SELECT uid FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1='%s') AND has_added_app = 1" % me.facebook_id
    result = request.facebook.fql.query(fql)
    # Extract the user ID's returned in the FQL request into a new array.
    if result and isinstance(result, list):
        friends_list = map(lambda x: str(x['uid']), result)
    else: friends_list = []
    # Convert the array of friends into a comma-delimeted string.
    exclude_ids = ','.join(friends_list) 
    
    template_dict = {
        'me':        me,
        'my_comments':  me.get_recent_comments(),
        'friends':   friends,
        'following': me.get_following_profiles(),
        'followers': me.get_followers_profiles(),
        'comments':  comments,
        
        'action_url':  settings.ROOT_URL + request.path,
        'content':     content,
        'exclude_ids': exclude_ids,
        
    }
    return render_to_response('profiles/personal.html', template_dict, context_instance=RequestContext(request))
    
def detail(request,profile_id):
    """show the public profile screen to another user or anonymous"""
    profile = UserProfile.objects.get(pk=profile_id)
    if request.user.is_authenticated() and profile.id == request.user.get_profile().id:
        return HttpResponseRedirect('/profiles/')
    template_dict = {
        'comments':  profile.get_recent_comments(),
        'followers': profile.get_followers_profiles(),
        'following': profile.get_following_profiles(),
        'profile':   profile,
    }
    return render_to_response('profiles/public_profile.html', template_dict, context_instance=RequestContext(request))

@login_required
def follow(request,profile_id):
    if request.method == "POST":
        request.user.get_profile().following.add(UserProfile.objects.get(pk=profile_id))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
@login_required
def unfollow(request,profile_id):
    if request.method == "POST":
        request.user.get_profile().following.remove(UserProfile.objects.get(pk=profile_id))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
