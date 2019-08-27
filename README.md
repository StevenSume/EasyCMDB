# EasyCMDB
This is a CMDB develop based on flask python3.7 

# Config 
SQLALCHEMY_COMMIT_ON_TEARDOWN = True 

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@hostname/dbname'  #can be change to other database

SECRET_KEY = 'secret_key' # should be changed for security

TOKEN_EXPIRES_IN = 600

USERNAME='admin' # should develop your identification 

PASSWORD='admin'

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

# BUILD DOCKER IMAGE:
docker build -t $your_tag .

# RUN IMAGE:
docker run -itd -p 5000:5000 -v /your_path_to_config:/main/config.py

# API LIST BELOW:
##login and get token
curl -u admin:admin -i -X GET http://hostname:5000/token
## show project list
curl -u token_string:useless -i -X POST http://hostname:5000/get/project
## create project
curl -u token_string:useless -i -X POST --data '{"project_name":"test_project_name"}' http://hostname:5000/create/project
## delete project
curl -u token_string:useless -i -X POST --data '{"project_name":"test_project_name"}' http://hostname:5000/delete/project
### 
note!!! all items under the project will be deleted also
## rename project
curl -u token_string:useless -i -X POST --data '{"project_old_name":"test_project_old_name","project_new_name":"test_project_new_name"}' http://hostname:5000/rename/project
## get all items of project
curl -u token_string:useless -i -X --data '{"project_name":"test_project"}' http://hostname:5000/get/items
## create item 
curl -u token_string:useless -i -X --data '{"project_name":"test_project","key":"testkey","value":"testvalue"}' http://hostname:5000/create/item
###
note !!! if key is exist in this project ,the value will be updated
## delete item
curl -u token_string:useless -i -X --data '{"project_name":"test_project","key":"testkey1"}' http://hostname:5000/delete/item