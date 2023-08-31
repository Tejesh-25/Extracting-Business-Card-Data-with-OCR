import streamlit as st
from PIL import Image
import easyocr as ocr
import mysql.connector
import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
connect=mysql.connector.connect(
                host="localhost",
                user="root",
                password="Guvi12345",
                auth_plugin='mysql_native_password',
                database="bizcards")
mycursor=connect.cursor()
create_table_query = """CREATE TABLE IF NOT EXISTS business_Cards (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(255),
                    Designation VARCHAR(255),
                    Contact_Number VARCHAR(20),
                    Alternative_Number VARCHAR(20),
                    Email VARCHAR(255),
                    Website VARCHAR(255),
                    Street VARCHAR(255),
                    City VARCHAR(255),
                    State VARCHAR(255),
                    Pincode VARCHAR(10),
                    Company_name VARCHAR(255)
                    )"""
mycursor.execute(create_table_query)
connect.commit()
st.set_page_config(page_title="Business Cards Exatracting!!!",page_icon=":card_file_box:",layout="wide")
st.title(":card_file_box: :blue[Extracting Business Cards using Easyocr]")
image=st.file_uploader(":file_folder: :blue[Upload an image]",type=(["CSV","JPG","JPEG","PNG"]))
menu=["Add","View","Update","Delete"]
choice=st.sidebar.selectbox("Select an option",menu)
def load_model():
    reader=ocr.Reader(['en'])
    result=reader.readtext(np.array(input_image))
    details=[]
    for i in range(len(result)):
        details.append(result[i][1])
    id=[]
    name=[]
    designation = []
    contact =[]
    email=[]
    website=[]
    street =[]
    city =[]
    state =[]
    pincode=[]
    company =[]
    for i in range(len(details)):
        match1 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)',details[i])
        match2 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+)', details[i])
        match3 = re.findall('^[E].+[a-z]',details[i])
        match4 = re.findall('([A-Za-z]+) ([0-9]+)',details[i])
        match5 = re.findall('([0-9]+ [a-zA-z]+)',details[i])
        match6 = re.findall('.com$' , details[i])
        match7 = re.findall('([0-9]+)',details[i])
        if details[i]==details[0]:
            name.append(details[i])
        elif details[i]==details[1]:
            designation.append(details[i])
        elif "-" in details[i]:
            contact.append(details[i])
        elif "@" in details[i]:
            email.append(details[i])
        elif "www"in details[i].lower() or"www."in details[i].lower():
            website.append(details[i])
        elif "WWW" in details[i]:
            website.append(details[i]+"."+details[i+1])
        elif match6:
            pass
        elif match1:
            street.append(match1[0][0])
            city.append(match1[0][1])
            state.append(match1[0][2])
        elif match2:
            street.append(match2[0][0])
            city.append(match2[0][1])
        elif match3:
            city.append(match3[0])
        elif match4:
            state.append(match4[0][0])
            pincode.append(match4[0][1])
        elif match5:
            street.append(match5[0]+'St.,')
        elif match7:
            pincode.append(match7[0])
        else:
            company.append(details[i])
    if len(company)>1:
        comp =company[0]+" "+company[1]
        print(comp)
    else:
        comp = company[0]
    if len(contact) >1:
        contact_number = contact[0]
        alternative_number = contact[1]
    else:
        contact_number = contact[0]
        alternative_number = 0
    info={"Name":name[0] if name else "",
          "Designation":designation[0] if designation else "",
          "Contact_Number":contact[0] if contact else " ",
          "Alternative_Number":alternative_number if alternative_number else "0",
          "Email":email[0] if email else "",
          "Website": website[0] if website else "",
          "Street": street[0] if street else "",
          "City": city[0] if city else "",
          "State": state[0] if state else "",  
          "Pincode": pincode[0] if pincode else "",
          "Company_Name": comp if company else ""
            }
    return info
if choice=="Add":
    if image is not None:
        input_image=Image.open(image)
        st.image(input_image)
        if st.button('Extract Information'):
            with st.spinner(":smiling_imp: AI is at work"):
                information=load_model()
                st.write(information)
                st.balloons()
        if st.button("Store data in MYSQL"):
             with st.spinner(":smiling_imp: AI is at work"):
                information=load_model()
                df=pd.DataFrame.from_dict(information,orient='index').T
                connect=mysql.connector.connect(
                host="localhost",
                user="root",
                password="Guvi12345",
                auth_plugin='mysql_native_password',
                database="bizcards")
                mycursor=connect.cursor()
                mycursor.execute('create database if not exists bizcards')
                engine=create_engine('mysql+mysqlconnector://root:Guvi12345@localhost/bizcards',echo=False)
                df.to_sql('business_cards',engine,if_exists='append',index=False)
                st.balloons()
                st.success("sucessfuly stored in Mysql")
    else:
        print("upload an image")
elif choice == "View":
    mycursor.execute("SELECT * FROM business_Cards")
    result = mycursor.fetchall()
    df1 = pd.DataFrame(result, columns=["Id","Name", "Designation", "Contact_Number", "Alternative_number", "Email", "Website","Street", "City", "State", "Pincode", "Company_Name"])
    st.dataframe(df1)
elif choice == "Update":
    mycursor.execute("SELECT id, name FROM business_Cards")
    result = mycursor.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[1]] = row[0]
    selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()))
    mycursor.execute("SELECT * FROM business_Cards WHERE name=%s", (selected_card_name,))
    result = mycursor.fetchone()
    st.write("Name:", result[1])
    st.write("Designation:", result[2])
    st.write("Contact_Number:", result[3])
    st.write("Alternative_Number:", result[4])
    st.write("Email:", result[5])
    st.write("Website:", result[6])
    st.write("Street:", result[7])
    st.write("City:", result[8])
    st.write("State:",result[9])
    st.write("Pincode:",result[10])
    st.write("Company_Name",result[11])
    name = st.text_input("Name", result[1])
    designation = st.text_input("Designation", result[2])
    contact_number = st.text_input("Contact_Number", result[3])
    alternative_number = st.text_input("Alternative_Number", result[4])
    email= st.text_input("Email", result[5])
    website = st.text_input("Website", result[6])
    street = st.text_input("Street", result[7])
    city=st.text_input("City",result[8])
    state=st.text_input("State",result[9])
    pincode=st.text_input("Pincode",result[10])
    company_name = st.text_input("Company_Name:", result[11])
    if st.button("Update Business Card"):
        mycursor.execute("UPDATE business_Cards SET name=%s, designation=%s, contact_number=%s, alternative_number=%s, email=%s, website=%s, street=%s, city=%s, state=%s, pincode=%s, company_name=%s WHERE name=%s", 
                             (name, designation, contact_number, alternative_number, email, website, street, city, state, pincode, company_name, selected_card_name))
        connect.commit()
        st.success("Business card information updated in database.")
elif choice == 'Delete':
    mycursor.execute("SELECT id, name FROM business_Cards")
    result = mycursor.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[0]] = row[1]
    selected_card_id = st.selectbox("Select a business card to delete", list(business_cards.keys()), format_func=lambda x: business_cards[x])
    mycursor.execute("SELECT name FROM business_Cards WHERE id=%s", (selected_card_id,))
    result = mycursor.fetchone()
    selected_card_name = result[0]
    st.write("Name:", selected_card_name)
    if st.button("Delete Business Card"):
        mycursor.execute("DELETE FROM business_Cards WHERE name=%s", (selected_card_name,))
        connect.commit()
        st.success("Business card information deleted from database.")
