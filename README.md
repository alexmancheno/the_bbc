#### Only do if you want to use with virtual environment
Install python3 pip:
```
sudo apt-get install python3-pip
```

Install virtualenv:
```
sudo apt-get install python-virtualenv
```

Create your virtual environment:
```
virtualenv venv
```

Start virtual environment first:
```
source venv/bin/activate
```

To install dependencies (from within the virtual environment):
```
pip3 install -r requirements.txt
```

If any packages were not installed, you need to manually install. Example:
```
pip3 install pandas
```

To run:
```
python3 index.py
```

To transfer the python code to server:
```
scp -r *.py root@97.107.142.134:/root/apps/the_bbc
scp requirements.txt root@97.107.142.134:/root/apps/the_bbc
```

To restart the python flask server (while logged in the server):
```
systemctl restart the_bbc.service
```

To check the status of the flask server
```
systemctl status the_bbc.service
```