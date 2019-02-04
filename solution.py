import pandas as pd
import time

city_csv = { 'c': 'chicago.csv','w': 'washington.csv','ny': 'new_york_city.csv' }

months = { '1': 'January', '2': 'Feburary', '3': 'March', '4': 'April', '5': 'May', '6': 'June'}

days = {'1':'sunday','2':'monday','3':'tuesday','4':'wednessday','5':'thursday','6':'firday','7':'saturday' }

def get_filters():
	"""
	Asks user to specify a city, month, and day to analyze.

	Returns:
		(str) city - name of the city to analyze
		(str) month - name of the month to filter by, or "all" to apply no month filter
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""

	# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
	city = input('\nWhich city you want to explore chicago or washington or new york city?? ( enter c,w,ny respectively)\n')
	while city not in ['c','w','ny']:
		print("Enter vaild city name")
		city = input('\nWhich city you want to explore chicago or washington or new york city?? ( enter c,w,ny respectively)\n')

	# get user input for the type of filter (month, day, both, none)
	filters = input('do you want to filters by Month, Day, or both? "none" for no filters\n')
	while filters not in ['month','day','both','none']:
		print("please enter a vaild filters")
		filters = input('do you want to filters by Month, Day, or both? "none" for no filters\n')

	return city,filters

def load_data(city,filters):
	"""
	Loads data for the specified city and filters by month and day if applicable.

	Args:
		(str) city - name of the city to analyze
		(str) month - name of the month to filter by, or "all" to apply no month filter
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	Returns:
		df - Pandas DataFrame containing city data filtered by month and day
	"""

	# reading the csv file using Pandas
	df = pd.read_csv(city_csv[city])

	# coverting Start Time to covert datetime format
	df['Start Time'] = pd.to_datetime(df['Start Time'])

	# appending month and day_of_week Columns
	df['month'] = df['Start Time'].dt.month
	df['day_of_week'] = df['Start Time'].dt.weekday_name

	# filtering the DataFrame according to the Filters provided
	if filters.lower() != 'none':

		if filters.lower() == 'month':

			month = input('Enter the Month in Number (January = 1,..., June = 6)\n')
			df = df[df['month'] == int(month)]

			return df

		elif filters.lower() == 'day':

			day = input('Enter the Day in Number (sunday = 1)\n')
			day = days[day]
			df = df[df['day_of_week'] == day.title()]

			return df

		elif filters.lower() == 'both':

			month = input('Enter the Month in Number (January = 1,..., June = 6)\n')
			df = df[df['month'] == int(month)]			
			
			day = input('Enter the Day in Number (sunday = 1)\n')
			day = days[day]
			df = df[df['day_of_week'] == day.title()]

			return df

	else:
		return df

def time_stats(df,filters):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # finding the most common start hour
    hour = df['Start Time'].dt.hour.mode()[0]

    # finding the most common month
    month = df['month'].mode()[0]

    # finding the most common day of week
    day = df['day_of_week'].mode()[0]

    if filters.lower() != 'none':

    	if filters.lower() == 'month':
    		# statistics of frequent Time Stats wiht Month filter 
    		print('most popular day : {}\nmost popular hour : {}\nfilter : {}'.format(day,hour,filters))

    	elif filters.lower() == 'day':
    		# statistics of frequent Time Stats wiht day filter
    		print('most popular month : {}\nmost popular hour : {}\nfilter : {}'.format(months[str(month)],hour,filters))

    	elif filters.lower() == 'both':
    		# statistics of frequent Time Stats wiht both filter
    		print('most popular hour : {}\nfilter : {}'.format(hour,filters))

    else:
    	# statistics of frequent Time Stats wiht none filter
    	print('most popular day : {}\nmost popular month : {}\nmost popular hour : {}\nfilter : {}'.format(day,months[str(month)],hour,filters))
	
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # adding Column journey by cancatnating columns Start Station and End Station
    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep = ' -> ')    

    # display most commonly used start station
    start = df['Start Station'].mode()[0]
    print('most commonly used start station : {}'.format(start))

    # display most commonly used end station
    end = df['End Station'].mode()[0]
    print('most commonly used end station : {}'.format(end))

    # display most frequent combination of start station and end station trip
    combination = df['journey'].mode()[0]
    print('most frequent combination of start station and end station : {}'.format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('total travel duration : {}'.format(total))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('mean travel time : {}'.format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts()
    print('counts of user types : {}\n'.format(users))

    if city in ['c','ny']:

    	# Display counts of gender
    	sex = df['Gender'].value_counts()
    	print('counts of gender : {}\n'.format(sex))

    	# Display earliest, most recent, and most common year of birth
    	earliest = int(df['Birth Year'].min())
    	recent = int(df['Birth Year'].max())
    	common = int(df['Birth Year'].mode())
    	print('The oldest users are born in {}.\nThe youngest users are born in {}.\nThe most popular birth year is {}.'.format(earliest, recent, common))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
	""" display 5 lines of user data if user specifies to"""

	start = 0
	end = 5
	while True:

		print(df[df.columns[1:-1]].iloc[start:end])

		restart = input('Would you like to view more data?? (please enter "yes" or "no")\n')

		if restart == 'yes':
			start += 5
			end += 5
		else:
			break



	



def main():
	while True:
		city,filters = get_filters() # gettting city name and filter from user
		
		df = load_data(city,filters) # loading the data according to user input
		
		time_stats(df,filters)	# function call to display popular Month, Day and Hour 
		
		station_stats(df) # function call to display popular Start Station, End station and Journey 
		
		trip_duration_stats(df) # function call to display Total and Average trip duration
		
		user_stats(df,city) # function call to display User Statistics (Gender, User type, Birth year)

		answer = input('Would you like to view individual user data!? (please enter "yes" or "no")\n')
		if answer == 'yes':
			display_data(df) # function call to display Individual User data

		restart = input('\n do u want to continue yes or no?')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()