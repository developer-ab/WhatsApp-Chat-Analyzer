# Importing the required liberaries
from urlextract import URLExtract          # for extracting url from the string
from wordcloud import WordCloud            # for building the wordcloud
import pandas as pd                        # for data manipulation
from collections import Counter            # for counting 
import emoji                               # for the analysis of emojis

extractor = URLExtract()                   # making an object of URLExtract class


# function for the stats dashboard
def fetch_stats(selected_user, df):

    # checking if data is required for perticular user 
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # number of messages
    messages_num = df.shape[0]

    # number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # number of media messages
    media_num = df[df['message'] == '<Media omitted>\n'].shape[0]  

    # number of links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return messages_num, len(words), media_num, len(links)


# function for most active user        
def fetch_most_active_members(df):
       # for bar-chart
       x = df['user'].value_counts().head()

       # for table
       df = round((df['user'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns = {'imdex' : 'name', 'user' : 'percent'})

       return x, df


# function for the wordcloud 
def create_wordcloud(selected_user,df):
     
    # opening the file consisting the stop words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    # checking for perticular user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # removing the group notifications from the messages 
    temp_df = df[df['user'] != 'group_notification']

    # removing the media omitted message
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

    # function for removing the stop words
    def remove_stop_words(message):

        y = []

        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # generating the wordcloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp_df['message'] = temp_df['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp_df['message'].str.cat(sep=" "))
    
    return df_wc


# function for most used words
def most_common_words(selected_user, df):

    # opening the file consisting the stop words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    # checking for perticular user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # removing the group notifications from the messages 
    temp_df = df[df['user'] != 'group_notification']

    # removing the media omitted message
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

    # removing the stop words and making the data frame of top 20 most commomly used words
    words = []

    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    ret_df = pd.DataFrame(Counter(words).most_common(20))
    return ret_df

# function for geting most used emoji
def emoji_analysis(selected_user, df):

    # checking for perticular user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # making a list of emojis 
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    # making a data frame of most used emojis
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))      

    return emoji_df 