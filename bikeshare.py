import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Args:
        None.

    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print(" ")
    print('Hi! This program is used for exploring some US bikeshare data!')
   
    city = '' #Create an empty variable for storing the user choice
    #This loop shall be run to be ensure that the user has entered the correct input and if not the loop will be repeated
    while city not in CITY_DATA.keys():
        print("\nWelcome, Please choose the city: (Chicago, New York City or Washington)")
        city = input().lower() #Take the user choice and convert it to a lower case

        if city not in CITY_DATA.keys():
            print("\nPlease check your input it is not the correct City!!!")
     

    print(f"\nThe selected city is {city.title()}.")

    #Make a dictionary for storing all the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, between January to June, or select all months by entering all:")
        month = input().lower() #Take the user choice and convert it to a lower case

        if month not in MONTH_DATA.keys(): #Check if the entered month is correct
            print("\nInvalid input. Please try again...")
            print("\nRestarting...")

    print(f"\nThe selected month is {month.title()}.")

    #Make a list for storing all the days including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice, or select all days by entering all:")
        day = input().lower() #Take the user choice and convert it to a lower case

        if day not in DAY_LIST: #Check if the entered day is correct
            print("\nInvalid input. Please try again...")
            print("\nRestarting...")

    print(f"\nThe selected day is {day.title()}.")
    print(f"\nYour choice shall display the data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*80)
 
    return city, month, day #Returning the user choice city, month and day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    #Load data for city
    print("\nThe Data is Loading...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the format of the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract the month and the day of the week from Start Time for creating new columns
    df['month'] = df['Start Time'].dt.month # Get the month and make a column for it
    df['day_of_week'] = df['Start Time'].dt.day_name() # Get the day and make a column for it

    #Check by the month if it is applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 # Get the index of the month

        #create a new dataframe for the selected month
        df = df[df['month'] == month]

    #Check by day of week if applicable
    if day != 'all':
        #create a new dataframe for the selected day
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Finding the most popular month
    most_popular_month = df['month'].mode()[0]

    print(f"The Most Popular Month (1 = January,...,6 = June) is: {most_popular_month}")

    #Finding the most popular day
    most_popular_day = df['day_of_week'].mode()[0]

    print(f"\nThe Most Popular Day is: {most_popular_day}")

    #Get the hour from the Start Time column for creating an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Finding the most popular hour
    most_popular_hour = df['hour'].mode()[0]

    print(f"\nThe Most Popular Start Hour is: {most_popular_hour}")

    # Calculating the time of the execution
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Finding the most common start station
    most_common_start_station = df['Start Station'].mode()[0]

    print(f"The most common start station is: {most_common_start_station}")

    #Finding the most common end station
    most_common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most common end station is: {most_common_end_station}")

    #Combine two columns in the df and assign the result to a new column with name 'Start To End'
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')

    #Finding the most common combination of start and end station
    most_common_start_end = df['Start To End'].mode()[0]

    print(f"\nThe most common combination (Start and End station) of trips are from: {most_common_start_end}.")

    # Calculating the time of the execution
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Calculating the total trip duration using sum method
    sum_of_total_duration = df['Trip Duration'].sum()
    #Finding the duration in minutes and seconds
    minute, second = divmod(sum_of_total_duration, 60)
    #Finding the duration in hour and in minutes
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    #Calculating the average trip duration using mean method
    mean_average_duration = round(df['Trip Duration'].mean())
    #Finding the average duration in minutes and in seconds
    mins, sec = divmod(mean_average_duration, 60)
    #Check if the mins exceed 60 to prints the time in hours, mins, sec
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    # Calculating the time of the execution
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Counting the total users using value_counts method
    user_type = df['User Type'].value_counts()

    print(f"Counting of each user type:\n\n{user_type}")

    #Displaying the numebr of users according to the Gender.
    try:
        gender = df['Gender'].value_counts()
        print(f"\nCounting of each gender:\n\n{gender}")
    except:
        print("\nNo 'Gender' column in this file.")

 
    #Finding the earliest birth year, most recent birth year and the most common year of birth
    try:
        earliest_val = int(df['Birth Year'].min())
        recent_val = int(df['Birth Year'].max())
        common_year_val = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth is: {earliest_val}")
        print(f"\nThe most recent year of birth is: {recent_val}")
        print(f"\nThe most common year of birth is: {common_year_val}")
    except:
        print("No any birth year details in this file!!!")

    # Calculating the time of the execution

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def data_log(df):
    """
    Displaying 5 rows of the data from the csv file based on the selected city.

    """
    User_RESPONSE_LIST = ['yes', 'no'] # The expected user answers
    raw_data = '' # User answer that shall be yes or no
    
    counter = 0
    while raw_data not in User_RESPONSE_LIST:
        print("\nDo you want to view the raw data (yes or no)?")
        raw_data = input().lower() # Convert the user answer to a lower case
        if raw_data == "yes": # Check if the user answer is yes
            print(df.head())  # Display the first fifth raw of the selected dataset
        elif raw_data not in User_RESPONSE_LIST: # Test if the user entered a wrong choice
            print("\nYour input is wrong, please check your input.")
            print("\nRestarting...\n")

    #More while loop for asking the user if more five rows of data need to be displayed
    while raw_data == 'yes':
        print("Do you want more raw data to be displayed (yes or no)?")
        counter += 5
        raw_data = input().lower() # Convert the user answer to a lower case
        if raw_data == "yes": # Check if the user answer is yes
             print(df[counter:counter+5]) # Display more five rows of the dataset data
        elif raw_data != "yes": # If the answer is no, break the loop.
             break

    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        data_log(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nDo you want to restart? (yes or no).\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
