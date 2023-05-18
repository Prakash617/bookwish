from datetime import date, timedelta

def get_week_dates(base_date, start_day):
    
    # Calculate the date for Sunday of the week containing the base date
    sunday = base_date - timedelta(days=base_date.isoweekday())
    
    # writing two different conditions to check if the date is a sunday and proceed accordingly
    if (base_date.strftime("%A").lower() != "sunday"):
        
        
        # Calculate the start date of the week by adding the number of days corresponding to the desired start day
        start_date = sunday + timedelta(days=start_day)
        print("start", start_date)
    else:
        start_date = sunday + timedelta(days=start_day + 7)
        
    # Generate the dates for the week by adding the number of days from the start date
    week_dates = [start_date + timedelta(days=i) for i in range(7)]
    return week_dates

# # Call the function to generate the dates for the week starting from Sunday
# sunday_dates = get_week_dates(date(2023, 3, 20), 0)

# # Print the dates
# for d in sunday_dates:
#     print(d)
def get_week_dates_endday(base_date, start_day):
    
    # Calculate the date for Sunday of the week containing the base date
    sunday = base_date - timedelta(days=base_date.isoweekday())
    
    # writing two different conditions to check if the date is a sunday and proceed accordingly
    if (base_date.strftime("%A").lower() != "sunday"):
        # Calculate the start date of the week by adding the number of days corresponding to the desired start day
        start_date = sunday + timedelta(days=start_day)
        print("start", start_date)
    else:
        start_date = sunday + timedelta(days=start_day + 7)
        
    # Generate the dates for the week by adding the number of days from the start date
    week_dates = [start_date + timedelta(days=i) for i in range(7)]
    return week_dates


# from datetime import date

# # Set the base date to March 26, 2023 (a Sunday)
# base_date = date(2023, 3, 26)

# # Start the week on Monday (0)
# start_day = 0

# # Call the function with the given arguments
# week_dates = get_week_dates_endday(base_date, start_day)

# # Print the resulting list of dates
# print(week_dates)
