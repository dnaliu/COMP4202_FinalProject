import math
import numpy as np
import os
import glob
from PIL import Image
import pandas as pd
from math import *
from scipy import stats
import pathlib


basepath = pathlib.Path(__file__).parent.resolve()
doors_dir = str(basepath) + "/doors"
paper_dir = str(basepath) + "/paper_doors"
detected_texts = glob.glob(os.path.join(doors_dir, "*.txt"))
paper_texts = glob.glob(os.path.join(paper_dir, "*.txt"))

ground_truth = str(basepath) + "/elevation/Elevation_certificates.csv"
EC_df = pd.read_csv(ground_truth)
EC_df = EC_df.set_index("ID")

avg_door_h = 2.03
ft_to_m = 0.3048
fov_h = math.pi/6

column_names = ["image", "EC_id", "FFE_gsv_m","EC_FFE_m","error_m"]

def process_detected(object_fields):
    door = 0

    doorData = {}

    for idx, o in enumerate(object_fields):

        object_id = int(o[0])

        if object_id == door:

            doorData[idx] = float(o[2])
    
    if len(doorData) == 0:
        return None

        
    return max(doorData, key=doorData.get)

def get_altitude_angles(col, row, fov_horizontal, height, width):
    col = col - width/2
    row = height/2 - row
    r = (width/2)/math.tan(fov_horizontal/2)
    s = sqrt(col**2 + r**2)
    theta = math.atan(row/s)

    return theta

def getElevation(txt, index):
    #read file
    f = open(txt, 'r')
    lines = [line.replace(" \n", "") for line in f.readlines()]

    #extract object fields
    object_fields = [line.split(' ') for line in lines]
    basename = os.path.basename(txt)

    #extract image
    image_name = txt.replace(".txt", ".jpg")
    image = Image.open(image_name)
    image_w, image_h = image.size

    #extract elevation certificate data
    EC_id = int(basename.split("_")[0])
    EC_FFE_ft = EC_df.loc[EC_id]['FFE_ft']
    camera_h = EC_df.loc[EC_id]['camera_height_m']
    camera_dem_ft = EC_df.loc[EC_id]['DEM_ft']

    lowest_idx = process_detected(object_fields)

    if lowest_idx is None:
        return None

    xywh = object_fields[lowest_idx][index:]
    x, y, w, h = [float(i) for i in xywh]

    top_row = image_h * (y - h/2)
    bottom_row = image_h * (y + h/2)
    col = image_w * x

    bottom_angle = get_altitude_angles(col, bottom_row, fov_h, image_h, image_w)
    top_angle = get_altitude_angles(col, top_row, fov_h, image_h, image_w)

       
    distance = avg_door_h * cos(top_angle) * cos(bottom_angle) / sin(top_angle - bottom_angle)
    bottom_height = distance * tan(bottom_angle)

    return camera_h + bottom_height + camera_dem_ft * ft_to_m


def evaluate():
    measurement_df = pd.DataFrame(columns=column_names)
    undetected_file = f = open("undetected.txt", "w")

    paper_df = pd.read_csv(os.path.join(paper_dir, 'measurements.csv'))  
    #dataframe stuff
    for idx, txt in enumerate(detected_texts):
        paper_txt = paper_dir + "/" + pathlib.Path(txt).stem + ".txt"
        image_name = os.path.basename(txt.replace(".txt", ".jpg"))



        if(image_name in set(paper_df['image'])): 
            elevation = getElevation(txt, 1)

            if(elevation is None or elevation < 0):
                undetected_file.write(image_name + '\n')
                continue


            basename = os.path.basename(txt)
            EC_id = int(basename.split("_")[0])
            EC_FFE_m = EC_df.loc[EC_id]['FFE_ft'] * ft_to_m


            error = abs(elevation - EC_FFE_m)

            current_row = len(measurement_df)
            measurement_df.at[current_row, 'image'] = image_name
            measurement_df.at[current_row, 'EC_id']    = EC_id
            measurement_df.at[current_row, 'FFE_gsv_m'] = elevation
            measurement_df.at[current_row, 'EC_FFE_m'] = EC_FFE_m
            measurement_df.at[current_row, 'error_m']  = error

    measure_file = os.path.join(doors_dir, 'measurements.csv')
    measurement_df.to_csv(measure_file, index=False)
    undetected_file.close()

def compare_errors(filter_outliers= True):
    df = pd.read_csv(os.path.join(doors_dir, 'measurements.csv'))  
    paper_df = pd.read_csv(os.path.join(paper_dir, 'measurements.csv'))  

    df = df[(np.abs(stats.zscore(df['error_m'])) < 3)]
    paper_df = paper_df[(np.abs(stats.zscore(paper_df['error_m'])) < 3)]

    df = df[df['error_m'] < 1]
    paper_df = paper_df[paper_df['error_m'] < 1]

    return [f"Our Mean Error: {df['error_m'].mean()}\nPaper's Mean Error: {paper_df['error_m'].mean()}",
            f"Our Median Error: {df['error_m'].median()}\nPaper's Median Error: {paper_df['error_m'].median()}"]

if __name__ == '__main__':
    evaluate()
    for el in compare_errors():
        print(el)
    
   

        





        
        



        


