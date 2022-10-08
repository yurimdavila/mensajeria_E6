#EL controlador sirve para administrar mejor las funciones para el uso de la BD, para que el código no se extienda demasiado

import sqlite3

#El usuario y password vienen del app.py
def validar_usuario(usuario, password):
    db=sqlite3.connect("mensajeria.db3")                      #conexion a la BD
    db.row_factory=sqlite3.Row                                #Asigno a mi variable todas las cabeceras(id, nombre se convierten en variables)
    cursor=db.cursor()                                        #sirve para poder crear la consulta
    consulta="SELECT * FROM usuarios WHERE correo='"+usuario+"' AND password='"+password+"' AND estado='1'"    #se crea la cadena string que permite realizar la consulta
    cursor.execute(consulta)                                  #se ejecuta la consulta
    resultado=cursor.fetchall()                               #la respuesta se recibe con resultado
    return resultado                                          #devuelvo resultado como función

def registrar_usuario(nombre, correo, password, codigo):
    try:
        db=sqlite3.connect("mensajeria.db3")                      
        db.row_factory=sqlite3.Row                                
        cursor=db.cursor()                                        
        consulta="INSERT INTO usuarios (nombreUsuario, correo, password, estado, codigoActivacion) VALUES ('"+nombre+"', '"+correo+"', '"+password+"', '0', '"+codigo+"')"
        print("op 1")
        cursor.execute(consulta)     
        print("op 2")                             
        db.commit()
        print("op 3")                             
        return "Usuario registrado satisfactoriamente"
    except:
        return "¡Error! No es posible registrar al usuario debido a que el CORREO y/o NOMBRE DE USUARIO existen. Lo invitamos a modificar los campos pertinentes"

def activar_Usuario(codigo):
    db=sqlite3.connect("mensajeria.db3")                      
    db.row_factory=sqlite3.Row                                
    cursor=db.cursor()                                        
    consulta="UPDATE usuarios SET estado='1' WHERE codigoActivacion='"+codigo+"' "
    cursor.execute(consulta)                                  
    db.commit()  
    
    consulta2= "SELECT * FROM usuarios WHERE codigoActivacion='"+codigo+"' AND estado='1' " 
    cursor.execute(consulta2) 
    resultado=cursor.fetchall()                           
    return resultado

def lista_destinatarios(usuario):
    db=sqlite3.connect("mensajeria.db3")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="SELECT * FROM usuarios WHERE correo<>'"+usuario+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def registrar_mail(origen, destino, asunto, mensaje):
    db=sqlite3.connect("mensajeria.db3")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="INSERT INTO mensajeria (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) VALUES ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def ver_enviados(correo):
    db=sqlite3.connect("mensajeria.db3")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="SELECT m.asunto,m.mensaje,m.fecha, m.hora, u.nombreUsuario FROM usuarios u, mensajeria m WHERE u.correo=m.id_usu_recibe AND m.id_usu_envia='"+correo+"' ORDER BY fecha DESC,hora DESC"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def ver_recibidos(correo):
    db=sqlite3.connect("mensajeria.db3")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="SELECT m.asunto,m.mensaje,m.fecha, m.hora, u.nombreUsuario FROM usuarios u, mensajeria m WHERE u.correo=m.id_usu_envia AND m.id_usu_recibe='"+correo+"' ORDER BY fecha DESC,hora DESC"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def actualizapass(password, correo):
    db=sqlite3.connect("mensajeria.db3")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="UPDATE usuarios SET password='"+password+"' WHERE correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"