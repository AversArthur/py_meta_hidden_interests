from flask import Flask, request, render_template, redirect, url_for
from meta_hidden_interests_extractor import get_hidden_interests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Получаем search_key из запроса
    search_key = request.args.get('search_key', '')
    print(f"Received search_key from GET: {search_key}")

    page = int(request.args.get('page', 1))
    per_page = 50

    if request.method == 'POST':
        search_key = request.form['search_key']
        print(f"Search key received via POST: {search_key}")
        return redirect(url_for('index', search_key=search_key, page=1))  # Используем redirect с параметрами

    if not search_key:
        print('No search key, returning empty page.')
        return render_template('index.html', search_key=search_key, page=page, total_pages=0, data=[])

    # Если есть search_key, вызываем функцию для получения данных
    all_data = get_hidden_interests(search_key)
    print(f"Data received: {len(all_data)} items")

    offset = (page - 1) * per_page
    data_for_page = all_data[offset:offset + per_page]

    total_items = len(all_data)
    total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)

    return render_template('index.html', data=data_for_page, search_key=search_key, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True, port=5100)
