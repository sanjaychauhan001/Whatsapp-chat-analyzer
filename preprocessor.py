import re
import pandas as pd

def preprocessing(data):
    pattern = r'\d{1,2}\/\d{1,2}\/\d{1,4},\s\d{1,2}:\d{1,2}\s[APMapm]{2}\s-\s'

    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]

    df = pd.DataFrame({'message':messages,'date':dates})
    def date_parser(date_str):
        # Remove the trailing hyphen and space
        date_str = date_str.rstrip(' -')
        return pd.to_datetime(date_str, format="%d/%m/%Y, %I:%M %p")
    df['date'] = df['date'].apply(date_parser)

    user = []
    messages = []
    for msg in df['message']:
        l = msg.split(":")
        if len(l) == 1:
            user.append("group_notification")
            messages.append(l[0])
        elif len(l) >=2:
            user.append(l[0])
            messages.append(l[1])
    df['user'] = user
    df['message'] = messages
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()

    return df