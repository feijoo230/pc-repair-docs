from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def generar_pdf(data, output_path):
    # Definir la ruta al directorio de plantillas
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    template = env.get_template("pdf_template.html")

    rendered_html = template.render(**data)

    base_url = os.path.join(os.path.dirname(__file__), '..', '..')
    
    # Generar PDF
    HTML(string=rendered_html, base_url=base_url).write_pdf(output_path)
    print(f"PDF generado exitosamente en {output_path}")