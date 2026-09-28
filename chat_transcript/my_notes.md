# My own notes while building this project

(These are my personal notes, not the chat export. The exported chats are the other files in this folder.)

First i was created a project folder in my project directory
Then i was done the required setup like basically we need here one project, one app, and also the some files like a .env and .gitignore

The .env file we used for setup the environment variable like in development phase i mean in local directory we used debug = true but in production we used debug = false and in .env we set all the things like a secret  key which is we generate using the the django command :- python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
also there we will be able to configure the setp like a database url or cloudinary database setup and also SMTP credentials etc stuff

The .gitignore file we created to hide or delete the important files and crendentials which is very important assue if we dont have this file then we need to go to git hub repo and delete the manually the harmful files someone can be stole the your important file and used for a inllegal purposes for that thing we need to used this .gitignore beacause it is not commet the that things which is define under it and not shows that conent on gthub 

when i was develop a my first website at that time donet ahave a much knoeledge about this i was simply watch the tutorials and implement it in my project at that time my .env file is publically shown on a github repo of my project and someone is stole the my SMTP Secrect credential and used for a fake spaming message but he was used a automation for sending the message and most of the mails are faild to send and save as a draft i was see that thing in my working dummy email and i was enable the the 2 factor authntication and changes the password and remove the .env file from my projects as a begineers it may be happen with many peoples but it teach me and in my other projects i was first setup required things

lets create a django app shipping using the django command python manage.py startapp shipping
when we run this command then django create a suitable required file for the app like a admin.py, models.py, apps.py, tests.py, views.py and this is important file for creating a setup  for a application

the models.py file we used to define the dataset of a our application where which data should be need to store
in views.py we define the application logic i mean how it acts on some request or somethings else like request handling etc
also the admin.py it's usefull where the we define what data should be display on the admin pannel

django has a built in admin pannel and its most popular and many developer  used django over the flask beacause of this reasn but i was choose django beacause its built for a high scale projects and taks and it have wild range of communit and featurs and many things

The apps.py is used to define a App configuration its set automatcally most of thime dev not touch it and used it

also in main project folder we have a settings.py file there will be we state the most of important connection like we now createa a shipping app so first after crated the app we need to define it Under the INSTALLED_APPS we need to be define the all created apps in the project. In our case we have created one app called shipping. So we need to define it here.

settings.py file :-

# Import the os for the local path and import Path from pathlib to define the base directory of the project.
import os

# We import the os and used them to get the environment variable for the secret key. If the environment variable is not set, it will use a default value of "dev-only-insecure-key-change-me". This is useful for development purposes, but in production, you should set the environment variable to a secure value.
Old :- (the generated Django development key, removed from this file on purpose)
New :- 
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
similar happens with a ALLOWED_HOSTS, DEBUG, etc, all

By default we have a DATABASES which is a dbsqlite 

We are create a separate urls file within a shipping app eit helps to look clean the project in url we define the routes of a recommend box and orders
also created a packing and serivecs files in shipping file where we packing.py file handle and  Given these items and the available shipping boxes, which is the cheapest box in which all items can physically fit?" and the services.py file is the bridge between Django/database models and the pure packing algorithm in packing.py.

create a tests folder in which we have a test the whole application like api for we create a test_api.py and packing we have a test_packing.py

create a tests/test_api.py is an integration/API test file for your shipping application. and its purpose is to verify that the Django models, services, packing logic, HTTP API work correctly together

create a tests/test_packing.py is a unit-test file for packing.py. It checks whether your box-selection algorithm works correctly without Django or a database.

basicallu overall in short they ar :- 

test_packing.py
    → tests the packing algorithm itself

test_api.py
    → tests the whole application through Django API endpoints

    By default, Django includes the admin site at the URL path /admin/. You can customize this path by changing the argument to the path() function. For example, if you want to change the admin site URL to /myadmin/, you can modify the urlpatterns list as follows:
urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import include, path
We are from django.urls import include for including the URLs from the shipping app. The include() function allows us to reference other URLconfs. In this case, we are including the URLs defined in the shipping app's urls.py file.

The line path("api/", include("shipping.urls")) includes the URL patterns defined in the shipping app's urls.py file under the /api/ path. This means that any URL starting with /api/ will be handled by the views defined in the shipping app. For example, the URL /api/recommend-box/ will be routed to the recommend_box_view function in shipping/views.py, and /api/orders/<reference>/box/ will be routed to the order_box_view function in shipping/views.py.
