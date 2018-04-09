import psycopg2
from flask import Flask, request

application = Flask(__name__)

application.secret_key = 'badpassword123'


class Database(object):

    @staticmethod
    def update(state, comment):
        client = psycopg2.connect(database='databasename',
                                  user='userid',
                                  password='password',
                                  host='databse.address.com',
                                  port='5432')
        cur = client.cursor()

        upsertsql = 'INSERT INTO COMMENTS (state, comment) VALUES (%s, %s) ON CONFLICT (state) DO UPDATE SET comment = %s'

        cur.execute(upsertsql, (state, comment, comment))

        client.commit()
        cur.close()
        client.close()


@application.route('/post')
def post_to_mongo():
    state = request.args.get('state')
    comment = request.args.get('comment')

    if state is None:
        return '<html><body><h3>State Field Missing!</h3></body></html>'
    if comment is None:
        return '<html><body><h3>Comment Must Not Be Blank!</h3></body></html>'
    Database.update(state=state, comment=comment)
    return '<html><body><h6>Comment Posted!<br />State: {}<br />Comment: {}</h6></body></html>'.format(state, comment)


if __name__ == '__main__':
    application.run(debug=True, port=80)
