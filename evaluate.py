import matplotlib.pylab as plt
import math
import pandas as pd
import numpy as np
import os
import glob
import glob
import os
import math
from PIL import Image
from tqdm import tqdm
import pandas as pd
import math
from math import *
from scipy.stats import norm
from sklearn.metrics import r2_score

import pathlib

#import detect from detect

import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter

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

def cartesian_to_spherical(col, row, fov_h, height, width):

    col = col - width/2
    row = height/2 - row

    fov_v = atan((height * tan((fov_h/2))/width))*2

    r = (width/2)/tan(fov_h/2)
    s = sqrt(col**2 + r**2)

    theta = atan(row/s)

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

    bottom_angle = cartesian_to_spherical(col, bottom_row, fov_h, image_h, image_w)
    top_angle = cartesian_to_spherical(col, top_row, fov_h, image_h, image_w)

       
    distance = avg_door_h * cos(top_angle) * cos(bottom_angle) / sin(top_angle - bottom_angle)
    bottom_height = distance * tan(bottom_angle)

    return camera_h + bottom_height + camera_dem_ft * ft_to_m


def evaluate():
    measurement_df = pd.DataFrame(columns=column_names)
    undetected_file = f = open("undetected.txt", "w")

    #dataframe stuff
    for idx, txt in enumerate(detected_texts[0:]):
        paper_txt = paper_dir + "\\" + pathlib.Path(txt).stem + ".txt"
        image_name = os.path.basename(txt.replace(".txt", ".jpg"))


        if(not os.path.exists(paper_txt)):
            continue
        
        elevation = getElevation(txt, 1)

        if(elevation is None):
            undetected_file.write(image_name)
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



if __name__ == '__main__':
    evaluate()
   

        





        
        



        


