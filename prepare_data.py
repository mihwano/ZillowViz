import pandas as pd
import numpy as np


properties = pd.read_csv("data/properties_2017.csv")
data = pd.read_csv("data/train.csv")

properties = properties[["parcelid", "rawcensustractandblock", "regionidzip", "latitude", "longitude",
                         "taxamount", "landtaxvaluedollarcnt", "taxvaluedollarcnt",
                         "structuretaxvaluedollarcnt", "buildingqualitytypeid",
                         "yearbuilt", "bathroomcnt", "bedroomcnt", "calculatedfinishedsquarefeet"]]

properties.rename(columns={"rawcensustractandblock": "censustract", "regionidzip": "zipcode",
                           "taxamount": "collectedtax",
                           "landtaxvaluedollarcnt": "landvalue",
                           "structuretaxvaluedollarcnt": "housevalue",
                           "taxvaluedollarcnt": "propertyvalue",
                           "buildingqualitytypeid": "building_quality",
                           "calculatedfinishedsquarefeet": "sqft_area"}, inplace=True)

# extract censustract
properties['censustract'] = [float(repr(x)[:8]) if np.isfinite(x) else -1 for x in properties['censustract']]

# fill missing values or remove row
properties.dropna(subset=["landvalue", "propertyvalue", "housevalue",
                          "yearbuilt", "bathroomcnt", "bedroomcnt",
                          "sqft_area"], inplace=True)
properties["collectedtax"] = properties["collectedtax"].fillna(0)
properties["building_quality"] = properties["building_quality"].fillna(-1) 
properties["censustract"] = properties["censustract"].fillna(-1) 
properties["zipcode"] = properties["zipcode"].fillna(-1)

properties["latitude"] = properties["latitude"] / 1.0e6
properties["longitude"] = properties["longitude"] / 1.0e6

# merge with sales file
data = pd.merge(data, properties, on="parcelid", how="left")

properties.to_csv("data/fulldataset.csv", index=False)
data.to_csv("data/transactions.csv", index=False)
