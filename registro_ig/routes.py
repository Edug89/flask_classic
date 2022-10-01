from flask import render_template,request,redirect,url_for
from registro_ig import app
from registro_ig.forms import MovementForm
from registro_ig.models import select_all, insert, delete_by,select_by,update_by
from datetime import date

@app.route("/")
def index():
    #Consultar todos los datos de la base de datos
    registros = select_all()
    return render_template("index.html", pageTitle = "Todos", data=registros)

@app.route("/new", methods=["GET", "POST"])
def new():
    form = MovementForm()
    if request.method == "GET":
        return render_template("new.html", el_formulario=form, pageTitle="")
    else:
        if form.validate():
            insert([form.date.data.isoformat(),
                    form.concept.data,
                    form.quantity.data
                    ])
                    
            return redirect(url_for("index"))

        else:
            return render_template("new.html", el_formulario=form, pageTitle="Alta")













def form_to_list(id, form):
    return [str(id),
            form['date'], 
            form['concept'],
            form['quantity']
            ]


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def borrar(id):
    if request.method == "GET":
        """
        1. Consultar en movimientos.txt y recueperar el registro con id al de la petición
        2. Devolver el formulario html con los datos de mi registro, no modificables 
        3. Tendrá un boton que diga confirmar.
        """
        registro_definitivo = select_by(id)
        if registro_definitivo:
            return render_template("delete.html", registro=registro_definitivo)
        else:
            return redirect(url_for("index"))
    else:
        """
            Borrar el registro
            1. abrir fichero movimientos.txt en lectura
            2. abrir fichero nmovimientos.txt en escritura
            3. copiar todo los registros uno a uno en su orden exceptuando el que queremos borrar
            4. borrar movimiento.txt
            5. renombrar nmovimeintos.txt a movmientos.txt
        """       
        delete_by(id)

        return redirect(url_for("index"))

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

@app.route("/update/<int:id>", methods=["GET", "POST"])
def modifica(id):
    if request.method == "GET":   
        registro_definitivo = select_by(id)
        if registro_definitivo:
            return render_template("update.html", pageTitle="Modificar", registro=registro_definitivo)
        else:
            return redirect(url_for("index")) 
    else:
       
        errores = validaFormulario(request.form)
        if not errores:           
            update_by(fomr_to_list(id,request.form))
            return redirect(url_for("index"))

        else:                         
            return render_template("update.html", pageTitle="Modificar", msgErrors=errores, registro=fomr_to_list(id,request.form))

def fomr_to_list(id,form):   
    return [str(id),form['date'],form['concept'],form['quantity']]