## Only do if you want to use with virtual environment
Create your virtual environment:
virtualenv venv

Start virtual environment first:
. venv/bin/activate

To install dependencies (from within the virtual environment):
pip install -r requirements.txt

To run the Flask app:
export FLASK_APP=index.py
flask run

To transfer the python code to server:
scp -r *.py root@97.107.142.134:/root/apps/the_bbc

To restart the python flask server
systemctl restart the_bbc.service

To check the status of the flask server
systemctl status the_bbc.service