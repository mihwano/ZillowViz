import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import Point, shape
import sys


def zillow_data():
    df = pd.read_csv("data/transactions.csv", parse_dates=["transactiondate"])
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    df.drop(["longitude", "latitude", "parcelid"], axis=1, inplace=True)
    crs = {"init": "epsg:4326"}
    df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
    #df["geometry"] = df.apply(lambda row: Point((row["longitude"], row["latitude"])), axis=1)
    return df


# def zipcode_json():
#     with open("data/ZCTA/ca_zcta.geojson") as jsonfile:
#         zipcodes = json.load(jsonfile)
#     return zipcodes

def zipcode_data():
    return gpd.read_file("data/ZCTA/ca_zcta.geojson")


def get_zipcode(longitude, latitude, jsonfile):
    point = Point(longitude, latitude)                          # coordinates of each data point
    for record in jsonfile["features"]:                         # loop over json boundary file records
        polygon = shape(record["geometry"])                     # polygon object is the geometry of the record
        if polygon.contains(point):                             # check whether the data point is contained in boundary
            return int(record["properties"]["GEOID10"])         # if yes: retrieve the zip code value
    return "unknown"


def cleaned_data():
    df = zillow_data()
    zipcodes = zipcode_data()
    #zipcodes = zipcode_json()
    print("acquiring the zip codes through spatial join")
    df = gpd.sjoin(df, zipcodes, how="left", op="within")
    return df
#df['zipcode'] = df.apply(lambda row: get_zipcode(row['longitude'],
#                                                  row['latitude'], zipcodes), axis=1)

df = cleaned_data()