# Background #

The initial release of News Mixer was the result of eleven weeks of intensive research and development by graduate students at Northwestern University's Medill school of journalism. The goal of the first release was not to produce a fully functional news website, but rather to demonstrate different ways of thinking about how foster communities and conversations around news articles on the web.

Version 1.0 of News Mixer is a standalone application built on Python and Django. It is meant as a technology demo. For those who liked the ideas and wanted the software, News Mixer is a great commenting system, but it lacks depth. There was very little time put into anything else. The content management component is minimal. There is no support for media: images or video. There was a lot of thought, but little dev time put into comment moderation, either for site owners or visitors.

Despite the minimalism of News Mixer 1.0, it was a hit. People were impressed and inspired by it. So for a tech demo it was a success. Now to make it usable ...

# Usefulness #

The 2.0 release of News Mixer will move towards a more useful application built to be used news organizations and anyone who wants the features. The plan is to turn the current code into a backend system to manage commenting, to build an api, and to build a plugin to make the features available for Wordpress.

Why not just put all the commenting features into a Wordpress plugin?

So no wheels are re-invented, and so we can write plugins for other content management systems down the line. And so organizations can manage the comments for many sites in one place.


# Details #

What is going to be in News Mixer 2.0:

  * Manage multiple sites
  * API to create/retrieve content – options to include return format of XML or JSON
  * API to Display Quips, Q&A and Letters to the editor
  * API to search content
  * Passthrough Facebook Connect
  * Wordpress Plugin
    * Login with Facebook connect
    * Send content back to Facebook
    * Display Quips, Q&A and Letters to the editor in a post
    * Display all Quips for home page
    * Users can add Quips, Q&A and Letters
    * Wordpress search displays News Mixer content