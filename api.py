from flask import Flask,render_template, request, redirect

from DB import DB
from main import update_deals, get_existing_deals

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    deals = get_existing_deals()
    return render_template('index.html', deals=deals)

@app.route('/list', methods=['GET'])
def list():
    db = DB()
    deals = db.get_saved_deals()
    return render_template('list.html', deals=deals)

@app.route('/update', methods=['POST'])
def update():
    update_deals()
    return redirect("/", code=302)

@app.route('/hide', methods=['POST'])
def hide():
    db = DB()
    id = request.json.get('id')
    db.toggle_hide(id)
    next_id = db.get_next_visible_deal_id(id)['id']
    return redirect(f"/#{next_id}", code=302)

@app.route('/favorite', methods=['POST'])
def favorite():
    db = DB()
    id = request.json.get('id')
    db.toggle_favorite(id)
    next_id = db.get_next_visible_deal_id(id)['id']
    return redirect(f"/#{next_id}", code=302)


@app.route('/add', methods=['POST'])
def add():
    db = DB()
    id = request.json.get('id')
    db.toggle_save(id)
    next_id = db.get_next_visible_deal_id(id)['id']
    return redirect(f"/#{next_id}", code=302)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8850)
