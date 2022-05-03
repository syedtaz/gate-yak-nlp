from transformers import BartForSequenceClassification, BartTokenizer
import pandas as pd
import numpy as np
from tqdm import tqdm


def create_queries():
    classes = [
        "campus life",
        "drugs",
        "alcohol",
        "greek life",
        "humor",
        "pop culture",
        "dating",
        "sex",
        "sexuality",
        "race",
        "ethnicity",
    ]

    queries = ["This sentence is about " + x + "." for x in classes]
    q_dict = {k: v for k, v in zip(classes, queries)}

    q_dict.update(
        {
            "profanity": "This sentence contains profanity.",
            "question": "This sentence is asking a question.",
            "announcement": "This sentence is an announcement.",
        }
    )

    return q_dict


def classify(text: str, tokenizer, model, queries: dict[str, str]):
    premise = text
    p_vec = {}

    for klass, query in queries.items():
        input_ids = tokenizer.encode(premise, query, return_tensors="pt")
        logits = model(input_ids)[0]
        entail_contradiction_logits = logits[:, [0, 2]]
        probs = entail_contradiction_logits.softmax(dim=1)
        prob = probs[:, 1].item() * 100
        p_vec[klass] = prob

    return p_vec


def main():
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-mnli")
    model = BartForSequenceClassification.from_pretrained("facebook/bart-large-mnli")

    df = pd.read_csv(
        "/Users/tazmilur/Academics/spring-2022/gate-yak-nlp/data/yikyak.csv"
    )  # Change to pathlib
    df = df.drop(["vulgarity"], axis=1)
    df["content"].replace("", np.nan, inplace=True)
    df.dropna(subset=["content"], inplace=True)

    queries = create_queries()

    lst = []
    for i in tqdm(df["content"]):

        lst.append(classify(i, tokenizer, model, queries))

    final = pd.concat([df, pd.DataFrame(lst)], axis=1)
    final.to_csv(
        "/Users/tazmilur/Academics/spring-2022/gate-yak-nlp/data/final.csv"
    )  # Change to pathlib


if __name__ == "__main__":
    main()
