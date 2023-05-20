def change_time(time):
    h, m = map(int, time.split(':'))
    return h * 60 + m


def change_date(date):
    import datetime
    day, month, year = (int(x) for x in date.split('.'))
    ans = datetime.date(year, month, day)
    temp_date = ans.strftime("%A")
    if temp_date == 'Monday':
        return 1
    elif temp_date == 'Tuesday':
        return 2
    elif temp_date == 'Wednesday':
        return 3
    elif temp_date == 'Thursday':
        return 4
    elif temp_date == 'Friday':
        return 5
    elif temp_date == 'Saturday':
        return 6
    elif temp_date == 'Sunday':
        return 7


def generate_pivot_table(df):

    group_all_time = df.groupby(['area', 'type_of_road'])['load_index'].mean()
    pivot_table_all_time = group_all_time.unstack()  # all_time

    group_date = df.groupby(['area', 'type_of_road', 'date'])['load_index'].mean()
    pivot_table_date = group_date.unstack()  # date

    group_time = df.groupby(['area', 'type_of_road', 'time'])['load_index'].mean()
    pivot_table_time = group_time.unstack()  # date

    return pivot_table_all_time, pivot_table_date, pivot_table_time