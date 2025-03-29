# f1-web-visualizations

## Introduction
This project explores various [research questions](#ResearchQuestions)
related to Formula 1.
On this website the results are presented with visualizations and analysis.
[Data collection](#Data) was happening in a different private repository.
This project was conducted as part of the "Data Science Project"-course at CAU University.

## Research Questions
The research questions that we are exploring:

- How does the starting grid position influence the finishing position of drivers in the seasons from 1994 - 2024?
    - How does this differ between circuits that have been driven on at least X times?
    - How does this differ between drivers of different experience levels (as determined by the amount of races they participated in)?
    - Are there specific drivers who excel or struggle more in wet conditions compared to dry conditions?

- How has the total number of crashes and retirements evolved in the seasons from 1994 - 2024?
    - Which tracks have the highest frequency of crashes or retirements compared to others?
    - How does weather affect race completion rates and the likelihood of crashes or retirements in the seasons from 2005 - 2024?

- How does the number and the average duration of pitstops for a driver in a race relate to his finishing position?

## Data
All data needed to run the website visualizations is stored as CSVs in the [data directory](data).
The data was gathered using the
[Jolpica F1 API](https://github.com/jolpica/jolpica-f1/blob/main/README.md)
for Formula 1 data and the
[Open Meteo API](https://open-meteo.com/en/docs/historical-weather-api)
for weather data tailored to each race's location and time.
The data collection process was done in the **private**
[F1-Data-Collection](https://github.com/JnsTrn/F1-Data-Collection) repository.

# Build and Deploy
To build the website the following components are needed:
 - All stylistic assets are located in the [assets directory](assets)
 - The data is stored as CSVs in the [data directory](data)
 - Most code for the visualizations is located in the [modules directory](modules)
 - The content of different pages is located in the [pages directory](pages)
 - The initilization of the application together with page independent content is located in [app.py](app.py).
To host the webiste all libraries listet in [requirements](requirements.txt)
must be installed (can be done by using pipenv). Python version 3.12.0 was used.
To start the website [app.py](app.py) must be executed.

# Website Walkthrough
The way to access all pages on the website is the navigation bar.
The a navigation bar is always available at the top as well as the imprint at the bottom.
The different pages will be explained in the following sections.

## Home Page
The web application starts initially at the home page.
On the home page an intruduction is given and the research questions are shown.
By clicking on one of the research questions the user is redirected to the respective page for that research question.

## Research Question Pages
These page display the respective results with visualizations.
Where it is nessecary a short description and analysis is also provided in the application.
How to use all important features is also provided here.
First some general information about all graphs:
 - All graphs have a menu on the top right
 - The graphs can be downloaded in its current state as png
 - The graph state can be altered by zooming and panning
 - To restore the original state click on 'Reset Axis' or reload the page
 - All graphs provide tooltips on hover

### Grid Position Analysis
Average placement depending on starting position:
 - The plots for 'race completed' and 'All races' can be toggled by clicking on the legend on the right

Relation between Starting and Finishing Position for the X:
 - The specific circuit can be selected with the drop down menu above (can be filtered with text input)
 - The circuits displayed in the drop down menu can be filtered by the slider above 

Amount of Times X has started and ended the race in a position from 1994 - 2024:
 - The bars for 'Start' and 'Finish' can be toggled by clicking on the legend on the right
 - The specific driver can be selected with the drop down menu above (can be filtered with text input)
 - The drivers displayed in the drop down menu can be filtered by the slider above 

Average placement of drivers with at least X races:
 - The plots for 'Races completed' and 'All races' can be toggled by clicking on the legend on the right. 
 The drivers also always sorted in ascending order by the top enabled category in the legend.
 - The number of races driven can be toggled with the slider above

Average placements of drivers in X conditions since 2005 and at least 20 races driven:
 - The bars for 'start' and 'finish' can be toggled by clicking on the legend on the right
 - The weather condition during the races can be toggled by the buttons above

### Retirement Analysis
Total Incidents by Year (1994 - 2024)
 - The plots for 'Total Retirements', 'Incidents/Crashes' and 'Technical Failures' can be toggled by clicking on the legend on the right

Incidents by Circuit (X - X) (Minimum X races):
 - The timeframe of the data can be toggled with the slider below
 - The minimum number of races driven on that circuit can be toggled with the slider below
 - The representation type of the data can be toggled between count per race and rate

### Pitstop Analysis
Pit Stop Analysis: X:
 - The plots for 'Fast', 'Average' and 'Slow' can be toggled by clicking on the legend on the right
 - The specific driver can be selected with the drop down menu above (can be filtered with text input)

Pit Stop Analysis: X (X) and Total Pit Stop Time per Driver(X):
 - The plots for 'Fast', 'Average' and 'Slow' can be toggled by clicking on the legend on the right
 - The specific circuit and year can be selected with the drop down menu above (can be filtered with text input)

## About the Data
This page provides information about where the data comes from and how it was processed.
