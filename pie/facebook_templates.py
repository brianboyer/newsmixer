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

FACEBOOK_TEMPLATES = (
    ('question',(
        #one-line
        ['{*actor*} <a href="{*url*}">asked a question about the article</a>: {*headline*}.'],
        [{#short story
            'template_title': '{*actor*} <a href="{*url*}">asked a question about the article</a>: {*headline*}.',
            'template_body': '<b>"{*question*}"</b>'
        }],
        {#full story
            'template_title': '{*actor*} <a href="{*url*}">asked a question about the article</a>: {*headline*}.',
            'template_body': '''<div style="font-size:1.5em;margin-bottom:0.4em;">"{*question*}"</div>
                <div style="font-weight:bold;margin-bottom:0.2em;">{*headline*}</div>
                <div>{*article*} ...</div>'''
        },
        [{#action
            'text': "Answer {*actor*}'s question",
            'href': '{*url*}'
        }],
    )),
    ('answer',(
        #one-line
        ['{*actor*} <a href="{*url*}">answered a question about the article</a>: {*headline*}.'],
        [{#short story
            'template_title': '{*actor*} <a href="{*url*}">answered a question about the article</a>: {*headline*}.',
            'template_body': '''Q: "{*question*}" - <fb:name uid="{*asker*}" /><br/>
            A: <b>"{*answer*}"</b> - {*actor*}'''
        }],
        {#full story
            'template_title': '{*actor*} <a href="{*url*}">answered a question about the article</a>: {*headline*}.',
            'template_body': '''<div style="margin-bottom:0.4em;">Q: "{*question*}" - <fb:name uid="{*asker*}" /></div>
            <div style="font-size:1.5em;margin-bottom:0.2em;">A: "{*answer*}"</div>
            <div style="font-size:1.5em;margin-bottom:0.4em;text-align:right;">- {*actor*}</div>
            <div style="font-weight:bold;margin-bottom:0.2em;">{*headline*}</div>
            <div>{*article*}</div>'''
        },
        [{#action
            'text': "Read {*actor*}'s answer",
            'href': '{*url*}'
        }],
    )),
    ('bumble',(
        #one-line
        ['{*actor*} <a href="{*url*}">quipped about the article</a>: {*headline*}.'],
        [{#short story
            'template_title': '{*actor*} <a href="{*url*}">quipped about the article</a>: {*headline*}.',
            'template_body': '<b>{*actor*} {*verb*} {*bumble*}</b>'
        }],
        {#full story
            'template_title': '{*actor*} <a href="{*url*}">quipped about the article</a>: {*headline*}.',
            'template_body': '''<div style="font-size:1.5em;margin-bottom:0.4em;margin-top:2px;"><span style="border:solid 2px lightblue;text-transform:uppercase;padding:0 2px;">{*actor*}</span> <span style="border:solid 2px blue;background-color:{*verb_color*};color:white;text-transform:uppercase;padding:0 2px;">{*verb*}</span> {*bumble*}</div>
            <div style="font-weight:bold;margin-bottom:0.2em;">{*headline*}</div>
            <div>{*article*}</div>'''
        },
        [{#action
            'text': "Quip back!",
            'href': '{*url*}'
        }],
    )),
    ('letter',(
        #one-line
        ['{*actor*} wrote a letter to the editor: <a href="{*url*}">{*title*}</a>.'],
        [{#short story
            'template_title': '{*actor*} wrote a letter to the editor: <a href="{*url*}">{*title*}</a>.',
            'template_body': '<b>{*title*}</b><br/>{*body*}'
        }],
        {#full story
            'template_title': '{*actor*} wrote a letter to the editor: <a href="{*url*}">{*title*}</a>.',
            'template_body': '''<div style="font-size:1.5em;margin-bottom:0.2em;">{*title*}</div>
            <div>{*body*}</div>'''
        },
        [{#action
            'text': "Read {*actor*}'s letter",
            'href': '{*url*}'
        }],
    )),
    ('letter_re_article',(
        #one-line
        ['{*actor*} <a href="{*url*}">wrote a letter to the editor</a> in response to the article: {*headline*}'],
        [{#short story
            'template_title': '{*actor*} <a href="{*url*}">wrote a letter to the editor</a> in response to the article: {*headline*}',
            'template_body': '<b>{*title*}</b><br/>{*body*}'
        }],
        {#full story
            'template_title': '{*actor*} <a href="{*url*}">wrote a letter to the editor</a> in response to the article: {*headline*}',
            'template_body': '''<div style="margin-top:0.8em;">{*actor*} wrote:</div>
            <div style="font-size:1.5em;margin-bottom:0.2em;">{*title*}</div>
            <div>{*body*}</div>
            <div style="margin-bottom:0.2em;margin-top:1em;">In response to:</div>
            <div style="font-weight:bold;margin-bottom:0.2em;">{*headline*}</div>
            <div>{*article*}</div>'''
        },
        [{#action
            'text': "Read {*actor*}'s letter",
            'href': '{*url*}'
        }],
    )),
    ('letter_re_letter',(
        #one-line
        ['{*actor*} responded to a letter to the editor: <a href="{*url*}">{*title*}</a>'],
        [{#short story
            'template_title': '{*actor*} responded to a letter to the editor: <a href="{*url*}">{*title*}</a>',
            'template_body': '''In response to <fb:name uid="{*original_user*}" possessive="true"/> letter, {*actor*} wrote:<br/>
            <b>{*title*}</b><br/>{*body*}'''
        }],
        {#full story
            'template_title': '{*actor*} responded to a letter to the editor: <a href="{*url*}">{*title*}</a>',
            'template_body': '''<div style="margin-top:0.8em;">{*actor*} wrote:</div>
            <div style="font-size:1.5em;margin-bottom:0.2em;">{*title*}</div>
            <div>{*body*}</div>
            <div style="margin-bottom:0.2em;margin-top:1em;">In response to <fb:name uid="{*original_user*}" possessive="true"/> letter:</div>
            <div style="font-weight:bold;margin-bottom:0.2em;">{*original_title*}</div>
            <div>{*original_body*}</div>'''
        },
        [{#action
            'text': "Read {*actor*}'s letter",
            'href': '{*url*}'
        }],
    )),
    ('letter_re_letter_re_article',(
        #one-line
        ['{*actor*} <a href="{*url*}">responded to a letter to the editor</a> about the article: {*headline*}'],
        [{#short story
            'template_title': '{*actor*} <a href="{*url*}">responded to a letter to the editor</a> about the article: {*headline*}',
            'template_body': '''In response to <fb:name uid="{*original_user*}" possessive="true"/> letter, {*actor*} wrote:<br/>
            <b>{*title*}</b><br/>{*body*}'''
        }],
        {#full story
            'template_title': '{*actor*} <a href="{*url*}">responded to a letter to the editor</a> about the article: {*headline*}',
            'template_body': '''<div style="margin-top:0.8em;">{*actor*} wrote:</div>
            <div style="font-size:1.5em;margin-bottom:0.2em;">{*title*}</div>
            <div>{*body*}</div>
            <div style="margin-bottom:0.2em;margin-top:1em;">In response to <fb:name uid="{*original_user*}" possessive="true"/> letter about {*headline*}:</div>
            <div style="font-weight:bold;margin-bottom:0.2em;">{*original_title*}</div>
            <div>{*original_body*}</div>'''
        },
        [{#action
            'text': "Read {*actor*}'s letter",
            'href': '{*url*}'
        }],
    )),
)
