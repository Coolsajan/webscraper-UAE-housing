import os 
from bs4 import BeautifulSoup
import pandas as pd

#collecting all .html file scraped from selenium
links=os.listdir("Data")

full_data_list=[]
count=0

#looping around all the .html
for link in links:
    with open(f"Data/{link}",encoding="utf-8") as f:  # opening and reading the data
        data_link=f.read()
    
        soup=BeautifulSoup(data_link,"html.parser")
        try:
            price=soup.find("p",class_="MuiTypography-root MuiTypography-body1 mui-style-1qcnehy").text
        except:
            print(f"Failed to get the price for the {link}")
            pass
        
        try:
            locate_space=soup.find("div",class_="mui-style-1u8h5t9")
            
            bedroom = locate_space.find_all("p",class_="MuiTypography-root MuiTypography-body1 mui-style-vhs5k")[0].text
            bathroom= locate_space.find_all("p",class_="MuiTypography-root MuiTypography-body1 mui-style-vhs5k")[1].text
            area = locate_space.find_all("p",class_="MuiTypography-root MuiTypography-body1 mui-style-vhs5k")[2].text
        except :
            print(f"Failed to get the space locater for the {link}")
            pass
            
        try:
            locate_address = soup.find("div",class_="mui-style-13xiveh")
        
            address = locate_address.find("p",class_="MuiTypography-root MuiTypography-body1 mui-style-uq2ei").text.split(',')[-3]
            city = locate_address.find("p",class_="MuiTypography-root MuiTypography-body1 mui-style-uq2ei").text.split(',')[-2]
            country_name = locate_address.find("p",class_="MuiTypography-root MuiTypography-body1 mui-style-uq2ei").text.split(',')[-1]

            if len(locate_address.text.split(',')) == 4:
                project_name = locate_address.find("p",class_="MuiTypography-root MuiTypography-body1 mui-style-uq2ei").text.split(',')[0]
            
            locater=soup.find("div",class_="mui-style-p58oka")
            for find in locater:
                header=find.find("div",class_="MuiTypography-root MuiTypography-body1 mui-style-3ehvk").text
                if header == "Type":
                    property_type = find.find("div",class_="MuiTypography-root MuiTypography-subtitle1 mui-style-1keq46t").text
                elif header == "Purpose":
                    purpose = find.find("div",class_="MuiTypography-root MuiTypography-subtitle1 mui-style-1keq46t").text
                elif header == "Furnishing" :
                    furnishing_status = find.find("div",class_="MuiTypography-root MuiTypography-subtitle1 mui-style-1keq46t").text
                elif header == "Completion Status" :
                    completion_status = find.find("div",class_="MuiTypography-root MuiTypography-subtitle1 mui-style-1keq46t").text
                elif header == "Handover" :
                    handover = find.find("div",class_="MuiTypography-root MuiTypography-subtitle1 mui-style-1keq46t").text
                elif header == "Project Name" :
                    project_name = find.find("div",class_="MuiTypography-root MuiTypography-subtitle1 mui-style-1keq46t").text
        except :
            print(f"Failed to get the detial locater for the {link}")
            pass
        data={"price":price,"bedroom":bedroom ,"bathroom":bathroom,"area(sqft)":area ,"country":country_name,"city":city,"address":address,
             "property_type":property_type,"purpose":purpose,"furnishing":furnishing_status,"completion_status":completion_status,"handover":handover,
             "project_name":project_name}
        
        full_data_list.append(data)
        count+=1
        print(f"Collected Data Count : {count}")

os.makedirs("Dataset",exist_ok=True)

dataset=pd.DataFrame(full_data_list)
output_path=os.path.join("Dataset","uae-housing_dataset.csv")
dataset.to_csv(output_path,index=False)


print(f"Data collection completed and .csv saved as {output_path}")