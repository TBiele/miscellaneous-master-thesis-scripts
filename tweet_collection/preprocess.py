import nltk
import pandas as pd


def remove_stop_words(language, text):
    german_stop_words = nltk.corpus.stopwords.words(language)
    input_text_split = text.split()
    return " ".join([w for w in input_text_split if w not in german_stop_words])


def remove_stop_words_from_csv(csv_name):
    df = pd.read_csv(f"csv/{csv_name}.csv", index_col=0)
    df["content"] = df["content"].apply(lambda text: remove_stop_words("english", text))
    df.to_csv(f"csv/{csv_name}_condensed.csv")


if __name__ == "__main__":
    remove_stop_words_from_csv("train")
