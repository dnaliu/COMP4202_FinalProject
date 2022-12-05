import os
import subprocess
import pandas as pd
import pathlib

basepath = pathlib.Path(__file__).parent.resolve()
ground_truth = str(basepath) + "/elevation/Elevation_certificates.csv"

df = pd.read_csv(ground_truth)
images = list(df["ID"].values) 

image_names = os.listdir(os.getcwd()+"/inference/images")

def runDetect():

    i = 0
    for image_name in image_names:

        if(i > 5):
            return

        i = i+1
        
        if(int(image_name.split("_")[0]) in images):
            print("here")
            subprocess.run(f"python detect.py --weights door_final.pt --img-size 640 --save-txt --source inference/images/{image_name}")

if __name__ == '__main__':
    runDetect()