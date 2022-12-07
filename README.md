# COMP4202_Final_Project
Comp 4202 Final Project - Lowest Floor elevation

Instructions:

Ensure proper python version: 3.7+
And the most updated version of pip.

Run:
  - pip install requirements.txt

Run the following command to detect doors at /inference/images folder:
  - python runbatch.py
  
The image of the door, and its corresponding text file will be stored at /doors

Run the following command to determine the lowest door elevation:
  - python evaluate.py

The result will be stored in measurement.csv file at /doors. All images with no doors will be stored in undetected.txt in the base directory.
