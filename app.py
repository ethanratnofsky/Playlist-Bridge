from flask import Flask, render_template, request
from api.bridger import bridge

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    form = request.form
    print('Source Service: ', form['src_service'])
    print('Destination Service: ', form['dest_service'])
    print('Playlist URL: ', form['playlist_url'])
    # bridge(form['src_service'], form['dest_service'], form['playlist_url'])
    return 'doing things!'


if __name__ == '__main__':
    app.run(debug=True)
