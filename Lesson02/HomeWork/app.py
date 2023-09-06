from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome', methods=['POST'])
def welcome():
    name = request.form['name']
    email = request.form['email']

    # Создание куки-файла с данными пользователя
    response = make_response(redirect('/greet'))
    response.set_cookie('user_data', f'{name}|{email}')

    return response


@app.route('/greet')
def greet():
    user_data = request.cookies.get('user_data')
    if user_data:
        name, _ = user_data.split('|')
        return render_template('greet.html', name=name)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    # Удаление куки-файла с данными пользователя
    response = make_response(redirect('/'))
    response.delete_cookie('user_data')
    return response


if __name__ == '__main__':
    app.run()