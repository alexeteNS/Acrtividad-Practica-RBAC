from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_total_segura_iti'

USUARIOS_DB = {
    "admin": {"password": "123", "rol": "administrador"},
    "alumno": {"password": "456", "rol": "estudiante"}
}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    usuario = request.form.get('usuario')
    password = request.form.get('password')

    if usuario in USUARIOS_DB and USUARIOS_DB[usuario]['password'] == password:
        session['usuario'] = usuario
        session['rol'] = USUARIOS_DB[usuario]['rol']
        if session['rol'] == 'administrador':
            return redirect(url_for('panel_admin'))
        return redirect(url_for('panel_estudiante'))

    return render_template('login.html', error='Usuario o contraseña incorrectos')


@app.route('/panel-admin')
def panel_admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if session.get('rol') != 'administrador':
        return render_template('403.html'), 403
    return render_template('panel_admin.html', usuario=session['usuario'], usuarios=USUARIOS_DB)


@app.route('/panel-estudiante')
def panel_estudiante():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if session.get('rol') != 'estudiante':
        return render_template('403.html'), 403
    return render_template('panel_estudiante.html', usuario=session['usuario'], rol=session['rol'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    print('Servidor corriendo en: http://127.0.0.1:5000/login')
    app.run(debug=True)
