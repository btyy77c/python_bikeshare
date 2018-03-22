import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
          'october', 'november', 'december', 'all']

def get_input(message, available_options):
    """ Gets user input.  Uses a while loop to validate user submissions. """
    while True:
        choice = input(message).lower().strip()
        if choice in available_options:
            print('\nThanks for choosing ' + choice + '!')
            break
        else:
            print('\nSorry! ' +  choice + ' is not an available option. Please try again.')
    return choice


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """ get user input for city (chicago, new york city, washington) """
    city = get_input('\nWhich city would you like to analyze? \n Enter: Chicago, New York City, or Washington: ',
                     list(CITY_DATA.keys()))

    """ get user input for month (all, january, february, ... , june) """
    month = get_input('\nWhich month would you like to analyze? \
                       \n Enter a month like: january, february, etc. OR all for no filter: ',
                       months)

    """ get user input for day of week (all, monday, tuesday, ... sunday) """
    day = get_input('\nWhich day would you like to analyze? \
                     \n Enter a day of the week: monday, tuesday, etc. OR all for no filter: ',
                    ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

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
    print("Loading data.  Please wait.")
    df = pd.read_csv(city.replace(' ', '_') + '.csv')

    start_time = pd.to_datetime(df['Start Time'])
    df['month'] = start_time.dt.strftime("%B")
    df['day'] = start_time.dt.strftime("%A")
    df['hour'] = start_time.dt.strftime("%H")
    df['total_travel'] = pd.to_datetime(df['End Time'])  - start_time

    """ Filter by month """
    if month != 'all':
        df = df[df['month'] == month.title()]

    """ Filter by day """
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """ display the most common month """
    print('\n The most common month was: ' + df['month'].mode()[0])
    print('---------------------')


    """ display the most common day of week """
    print('\n The most common day was: ' + df['day'].mode()[0])
    print('---------------------')


    """ display the most common start hour """
    print('\n The most common start hour was: ' + df['hour'].mode()[0])
    print('---------------------')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ display most commonly used start station """
    print('\n The most commonly used start station was: ' + df['Start Station'].mode()[0])
    print('---------------------')

    """ display most commonly used end station """
    print('\n The most commonly used end station was: ' + df['End Station'].mode()[0])
    print('---------------------')

    """
     display most frequent combination of start station and end station trip
     Credit: Stack Overflow helped me find this solution
    """
    print('Top 3 most frequent combinations of start station and end station: ')
    print(df.groupby(['Start Station','End Station']).size().nlargest(3))
    print('---------------------')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """ display total travel time """
    print('Total Travel Time: ')
    print(df['total_travel'].sum())
    print('---------------------')

    """ display mean travel time """
    print('Mean Travel Time: ')
    print(df['total_travel'].mean())
    print('---------------------')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Display counts of user types """
    print('User Type Counts: ')
    if 'User Type' in df.keys():
        print(df['User Type'].value_counts(dropna=True))
    else:
        print('User Type not available')
    print('---------------------')

    """ Display counts of gender """
    print('Gender Counts: ')
    if 'Gender' in df.keys():
        print(df['Gender'].value_counts(dropna=True))
    else:
        print('Gender is not available')
    print('---------------------')

    """ Display earliest, most recent, and most common year of birth """
    if 'Birth Year' in df.keys():
        print('Earliest birth year: ')
        print(int(df['Birth Year'].min()))
        print('---------------------')

        print('Most recent birth year: ')
        print(int(df['Birth Year'].max()))
        print('---------------------')

        print('Most common birth year: ')
        print(int(df['Birth Year'].mode()[0]))
        print('---------------------')
    else:
        print('Birth Year data not available')
        print('---------------------')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = get_input('\nWould you like to see table raw data? Enter yes or no.\n', ['yes', 'no'])
        if raw_data == 'yes':
            print(df.head())

        restart = get_input('\nWould you like to restart the program? Enter yes or no.\n', ['yes', 'no'])
        if restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
