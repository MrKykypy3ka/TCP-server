def change_time(time):
    h, m = map(int, time.split(':'))
    return h * 60 + m


def change_date(date):
    import datetime
    day, month, year = (int(x) for x in date.split('.'))
    ans = datetime.date(year, month, day)
    temp_date = ans.strftime("%A")
    if temp_date == 'Monday':
        return 'ПН'
    elif temp_date == 'Tuesday':
        return 'ВТ'
    elif temp_date == 'Wednesday':
        return 'СР'
    elif temp_date == 'Thursday':
        return 'ЧТ'
    elif temp_date == 'Friday':
        return 'ПТ'
    elif temp_date == 'Saturday':
        return 'СБ'
    elif temp_date == 'Sunday':
        return 'ВС'

def generate_pivot_table(df):

    group_all_time = df.groupby(['area', 'type_of_road'])['load_index'].mean()
    pivot_table_all_time = group_all_time.unstack()  # all_time
    #pivot_table_all_time = pivot_table_all_time.fillna("-")

    group_date = df.groupby(['area', 'type_of_road', 'date'])['load_index'].mean()
    pivot_table_date = group_date.unstack()  # date
    #pivot_table_date = pivot_table_date.fillna("-")
    pivot_table_date = pivot_table_date.reindex(columns=['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'])

    group_time = df.groupby(['area', 'type_of_road', 'time'])['load_index'].mean()
    pivot_table_time = group_time.unstack()  # date
    #pivot_table_time = pivot_table_time.fillna("-")

    return pivot_table_all_time, pivot_table_date, pivot_table_time