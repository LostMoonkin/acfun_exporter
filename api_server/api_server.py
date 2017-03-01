from flask import Flask
from flask_restful import Resource, Api
import config
import db_op
import json

app = Flask(__name__)
api = Api(app)


class ArticleAPI(Resource):

    def get(self, date):
        sqlite_op = db_op.SqliteOp(config.DB_FILE)
        if date.lower() == 'latest':
            articles = sqlite_op.get_latest_articles()
        else:
            articles = sqlite_op.get_articles(date)
        res = []
        for article in articles:
            res.append({
                'title': article[0],
                'url': article[1],
                'type': article[2],
                'info': json.loads(article[3])
            })

        return res

api.add_resource(ArticleAPI, '/api/v0.1/top_articles/<date>')

if __name__ == '__main__':
    app.run(port=config.port, debug=True)
