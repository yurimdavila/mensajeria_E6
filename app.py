from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen=""

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/validarUsuario', methods=['GET', 'POST'])
def validarUsuario():
    if request.method=='POST':
        usu=request.form['txtusuario']
        usu=usu.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=request.form['txtpass']
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        #Encriptación de la contraseña:
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
        
        respuesta=controlador.validar_usuario(usu, passw2)
        
        global email_origen
        
        if len(respuesta)==0:
            email_origen=""
            mensaje1="ERROR DE AUTENTICACIÓN!!! Lo invitamos a verificar su usuario(correo) y contraseña"
            return render_template('informacion.html', datas=mensaje1)       # la variable 'datas' puede ser llamada como desee
        else:
            email_origen=usu
            respuesta2= controlador.lista_destinatarios(usu)
            return render_template('principal.html', datas=respuesta2)
        
@app.route('/registrarUsuario', methods=['GET', 'POST'])
def registrarUsuario():
    if request.method=='POST':
        nombre=request.form['txtnombre']
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email=request.form['txtusuario2registro']
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=request.form['txtpassregistro']
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        #Encriptación de la contraseña:
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
        
        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-", "")
        codigo2=codigo2.replace(" ", "")
        codigo2=codigo2.replace(":", "")
        codigo2=codigo2.replace(".", "")
        
        mensaje="Sr(a) "+nombre+", su código de activación es:\n\n"+codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la sección de login y activar su cuenta.\n\nMuchas Gracias "
        
        envioemail.enviar(email,mensaje,"Codigo de Activacion")
        
        respuesta=controlador.registrar_usuario(nombre, email, passw2, codigo2)
        
        return render_template('informacion.html', datas=respuesta)     
    
@app.route('/activarUsuario', methods=['GET', 'POST'])
def activarUsuario():
    if request.method=='POST':
        codigo=request.form['txtcodigo']
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        respuesta=controlador.activar_Usuario(codigo)
        
        if len(respuesta)==0:
            mensaje3="El código de activación es erróneo, verifíquelo."
        else:
            mensaje3="El usuario se ha activado correctamente"
        return render_template('informacion.html', datas=mensaje3)       

@app.route('/enviarMAIL', methods=['GET', 'POST'])
def enviarMAIL():
    if request.method=='POST':
        emailDestino=request.form['emailDestino']
        emailDestino=emailDestino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        asunto=request.form['asunto']
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        mensaje=request.form['mensaje']
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        controlador.registrar_mail(email_origen,emailDestino,asunto,mensaje)
        
        mensaje2="Sr(a) usuario, usted recibió un mensaje nuevo, por favor ingrese a la plataforma para leer su email en la pestaña Historial. \n\n Muchas gracias."
        envioemail.enviar(emailDestino, mensaje2, "Nuevo mensaje enviado")
        return "Mensaje enviado satisfactoriamente"

@app.route("/HistorialEnviados",methods=["GET","POST"])
def HistorialEnviados():
    resultado=controlador.ver_enviados(email_origen)
    return render_template("respuesta.html",datas=resultado)

@app.route("/HistorialRecibidos",methods=["GET","POST"])
def HistorialRecibidos():
    resultado=controlador.ver_recibidos(email_origen)
    return render_template("respuesta.html",datas=resultado)

@app.route("/actualizacionPassword",methods=["GET","POST"])
def actualizacionPassword():
    if request.method=="POST":
        pass1=request.form["pass"]
        pass1=pass1.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2=pass1.encode()
        passw2=hashlib.sha384(passw2).hexdigest()
               
        controlador.actualizapass(passw2,email_origen)
        return "ActualizaciÓn de password satisfactoria"

if __name__=="__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)