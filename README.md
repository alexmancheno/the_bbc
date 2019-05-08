## For the backend
**Note:** the following commands should be ran at 'application/'
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

To transfer the python and `requirements.txt` code to server:
```
scp -r *.py requirements.txt root@97.107.142.134:/root/apps/the_bbc
```

To restart the python flask server (while logged in the server):
```
systemctl restart the_bbc.service
```

To check the status of the flask server
```
systemctl status the_bbc.service
```

If new dependencies were added to the flask app, you need to install them on the server
```
cd /root/apps/the_bbc
pip3 install -r requirements.txt
```

The above will only work if `requirements.txt` is updated. Otherwise, you need to install new dependency manually:
```
pip3 install my_new_dependency
```

## For the frontend
**Note:** the following commands should be ran at 'frontend/react-app/'

To deploy to server:
```
scp -r public src package-lock.json package.json root@97.107.142.134:/root/apps/frontend
```

After deploying, you must restart the React app while logged into server:
```
sudo systemctl restart the_bbc_frontend.service
```

If new dependencies were added to `package.json`, you need to install them while logged onto server:
```
cd /root/apps/frontend
npm install --save
```