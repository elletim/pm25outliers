# pm25outliers
This django project plots the PM2.5 levels for an option of fourteen locations: Las Angeles, San Diego, New York, New Delhi, San Francisco, Denver, Atlanta, Houston, Pheonix, Baltimore, Mumbai, Dubai, Dhaka, and Guangzhou. Pm2.5 is an air pollutent that can impact health at high levels.
The data that is plotted is pulled from the aq_data table located in the aq database.
The data is analyzed at four different levels: hourly, monthly, daily, and all cities together.

To start, make sure that the aq Postgres database is running.
The tables aq_data and aq_meta also need to be created. If the tables do not exist,
run the python project Project 1 Metadata in the terminal:
    python ingest_aq_data.py
    python ingest_aq_meta.py
Now pm25outliers is ready to run in the terminal:
    python manage.py runserver 
This command will display the development server.  The site will be found at 
    http://127.0.0.1:8000/graph
This page will allow the user to select the desired grouping.
The address for each choice is as follows: 
    http://127.0.0.1:8000/graph/hour/
    http://127.0.0.1:8000/graph/day/
    http://127.0.0.1:8000/graph/month/
    http://127.0.0.1:8000/graph/all/
Clicking one of the fourteen cities will bring the user to the next page which displays the plots.
At the bottom of each page is a link than will allow the user to select a new city or select a new grouping. 

** any data that was generated for the final PM25 report is commented at the end of each view, before the context.  To view the data, simply uncomment the print statement.
    
