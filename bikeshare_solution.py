import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_month():
    """
This Function is used to get the month
INPUT: a user input of a month from january to june
OUTPUT:(str) mon- The user's input of the month after handling any possible errors 

    """
    months=['all','january','february','march','april','may','june']
    while True:
        mon=input("Please choose a specific month from [january to june] or type all to give data of all months ").lower()
        if mon not in months:
            print("Please Re-check the entered month")
            
        else:
            print("You Choosed {}".format(mon))
            break
    return mon

def get_day():
    '''
This Function is used to get the day
INPUT: a user input of a day from the week
OUTPUT: (str) day - The user's input of the day after handling any possible errors 
    '''
    days= ['all','saturday','sunday','monday','tuesday','wednesday','thursday','friday']
    while True:
        day=input("Please choose a specific day of the week or type all to give data of all days ").lower()
        if day not in days:
            print("Please Re-check the entered day")
        else:
            print("You Choosed {}".format(day))
            break
    return day
            
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) mon - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities=['chicago','new york city','washington']
    # asking for the user's input for the city
    while True :
        city=input("Please choose a city from the following (Chicago, New York City, Washington) ").lower()
        if city not in cities:
            print("Please Re-check the entered city")
        else:
            print("You Choosed {}".format(city))
            break
    # getting user's input for the filteration options
    while True :
        filters=["month","day","both"]
        filter=input("Do you want to filter by Month, Day, both? ").lower()
        if filter not in filters:
            print("Please Re-check the entered filteration option")
            continue
        elif filter=="month":
            mon= get_month()
            day= "all"
            break
        elif filter=="day":
            day= get_day()
            mon= "all"
            break
        elif filter=="both":
            mon= get_month()
            day= get_day()
            break  
    print('-'*40)
    return city, mon, day


def load_data(city, mon, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] =df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if mon != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        mon =months.index(mon)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']== mon]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df   

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    cmonth=df['month'].mode()[0]
    print("The most common month for travels is {}".format(cmonth))
    # display the most common day of week
    cday=df['day_of_week'].mode()[0]
    print("The most common day of the week for travels is {}".format(cday))
    # display the most common start hour
    chour=df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour of travels is {}".format(chour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    cstart=df['Start Station'].mode()[0]
    print("The most commonly used start station is ( {} )".format(cstart))
    # display most commonly used end station
    cend=df['End Station'].mode()[0]
    print("The most commonly used end station is ( {} )".format(cend))

    # display most frequent combination of start station and end station trip
    #ccomb= (df['Start Station'] + df['End Station']).mode()[0]
    ccomb=df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print("The most common trip is between ( {} )".format(ccomb))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tttime=df['Trip Duration'].sum()
    tsplitted = time.strftime("%H:%M:%S", time.gmtime(tttime))
    print("The total travel time is {} ".format(tsplitted))
    # display mean travel time
    mttime=df['Trip Duration'].mean()
    msplitted = time.strftime("%H:%M:%S", time.gmtime(mttime))
    print("The average travel time is {} ".format(msplitted))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ctype=df['User Type'].value_counts()
    print("The Count of each user type is : \n",ctype)
    # Display counts of gender
    if "Gender" in df:
        cgender=df['Gender'].value_counts()
        print("The Count of each gender is : \n",cgender)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        erl=int(df['Birth Year'].min())
        rec=int(df['Birth Year'].max())
        cyear=int(df['Birth Year'].mode()[0])
        print("The oldest user is born in : {}\nThe youngest user is born in : {}\nMost users are born in: {} ".format(erl,rec,cyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def show_data(df):
    '''
This Function is used to show raw samples of data
INPUT: a user input of a yes or no based on what they want
OUTPUT:5 rows of the raw data 
    '''
    n=0
    while True:        
        show=input("Do you want to see a sample of the raw data? (yes/no) ").lower()
        if show == 'no':
            break
        elif show == 'yes':
            print(df.iloc[n : n+5])
            n+=5
        else:
            print("Please only enter yes or no")
def main():
    while True:
        city, mon, day = get_filters()
        df = load_data(city, mon, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
   main()
