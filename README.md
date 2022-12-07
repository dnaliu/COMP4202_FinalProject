# COMP4202_Final_Project
Comp 4202 Final Project - Lowest Floor elevation

Note: The project is currently set up to run on 5 sample data

**Project dependancies setup**:
1. Ensure proper python version: 3.7+
2. And the most updated version of pip.
3. Run: pip install requirements.txt
4. Go the the drive: https://drive.google.com/drive/folders/1DdgDFNHDaJ0TPHCFzcYnLigQ-u3aNamD?usp=sharing
5. Download the weight file found in the weight_file folder named and put into the base directory of the project: door_final.pt

**RUN ON SAMPLE DATA*
1. Run the following command to detect doors at /inference/images folder:
  - python runbatch.py
  The image of the door, and its corresponding text file will be stored at /doors

2. Run the following command to determine the lowest door elevation:
  - python evaluate.py
  The result will be stored in measurement.csv file at /doors. All images with no doors will be stored in undetected.txt in the base directory.


**HOW TO RUN THE PROJECT ON THE ENTIRE DATASET**

Go to the following Google Drive link to extract the files needed to run the application: 
https://drive.google.com/drive/folders/1DdgDFNHDaJ0TPHCFzcYnLigQ-u3aNamD?usp=sharing

**OPTION 1. To run the application end to end for the entire dataset**:
  - copy the following folder with folder name from the drive into the base directory of the project and replace the existing folder: inference
  - copy the following folder with folder name from the drive into the base directory of the project and replace the existing folder: paper_doors

1. Run the following command to detect doors at /inference/images folder:
  - python runbatch.py
  The image of the door, and its corresponding text file will be stored at /doors

2. Run the following command to determine the lowest door elevation:
  - python evaluate.py
  The result will be stored in measurement.csv file at /doors. All images with no doors will be stored in undetected.txt in the base directory.


**OPTION 2. To run only evaluate on larger sample dataset to see measurements**:
  -  copy the following folder with folder name from the drive into the base directory of the project and replace the existing folder: doors
  -  copy the following folder with folder name from the drive into the base directory of the project and replace the existing folder: paper_doors

  1. Run the following command to determine the lowest door elevation:
  - python evaluate.py
  The result will be stored in measurement.csv file at /doors. All images with no doors will be stored in undetected.txt in the base directory.

  

**General instructions**: 

1. Run the following command to detect doors at /inference/images folder:
  - python runbatch.py
  
The image of the door, and its corresponding text file will be stored at /doors

2. Run the following command to determine the lowest door elevation:
  - python evaluate.py

The result will be stored in measurement.csv file at /doors. All images with no doors will be stored in undetected.txt in the base directory.
