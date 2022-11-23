import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in ['chicago','new york city','washington']:
        city = input('Input city (chicago, new york city, washington): ').lower()
    
    # get user input for month (all, january, february, ... , june)
    month = input('Input month (all, january, february, ... , june): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Input day(all, monday, tuesday, ... sunday: ').lower()

    print('-'*40)
    return city, month, day

def display_data(df):
    """Displays 5 rows  of data based on user choice."""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data.lower() == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc = start_loc + 5
        view_data = input("Do you wish to continue?: ").lower()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

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
    common_month = df['month'].mode()[0]
    print("Mostly common month is: {}".format(common_month))

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("Mostly common day of week is: {}".format(common_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Mostly common hour is: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    display_data(df)

    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Mostly common start station is: {}".format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Mostly common end station is: {}".format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End_Station'] = df['Start Station'] + ' ' + df['End Station']
    #Combine both start and end of stattion
    start_end_station = df['Start_End_Station'].mode()[0]
    print("Mostly frequent combination of start station and end station trip is: {}".format(start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    display_data(df)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Start_Trip_Datetime'] = pd.to_datetime(df['Start Time'])
    df['End_Trip_Datetime'] = pd.to_datetime(df['End Time'])
    # Add new column to calculate duration by hour each trip
    df['Trip_Duration_Hour'] = (df['End_Trip_Datetime'] - df['Start_Trip_Datetime']).dt.total_seconds() / 60
    total_travel_time = df['Trip_Duration_Hour'].sum()
    print("Total travel time(by hour) is: {}".format(total_travel_time))
        
    # TO DO: display mean travel time
    mean_travel_time = df['Trip_Duration_Hour'].sum() / df['Trip_Duration_Hour'].count()
    print("Mean travel time(by hour) is: {}".format(mean_travel_time))
    
    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    display_data(df)
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    # TO DO: Display counts of gender
    print('Count of gender:')
    user_gender = df['Gender'].value_counts()
    print(user_gender)

    
    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()
    recent_year = df['Birth Year'].max()
    common_year = df['Birth Year'].value_counts().idxmax()
    print('earliest year of birth:{}, most recent year of birth: {}, most common year of birth: {}'.format(earliest_year,recent_year,common_year))

    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    display_data(df)
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city.lower() != 'washington':
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
