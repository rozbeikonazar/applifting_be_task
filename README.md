# applifting_be_task
To start my project, first you need to install dependencies from requirements.txt using this command  pip install -r requirements.txt. Then you need to run Offers API using this command in directiory offers_api: uvicorn main:app --host 0.0.0.0 --port 9000.
And after this run Products API using this command in directiory products_api: uvicorn main:app --host 0.0.0.0 --port 8000

In products_api/test_main.py in function test_create_product I have used creation directly through database, not through endpoint, because in Offers API I have function that register product. 

In offers_api/test_main.py I asserted in test functions only response code 200, because my background service is changing price every minute.