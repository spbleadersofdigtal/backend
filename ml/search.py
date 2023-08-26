import pickle

from annoy import AnnoyIndex
from sentence_transformers import SentenceTransformer

model = None
data = None
index = None


def get_model():
    global model
    if not model:
        model = SentenceTransformer("sentence-transformers/LaBSE")
    return model


def get_data():
    global data
    if not data:
        with open("ml/data.pic", "rb") as file:
            data = pickle.load(file)
    print(len(data))
    return data


def get_index():
    global index
    if not index:
        index = AnnoyIndex(768, "angular")
        index.load("ml/index.ann")
    return index


def search(search_string):
    embs = get_model().encode([search_string])[0]
    indexes = get_index().get_nns_by_vector(embs, 5)
    res = []
    for i in indexes:
        res.append(get_data()[i])
    return list(
        map(
            lambda x: {
                "logo": x["image"],
                "name": x["name"],
                "description": x["description"],
            },
            res,
        )
    )
