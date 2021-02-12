## VERSION NOTES: Python=3.6.3, pandas=0.19.2
#This program provides an interactive way to explore bikeshare data! :D

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
DAY_OF_WEEK = { 'Mon' : 'Monday',
                'Tue' : 'Tuesday',
                'Wed' : 'Wednesday',
                'Thu' : 'Thursday',
                'Fri' : 'Friday',
                'Sat' : 'Saturday',
                'Sun' : 'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! Which city would you like to explore?')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Please type Chicago, New York City, or Washington: ").lower()
        try:
            CITY_DATA[city]
            break
        except:
            print('\n\nINVALID INPUT, please try again. Type city as shown.')
    # get user input for month (all, january, february, ... , june)
    print('\n\nWhich month would you like to explore?')
    while True:
        try:
            month = input('Enter a number from 1 to 12, or type ALL: ').title()
            assert(month in ('1','2','3','4','5','6','7','8','9','10','11','12','All'))
            break
        except:
            print('\n\nINVALID INPUT, please try again.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\n\nWhich day of week would you like to explore?')
    while True:
        try:
            day = input('Type Mon, Tue, Wed, Thu, Fri, Sat, Sun, or ALL: ').title()
            assert(day in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun','All'))
            break
        except:
            print('\n\nINVALID INPUT, please try again.')

    print('-'*40)
    return city, month, day


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

    # convert timestamps to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    # create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # create trips column
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    month_filter = False
    if month != 'All':
        df = df[df['month'] == int(month)]
        month_filter = True

    # filter by day of week if applicable
    day_filter = False
    if day != 'All':
        df = df[df['day_of_week'] == DAY_OF_WEEK[day]]
        day_filter = True

    return df , month_filter, day_filter


def time_stats(df, month_filter, day_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month_filter:
        print('Only showing data for selected month')
    else:
        popular_month = df['month'].mode()[0]
        print('The most popular month was {}'.format(popular_month))

    # display the most common day of week
    if day_filter:
        print('Only showing data for selected day of week')
    else:
        popular_day = df['day_of_week'].mode()[0]
        print('The most popular day of week was {}'.format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour was {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most popular start station was {}'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most popular end station was {}'.format(popular_end))

    # display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    print('The most frequent start/stop station combination was from {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total/mean travel time
    travel_time = df['Travel Time'].sum().total_seconds() / (60*60*24)
    mean_travel_time = df['Travel Time'].mean().total_seconds() / (60)
    print('The total travel time was {} days, and the average travel time was {} minutes.'.format(travel_time, mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = pd.value_counts(df['User Type'])
    print('The distribution of user types was:\n', user_types, '\n')
    # Display counts of gender
    try:
        user_gender = pd.value_counts(df['Gender'])
        print('\nThe distribution of user gender was:\n', user_gender,'\n')
    except:
        print('gender not avaiable.\n')
    # Display earliest, most recent, and most common year of birth
    try:
        user_age_max = int(df['Birth Year'].max())
        user_age_min = int(df['Birth Year'].min())
        user_age_mode =int(df['Birth Year'].mode()[0])
        print('The earliest birth year was {}, while the most recent was {}, and the most common was {}.'.format(user_age_min, user_age_max, user_age_mode))
    except:
        print('birth year not avaiable')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    view_display = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_display == 'yes':
        print('\n', df.iloc[start_loc:start_loc + 5], '\n')
        start_loc += 5
        view_display = input('Do you wish to continue? Enter yes or no: ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df , month_filter, day_filter = load_data(city, month, day)
        time_stats(df, month_filter, day_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
