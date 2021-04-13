#! /bin/python3
#  PAI789 (PJW)
#
#  Demonstrate using geopandas for joining data onto a shapefile. To use 
#  this script, download the Census shapefile tl_2019_us_state.zip and the 
#  CSV file population.csv from the course Google Drive.
#

import pandas as pd
import geopandas

#%%
#
#  Read the shapefile
#

states = geopandas.read_file("zip://tl_2019_us_state.zip")

print( '\nOriginal length:', len(states) )

#
#  Now filter out the states or equivalent entities that aren't part 
#  of the contiguous (or conterminous) US
#

po_notcon = ['AK','AS','GU','HI','MP','PR','VI']

is_conus = states['STUSPS'].isin(po_notcon) == False

conus = states[ is_conus ]

print( '\nFiltered length:', len(conus) )

#%%
#
#  What's in conus?
#

print( 'number of rows, columns:', conus.shape )
print( 'columns:', list(conus.columns) )

#
#  Grab the row for the first state, which happens to be WV 
#

wv = conus.iloc[0]
print( wv )

#
#  Get information about its geometry
#

wv_geo = wv['geometry']

print( 'Type of object:', type(wv_geo) )
print( 'Number of points:', len(wv_geo.exterior.coords) )

print( wv_geo )

#%%
#
#  Read the population data, being careful to keep the state 
#  FIPS code as a string
#

pop = pd.read_csv('population.csv',dtype={'state':str})

#  Rename the state FIPS code to match the shapefile's name

pop = pop.rename({'state':'STATEFP'},axis='columns')

#  Convert the population to millions and also compute the percentage

pop['mil'] = pop['B01001_001E']/1e6

pop['pct'] = 100*pop['mil']/pop['mil'].sum()
pop['pct'] = pop['pct'].round(2)

#  Select the variables to join onto the shapefile

sel_vars = ['STATEFP','mil','pct']

trim = pop[sel_vars]

#%%
#
#  Now merge the population data onto the shapefile
#

conus = conus.merge(trim,
                    on='STATEFP',
                    how='left',
                    validate='1:1',
                    indicator=True)

print( conus['_merge'].value_counts() )
conus.drop('_merge',axis='columns',inplace=True)

#%%
#
#  Write it out as a geopackage file. Put the data into a layer 
#  called states.
#

conus.to_file("conus.gpkg",layer="states",driver="GPKG")
