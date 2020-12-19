# Hybrid Slackbot


## Download for development
Create a slack account if you dont have one.
On api.slack.com go to "your apps" and create a new app. 

`git clone REPO`. and install the requirements into a virtual environment or use the container.

Copy the CLIENT_SECRET (aliased as SLACK_TOKEN) and the SIGNING_SECRET from the basic information tab into a .env file. 

You'll need to set up a development server. Using ngrok.io is recommeneded.
create an event subscription with the request URL provided by ngrok.


## Functionality
- keeps track of user activity
- responds to users joining a workspace with a welcome message

## Features 
Create channel specific welcome messages via slack command (or a general
message if one does not exist) 
- stored in a WelcomeMessages class (1 per channel_id)
- created by a create-welcome-message command (only available to admin)
- override Welcome messages with commands referencing the same channel (class properties?)


ADVANCED
-beyond the analytics dashboard, use the analytics API for stateless
slack messaging
-record user activity (investigate admin user auth token level
permissions
-create user activity reports for managers.

