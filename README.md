## Inventory System API

I developed this one as a part of practise. The aim is to develop an inventory management system,
and currently it has few features which are:

1. User registration as Owner
2. User verification (For simplification, it is now by auth code)
3. Create Store as Owner
4. Create SALES Stuff 
5. CRUD operation on product on your Store as Owner
6. Generate Invoice as Owner/Sales
7. Fetch Invoice List

more feature will be added soon ...

### Here I used:
* Oauth2 for login
* Pydantic DTO class for serialization and deserialization
* Faker & Factory boy for testing

## Project setup process:

* Clone from this repository
* Create virtual environment and turn it on (Suppose virtual environment name is venv)`source venv/bin/activate`
* Create a postgresql db in your machine
* Create a file called `local_settings.json`, copy all things from `sample_local_settings.json` file to `local_settings.json`
* In the `local_settings.json` file, set proper data (Ex. DB info)
* Install packages by `pip install -r requirements.txt`
* Migrate database `python manage.py migrate`
* Create Oauth2 application from `http://localhost:8000/oauth/applications/`
* Use the created client id & client secret during login

### Test case
* Run test cases `python manage.py test`

## Swagger API Doc

http://localhost:8000/swagger/

### Postman collection
A postman collection added for test purpose