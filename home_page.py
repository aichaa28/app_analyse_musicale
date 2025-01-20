import streamlit as st


def home_page():
    st.markdown("""
    ## Welcome to **Music Sales Maximizer** 🎵
    
    Are you ready to take your music business to the next level?  
    **Music Sales Maximizer** is your ultimate partner in exploring the trends, styles, and insights that can **skyrocket your sales**.  
    
    Whether you're a producer, an artist, or a music label executive, this app empowers you with **data-driven decisions** to ensure you're always a step ahead in the ever-evolving music industry.
    
    ### What You'll Get:
    - 📊 **Comprehensive Analytics**: Discover trends and insights tailored to your music data.  
    - 🎼 **Strategic Recommendations**: Identify the best music styles for your audience.  
    - 🚀 **Sales Boosting Potential**: Maximize profits with actionable insights.  

    Ready to make data work for your music? Click below to get started!
    """)
    if st.button("Dashboard"):
        st.session_state.page = "dashboard"
