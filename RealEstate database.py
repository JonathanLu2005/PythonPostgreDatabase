import psycopg2

#connect to db
print("please enter your password for your PostgreSQL database on line 8 :) ")

try:
    cur.execute("CREATE database RealEstate")
    conn = psycopg2.connect(dbname="RealEstate", user="postgres", password="", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    conn.autocommit = True

except:
    pass


cur.execute("""CREATE TABLE IF NOT EXISTS Property(
PropertyID SERIAL PRIMARY KEY NOT NULL,
CountyName VARCHAR(100) NOT NULL,
NoOfRooms INT NOT NULL,
NoOfKitchens INT NOT NULL,
NoOfBathrooms INT NOT NULL,
Rating FLOAT NOT NULL,
Price FLOAT NOT NULL);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Customer(
CustomerID SERIAL PRIMARY KEY NOT NULL,
FirstName VARCHAR(40) NOT NULL,
Surname VARCHAR(40) NOT NULL,
CountyLivesIn VARCHAR(100) NOT NULL);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Viewing(
ViewingID SERIAL PRIMARY KEY,
ViewingDay INT,
ViewingMonth INT,
ViewingYear INT,
ViewingTime INT,
PropertyID INT NOT NULL REFERENCES Property(PropertyID),
CustomerID INT NOT NULL REFERENCES Customer(CustomerID));""")


def Options():
    Correct = False

    while Correct == False:
        Choice = int(input("""
Please choose one of the options

1 - Add property
2 - Add customer
3 - View properties
4 - Create an appointment/viewing
5 - Statistics
"""))


        if Choice == 1:
            Properties()

        elif Choice == 2:
            Customers()

        elif Choice == 3:
            Viewings()

        elif Choice == 4:
            Bookings()

        elif Choice == 5:
            Statistics()

        else:
            print("Please choose an viable option")

def Properties():
    print("Please fill in these details to add an property to the system")
    County = str(input("What county is this property in?"))
    Rooms = int(input("How many rooms are there in this property?"))
    Kitchens = int(input("How many kitchens are there in this property?"))
    Bathrooms = int(input("How many bathrooms are there in this property?"))
    Rating = float(input("From a scale of 0 to 10, what is the rating of this property?"))
    Price = float(input("What is the listed price of this property?"))

    cur.execute("""INSERT INTO Property (CountyName, NoOfRooms, NoOfKitchens, NoOfBathrooms, Rating, Price) VALUES
(%s,%s,%s,%s,%s,%s);""", [County, Rooms, Kitchens, Bathrooms, Rating, Price])
    conn.commit()
    Options()
    

def Customers():
    print("Please fill in these details to add an customer to the system")
    FirstName = str(input("Please enter your first name?"))
    Surname = str(input("Please enter your surname?"))
    County = str(input("What county do you live in?"))

    cur.execute("""INSERT INTO Customer (FirstName, Surname, CountyLivesIn) VALUES
(%s, %s, %s);""", [FirstName, Surname, County])
    conn.commit()
    Options()

def Viewings():
    Filters = int(input("""
Please choose one of these options to choose from on how you would like to filter down the list of properties

1 - Room Count
2 - Kitchen Count
3 - Bathroom Count
"""))

    MinPrice = int(input("What is the minimum price you're looking for?"))
    MaxPrice = int(input("What is the maximum price you're looking for?"))

    MinRating = float(input("What is the minimum rating you're looking for?"))
    MaxRating = float(input("What is the maximum rating you're looking for?"))

    Limit = int(input("How many properties would you like to see available?"))

    CustomerID = int(input("What is your customer ID?"))

    cur.execute("""
    SELECT CountyLivesIn FROM Customer WHERE CustomerID = %s""", [CustomerID])
    CountyName = ((cur.fetchall()[0])[0])
    print(CountyName)
    

    if Filters == 1:
        RoomCount = int(input("How many rooms would you like it has?"))
        cur.execute("""
    SELECT * FROM Property
    WHERE CountyName = %s
    AND NoOfRooms = %s
    AND Price BETWEEN %s AND %s
    AND Rating BETWEEN %s AND %s
    ORDER BY Price DESC
    LIMIT %s;""", [CountyName, RoomCount, MinPrice, MaxPrice, MinRating, MaxRating, Limit])

        for row in cur.fetchall():
            print(row)

    elif Filters == 2:
        KitchenCount = int(input("How many kitchens would you like it has?"))
        cur.execute("""
    SELECT * FROM Property
    WHERE CountyName = %s
    AND NoOfKitchens = %s
    AND Price BETWEEN %s AND %s
    AND Rating BETWEEN %s AND %s
    ORDER BY Price DESC
    LIMIT %s;""", [CountyName, KitchenCount, MinPrice, MaxPrice, MinRating, MaxRating, Limit])

        for row in cur.fetchall():
            print(row)


    elif Filters == 3:
        BathroomCount = int(input("How many bathrooms would you like it has?"))
        cur.execute("""
    SELECT * FROM Property
    WHERE CountyName = %s
    AND NoOfBathrooms = %s
    AND Price BETWEEN %s AND %s
    AND Rating BETWEEN %s AND %s
    ORDER BY Price DESC
    LIMIT %s;""", [CountyName, BathroomCount, MinPrice, MaxPrice, MinRating, MaxRating, Limit])

        for row in cur.fetchall():
            print(row)

    else:
        print("Please choose an suitable filter")
        Viewings()

    Options()
        
    

def Bookings():
    ViewingDay = int(input("Please choose what day (number) you would like to view this property?"))
    ViewingMonth = int(input("Please choose what month (number) you would like to view this property?"))
    ViewingYear = int(input("Please choose what year (number) you would like to view this property?"))
    ViewingTime = int(input("Please choose what time (hours) you would like to view this property?"))
    PropertyID = int(input("What property ID would you like to view?"))
    CustomerID = int(input("What is your customer ID?"))

    cur.execute("""INSERT INTO Viewing (ViewingDay, ViewingMonth, ViewingYear, ViewingTime, PropertyID, CustomerID)
VALUES (%s, %s, %s, %s, %s, %s);""", [ViewingDay, ViewingMonth, ViewingYear, ViewingTime, PropertyID, CustomerID])
    conn.commit()
    
    print("This is your confirm viewing details")
    cur.execute("""
SELECT ViewingDay, ViewingMonth, ViewingYear FROM Viewing, Property, Customer
WHERE Viewing.PropertyID = Property.PropertyID
AND Viewing.CustomerID = Customer.CustomerID;""")
    print(cur.fetchall())
    Options()

def Statistics():
    cur.execute("SELECT MAX(Price) FROM Property;")
    print("Max house price is " + str(round(((cur.fetchall()[0])[0]), 2)))

    cur.execute("SELECT MIN(Price) FROM Property;")
    print("Min house price is " + str(round(((cur.fetchall()[0])[0]), 2)))

    cur.execute("Select AVG(Price) FROM Property;")
    print("Average house price is " + str(round(((cur.fetchall()[0])[0]), 2)))

    cur.execute("SELECT DISTINCT CountyName FROM Property;")
    print("These are all the different counties that have property available")
    for row in cur.fetchall():
        print(row[0])

    Options()

Options()
