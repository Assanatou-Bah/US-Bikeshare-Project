# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:01:39 2023

@author: ams_j
"""

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
    print("\nHello! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # prompt the user to enter the name of a city
    city = ''
    #Running this loop to ensure the correct user input gets selected else repeat
    while city not in CITY_DATA.keys():
        print("\nPlease enter your city: Chicago, New York City or Washington")
        #Taking user input and converting into lower to standardize them
        #You will find this happening at every stage of input throughout this
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nInvalid city. Please try again.")
            print("\nRestarting...")

    print(f"\nYou have chosen {city.title()} as your city.")

    # get user input for month (all, january, february, ... , june)
    # define a list of valid months
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    # prompt the user to enter a month
    month = input("Enter a month (all, january, february, ..., june): ").lower()

    # use a while loop to handle invalid inputs
    while month.lower() not in months:
            print("Invalid month. Please try again.")
            month = input("Enter a month (all, january, february, ..., june): ").lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    # define a list of valid days of the week
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # prompt the user to enter a day of the week
    day = input("Enter a day of the week (all, monday, tuesday, ..., sunday): ").lower()

    # use a while loop to handle invalid inputs
    while day.lower() not in days:
        print("Invalid day of the week. Please try again.")
        day = input("Enter a day of the week (all, monday, tuesday, ..., sunday): ").lower()

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
    # load data file into a DataFrame

    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    #print('Most Common Month:', popular_month)
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station is:', Start_Station)

    # display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station is:', End_Station)

    # display most frequent combination of start station and end station trip
    start_end_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nMost frequent combination of start station and end station trip is:', start_end_combination)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time in mins:', round(total_travel_time / 60, 2))
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean Travel Time in mins: ', round(mean_travel_time / 60, 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    try:
       gender = df['Gender'].value_counts()
       print('\nCount of Gender:\n', gender)
    except KeyError:
        print('\nGender data not available for this city.')

    # Display earliest, most recent, and most common year of birth  
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        
        print('\nEarliest year of birth:', earliest_birth_year)
        print('Most recent year of birth:', most_recent_birth_year)
        print('Most common year of birth:', most_common_birth_year)
        
    except KeyError:
        print('\nBirth year data not available for this city.')
    except ValueError:
        print('\nBirth year data is incomplete for this city.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   

def display_data(df):
    """Display raw data upon request by the user"""
    # Initialize the starting and ending location
    start_loc = 0
    end_loc = 5
    
    # Ask the user if they want to view 5 rows of individual trip data
    view_data = input("\nWould you like to view 5 rows of individual trip data? Enter yes or no\n").lower()
    
    while True:
        # Display 5 rows of the data frame if user entered yes
        if view_data == 'yes': 
            print(df.iloc[start_loc:end_loc])
            start_loc += 5
            end_loc += 5
            view_data = input("Do you wish to continue?: ").lower()
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()