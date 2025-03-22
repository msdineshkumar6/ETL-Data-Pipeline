'''
Authour = M.S.Dinesh Kumar
Purpouse= get the data from the files stored in the repositry transform the data and combine to a single file
'''

# Import the required libraries
import pandas as pd  
import glob 
import logging
import os
import json
import xml.etree.ElementTree as ET

# specifify the path of the sorce file
folder_path='C:/Users/HP/Desktop/Guvi/SourceFile'

# initialize log process
logging.basicConfig(
    filename='C:/Users/HP/Desktop/Guvi/Output data/log_file.txt',  
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting the process of preparing the list of files based on format")
# get all the  files from the folder and store them in list based on format
csv_files=glob.glob(folder_path+'/*.csv')
json_files=glob.glob(os.path.join(folder_path+'/*.json'))
xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
logging.info(" process of preparing the list of files based on format completed")

#create an empty array to hold all the data frmes
df_list=[]

# create an empty list to store the data from each xml file
combined_data = []

logging.info("Starting the process to extract data from csv files")
# Combine the data in csv files to data frame and store the data frames in list
for file in csv_files:
    df=pd.read_csv(file)
    df_list.append(df)

logging.info("Data extraction  process for csv files completed")
logging.info("Starting the process to extract data from json files")

# combine the data in json files to data frame and store the data frame to the list
for file in json_files:

    #open the json file to read the data
    with  open(file,'r')as f:
        lines=f.readlines()
    
    #Declare an empty list to store json objects
    data = []

    # combine individual json objects into an list of json objects
    for line in lines:
        
        # try catch block to ignore empty json objects
        try:
            json_object=json.loads(line)
            data.append(json_object)
        except json.JSONDecodeError:
            continue
    
    # convert the list of json objects to a data frame and append them to list of dataframe
    df=pd.DataFrame(data)
    df_list.append(df)


logging.info("Data extraction  process for json files completed")
logging.info("Starting the process to extract data from xml files")

# combine the data in xml files to data frame and store the data frame to the list
for file in xml_files:
    #get the file path
    file_path = os.path.join(folder_path, file)

    # get the root of the xml tree
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Extract data from each  element and append to combined_data
    for person in root.findall('person'):
        # get the individual data and store it in variables to append the combined data
        name = person.find('name').text
        height = person.find('height').text
        weight = person.find('weight').text         
        
        # Append the extracted data as a dictionary to the combined data list
        combined_data.append({
            'name': name,
            'height': height,
            'weight':weight
        })
    
# convert the dictioneries in combined_data list to a data frame
df = pd.DataFrame(combined_data)

# Appentd the data frame to data frame array
df_list.append(df)

logging.info("Data extraction  process for xml files completed")

# combine the data frames in list to a single data frame
combined_df=pd.concat(df_list,ignore_index=True)

logging.info("Combined the data into a single data frame")

# Remove duplicated in data frame
df_no_duplicates = combined_df.drop_duplicates()
logging.info("Removed the duplicates from the data frame")

# function to convert length from inch to meter
def convert_inches_to_meter(height): return height*0.0254

# function to convert weight from kilogram to pound
def convert_kilogram_to_pound(weight) : return weight*2.20462

logging.info("starting the process of data transformation")

# converting the type of the height and weght to numeric 
df_no_duplicates['height'] = pd.to_numeric(df_no_duplicates['height'], errors='coerce')
df_no_duplicates['weight'] = pd.to_numeric(df_no_duplicates['weight'], errors='coerce')

df_no_duplicates['height']=df_no_duplicates['height'].apply(convert_inches_to_meter)
df_no_duplicates['weight']=df_no_duplicates['weight'].apply(convert_kilogram_to_pound)

logging.info("data transformation process completed")

df.to_csv('C:/Users/HP/Desktop/Guvi/Output data/output.csv', index=False)