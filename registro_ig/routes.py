from operator import index
from registro_ig import app

@app.route("/")
def index():
    return "Funcionando"
