# Cost of Living in the Philippines
### _A data visualization project to aid Filipinos with the cost of living in the Philippines._

This repository contains the files needed to run a data visualization app that shows the cost of living in the Philipiines, per region and province.
This was made with Plotly Dash in Python.

Sources for the data used can be found in ***References***.

## Instructions for running the app
Ensure beforehand that Command Prompt/command-line interpreter can detect Python!

1) Download files.
2) Open cmd/Terminal/command-line interpreter.
3) Change current directory to the path of the folder with the files, so ```cd <path to the folder>```
4) Type in ```python -m venv venv```
5) Type in ```venv\Scripts\activate```
6) Install the required packages by typing in ```pip install -r requirements.txt```
7) Run the app by typing in ```python app.py```
8) Follow the http link, or copy-paste into a web browser.

Step 6) can be skipped if the packages have been installed previously.

## What qualifies as Cost of Living?
To calculate the cost of living for each region/province, an estimate per household is obtained by summing up important expenses (food, healthcare, transportation, communication, insurance, housing and water).
Then, monthly cost of living per household is derived by adjusting the estimate based on the span of months the information has been gathered in; which as of the latest version of the app, is 6 months.
This is processed into percentages that show the distribution of families within determined cost of living price ranges. (see __Histogram and Line Graph__ under ***Features***)

Additionally, adjusted cost of living is taken per person, to be processed as an index for the choropleth map (see __Choropleth Map__ under ***Features***), 
with the raw value shown as well. (see __Categorical controls__ under ***Features***)

To see the exact code used for pre-procesing the data, see under ***References***.

## Features
- Categorical controls

![Screenshot of the categorical controls, with some information about the chosen category below for a family of 4 and per person](https://github.com/CyAdrienneRamos/col_datavis/blob/main/screenshots/Screenshot%202025-08-11%20105359.png)

Part of the top half of the right column is the controls for choosing which category the user would like to choose. 
The graphs and table change depend on the chosen category.
In addition, information about the cost/expenses of the chosen category is shown just below, for a family of four and per person.
When comparision is enabled, both provinces'/regions' respective information will show side-by-side, for ease of comparison.

- Compare between regions/provinces

![Screenshot of the controls for choosing between region or province, as well as choosing which region/province, plus the comparison enabler](https://github.com/CyAdrienneRamos/col_datavis/blob/main/screenshots/Screenshot%202025-08-11%20113945.png)

Part of the top half of the right column is the controls for the regions and province. 
Users can choose to display either region or province, with the first dropdown list for choosing which region/province to show cost of living information.
This is where users can also enable comparison, with the second dropdown list for choosing the compared region/province.

- Choropleth Map

![Screenshot of choropleth map of the Philippines, shaded based on the Cost of Living within each province/region](https://github.com/CyAdrienneRamos/col_datavis/blob/main/screenshots/Screenshot%202025-08-11%20105124.png)

On the left column, the app shows a choropleth map of the Philippines, segmented into each region or province. It is shaded based on an index taken from the cost of living per region/province, using gradients of two contrasting colors (blue to yellow).
This is so that users may not only easily distinguish the median cost of living within each region/province, but also compare with other regions/provinces in the surrounding area.

- Histogram and Line Graph

![Screenshot of histogram and line graph, with the former showing the distribution of median costs of the category chosen, while the latter shows the median costs/expenses of the chosen category by family size](https://github.com/CyAdrienneRamos/col_datavis/blob/main/screenshots/Screenshot%202025-08-11%20105232.png)

In the middle column, the app shows a histogram and line graph. The histogram shows the distribution of median costs, depending on the chosen category and province/region. 
The line graph shows the median costs/expenses of the chosen category by family size, also depending on the province/region. 
When comparison is enabled, both provinces'/regions' respective graphs will be shown comparitavely, for ease of comparison.
Each province/region also have their own color (blue or red), constrasting the other for ease of comparison in the merged graphs.

- Table of Food prices

![Screenshot of the table of food prices for the province/region chosen](https://github.com/CyAdrienneRamos/col_datavis/blob/main/screenshots/Screenshot%202025-08-11%20105312.png)

The bottom half of the right column shows a table of prices for various foods, for the chosen province/region.
When comparison is enabled, both provinces'/regions' respective prices for foods will be shown side-by-side, for ease of comparison.

## References
The following data was used for this project:
- [OpenSTAT Prices database (open in new tab)](https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__2018NEW/?tablelist=true), provided by the PSA. Prices are taken from Jan 2025 - Jun 2025.
- [Family Income and Expenditure Survey](https://psada.psa.gov.ph/catalog/FIES/about), also provided by the PSA. The dataset used is FIES 2023 Volume 2.
- [GeoJSON Repository of Philippine Maps](https://github.com/macoymejia/geojsonph). A repository of Philippine GeoJSON files.

In addition, the Jupyter Notebook used for pre-processing the data can be accessed in the folder __rawdata__. The folder includes the csv files used in the Notebook.
