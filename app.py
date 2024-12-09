# Importing the rewuired liberaries

import streamlit as st                                    # for the web app
import preprocessor, helper                               # other files which will help in getting the desired data
import matplotlib.pyplot as plt                           # for the visual representation of data as bar charts, pie charts, etc

# title of the sidebar
st.sidebar.title("WhatsApp Chat Analyzer")

# input box for uploading the file 
uploaded_file = st.sidebar.file_uploader("Choose a file")

# cheking if the file is uploaded
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetching unique users from the data frame
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()

    # inserting an extra user to 'Overall' which will show the oveall analysis of the chat.
    user_list.insert(0, "Overall")

    # drop box to selec the user
    selected_user = st.sidebar.selectbox("Show Analysis wrt ", user_list)

    if st.sidebar.button("Show Analysis"):

    # for the stats dashboard

        # fetching the data with the help of fetch_stats function from the helper file
        messages_num, words, media_num, links_num = helper.fetch_stats(selected_user, df)

        # title 
        st.title("Statistics")
        # making columns
        col1, col2, col3, col4 =  st.columns(4)

        # column for the total messages
        with col1:
            st.header("Total Messages")
            st.title(messages_num)

        # column for the total number of words
        with col2:
            st.header("Total Words")
            st.title(words)

        # column for the total number of media shared
        with col3:
            st.header("Media Shared")
            st.title(media_num)  

        # column for the total number of links shared
        with col4:
            st.header("Links Shared")
            st.title(links_num)


    # finding the most active Users in the group

        # checking for the overall analysis 
        if selected_user == 'Overall':

            st.title('Most Active Users')

            # fetching data
            x, tab_df = helper.fetch_most_active_members(df)

            # ploting the bar chart
            fig, ax = plt.subplots()

            # making columns
            col1, col2 = st.columns(2)

            # column for bar chart
            with col1:
                ax.bar(x.index, x.values, color = '#06402b')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            # column for the table
            with col2:
                st.dataframe(tab_df)  


    # WordCloud
        st.title("Word Cloud")

        #fetching the data
        df_wc = helper.create_wordcloud(selected_user, df)

        # creating space for the wordcloud   
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    # top-20-words

        # fetching the data
        most_common_df = helper.most_common_words(selected_user, df)

        # ploting the horizontal bar chart
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = 'vertical')

        st.title("Most Common Words")
        st.pyplot(fig)

    # emoji analysis

        st.title("Emoji Analysis")

        # fetching the data
        emoji_df = helper.emoji_analysis(selected_user, df)

        # maing columns
        col1, col2 = st.columns(2)

        # column for table
        with col1:
            st.dataframe(emoji_df)

        # column for the pie chart
        with col2:
            fig, ax = plt.subplots()
            # creating the pie chart
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct = "%0.2f")
            st.pyplot(fig)