import helper
import streamlit as st
import preprocesser
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.preprocess(data)  
    # st.text(data)
    # st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_message,number_of_word,num_media_messages,number_of_links = helper.fetch(selected_user, df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_message)
            # st.title("123")
        with col2:
            st.header("Total Words")
            st.title(number_of_word)
            # st.title("123")
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("No. of Links shared")
            st.title(number_of_links)
        
        # timeline
        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        # activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_actively_map(selected_user,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation = 'vertical')
            ax.bar(busy_day.index , busy_day.values,color ='green')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index , busy_month.values,color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        # activity heatmap
        # st.title()

        st.title("Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, annot=True)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title("Most busy users")
            x,new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_word(selected_user,df)
        fig,ax = plt.subplots()
        # plt.xticks(rotation = 'vertical')
        ax.barh(most_common_df[0],most_common_df[1])
        st.title('Most common Words')
        st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        emoji_df  = helper.analyze_emojis(selected_user,df)
        
        col1,col2 = st.columns(2)
        with col1 :
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels = emoji_df[0] ,autopct = "%0.2f")
            st.pyplot(fig)

        
        