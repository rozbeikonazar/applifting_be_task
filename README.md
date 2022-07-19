# applifting_be_task
REST API JSON Python microservice which allows users to browse a product catalog and which automatically updates prices from the offer service

To start my project, first you need to install dependencies from requirements.txt using this command  pip install -r requirements.txt. Then you need to run App using this command: uvicorn main:app --host 0.0.0.0 --port 9000.
Or you can start project with docker-compose.
The main page can be accessed by this link "/api/v1/products-crud/docs"
To check test_main.py You should first start server with commands above.
Also I deployed project on Heroku here is a link: http://appliftingtask.herokuapp.com/