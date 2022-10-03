import math
import logging
import joblib
import pathlib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# import json

import azure.functions as func

# --- Loading model files ---
(reco_als, sparse_matrix, article_lookup_cat_id, user_lookup_id_cat) = joblib.load(pathlib.Path('data', 'collaborative_recommender.pkl'))
(article_embedding, data_train) = joblib.load(pathlib.Path('data', 'content_based_recommender.pkl'))

# file = open(pathlib.Path('data','articles_embeddings.pickle'),"rb")
# article_embedding = pickle.load(file)


# --- Define recommendation functions ---

def get_collaborative_recommendations(user_id, reco_size):
    user_codes = user_lookup_id_cat['user_cat'][user_id]
    codes, scores = reco_als.recommend(user_codes, sparse_matrix[user_codes], N=reco_size, filter_already_liked_items=True)
    recommendations = pd.DataFrame(np.vstack((codes, scores)).T, columns=['article_id', 'score'])
    recommendations['article_id'] = recommendations['article_id'].apply(lambda x: article_lookup_cat_id['article_id'][x])
    return recommendations


def get_content_based_recommendations(user_id, reco_size=5):
    print(user_id)

    # --- Compute viewed mean_embedding
    viewed_train = data_train[data_train.user_id == user_id]['article_id']
    # if len(viewed_train) < 1: return
    mean_vector_viewed_train = get_mean_vector(viewed_train.values)

    # --- Compute cosine similarity the mean of the viewed articles and the rest
    A = article_embedding.copy()
    B = mean_vector_viewed_train
    A[viewed_train.values] = -B  # Discard read articles
    cosine = cosine_similarity(A, B.reshape(1, -1))

    recommendations = recommend_articles(cosine, reco_size)
    return recommendations


def get_reco(user_id, reco_size):

    # Get Collaborative Filtering Recommendations
    candidates_collaborative_filtering = get_collaborative_recommendations(user_id, reco_size)

    # Get Content Based Recommendations
    candidates_content_based_filtering = get_content_based_recommendations(user_id, reco_size)

    # Select some of them at random
    cf_size, cbf_size = math.floor(reco_size/2), math.ceil(reco_size/2)  # 1/2 vs 1/2 avec priorité cbf
    # cf_size, cbf_size = round(reco_size/3*1), round(reco_size/3*2)  # 1/3 vs 2/3
    p_cf = candidates_collaborative_filtering.sample(cf_size)
    p_cbf = candidates_content_based_filtering.sample(cbf_size)

    # Return the selected articles_id
    return np.concatenate((p_cf['article_id'].values, p_cbf['article_id'].values)). astype(int)


def recommend_articles(cosine, reco_size):
    cos = pd.DataFrame(cosine, columns=['cosine_sim'])
    selection = cos.sort_values('cosine_sim', ascending=False)[:reco_size]
    selection.reset_index(inplace=True)
    selection.rename(columns={'index': 'article_id'}, inplace=True)
    return selection


def get_mean_vector(articles_idx):
    apply_numpy = lambda x: article_embedding[x].mean(axis=0)
    return apply_numpy(articles_idx)


# --- Run Azure MAIN function ---

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')
    if not user_id:
        try:
            req_body = req.get_json()
            user_id = req_body.get('user_id')
        except ValueError:
            pass

    reco_size = req.params.get('reco_size')
    if not reco_size:
        try:
            req_body = req.get_json()
            reco_size = req_body.get('reco_size')
        except ValueError:
            reco_size = 5

    if user_id:
        article_ids = get_reco(int(user_id), int(reco_size))
        str_articles = ", ".join([str(x) for x in article_ids])
        return func.HttpResponse(str_articles)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_id in the query string or in the request body for a personalized response.",
             status_code=200
        )
