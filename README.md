# pm25outliers
This django project plots the PM2.5 levels for an option of four locations: Las Angeles, San Diego, New York, and New Delhi. Pm2.5 is an air pollutent that can impact health at high levels.
The data that is plotted is pulled from the aq_data table located in the aq database.
The first plot shows the mean pm2.5 level for the city, as well as +-2 standard deviations and +-3 standard deviations.  
The second scatterplot displays the spread of pm2.5 levels.  From this, ouliers can easily be spotted visually.

To start, make sure that the aq Postgres database is running.
The tables aq_data and aq_meta also need to be created. If the tables do not exist,
run the python project Project 1 Metadata in the terminal:
    python ingest_aq_data.py
    python ingest_aq_meta.py
Now pm25outliers is ready to run in the terminal:
    python manage.py runserver 
This command will display the development server.  The site will be found at 
    http://127.0.0.1:8000/graph
Clicking one of the four cities will bring the user to the next page which displays the plots: 
    http://127.0.0.1:8000/graph/results
