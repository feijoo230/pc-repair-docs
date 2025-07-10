import os
from flask import Blueprint, request, render_template, redirect, url_for, send_from_directory, current_app, flash
from werkzeug.utils import secure_filename
from .models import get_collection
from .utils.pdf_generator import generar_pdf
from .utils.helpers import formatear_fecha_larga 
from datetime import datetime
from bson.objectid import ObjectId

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "static/uploads"
PDF_FOLDER = "static/pdf"

@main.route("/", methods=["GET", "POST"])
def formulario():
    upload_path_abs = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    pdf_path_abs = os.path.join(current_app.root_path, PDF_FOLDER)
    os.makedirs(upload_path_abs, exist_ok=True)
    os.makedirs(pdf_path_abs, exist_ok=True)

    if request.method == "POST":
        hoy = datetime.today()
        data = {
            "fecha": request.form.get("fecha"),
            "descripcion": request.form.get("descripcion"),
            "caracteristicas": request.form.get("caracteristicas"),
            "inventario": request.form.get("inventario"),
            "responsable": request.form.get("responsable"),
            "tecnico_responsable": request.form.get("tecnico_responsable"),
            "observaciones": request.form.get("observaciones"),
            "conclusion": request.form.get("conclusion"),
            "fecha_creacion_corta": hoy.strftime("%d/%m/%Y"),
            "fecha_creacion_larga": formatear_fecha_larga(hoy)
        }

        
        fotos = request.files.getlist("fotos")
        saved_filenames = [] 
        for foto in fotos:
            if foto and foto.filename != "":
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(upload_path_abs, filename))
                saved_filenames.append(filename)

        data["fotos"] = saved_filenames
        data['base_path'] = f"file://{current_app.root_path}"
                
        inserted = get_collection().insert_one(data.copy())
        data["_id"] = str(inserted.inserted_id)

        
        pdf_filename = f"informe_{data['_id']}.pdf"
        pdf_output_path = os.path.join(pdf_path_abs, pdf_filename)
        generar_pdf(data, pdf_output_path)

        return redirect(url_for("main.descargar_pdf", filename=pdf_filename))

    return render_template("form.html", fecha_hoy=datetime.today().strftime("%d/%m/%Y"))

@main.route("/pdf/<filename>")
def descargar_pdf(filename):
    pdf_directory = os.path.join(current_app.root_path, PDF_FOLDER)
    return send_from_directory(pdf_directory, filename, as_attachment=True)

@main.route("/historial")
def historial():
    informes_collection = get_collection()
    lista_de_informes = list(informes_collection.find().sort("fecha", -1))  
    return render_template("historial.html", informes=lista_de_informes)


@main.route("/editar/<informe_id>", methods=["GET", "POST"])
def editar_informe(informe_id):
    informes_collection = get_collection()
    informe_a_editar = informes_collection.find_one({"_id": ObjectId(informe_id)})

    if not informe_a_editar:
        flash("Informe no encontrado.", "danger")
        return redirect(url_for("main.historial"))

    if request.method == "POST":
        datos_actualizados = {
            "fecha": request.form.get("fecha"),
            "descripcion": request.form.get("descripcion"),
            "caracteristicas": request.form.get("caracteristicas"),
            "inventario": request.form.get("inventario"),
            "responsable": request.form.get("responsable"),
            "tecnico_responsable": request.form.get("tecnico_responsable"),
            "observaciones": request.form.get("observaciones"),
            "conclusion": request.form.get("conclusion"),
        }
        
        
        informes_collection.update_one(
            {"_id": ObjectId(informe_id)},
            {"$set": datos_actualizados}
        )
        
        datos_completos = {**informe_a_editar, **datos_actualizados}

        try:
            fecha_obj = datetime.strptime(datos_completos["fecha_creacion_corta"], "%d/%m/%Y")
            datos_completos["fecha_creacion_larga"] = formatear_fecha_larga(fecha_obj)
        except (KeyError, ValueError):
            datos_completos["fecha_creacion_larga"] = formatear_fecha_larga(datetime.today())

        pdf_filename = f"informe_{informe_id}.pdf"
        pdf_path_abs = os.path.join(current_app.root_path, 'static', 'pdf')
        pdf_output_path = os.path.join(pdf_path_abs, pdf_filename)
        generar_pdf(datos_completos, pdf_output_path)
        
        #flash("Informe actualizado con éxito.", "success") hasta averiaguar los fallos 
        return redirect(url_for("main.historial"))
    
    return render_template("editar_informe.html", informe=informe_a_editar)

@main.route("/eliminar/<informe_id>", methods=["POST"])
def eliminar_informe(informe_id):
    try:
        informes_collection = get_collection()
        
        informes_collection.delete_one({"_id": ObjectId(informe_id)})
        
        print(f"Informe con ID {informe_id} eliminado exitosamente de la DB.")

    except Exception as e:

        print(f"Error al intentar eliminar el informe {informe_id}: {e}")

    
    return redirect(url_for("main.historial"))