The core-django-app is the core app of all other apps (sites). 
It is used to store the common functionalities:
- The menu
- The Login/Logout -Button

The Menu should only contain the links to the admin-apps if 
an admin is currently logged in.

All other apps should depend on the core / be added to the core.