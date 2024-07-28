import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title='Chat Analyzer', layout='wide', page_icon="random")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode()
    
    df = preprocessor.preprocessing(data)
    
    
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with",user_list)

    if st.sidebar.button("Show Analysis"):
        # stats
        total_msg, total_words, media_msg, no_link = helper.extract_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_msg)
        
        with col2:
            st.header("Total Words")
            st.title(total_words)

        with col3:
            st.header("Media Messages")
            st.title(media_msg)

        with col4:
            st.header("Link Shared")
            st.title(no_link)
        
        # Timeline
        st.title("Monthly Messages")
        year_month = helper.monthly_timeline(selected_user,df)
        fig = px.line(x=year_month['time'],y=year_month['message'])
        st.plotly_chart(fig)
        
        # weekly
        col1, col2 = st.columns(2)
        with col1:
            st.title("Weekly Activity")
            fig = px.bar(x=df['day_name'].value_counts().index,
                             y=df['day_name'].value_counts().values,
                             color_discrete_sequence=px.colors.qualitative.Pastel,
                             labels={'x':'day','y':'msg_count'})
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.title("Monthly Activity")
            fig = px.bar(x=df['month'].value_counts().index,
                             y=df['month'].value_counts().values,
                             color_discrete_sequence=px.colors.qualitative.Dark2,
                             labels={'x':'month','y':'msg_count'})
            st.plotly_chart(fig,use_container_width=True)

        # user_heatmap
        st.title("Weekly Activity")
        fig, ax = plt.subplots(figsize=(5,2.5))
        ax = sns.heatmap(df.pivot_table(index='day_name',columns='hour',values='message',aggfunc='count').fillna(0))
        
        st.pyplot(fig,use_container_width=True)

        
        if selected_user == 'Overall':
            col5, col6 = st.columns(2)

            with col5:
                st.header("Top Active Persons")
                fig = px.bar(x=df['user'].value_counts().head(5).index,
                             y=df['user'].value_counts().head(5).values,
                             color_discrete_sequence=px.colors.qualitative.Safe,
                             labels={'x':'name','y':'msg_count'})
                st.plotly_chart(fig,use_container_width=True)
            
            with col6:
                st.header("Percent of msg")
                temp_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns= {"user":'name','count':'percent'})
                st.dataframe(temp_df,use_container_width=True)
        
        # world cploud
        st.title('WordCloud')
        cloud_df = helper.extract_worldcloud(selected_user,df)
        fig , ax = plt.subplots()
        ax.imshow(cloud_df)
        st.pyplot(fig,use_container_width=True)

        # common words
        top_words = helper.extract_most_common_words(selected_user, df)
        st.header("Top Words")
        fig = px.bar(x=top_words[0], y=top_words[1],
                             color_discrete_sequence=px.colors.qualitative.Vivid,
                             labels={'x':'name','y':'count'})
        st.plotly_chart(fig,use_container_width=True)
        
        
        # emoji analysis
        st.header("Most Common Emoji")
        emoji_df = helper.extract_emoji(selected_user,df)
        fig2 = px.bar(x=emoji_df[0], y=emoji_df[1],
                             color_discrete_sequence=px.colors.qualitative.Bold,
                             labels={'x':'emoji','y':'count'})
        st.plotly_chart(fig2,use_container_width=True)