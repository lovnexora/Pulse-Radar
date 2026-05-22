import streamlit as st
import pandas as pd
import plotly.express as px  # <-- New tool to draw premium interactive charts!
from scraper import fetch_trending_topics
from engine import analyze_sentiment

# Set up browser page options
st.set_page_config(page_title="Global Pulse Radar", page_icon="⚡", layout="wide")

st.title("⚡ Pulse — Global Topic & Sentiment Radar")
st.subheader("Tracking high-velocity global internet topics with AI")

# Sidebar slider control
st.sidebar.header("Radar Settings")
post_limit = st.sidebar.slider("Number of global trends to scan", 10, 50, 25)

# The primary app action button
if st.button("Scan Global Network"):
    with st.spinner("Tapping into global stream and activating AI brains..."):
        
        # 1. Fetch the live traffic data
        raw_data = fetch_trending_topics(limit=post_limit)
        
        if raw_data.empty:
            st.error("Could not reach the global information stream. Please check your internet!")
        else:
            # 2. Run the text data through our AI model
            analyzed_data = analyze_sentiment(raw_data)
            
            # 3. Formulate high-level metrics
            total_topics = len(analyzed_data)
            positive_count = len(analyzed_data[analyzed_data["sentiment"] == "POSITIVE"])
            pos_percentage = int((positive_count / total_topics) * 100) if total_topics > 0 else 0
            
            # Show large summary cards
            col1, col2 = st.columns(2)
            col1.metric("High-Velocity Topics Captured", total_topics)
            col2.metric("Positive Sentiment Energy", f"{pos_percentage}%")
            
            st.markdown("---")

            # 📊 NEW VISUAL LAYER: Charts side-by-side
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.write("#### 📈 Top 10 Most Demanded Global Topics")
                # Create a horizontal bar chart showing the highest viewed topics
                top_10 = analyzed_data.nlargest(10, 'views')
                fig_bar = px.bar(
                    top_10, 
                    x='views', 
                    y='title', 
                    orientation='h',
                    color='sentiment',
                    color_discrete_map={'POSITIVE': '#00CC96', 'NEGATIVE': '#EF553B'},
                    title="Traffic Volume by Topic"
                )
                fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with chart_col2:
                st.write("#### 🌓 Global Sentiment Split")
                # Create a clean pie chart showing the percentage of positive vs negative news
                fig_pie = px.pie(
                    analyzed_data, 
                    names='sentiment',
                    color='sentiment',
                    color_discrete_map={'POSITIVE': '#00CC96', 'NEGATIVE': '#EF553B'},
                    hole=0.4,
                    title="Overall Vibe Distribution"
                )
                fig_pie.update_layout(template="plotly_dark")
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("---")
            
            # 4. Display the interactive data dashboard
            st.write("### Live Global Interest Feed")
            st.dataframe(
                analyzed_data[["title", "views", "sentiment", "confidence"]],
                use_container_width=True
            )





