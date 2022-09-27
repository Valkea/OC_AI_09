import logging
import joblib
# import json

import azure.functions as func

(reco_als, sparse_matrix) = joblib.load('globo_recommender.pkl')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('user_id')

    if user_id:
        codes, scores = reco_als.recommend(user_id, sparse_matrix[user_id], N=5, filter_already_liked_items=True)
        logging.debug(codes, scores)
        return func.HttpResponse(f"{codes}")
        # return json.dumps(codes)
        # return func.HttpResponse(f"The targetted used_id is {user_id}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_id in the query string or in the request body for a personalized response.",
             status_code=200
        )
