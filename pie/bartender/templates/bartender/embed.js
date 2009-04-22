{% load quips %}
{% load facebook %}
{% load bartender %}
{% autoescape off %}
	
/*-----------------------------------------------------------------------------
 * JS File Loader
 *-------------------------------------------------------------------------- */

function load(uri) {
	var XUL_NS_URI = 'http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul';
	if (document.documentElement &&
		document.documentElement.namespaceURI == XUL_NS_URI) {
		var tmp = document.createElementNS(XUL_NS_URI, 'script');
		    tmp.setAttribute('type', 'application/x-javascript');
		    tmp.setAttribute('src', uri);
		this.base.parentNode.appendChild(tmp);
	} else {
		document.write('<script type="text/javascript" src="' + uri +'"></script>');
	}
}
	
// Copyright 2009 Ryan Mark
//
// This file is part of Crunchberry Pie.
//
// Crunchberry Pie is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Crunchberry Pie is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with Crunchberry Pie.  If not, see <http://www.gnu.org/licenses/>.

load("http://static.ak.connect.facebook.com/js/api_lib/v0.4/FeatureLoader.js.php");
load("http://127.0.0.1:8000/public/jquery-1.2.6.min.js");
load("http://127.0.0.1:8000/public/jquery.maxlength.js");
load("http://127.0.0.1:8000/public/form.js");

var NM_loadInterval = setInterval(NM_bootstrap,250);

function NM_bootstrap() {
  if (!(window.jQuery === undefined) && 
      !(window.FB_RequireFeatures === undefined) &&
      !(window.jQuery.fn.maxlength === undefined) &&
      !(window.jQuery.fn.ajaxForm === undefined)) {
    console.log('done loading!');
    clearInterval(NM_loadInterval);
    window.NM_$ = NM.$ = jQuery.noConflict();
    window.NM.init({quipContainer:'quips-container'});
  }
}

var NM = new function() {
  var self = this; // makes for easier reference in inline functions
  
  this.init = function() {
    if (arguments.length > 0)
      this.settings(arguments[0]);
      
    FB_RequireFeatures(["XFBML"], function(){
        FB.init("690645e7abbfa790aac71a77a31c8ccb", "/public/connect/xd_receiver.htm");
        FB.ensureInit(function(){
          console.log("Facebook is ready, rendering the page...");
          my_id = FB.Connect.get_loggedInUser();
          NM_$("#"+self.quipContainer).html('{% filter js_string %}
            <h3>What are people saying right now?</h3>
            <div id="NM-quip-head"></div>
            <div id="NM-quip-body">
              <div id="start-message">
                <h4>Start the conversation.</h4>
                <p>What did you think about this article? Share what you think, feel, wonder, agree, disagree, love or hate. Your quips are limited to 140 characters, but you can quip as often as you like.</p>
              </div>
            </div>
            {% endfilter %}');
          if ( my_id ) {
            // render form
            self.renderForm();
          } else {
            self.renderConnect();
          }
          self.Quips.init();
          FB.XFBML.Host.parseDomTree();
        });
    });
  };
  
  this.renderForm = function() {
    NM_$("#NM-quip-head").html('{% filter js_string %}
      <form id="quip-form" method="POST" onsubmit="return NM_sendQuip();">
        <span class="name"><fb:name uid="'+FB.Connect.get_loggedInUser()+'" useyou="false"></fb:name></span>
        <input type="hidden" name="article_url" value="'+window.location.href+'" />
        <input type="hidden" name="facebook_id" value="'+FB.Connect.get_loggedInUser()+'" />
        {{ quip_form.verb }}
        {{ quip_form.message }}<br/>
        <div class="count">
          <span class="charsLeft">140</span> characters remaining 
          <input type="hidden" name="maxlength" value="140" />
        </div>
        <div class="submit"><input type="submit" value="Submit"/></div>
      </form>{% endfilter %}');
    this.Quips.initForm();
  };
  
  this.renderConnect = function() {
    NM_$("#NM-quip-head").html('{% filter js_string %}
      <h4>To join the conversation,<br/>log in with Facebook Connect. 
        <fb:login-button length="long" onlogin="NM.login();"></fb:login-button>
      </h4>{% endfilter %}');
  };
  
  this.settings = function(settingsObj) {
    for (var i in settingsObj)
      this[i] = settingsObj[i];
  };
  
  this.login = function() {
    this.renderForm();
    FB.XFBML.Host.parseDomTree();
  };
  
}

{% include "quips/quip.js" %}
{% endautoescape %}