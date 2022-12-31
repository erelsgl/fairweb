# fairweb
Fair division web application.

## Installation (on Ubuntu)

Copy the credentials from your Google account, and put them in file `credentials.json`.

Install python, virtualenv, and python-dev:

    apt install python3 python3-virtualenv python3-dev

Create a new virtual environment and activate it:

    virtualenv .venv
    source .venv/bin/activate

Install the requirements:

    pip install --upgrade pip
    pip install -r requirements.txt

To test the installation, run:

    python test_fairpy.py
    python test_gspread.py

## Usage

Create a Google Spreadsheet and share it with the email in your `credentials.json` file. It should look like: 

    test-159@spreadsheet-example-erelsgl.iam.gserviceaccount.com

Put the input in a worksheet named `input`.
[See here for input format example](https://docs.google.com/spreadsheets/d/1tJPV-y-r1TAx5FqbrqecKPJMeKHTtIDeiYck8eLoGKY/edit#gid=0).

Then, run `run.py`.

You will see the output in a worksheet named `output`.

## Flask app

To run the web-app, run:

    python app.py

Then, open the page `http://<your-address>:5000`.

Click the button to run the algorithm.

To run the web-app in the background, run:

    nohup python app.py > app.log 2>&1 &
    less app.log

    
