import time

from quart import Quart, render_template, request, redirect

from DB import DB
from main import update_deals, get_existing_deals

app = Quart(__name__)


@app.route('/', methods=['GET'])
async def index():
    deals = get_existing_deals()
    return await render_template('index.html', deals=deals)


@app.route('/list', methods=['GET'])
async def list():
    db = DB()
    deals = db.get_saved_deals()
    return await render_template('list.html', deals=deals)

@app.route('/last-update', methods=['GET'])
async def last_update():
    db = DB()
    timestamp_row = db.get_latest_timestamp()
    timestamp = timestamp_row.time
    cur_time = time.time()

    diff = (cur_time - timestamp) * 1000

    if diff < 60:
        return {'number': diff, 'unit': 'seconds'}
    elif diff < 60*60:
        return {'number': diff/60, 'unit': 'minutes'}
    elif diff < 60*60*24:
        return {'number': diff/(60*60), 'unit': 'hours'}
    else:
        return {'number': diff/(60*60*24), 'unit': 'days'}



@app.route('/update', methods=['POST'])
async def update():
    update_deals()
    return redirect("/", code=302)


@app.route('/hide', methods=['POST'])
async def hide():
    db = DB()
    id = (await request.json).get('id')
    db.toggle_hide(id)
    next_id = db.get_next_visible_deal_id(id)['id']
    return redirect(f"/#{next_id}", code=302)


@app.route('/favorite', methods=['POST'])
async def favorite():
    db = DB()
    id = (await request.json).get('id')
    db.toggle_favorite(id)
    next_id = db.get_next_visible_deal_id(id)['id']
    return redirect(f"/#{next_id}", code=302)


@app.route('/add', methods=['POST'])
async def add():
    db = DB()
    id = (await request.json).get('id')
    db.toggle_save(id)
    next_id = db.get_next_visible_deal_id(id)['id']
    return redirect(f"/#{next_id}", code=302)


@app.route('/manual/add', methods=['POST'])
async def manual_add():
    db = DB()
    item = (await request.json).get('item')
    db.manual_add(item)
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8850)
