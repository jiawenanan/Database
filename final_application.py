import psycopg2
import psycopg2.extras
import datetime
from datetime import datetime
import os
import sys
import termios

connection_string = "host='localhost' dbname='final' user='postgres' password='123456'"
conn = psycopg2.connect(connection_string)

def check_connectivity():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM county LIMIT 5")
    records = cursor.fetchall()
    if len(records) == 5:
        print("You have successfully connect to our db!!!")
    else:
        print("Connection to our db failed")


def top_ten_average_violent_rate_county_name (): #-- completed
    cursor = conn.cursor()
    cursor.execute("SELECT county_name FROM (SELECT county_id, AVG(violent_rate) as vr FROM vpf GROUP BY county_id ORDER BY AVG(violent_rate) DESC LIMIT 10) i LEFT JOIN county c ON i.county_id = c.county_id ORDER BY i.vr DESC")
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    print("Ten county names with the highest average historical violent rate are(from highest to lowest):")
    for county in result:
        print(county)



def top_ten_county_name_with_most_food_stores (): #-- completed
    cursor = conn.cursor()
    cursor.execute("SELECT co.county_name FROM food f LEFT JOIN address ad on f.address = ad.address LEFT JOIN county co ON ad.county_id = co.county_id GROUP BY co.county_id ORDER BY COUNT(*) DESC LIMIT 10")
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    print("Ten county names with the most numbers of food retail stores are(from highest to lowest):")
    for county in result:
        print(str(county))


def top_ten_latest_year_houseprice_county_name (): #-- completed
    cursor = conn.cursor()
    current = datetime.today()
    year_ago = current.replace(year = current.year-1)
    year_ago = year_ago.strftime('%Y-%m-%d')
    current = current.strftime('%Y-%m-%d')
    query_1 = "SELECT co.county_name FROM houseprice h LEFT JOIN county co ON h.county_id = co.county_id WHERE month_year >="
    query_2 = "AND month_year <="
    query_3 = "GROUP BY co.county_name ORDER BY AVG(h.price) DESC LIMIT 10"
    query = query_1 + "'" + year_ago + "'" + query_2 + "'" + current + "'" + query_3
    cursor.execute(query)
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    print("Ten county names with the highest average house price within the last year are(from highest to lowest):")
    for county in result:
        print(str(county))


def all_county_name (): # return a list of all county names
    cursor = conn.cursor()
    cursor.execute("SELECT county_name FROM county")
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append(record[0])
    return result


def lookup_county_all_info (user_input_county): 
    columns_list = ['county_id', 'county_name','metro','statecodefips','size_rank','municipalcodefips']
    county_list = all_county_name()
    pointer_user_input_county = user_input_county
    user_require = pointer_user_input_county.title() # make sure our application is case insensitive
    flag = False
    for x in county_list:
        if user_require == x:
            flag = True
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM county WHERE county_name = " + "'" + str(x) + "'")
            # a url for wikipedia of county from mongdb added here
            records = cursor.fetchone()
            print("Here is the information for county " + str(x))
            for tup_ele in range(0, len(records)):
                print(str(columns_list[tup_ele]) + ": " + str(records[tup_ele]))
            break
    if flag == False:
        print("Cannot find the input county :)")


def year_admission_prisoners_number (user_input_year):
    if user_input_year.isdigit() == False:
        print("Please enter a four-digit number x (2008 <= x <= 2019)")
    elif int(user_input_year) > 2019 or int(user_input_year) < 2008:
        print("Please enter the year x within the range (2008 <= x <= 2019) :)")
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prison WHERE admission_year = %s", (int(user_input_year),))
        records = cursor.fetchone()
        print("The number of prisoners admitted in year " + str(int(user_input_year)) + " is " + str(records[0]))


