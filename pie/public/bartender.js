/*-----------------------------------------------------------------------------
 * JS File Loader
 *  Example Source
	<script type="text/javascript" src="/js/Foo.js"></script>
	<script type="text/javascript" src="/files/Bar.js?load=Baz,Qux"></script>
	<script type="text/javascript" src="/files/Qux.js?date=20060727"></script>
	var loader = new JSFile();
	loader('Foo,Bar,Baz'.split(','), '/lib/')
 * load files is
 *   - /js/Foo.js
 *   - /files/Bar.js
 *   - /files/Baz.js
 *   - /files/Qux.js // NOT double load
 *   - /lib/Foo.js
 *   - /lib/Bar.js
 *   - /lib/Baz.js
 *-------------------------------------------------------------------------- */

function JSFile() {
	var scripts = document.getElementsByTagName('script');
	this.base = scripts[0];
	this.list = {};
	this.book = {};
	
	for (var i = 0, len = scripts.length; i < len; ++i) {
		var src = scripts[i].getAttribute('src');
		if (!src) continue;
		this.list[src] = true;
		var path = src.replace(/([^\/]+?)\.js(\?.*)?$/, ''), inc = src.match(/\?.*load=([^&]*)/);
		if (inc) {
			if (path in this.book)
				this.book[path] += ',';
			else
				this.book[path] = '';
			this.book[path] += inc[1];
		}
	}
	for (var path in this.book)
		this.load(this.book[path].split(','), path);
}

JSFile.prototype = {
	_load: function (uri) {
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
	},
	load: function (jsfile, prefix, suffix) {
		prefix = prefix || '';
		suffix = suffix || '.js';
		for (var i = 0, len = jsfile.length; i < len; ++i) {
			var path = prefix + jsfile[i] + suffix;
			if (!this.list[path]) this._load(path);
		}
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

var loader = new JSFile();
loader(["http://static.ak.connect.facebook.com/js/api_lib/v0.4/FeatureLoader.js.php",
  "http://newsmixer.com/public/jquery-1.2.6.min.js"])

function startNewsmixer(pQuipContainer,pContentBody,pLetterContainer) {
  if (arguments.length > 0) {
    //do the quips
    quipEle = document.getElementById(arguments[0]);
    quipForm = document.createElement("div");
    quipForm.setAttribute("id","connect-form");
    quipForm.appendChild(document.createTextNode("Join the conversation!"));
    quipForm.appendChild(document.createElement("br"));
    quipForm.appendChild(document.createElement("fb:login-button").setAttribute("length","long"));
  }
}
