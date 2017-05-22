## Manjunath Babu
# PlanetAssetsAPI
Built custom API using Python and Flask. A RESTful web service. 

### Downloading files
In your terminal, use this command to download all files
```
git clone https://github.com/10manjunath/PlanetAssetsAPI
```

### Development Environment
We use Anaconda development environment to run this application. If you do not have it installed on your system, kindly visit https://conda.io/docs/install/full.html. It has complete details for Windows, MacOS and Ubuntu. After installing, follow the below instructions to setup the environment and downloading dependency packages.

### Conda
****
<img src="https://conda.io/docs/_images/conda_logo.svg" width="300">

```
conda env create -f environment.yml
source activate assetsAPI
```
Make sure you can see the environment name ```assetsAPI``` on the left of your prompt.

<img width="584" alt="conda source activate" src="https://cloud.githubusercontent.com/assets/7700267/26282264/1067f74c-3ddc-11e7-92bd-7c411e5405da.png">

### Python
In this application, we use Python version 3.6.
****
<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="300">


### Flask
In this application, we use Flask version 0.12. Flask is a microframework for Python. 
****
<img src="http://flask.pocoo.org/static/logo/flask.png" width="300">

### pytest
pytest is a mature full-featured Python testing tool that helps you write better programs.
****

<img src="https://docs.pytest.org/en/latest/_static/pytest1.png" width="270">

### CURL
We use curl, a command line tool and library for transferring data with URLs.
****
<img src="https://curl.haxx.se/logo/curl-logo.svg" width="300">

### Postman
We also use Postman, A powerful GUI platform to make API development faster & easier, from building API requests through testing, documentation and sharing.
****
 <img src="https://raw.githubusercontent.com/postmanlabs/postmanlabs.github.io/develop/global-artefacts/postman-logo%2Btext-320x132.png" width="300">






## Overview

We have 2 main files in this project. ```planet.py``` and ```test_planet.py```. We start Flask server by running ```planet.py``` file. It will initialize the asset store with an empty list. We consider this as our database. 


Starting Flask server
======
Open a new terminal window and set the source to ```assetsAPI``` and then run the ```planet.py``` file

```
source activate assetsAPI
python planet.py
```
Server is running at http://127.0.0.1:5000/

<img width="650" alt="start server" src="https://cloud.githubusercontent.com/assets/7700267/26282324/bc19e5fe-3ddd-11e7-8278-93e346320d66.png">


URL Formats
====

Planet_API_URL = "http://127.0.0.1:5000/"

- ## GET Request

Welcome Screen

```python
requests.get(f'{Planet_API_URL}/',headers={'Content-type: application/json'})
```

All assets

```python
requests.get(f'{Planet_API_URL}/planet',headers={'Content-type: application/json'})
```


Specific asset

```python
requests.get(f'{Planet_API_URL}/planet/<asset name>',headers={'Content-type: application/json'})
```

Filter asset (Filter word can be ```satellite```, ```antenna```, ```dove```, ```rapideye```, ```dish```, ```yagi```)

```python
requests.get(f'{Planet_API_URL}/planet/filter/<filter word>',headers={'Content-type: application/json'})
```

- ## POST Request
This format is used to POST a request. Asset details can be removed if required.

```python
requests.post(f'{Planet_API_URL}/planet',
                    headers={'Content-type: application/json', 'X-User':<your username>}
                    json={'asset name':<asset name>,'asset type':<asset type>,'asset class':<asset class>,'asset details':<asset details>
                    )
```



Lets get started by posting using CURL
====
To see if this setup is working lets POST 2 Assets. Execute below two commands one after the other.
```
curl -X POST -H 'Content-Type: application/json' -H 'X-User: admin' -d '{"asset name":"ANT_01","asset type":"antenna", "asset class":"dish","asset details":{"diameter":"23.0","radome":"True"}}' http://127.0.0.1:5000/planet

curl -X POST -H 'Content-Type: application/json' -H 'X-User: admin' -d '{"asset name":"SAT_01","asset type":"satellite", "asset class":"rapideye"}' http://127.0.0.1:5000/planet
```
<img width="709" alt="curl 2 assets" src="https://cloud.githubusercontent.com/assets/7700267/26291714/4e54c75e-3e7e-11e7-9aba-7ad9f16896e4.png">

Output: Successfully Posted 2 assets

Verify using Postman extension
===
To verify if they were posted, we call GET request using Postman extension. Open the tool, set the header to ```'Content-Type': application/json ```. Enter correct URL. Hit send button. You will see all the assets displayed in json format.


<img width="842" alt="postman get" src="https://cloud.githubusercontent.com/assets/7700267/26291846/63790f22-3e7f-11e7-9dbd-a5781a5612c3.png">


View Server Activity
=====
All request are being logged in this terminal window.

<img width="649" alt="verify server activity" src="https://cloud.githubusercontent.com/assets/7700267/26282501/ae4a6464-3de0-11e7-88e1-85728ec39214.png">


Testing 
=====

#### It is always good to write detailed test cases during API development. The file ```test_planet.py``` has 24 test cases. Lets execute this file.
****
```
pytest test_planet.py
```
<img width="618" alt="test cases" src="https://cloud.githubusercontent.com/assets/7700267/26282683/1f8f7076-3de4-11e7-842a-4637c16d7b08.png">


#### Lets run the same test in verbose mode. It gives individual status of every testcase.
****
```
pytest -v test_planet.py
```
<img width="628" alt="verbose test cases" src="https://cloud.githubusercontent.com/assets/7700267/26282714/8d358106-3de4-11e7-9aff-732432acc716.png">


#### Executing ```test_planet.py``` file in Python will give detailed insight of all the test cases and edge cases.
****

```
python test_planet.py
```

**Thank you**