def user_interface_loop ():
    user_input = input("Please choose the API, 1 or 2? Type the number plz")
    if user_input == "1":
        user_input_county = input("Please enter a county name in New York State(it's case insensitive, for example, you can type albany/aLbany/alBany): ")
        lookup_county_all_info(user_input_county)
    elif user_input == "2":
        user_input_year = input("Please enter a year between 2008 and 2019 ")
        year_admission_prisoners_number(user_input_year)
    else:
        print("Please type 1 or 2")
    user_input_end_or_restart = input("If you want to quit, please enter q and press return. Otherwise, you can enter any characters and press return if you want to recall the API :)")
    if user_input_end_or_restart == "q":
        print("Thanks for exploring our application! Goodbye","\N{winking face}")
    else:
        user_interface_loop()


def press_any_key_exit(msg):
    fd = sys.stdin.fileno()
    old_ttyinfo = termios.tcgetattr(fd)
    new_ttyinfo = old_ttyinfo[:]
    new_ttyinfo[3] &= ~termios.ICANON
    new_ttyinfo[3] &= ~termios.ECHO
    sys.stdout.write(msg)
    sys.stdout.flush()
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
    os.read(fd, 7)
    termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)


if __name__ == "__main__":
    press_any_key_exit("Press any key to continue :)")



## start the interaction 

print("Hello, welcomen to our application")
print("Our application will bring some insights about New York State to you :)")
press_any_key_exit("Press any key to continue :)")
print("")
print("Our database is constructed with five different datasets on the internet with public liscenses")
press_any_key_exit("Press any key to continue :)")
print("")
print("It can be regarded as a good resource for exploring New York State and its 62 counties from following three aspects:")
print("Food","\N{winking face}")
print("Safety","\N{eyes}")
print("Living","\N{tent}")
press_any_key_exit("Press any key to continue :)")
print("")
print("We will present five insights to you")
print("The first three are outcomes that we consider to be meaningful resulted from our datasets")
print("While for the latter two, you can manually enter data to retrieve the results of the database.")
print("\N{winking face}","Let's check the connectivity at first!")
press_any_key_exit("Press any key to continue :)")
print("")
check_connectivity()
print("--------------------" + "\N{cheese wedge}" + "Let's begin" + "\N{cheese wedge}" + "--------------------")
press_any_key_exit("Press any key to continue :)")
print("")
print("Do you know which counties are the TOP 10 dangerouse", "\N{astonished face}", "in NYS based on the total number of violence from 1990 to 2018?")
press_any_key_exit("Press any key to continue :)")
print("")
top_ten_average_violent_rate_county_name ()
print("Is the answer similar to what you expected?")
press_any_key_exit("Press any key to continue :)")
print("")
print("Now let’s look at something fun", "\N{winking face}")
press_any_key_exit("Press any key to continue :)")
print("")
print("Would you like to know the Top 10 counties with the most food retail stores in NYS?")
press_any_key_exit("Press any key to continue :)")
print("")
print("The answers are:", "\N{drooling face}")
top_ten_county_name_with_most_food_stores()
press_any_key_exit("Press any key to continue :)")
print("")
print("Now it's the house price turn")
print("How about the 10 counties with the highest house price based on data for the past twelve months?")
press_any_key_exit("Press any key to continue :)")
print("")
print("\N{thought balloon}","\N{thought balloon}","\N{thought balloon}","\N{thought balloon}","\N{thought balloon}")
top_ten_latest_year_houseprice_county_name()
press_any_key_exit("Press any key to continue :)")
print("")
print("It's now your turn to make some explorations")
press_any_key_exit("Press any key to continue :)")
print("")
print("We provide you with two API which allow you to:")
print("1) Get all information about a county in NYS in our database")
print("2) Get total number of prisoners in NYS in a specific year (from 2008 to 2019)")
press_any_key_exit("Press any key to continue :)")
print("")
print("You can try any of them for several times")
print("Are you ready?", "\N{eyes}")
press_any_key_exit("Press any key to continue :)")
print("")
user_interface_loop ()
