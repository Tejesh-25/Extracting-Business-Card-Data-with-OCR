# Extracting-Business-Card-Data-with-OCR
# what is EasyOCR
EasyOCR, as the name suggests, is a Python package that allows computer vision developers to effortlessly perform Optical Character Recognition. A varied dataset of text images is fundamental for getting started with EasyOCR.Easy OCR is a font-dependent printed character reader based on a template matching algorithm. It has been designed to read any kind of short text (part numbers, serial numbers, expiry dates, manufacturing dates, lot codes, …) printed on labels or directly on parts.

# Project Overview
BizCardX is a user-friendly tool designed to extract and organize information from business cards. The tool employs OCR technology for recognizing text on business cards and then employs regular expressions to classify and organize the data before storing it in a SQL database. The extracted information is presented to users through a user interface created using Streamlit, making the entire process of uploading business card images, extracting data, and managing it intuitive. Users can also easily manage the stored data in the database by reading, updating, and deleting it according to their needs.

# Libraries/Modules used for the project!
EasyOCR-(To extract text from images)
pandas-(To make a DataFrame from scraped Data)
MYSQL- (To store and retrive the Data)
Streamlit-(To Create Graphical user Interface)

# Workflow
To get started with BizCardX Data Extraction, follow the steps below:

Install the required libraries using the pip install command. Streamlit, mysql.connector, pandas, easyocr.

pip install [Name of the library]

Execute the “filename.py” using the streamlit run command.

streamlit run filename.py

A webpage is displayed in browser, I have created the app with four sidebar options namely Add, View, Update and Delete.where user has the option to upload the respective Business Card whose information has to be extracted, stored, updated or deleted if needed.
Once user uploads a business card, the text present in the card is extracted by easyocr library.
The extracted text is sent to load_model() function(user defined- I have coded this function) for respective text classification as Name, Designation, Contact_Number,Alternative_Number, Email, Website, Street, city, state, Pincode and Company_Name using loops and some regular expression.
The classified data is displayed on screen which can be further edited by user based on requirement.
After clicking the add sidebar there will be two option one for extracting data and another one is to stored the data in the MySQL Database. (Note: Provide respective host, user, password, database name in create_database, sql_table_creation and connect_database for establishing connection.)
After that, there will be another three sidebar buttons View,Update,Delete once there is any error in data we can update the data in manually. After updating details click the update button to update details in mysql and also in sidebar there is a option called delete so, we can delete the particular card details if we want.
