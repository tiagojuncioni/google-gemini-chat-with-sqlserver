import pyodbc as po
 
# Connection variables
server = ''
database = ''
username = ''
password = ''
 
# Connection string
cnxn = po.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' +
        server+';DATABASE='+database+';UID='+username+';PWD=' + password+';TrustServerCertificate=yes;')
cursor = cnxn.cursor()
 
# Fetch data into a cursor
cursor.execute("SELECT [Id],[FirstName],[LastName],[Address] FROM [TestDatabase].[dbo].[Personal] \
     ORDER BY Id DESC;")
 
# iterate the cursor
row = cursor.fetchone()
while row:
    # Print the row
    print(str(row[0]) + ", " + str(row[1] or '') + ", " + str(row[2] or '') + ", " + str(row[3] or ''))
    row = cursor.fetchone()
 
# Close the cursor and delete it
cursor.close()
del cursor
 
# Close the database connection
cnxn.close()