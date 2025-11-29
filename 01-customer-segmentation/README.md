👥 Customer Segmentation — Python Exercise

Este proyecto contiene un ejercicio práctico de segmentación de usuarios basado en la recencia de login, típico en empresas SaaS.
El objetivo es demostrar dominio de condicionales en Python, lógica de negocio y testeo básico de funciones.

🎯 Objetivo del análisis

Clasificar usuarios en cuatro categorías según los días desde su último login:

Segmento	Criterio	Acción recomendada
Highly Active	< 1 día	Ofrecer promoción especial
Active	1–7 días	No requiere acción
At Risk	7–30 días	Enviar email de re-engagement
Churned	> 30 días	Añadir a campaña win-back

Estos segmentos ayudan a equipos de Producto, Marketing y CRM a identificar:

Usuarios sanos

Usuarios a punto de desconectarse

Usuarios que necesitan una reactivación

Usuarios ya churn (pero recuperables)

🧠 Lógica de negocio implementada
def classify_user_status(days_since_last_login):
    if days_since_last_login < 1:
        return "Highly Active", "Offer special promotion"
    elif days_since_last_login < 7:
        return "Active", "No action needed"
    elif days_since_last_login <= 30:
        return "At Risk", "Send re-engagement email"
    else:
        return "Churned", "Add to win-back campaign"


Puntos clave:

Condicionales claros y ordenados

Umbrales que reflejan comportamiento real de usuarios SaaS

Devuelve estado + acción (útil para automatización)

Maneja casos especiales (0, 0.5, etc.)

🧪 Tests incluidos en el ejercicio
users = [
    ("user_001", 3),
    ("user_002", 15),
    ("user_003", 45),
    ("user_004", 0),
    ("user_005", 30),
    ("user_006", 0.5)
]

for user_id, days in users:
    status, action = classify_user_status(days)
    print(f"{user_id}: {days} days → {status} ({action})")


Ejemplo de salida:

user_001: 3 days → Active (No action needed)
user_002: 15 days → At Risk (Send re-engagement email)
user_003: 45 days → Churned (Add to win-back campaign)
user_004: 0 days → Highly Active (Offer special promotion)
user_005: 30 days → At Risk (Send re-engagement email)
user_006: 0.5 days → Highly Active (Offer special promotion)

📈 ¿Qué demuestra este ejercicio?

Lógica condicional y control de flujo

Conversión de reglas de negocio a código Python

Manejo de valores límite

Claridad en prints y reporting

Enfoque hacia producto / retención / churn

Es un ejemplo perfecto para posts de portfolio o entrevistas de Junior Data Analyst.

👤 Autor

Francesc Cebrián
En transición desde F&B Operations hacia Data Analytics