import re
import pandas as pd

def preprocess(data):
    
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message' : messages, 'message_date' : dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format = '%m/%d/%y, %H:%M - ')
    df.rename(columns = {'message_date' : 'date'}, inplace = True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_message'], inplace = True)

    # Extracting year
    df['year'] = df['date'].dt. year
    # Extracting month number
    df['month_num'] = df['date'].dt.month 
    # Extracting month
    df['month'] = df['date'].dt.month_name
    # Extracting date
    df['day'] = df['date'].dt.day
    # Extracting day name
    df['day_name'] = df['date'].dt.day_name
    # Extracting hours
    df['hour'] = df['date'].dt.hour
    # Extracting minute
    df['minute'] = df['date'].dt.minute

    return df
