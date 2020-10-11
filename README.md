# Code Challenge

The results of this code challenge are split into three major parts: `data_ingestion`, `review_service`, and `review_app`. 

## `data_ingestion`

The `data_ingestion` project is a python script indented to load the yelp-dataset into a postgres database. It consists of two SQL scripts capable of initalizing and destroying a postgress database, and a program (located in `data_ingestion/src`) to both run diagnostics on the datafile, and to load it into the database.

## `review_service`

The `review_service` project is a server-side REST-like API which forwards and updates 'review' records from the database to the calling user. It has only three calls, (list*, get*, update*) and obfuscates the existence of a DB 'favorites' table by combining it with the records for the user's personal view.

## `review_app`

The `review_app` project is a statically hosted SPA that calls the review_service in order to display reviews to the user, allow the user to obtain more details about the reviews, and further let the user mark certain reviews as 'favorites'.

## To Install And Run
After unzipping, do the following to install and run:

### Set up the database
- This project uses postgres. Ensure postgres is install.
- Change directory to `/data_ingestion`
- Execute the create.sql script via `psql -U myUser -f create.sql` using your root user
- Create a new python virtual environment and activate it
- Install python requirements via `pip install -r requirements.txt`
- Optionally, run the ingestor in statistics mode to evaluate the dataset's possible columns. This was done before determining the structure of the tables in create.sql: `py src/ingest.py review.json -s` assuming your data-set file is called 'review.json'
- Fill the database with reviews from the data file: `py src/ingest.py review.json postgresql://challenger:abcd1234@localhost/code_challenge` assuming your data-set file is called 'review.json'

Filling the database will take some time; after each 10,000 entries, it will output its progress. Once done, the database is ready to be used.

### Set up and run the service
- Change directory to `/review_service`
- Create a new python virtual environment and activate it
- Install python requirements via `pip install -r requirements.txt`
- Set the environment variable `FLASK_APP` to `./code_challenge.py`
- Set the environment variable `CONNECTION_STRING` to `postgresql://challenger:abcd1234@localhost/code_challenge`
- Use `flask run` to start the service. It should be listening locally on port 5000

Leave the service running so the app can connect to it.

### Set up and start the app
- Change directory to `/review_app`
- Install required dependencies using npm: `npm install`
- If the service is not running on localhost:5000, you will need to update the `.env` so that the REACT_APP_API_ROOT points to the proper location and port. Do not include a trailing `/`
- Run project `npm run start`. The development webserver should be running on port 3000.
- Open a browser to `http://localhost:3000`

## Using the App
The app will show a toobar, and a list of reviews. 

Scrolling down the list will result in an infinite scroll, continuously loading more entries before you arrive at the bottom. This is limited by the browser's memory and will fail long before all records are received, but probably not before the user gets bored. 

To seek into reviews from a long time ago, provide the correct date and time in the 'Before' section of the header; only records at or after this time will be retreived. 

Clicking on a row will show the entire review. Clicking the 'close' link will close the individual review view.

The 'heart' icon in both views indicates a review has been marked as a 'favorite'. Clicking this icon in either view will toggle that review as a favorite, a change that will be visible in both locations.

In the review list view, the 'Show Favorites Only' checkbox will filter the list to only those that have been marked as favorite.

Any time the 'Before' date is changed, or the 'Show Favorites Only' checkbox is changed, the results will be set back to the beginning, and the user's previous continuation cursor will be lost.

## Known Issues
- Database sorting - there is currently an issue with sorting/continuation tokens. When using the  continuation token for the last entry received, and asking for the next set, a small amount of overlap is received.
- When modifying the 'Before' time in the app, each modification submits a request to list the information again. This should get throttled so as not to waste server-time.
- User-facing error handling is omitted, but should be included to gracefully recover from errors, give the user the ability to fix the problem, or nicely disappoint the user.
- Loading indicators are missing, but given sufficient time would smooth out the user experience in case of a slow network. 