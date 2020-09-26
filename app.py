from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    print('Source Service: ', request.form['src_service'])
    print('Destination Service: ', request.form['dest_service'])
    print('Playlist URL: ', request.form['playlist_url'])
    return 'doing things!'


if __name__ == '__main__':
    app.run(debug=True)
