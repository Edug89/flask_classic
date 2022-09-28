from flask import render_template,request,redirect,url_for
from registro_ig import app
from registro_ig.models import select_all, insert
from datetime import date

@app.route("/")
def index():
    #Consultar todos los datos de la base de datos
    registros = select_all()
    return render_template("index.html", pageTitle = "Todos", data=registros)

@app.route("/new", methods=["GET", "POST"])
def alta():
    if request.method == "GET":
        return render_template("new.html", pageTitle="Alta", 
                               dataForm={})
    else:
        """
            1. Validar el formulario
                Fecha valida y <= hoy
            2. Concepto no sea vacío
            3. Cantidad no se cero     
        """
        errores = validaFormulario(request.form)

        if not errores:
            #Obtener el nuevo id
            insert([request.form['date'],
                    request.form['concept'],
                    request.form['quantity']
                  ])
            return redirect(url_for("index"))
        else:
            return render_template("new.html", pageTitle="Alta", msgErrors=errores, dataForm=dict(request.form))

def validaFormulario(camposFormulario):
    errores = []
    hoy = date.today().isoformat()
    if camposFormulario['date'] > hoy:
        errores.append("La fecha introducida es el futuro.")

    if camposFormulario['concept'] == "":
        errores.append("Introduce un concepto para la transacción.")

    #La primera condición es para que el número sea distinto de cero
    #la segunda condición es para que el campo no esté vacío
    if camposFormulario["quantity"] == "" or float(camposFormulario["quantity"]) == 0.0:
        errores.append("Introduce una cantidad positiva o negativa.")

    return errores

def form_to_list(id, form):
    return [str(id),
            form['date'], 
            form['concept'],
            form['quantity']
            ]
