from datetime import datetime

def formatear_fecha_larga(dt=None):
    if dt is None:
        dt = datetime.today()

    meses = (
        "enero", "febrero", "marzo", "abril", "mayo", "junio", 
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    )

    return f"{dt.day} de {meses[dt.month - 1]} de {dt.year}"
