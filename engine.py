from transformers import pipeline
import pandas as pd


print("Initializing AI Engine... Please wait standard loading time...")


sentiment_classifier = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(df):
    if df.empty:
        return df
    titles = df["title"].tolist()
    results = sentiment_classifier(titles)
    df["sentiment"] = [res["label"] for res in results]
    df["confidence"] = [round(res["score"] * 100, 1) for res in results]
    return df

    