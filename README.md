# pm25outliers
This django project plots the PM2.5 levels for an option of four locations: Las Angeles, San Diego, New York, and New Delhi. Pm2.5 is an air pollutent that can impact health at high levels.
The data that is plotted is pulled from the aq_data table located in the aq database.
The plot shows the mean pm2.5 level for the city, as well as +-2 standard deviations and +-3 standard deviations.  From this, ouliers can easily be spotted visually.
The inital page can be found at /graph/. Here, the user is able to select what city to view.
The results, /graph/results/, will diplay the plot of the selected city.
