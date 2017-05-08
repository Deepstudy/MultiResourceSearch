# MultiResourceSearch
Multiple Resource Search RESTful API using Python and django
Clone the project from github.
Check out the rquirement.txt file and install all the updates and packages.
Run the Celery work Server using the following command: 
celery -A tasks worker --loglevel=info
Make sure that only worker server is running at a time. 
Open your web browser and type this : http://127.0.0.1:8000/my_resources/v1/search/?q=%22hello%22
Type your own query in place of hello.

