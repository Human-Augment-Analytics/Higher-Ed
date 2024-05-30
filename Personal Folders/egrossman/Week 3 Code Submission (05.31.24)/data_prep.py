import pandas as pd
import requests
import json
import uuid


def download_media(media_dict):
    """Downloads the picture in the media link (png, jpeg, etc) to the data folder and returns the image
    
    Ketword Arguments:
    media_dict -- a single media object with multiple links from the GBIF dataset
    """
    file_name = media_dict["identifier"]
    extension = file_name.split(".")[-1]

    identifier = str(uuid.uuid4())

    new_file_name = identifier + "." + extension

    file_path = "data/images/" + new_file_name
    
    image_data = requests.get(file_name).content
    
    with open(file_path, "wb") as f:
        f.write(image_data)
    return new_file_name


def parse_records(occurences, download_media=False):
    """Parses the IDIGBIO json to extract species, description, and media locations
    Keyword Arguments: occurences: list of occurances
    """

    for occurence in occurences:

        database = []

        for record in occurence["results"]:


            for media in record["media"]:

                record_dict = {}

                record_dict["id"] = record["key"]
                record_dict["speciesKey"] = record["speciesKey"]
                record_dict["scienceName"] = record["acceptedScientificName"]
                record_dict["simpleName"] = record["genericName"]
                record_dict["dataset"] = record["datasetName"]
                

                record_dict["media"] = ""
                if download_media:
                    file_name = download_media(media)
                    record_dict["media"] = file_name

                record_dict["media_location"] = media["identifier"]

                database.append(record_dict)


    print(database)
    df = pd.DataFrame(database)
    df.to_csv("data/input.csv")

    return df

def echo():
    print("Echo")