from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import pyodbc as po

import google.generativeai as genai
## Configure Genai Key
# generate api key from https://aistudio.google.com/app/u/3/apikey use leodevelopergcp google account
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


## Fucntion To retrieve query from the database

def read_sql_query(query):

    # Connection variables
    server = st.session_state["Host"]
    database = st.session_state["Database"]
    username = st.session_state["User"]
    password = st.session_state["Password"]
    
    # Connection string
    cnxn = po.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' +
            server+';DATABASE='+database+';UID='+username+';PWD=' + password+';TrustServerCertificate=yes;')
    
    if cnxn:
        st.success(f"Connected to the database {database} successfully!")
        cursor = cnxn.cursor()
        # Fetch data into a cursor
        cursor.execute(query)
        # iterate the cursor
        rows = cursor.fetchall()
        # Close the cursor and delete it
        cursor.close()
        del cursor
        # Close the database connection
        cnxn.close()
        return rows
    else:
        st.error("Failed to connect to the database.")

    

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database CustomerOrder has the table Customers and has the following columns - CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Email NVARCHAR(100),
    PhoneNumber NVARCHAR(15) and another table Orders nad has following columns - OrderID INT PRIMARY KEY IDENTITY(1,1),
    CustomerID INT,
    OrderDate DATE,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM Customers ;
    \nExample 2 - Tell me all the Orders for specific customer?, 
    the SQL command will be something like this SELECT * FROM Orders
    where CustomerID=1; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Google Generative AI Gemini App to Retrieve Data from SQL Server directly")



question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit and question:
    with st.spinner("Connecting to database..."):
        response=get_gemini_response(question,prompt)
        print(response)
        response=read_sql_query(response)
        st.subheader("The Response is")
        for row in response:
            print(row)
            st.write(row)


#side bar
with st.sidebar:
    st.subheader("Database Settings")
    st.write("This is a simple chat application using SQL Server. Connect to the database and start chatting.")
    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="1433", key="Port")
    st.text_input("User", value="sa", key="User")
    st.text_input("Password", type="password", value="admin", key="Password")
    st.text_input("Database", value="TestDatabase", key="Database")
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            # Create a connection to the database
            conn = po.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' +
            st.session_state["Host"]+';DATABASE='+st.session_state["Database"]+';UID='+st.session_state["User"]+';PWD=' + st.session_state["Password"]+';TrustServerCertificate=yes;')
            if conn:
                st.success("Connected to the database successfully!")

                # Close the connection
                conn.close()
            else:
                st.error("Failed to connect to the database.")