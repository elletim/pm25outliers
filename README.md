# pm25outliers
This django project plots the PM2.5 levels for an option of fourteen locations: Las Angeles, San Diego, New York, New Delhi, San Francisco, Denver, Atlanta, Houston, Pheonix, Baltimore, Mumbai, Dubai, Dhaka, and Guangzhou. Pm2.5 is an air pollutent that can impact health at high levels.
The data that is plotted is pulled from the aq_data table located in the aq database.
The data is analyzed at four different levels: hourly, monthly, daily, and all cities together.

To start, make sure that the aq Postgres database is running.
The tables aq_data and aq_meta also need to be created. If the tables do not exist,
run the python project Project 1 Metadata in the terminal:
    python ingest_aq_data.py
    python ingest_aq_meta.py

Next, the question and choice models need to be populated, which can be done in the Python shell.  Below is a list of the commands:
    from graph.models import Choice, Question
    >>>q = Question(question_text = "What city would you like to select?")
    >>>q.choice_set.create(choice_text="Los Angeles", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/California/Los_Angeles.txt")
    >>>q.choice_set.create(choice_text="San Diego", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/California/San_Diego.txt")
    >>>q.choice_set.create(choice_text="New York City", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/New_York/New_York_City.txt")
    >>>q.choice_set.create(choice_text="New Delhi", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/India/NCT/New_Delhi.txt")
    >>>q.choice_set.create(choice_text="San Francisco", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/California/San_Francisco.txt")
    >>>q.choice_set.create(choice_text="Denver", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/Colorado/Denver.txt")
    >>>q.choice_set.create(choice_text="Atlanta", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/Georgia/Atlanta.txt")
    >>>q.choice_set.create(choice_text="Houston", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/Texas/Houston.txt")
    >>>q.choice_set.create(choice_text="Phoenix", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/Arizona/Phoenix.txt")
    >>>q.choice_set.create(choice_text="Baltimore", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/Maryland/Baltimore.txt")
    >>>q.choice_set.create(choice_text="Mumbai", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/India/Maharashtra/Mumbai.txt")
    >>>q.choice_set.create(choice_text="Dubai", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_Arab_Emirates/Dubai/Dubai.txt")
    >>>q.choice_set.create(choice_text="Dhaka", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/Bangladesh/Dhaka/Dhaka.txt")
    >>>q.choice_set.create(choice_text="Guangzhou", choice_url="http://berkeleyearth.lbl.gov/air-quality/maps/cities/China/Guangdong/Guangzhou.txt")


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
    
