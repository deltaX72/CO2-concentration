from flask import render_template
from app import app
from app.forms import InputDataForm

@app.route('/')
@app.route('/index')
def index():
    form = InputDataForm()
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)