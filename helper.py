from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
uext = URLExtract()

def extract_stats(user_ka_naam,data):

    
    if user_ka_naam != 'Overall':
        data = data[data['user'] == user_ka_naam]

    # total msg
    total_msg = data.shape[0]
    # total words
    words = []
    for msg in data['message']:
        words.extend(msg.split())
    
    # number of media msg
    media_msg = data[data['message'] == ' <Media omitted>\n'].shape[0]
    
    # number of links
    links = []
    for msg in data['message']:
        links.extend(uext.find_urls(msg))

    return total_msg, len(words),media_msg, len(links)
    
def extract_worldcloud(user_ka_naam, df):
    if user_ka_naam != 'Overall':
        df = df[df['user'] == user_ka_naam]
    
    # temp = df[df['user'] != 'group_notification']
    # temp = temp[temp['message'] != " <Media omitted>\n"]
    # f = open('stop_hinglish.txt','r')
    # stop_words = f.read()
    # def remove_stopwords(message):
    #     y = []
    #     for word in message.strip().lower().split():
    #         if word not in stop_words:
    #             y.append(word)
    #     return " ".join(y)
    
    wc = WordCloud(width=500,height=500, min_font_size=10, background_color='white')
    # temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc


def extract_most_common_words(user_ka_naam, df):
    if user_ka_naam != 'Overall':
        df = df[df['user'] == user_ka_naam]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != " <Media omitted>\n"]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    words = []
    for msg in temp['message']:
        for word in msg.strip().lower().split():
            if word not in stop_words:
                words.append(word)
    top_words = pd.DataFrame(Counter(words).most_common(20))    

    return top_words

def extract_emoji(user_ka_naam,df):
    if user_ka_naam != 'Overall':
        df = df[df['user'] == user_ka_naam]
    
    emojis = []
    for msg in df['message']:
        emojis.extend([c['emoji'] for c in emoji.emoji_list(msg)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))

    return emoji_df

def monthly_timeline(user_ka_naam, df):
    if user_ka_naam != 'Overall':
        df = df[df['user'] == user_ka_naam]

    year_month = df.groupby(['year','month_num','month'])['message'].count().reset_index()
    time = []
    for i in range(year_month.shape[0]):
        time.append(year_month['month'][i] + "-" + str(year_month['year'][i]))
    year_month['time'] = time
    
    return year_month