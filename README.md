# Exercise: Mapping Median Earnings for New York Counties

### Summary

This exercise combines use of the Census API with use of the geopandas module and mapping via QGIS. It examines median earnings in New York counties over the last 12 months for the population 16 years and older who had any earnings. Just FYI, 'earnings' refers labor income and excludes income from capital (physical or financial assets) and transfer payments from the government.

### Input Data

The only input file is **tl_2019_us_county_36.zip**, a shapefile of New York counties that can be obtained from the previous assignment or from the Google Drive folder for this exercise. The remaining data will be obtained from the Census via its API. However, if you'd like to run the demo script, which is highly recommended, you'll need two other files from the Google Drive folder: **tl_2019_us_state.zip**, a Census TIGER/Line file of state boundaries, and **population.csv**, a file of population data downloaded from the Census API server.

### Deliverables

There are four deliverables: a script called **earnings.py** that will request data from the Census API, join the data to the county shapefile, save a histogram in a file called **earnings_hist.png**, and then write out the result as a geopackage file; a QGIS project file called **earnings_map.qgz**; and a PNG file called **earnings_map.png** that will be a heat map of median earnings.

### Instructions

**A. Script earnings.py**

1. Import modules as needed.

1. Using an approach similar to that of the earlier Census API assignment, download variable `"B20002_001E"` (median earnings in the last 12 months) for all counties in New York and create a dataframe from the results. Please call the dataframe `earnings`. As before, include `'NAME'` in the API query so the county names will be included. Since this task only involves a single Census variable, the steps in the earlier assignment related to `var_info` and the `"census-variables.csv"` file are not needed here. You can simply set the `'get'` part of the payload to the string `"NAME,B20002_001E"`. 

1. Create a new column in `earnings` called `'GEOID'` and set it to the result of concatenating the `'state'` and `'county'` columns of `earnings`. The result should be a 5-digit string that begins with 36.

1. Create a new numeric column in `earnings` called `"median"` that is the result of applying the `.astype(float)` method to the `"B20002_001E"` column of `earnings` and then dividing the result by 1000 to express the values in thousands of dollars.

1. Use the `to_csv()` method of `earnings` to write the data to `'earnings.csv'`. Use `index=False` because the index is just row numbers and does not need to be saved.

1. Use `fig, ax1 = plt.subplots()` to create a new single-panel figure as in previous exercises. 

1. Draw a histogram of median earnings by calling `sns.histplot()` with the arguments `data=earnings`, `x="median"`, `stat="density"`, and `ax=ax1`. The `stat` keyword indicates that the Y axis of the histogram should be the probability density.

1. Add a kernel density estimate to the figure by calling `sns.kdeplot()` with the arguments `data=earnings`, `x="median"`, `shade=True`, and `ax=ax1`. The `shade` option causes the area below the curve to be shaded.

1. Set the X axis label to `"Median Income in Thousands"`.

1. Tighten the layout and save the figure as `"earnings_hist.png"` using `dpi=300`.

1. Now create a trimmed-down dataframe for joining onto the shape file by setting `trim` equal to the `"GEOID"` and `"median"` columns of `earnings`.

1. Next, use the `geopandas.read_file()` function to read the New York county shapefile. Because the shapefile is zipped, the argument to `.read_file()` will need to be prefixed by `"zip://"` and should read `"zip://tl_2019_us_county_36.zip"`. Put the data into a variable called `geodata`.

1. Set `geodata` to the result of using a left one-to-one join to merge `trim` onto `geodata` using `on="GEOID"` and with `indicator` set to `True`.

1. Print the value counts for the `"_merge"` column of `geodata` to verify that all 62 counties matched, and then drop the column.

1. Write out `geodata` to a geopackage file called `"counties.gpkg"`. Set the layer to `"earnings"` and specify `driver="GPKG"`.

**B. Files earnings_map.qgz and earnings_map.png**

1. Create a new project in QGIS and add the vector layer in the `"counties.gpkg"`. If a `LIST_ALL_TABLES` option appears, set it to `<Default>`.

1. Then, build a heat map of the median earnings using "natural breaks" with 5 classes. The natural breaks mode does a pretty good job of dividing the counties into groups that a person might pick looking at the histogram: a very low group, two middle groups, a high group, and a very high group having just one member. You can choose the color ramp but keep in mind that the map will be easiest to interpret if low income areas are light and high income areas are dark. 

1. Label the counties using the medians. Set the point size to 7, turn on text buffers, and check the "Show all labels" box (on the brush tab).

1. Still adjusting the labels, go to the formatting tab (the one with "+ab" as part of its icon) and check "Formatted numbers" and set decimal places to 0.

1. Now save the QGIS project as `earnings_map.qgz` in the GitHub directory for the assignment. 

1. Export the map as an image to the GitHub directory as well and call it `earnings_map.png`.

### Submitting

Once you're happy with everything and have committed all of the changes to your local repository, please push the changes to GitHub. At that point, you're done: you have submitted your answer.

### Tips

+ A big plus about doing joins via Python rather than in QGIS itself is that it's much easier to manage the data types of the columns. QGIS will see the data types used by Python and will not try to infer them as it does with CSV files. Among other things, that means it won't accidentally clobber FIPS codes by coverting them from strings into numeric values.

+ A very nice feature of geopackage files is that they can contain multiple layers. Shapefiles, in contrast, can only contain a single layer. This exercise only involves a single layer but other projects will routinely involve several layers. Having one geopackage file is a lot more convenient than having several shapefiles, each of which is itself a directory of several component files. 
