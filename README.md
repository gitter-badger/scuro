<p align="center"><img width="17%" src="docs/Scuro_200x200.png" /></p>



Scuro is a web server that turns your PostgreSQL database directly into a RESTful API. The structural constraints and permissions in the database determine the API endpoints and operations.



**Scuro is under development, you check the dev branch for progress**

## Installation
- clone this repo:

`git clone git@github.com:TorchAI/scuro.git`

- change to the scuro project root folder, then Install dependencies:

`pipenv install`

- Run the app:

`uvicorn main:app --reload`

For more options, please refer to uvicorn documentation.

