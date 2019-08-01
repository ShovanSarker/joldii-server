# Joldii (Backend-Prototype)

This is the prototype for a Ridesharing app called Joldii. More details of this project are available [here](https://github.com/ShovanSarker/joldii-server/wiki).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash
pip install -r req.txt
```
or installing the required libraries manually by 
```bash
pip install Django
```
For more details, you are encouraged to see [here](https://github.com/ShovanSarker/joldii-server/wiki/Project-Setup).

## Usage
After the required libraries installed, go inside the project directory and check if the ```manage.py``` file is there. If it is there run the following code:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
these commands will update the database structure(if necessary) and run the service on [localhost](http://localhost:8000) on 8000 port.

## API Documentation
For API Documentation of this project, please see [here](https://github.com/ShovanSarker/joldii-server/wiki/API-Docs).

## License
[MIT](https://choosealicense.com/licenses/mit/)
