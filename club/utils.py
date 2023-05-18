# import datetime

from datetime import timedelta
import datetime
import time

from datetime import date

def same_week(dateString):
    '''returns true if a dateString in %Y%m%d format is part of the current week'''
    d1 = datetime.datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year | False



import datetime

def get_weeks(start_date, end_date):
    # Calculate the first day of the month
    first_day = datetime.date(start_date.year, start_date.month, 1)
    # Calculate the last day of the month
    last_day = datetime.date(end_date.year, end_date.month, 28) + datetime.timedelta(days=4)
    last_day -= datetime.timedelta(days=last_day.day)
    # Calculate the start day of the first week
    start_day = first_day - datetime.timedelta(days=first_day.weekday())
    # Calculate the end day of the last week
    end_day = last_day + datetime.timedelta(days=6 - last_day.weekday())
    
    # Initialize the list of weeks
    weeks = []
    # Loop over each week
    curr_day = start_day
    while curr_day <= end_day:
        # Add the current week to the list of weeks
        weeks.append([curr_day + datetime.timedelta(days=i) for i in range(7)])
        # Move to the next week
        curr_day += datetime.timedelta(days=7)
    
    # Check if the first week starts in the previous month
    if weeks[0][0].month != start_date.month:
        # Remove the first week
        weeks.pop(0)
    else:
        # Replace the first week with the correct start date
        weeks[0] = [start_date + datetime.timedelta(days=i) for i in range(7)]
    
    # Check if the last week ends in the next month
    if weeks[-1][-1].month != end_date.month:
        # Remove the last week
        weeks.pop()
    else:
        # Replace the last week with the correct end date
        weeks[-1] = [end_date - datetime.timedelta(days=6-i) for i in range(7)]
    
    return weeks



# def get_dates():


#     start_date_str = "2023-04-01"
#     end_date_str = "2023-04-30"
#     start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
#     end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

#     delta = end_date - start_date

#     num_weeks = delta.days // 7
#     remainder_days = delta.days % 7

#     dates = []
#     current_date = start_date

#     for i in range(num_weeks + 1):
#         week_dates = [current_date + timedelta(days=d) for d in range(7)]
#         dates.append(week_dates)
#         current_date += timedelta(days=7)

#     if remainder_days > 0:
#         remaining_dates = [end_date - timedelta(days=(remainder_days - 1) - d) for d in range(remainder_days)]
#         dates.append(remaining_dates)

#     for date in dates:
#         for item in date:
#             print(item.strftime('%Y-%m-%d'))
#         print()
    

#     # start_date_str = "2023-04-01"
#     # end_date_str = "2023-05-03"
#     # start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
#     # end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

#     # delta = end_date - start_date

#     # num_weeks = delta.days // 7
#     # remainder_days = delta.days % 7

#     # dates = []
#     # current_date = start_date

#     # for i in range(num_weeks):
#     #     week_dates = [current_date + timedelta(days=d) for d in range(7)]
#     #     dates.append(week_dates)
#     #     current_date += timedelta(days=7)

#     # if remainder_days > 0:
#     #     remaining_dates = [current_date + timedelta(days=d) for d in range(remainder_days)]
#     #     dates.append(remaining_dates)

#     # for date in dates:
#     #     for item in date:
#     #         print(item.strftime('%Y-%m-%d'))
#     #     print()

    

def get_dates(start_date_str1):
    # print(start_date_str)
    start_date_str = 0
    start_date_str = str(start_date_str1)

    # start_date_str = "2023-03-28"
    given_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    start_date = given_date - timedelta(days=1)
    dates = []
    required_dates = []
    generatingOn = True

    if given_date < datetime.datetime.now():
        while generatingOn:
            count = 0
            current_dates = []
            while count < 7:
                end_date = start_date + datetime.timedelta(days=1)
                current_dates.append(end_date)
                start_date = end_date
                count += 1
                
                if (end_date.date() == datetime.datetime.today().date()):
                    generatingOn = False
                    break
            dates.append(current_dates)
        
    return dates[-4::]




   



if __name__ == "__main__":
    dates = get_dates()
    for date_items in dates:
        print(date_items)
        print()





