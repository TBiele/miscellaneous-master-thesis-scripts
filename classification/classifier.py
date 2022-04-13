# Was only used for testing

import numpy as np
import nltk
import pickle
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification


def initialize_classifier(model_directory, number_of_labels):
    return AutoModelForSequenceClassification.from_pretrained(
        model_directory, num_labels=number_of_labels
    )


def classify_message_binary(classifier, base_model, input_message, threshold):
    # Remove stop words
    german_stop_words = nltk.corpus.stopwords.words("german")
    input_message_split = input_message.split()
    processed_message = " ".join(
        [w for w in input_message_split if w not in german_stop_words]
    )
    # Tokenize message
    tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=True)
    input = tokenizer(
        processed_message,
        max_length=512,
        padding=True,
        truncation=True,
        return_tensors="pt",
    )

    # Classify message
    logits = classifier(**input).logits.tolist()[0]
    predictions = np.exp(logits) / np.sum(np.exp(logits))
    predicted_label = "irrelevant"
    if predictions[1] > threshold:
        predicted_label = "relevant"
    return predicted_label, predictions


def classify_message(model_directory, input_message, threshold):
    # Load mapping from ids to labels
    id2label = pickle.load(open(f"{model_directory}/id2label.p", "rb"))
    number_of_labels = len(id2label.keys())

    # Initialize model
    classification_model = AutoModelForSequenceClassification.from_pretrained(
        model_directory + "/model/", num_labels=number_of_labels
    )

    # Remove stop words
    german_stop_words = nltk.corpus.stopwords.words("german")
    input_message_split = input_message.split()
    processed_message = " ".join(
        [w for w in input_message_split if w not in german_stop_words]
    )
    # Tokenize message
    tokenizer = AutoTokenizer.from_pretrained(
        "distilbert-base-german-cased", use_fast=True
    )
    input = tokenizer(
        processed_message,
        max_length=512,
        padding=True,
        truncation=True,
        return_tensors="pt",
    )

    # Classify message
    logits = classification_model(**input).logits.tolist()[0]
    predictions = np.exp(logits) / np.sum(np.exp(logits))

    # Determine predicted labels
    prediction_booleans = [value > threshold for value in predictions]
    predicted_label_indices = np.where(prediction_booleans)[0].flatten().tolist()
    predicted_labels = [id2label[val] for val in predicted_label_indices]
    return predicted_labels


if __name__ == "__main__":
    # Uncomment, set variables and run to test classification model
    message = MY_MESSAGE_TEXT

    # Multi-label classification
    # model_directory = MULT_MODEL_DIR
    # threshold = 0.18
    # labels = classify_message(
    #     model_directory=f"input/{model_directory}",
    #     input_message=message,
    #     threshold=threshold,
    # )
    # print("predicted labels:", labels)

    # Binary classification
    # model_directory = BINARY_MODEL_DIR
    # classifier = initialize_classifier(f"input/{model_directory}", 2)
    # prediction_result = classify_message_binary(
    #     classifier=classifier,
    #     base_model="distilbert-base-german-cased",
    #     input_message=message,
    #     threshold=0.5,
    # )
    # print(prediction_result)
