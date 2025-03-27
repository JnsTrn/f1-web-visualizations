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
• Showcase how to use your web application and the highlights


