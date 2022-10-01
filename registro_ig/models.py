import sqlite3
from config import ORIGIN_DATA

def select_all():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    result = cur.execute("SELECT id, date, concept, quantity from movements order by date;")

    filas = result.fetchall()
    columnas = result.description
    resultado = []
    for fila in filas:
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    conn.close()

    """
    Es lo mismo que los dos FOR de arriba:
    for fila in filas:
        d = {}
        for posicion, campo in enumerate(columnas):
            d[campo[0]] = fila[posicion]
        resultado.append(d)
    """

    return resultado

def insert(registro):
    """
    INSERT INTO moviments(date,concept,quantity) values(?,?,?)
    params

    cur.execute("INSERT INTO moviments(date,concept,quantity) values(?,?,?), ['20022-04-08','cumple',-80]")

    importante 
    con.commit() antes de hacer el con.close()
    """

    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    cur.execute("INSERT INTO movements(date,concept,quantity) values(?,?,?)",registro)

    con.commit()
    con.close()


def select_by(id):
    """
    Devolverá un registro con el id de la entrada o vacío si no lo encuentra
    ORIGIN_DATA
    """
    #print(id) #TODO se lo he visto a Enric pero no le veo cambio.
    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("SELECT id, date, concept, quantity FROM movements WHERE id=? " , (id,))
    filas = result.fetchall()
    con.close()
    return filas[0]


def delete_by(id):
    """
    Borrará el registro cuyo id coincide con el de la entrada
    ORIGIN_DATA
    """
    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("DELETE FROM movements WHERE id=? " , id)
    con.commit()
    con.close()


def update_by(registro_mod):
    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("UPDATE movements SET date=?,concept=?,quantity=? WHERE id=?; " , registro_mod)
    con.commit()
    con.close()