## steps to run this

- #### first go into the directory then do

- `python3 -m venv ./venv`
- `. ./venv/bin/activate`
- `pip3 install -r requirements.txt`
- `uvicorn app.app:app --reload`

#### `now you can open http://localhost:8000 in your browser` for http connection

plus -

###### `deactivate` (to get out from your virtual environment)

extra -
(although port 8000 is default just make sure your port 8000 is free, in case it's not then check your console on which port this app is running)
