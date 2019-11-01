import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    # city filter input
    while True:
        city = input('\nWould you like to see data for Chicago, New York, or Washington? \n').lower()
        if city not in (CITY_DATA):
            print('\nSorry there was a mistake in your input, please try again.')
            continue
        else:
            break

    # time filter input
    while True:
        filters = ['month', 'day', 'no', 'both']
        time_filter = input('\nWould you like to filter the data by month, day, both, or not at all? \n(If not at all enter \'no\') \n')

        if time_filter not in filters:
            print('\nSorry you entered a wrong input, please enter \'month\', \'day\', or \'no\' to continue')
            continue

        # get user input for month (all, january, february, ... , june)
        elif time_filter == 'month':

            months = ['January', 'February', 'March', 'April', 'May', 'June']
            month = input('\nWhich month would you like to know about? \n(January, February, March, April, May, or June)\n').title()

            if month not in months:
                print('\nSorry there was a mistake in your input, please try again.')
                continue
            else:
                day = 'all'
                break


        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif time_filter == 'day':

            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = input('\n\nWhich day of the week would you like to know about? \n(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday)\n').lower()

            if day not in days:
                print('\nSorry there was a mistake in your input, please try again.')
                continue
            else:
                month = 'all'
                break

        # if user entered no
        elif time_filter == 'no':
            month = 'all'
            day = 'all'
            break


        # if user entered both, asks to enter month and day to filter
        elif time_filter == 'both':

            # get user input for month (all, january, february, ... , june)
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            month = input('\nWhich month would you like to know about? \n(January, February, March, April, May, or June)\n').title()

            if month not in months:
                print('\nSorry there was a mistake in your input, please try again.')
                continue
            else:

                # get user input for day of week (all, monday, tuesday, ... sunday)
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day = input('\n\nWhich day of the week would you like to know about? \n(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday)\n').title()

                if day not in days:
                    print('\nSorry there was a mistake in your input, please try again.')
                    continue
                else:
                    break


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

    # load city into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of the week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1

        df = df[df['month'] == month]

    # filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    ''' use count and max to find the most common ...'''

    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    popular_month = df['month'].mode()[0]
    popular_month = months[popular_month]
    print('Most common month: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day: {}'.format(popular_day))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip:\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('{} is the most popular start station.'.format(pop_start))

    # display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('{} is the most popular end station.'.format(pop_end))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    pop_trip = df['Trip'].mode()[0]
    print('{} is the most popular trip.'.format(pop_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time: {}'.format(total_travel))

    # display mean travel time
    average_travel = df['Trip Duration'].mean()
    print('Average travel time: {}'.format(round(average_travel,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_type_counts = df['User Type'].value_counts()
        print('User Types:\n\n{}\n'.format(user_type_counts))
    except:
        print('There is no user type data in this time frame.\n')

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nGender:\n\n{}\n'.format(gender_counts))
    except:
        print('There is no gender data in this time frame.\n')
    # Display earliest, most recent, most common year of birth, and average age
    try:
        oldest_yr = int(df['Birth Year'].min()) # provides oldest year of birth
        earliest_yr = int(df['Birth Year'].max()) # provides most recent year of birth
        popular_yr =  int(df['Birth Year'].mode()[0]) # provides most common year of birth

        print('\nBirth Year:\n\nEarliest birth year: {}\nMost recent birth year: {}\nMost common year of birth: {}\nMost common age: {}\n'.format(oldest_yr,earliest_yr,popular_yr,average_age))

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['year'] = df['Start Time'].dt.year

        actual_yr =  int(df['year'].max()) # provides this year
        average_age = actual_yr - int(df['Birth Year'].mean())  # provides average age
        oldest_age = actual_yr - oldest_yr # provides oldest age
        youngest_age = actual_yr - earliest_yr # provides youngest age

        print('\nBirth Year:\n\nMost common age: {}\nOldest age: {}\n Youngest age: {}'.format(average_age,oldest_age,youngest_age))


    except:
        print('There is no birth year or age data in this time frame.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_rows(df):
    """ Drops new columns created in the process and isplays 5 rows of data if the user enters yes."""

    # drop month and day of week columns as they are not in the original dataframe
    df = df.drop(['Unnamed: 0', 'month', 'day_of_week', 'hour', 'Trip'], axis = 1)

    start_row = 0
    end_row = 5

    # asks the user to display the lines of data, if yes
    display = input('\nWould you like to view individual trip data? (Enter yes or no)\n').lower()

    while True:
        if display != 'yes' and display != 'no':
            print('\nSorry there was a mistake in your input, please try again.')

        elif display == 'yes':
            print(df[start_row:end_row])

            #  asks user if they wish to view 5 more lines of data
            while True:
                display = input('\nWould you like to view 5 more rows of data? (Enter yes or no)\n').lower()

                if display != 'yes' and display != 'no':
                    print('\nSorry there was a mistake in your input, please try again.')
                elif display == 'yes':
                    start_row += 5
                    end_row += 5
                    print(df[start_row:end_row])
                else:
                    break

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
        display_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
