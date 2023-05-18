import datetime
def day_ago(date):
    
    previous_date = datetime.datetime.strptime(date, '%Y-%m-%d')

    # notification_time = time.strftime('%I:%M %p')

    today = datetime.datetime.today()

    # compute difference
    ndays = (today - previous_date).days

    # Calculating years
    years = ndays / 365

    # month = ndays // 30
    if ndays <= 30:
        if ndays == 1:
            return (f"Yesterday")
        elif ndays<1:
            return (f'Today')
        elif ndays <7:
            return (f'{ndays}d')
        else:
            week = int(ndays%365)/7
            return (f"{int(week)}w.")
    elif ndays >= 30 and  ndays < 365 :
        # month = ndays/30
        month = int(ndays%365)/30
        # week = int((ndays%365)%30)/7
        return (f"{int(month)}m")
    elif ndays >= 365:
        # month = int(ndays%365)/30
        # print(f"type {type(int(month))}, {month}).")
        # month  = 'and ' + str(int(month)) + " month " if int(month) != 0 else ''
        return (f"{int(years)}y")
    else:
        print(f"a month than a year ago ")