import os
import subprocess
import pandas as pd
import pathlib

basepath = pathlib.Path(__file__).parent.resolve()
ground_truth = str(basepath) + "/elevation/Elevation_certificates.csv"

doors_dir = str(basepath) + "/doors"

df = pd.read_csv(ground_truth)
images = list(df["ID"].values) 

image_names = os.listdir(os.getcwd()+"/inference/images")

def runDetect():

    existing_files = os.listdir(doors_dir)
    i = 0
    for image_name in image_names:
        i = i+1
        
        if(image_name != '.DS_Store' and int(image_name.split("_")[0]) in images and image_name not in set(existing_files)):
            print("here")
            subprocess.run(f"python detect.py --weights door_final.pt --img-size 640 --save-txt --source inference/images/{image_name}", shell=True)

if __name__ == '__main__':
    
    # subprocess.run("python detect.py --weights door_final.pt --img-size 640 --save-txt --source inference/images/2840_37.050832_-76.352762_0_229.92.jpg", shell=True)

    runDetect()