🔍 Transaction Analysis — Python Exercise

Este proyecto implementa un sistema básico de detección de transacciones anómalas, similar a los que utilizan equipos de fraud detection en empresas SaaS, eCommerce o fintech.

El objetivo es clasificar una transacción según:

el monto (€),

la frecuencia del usuario en 24h,

y si es cliente nuevo.

🎯 Objetivo del análisis

Detectar automáticamente transacciones que requieren revisión manual o bloqueo:

Categoría	Criterio	Acción recomendada
Normal	Monto < €500 y freq < 5	No acción
High Value	Monto ≥ €500 y freq < 10	Cliente VIP, transacción válida
Suspicious	Freq ≥ 10	Bloquear y contactar usuario
Suspicious	Monto ≥ €1000 y freq ≥ 5	Alerta roja
Suspicious (extra)	Cliente nuevo y compra alta	Revisar manualmente
Suspicious (extra)	Risk score > 70	Revisar manualmente

Este tipo de reglas combinan heurísticas de negocio y un pequeño risk score, técnica común en sistemas antifraude junior.

🧠 Lógica implementada
def analyze_transaction(amount, transactions_24h, is_new_customer=False):
    risk_score = 0
    status = "Normal"
    action = "No action needed"

    # Risk score
    if amount > 500:
        risk_score += 20
    if transactions_24h > 5:
        risk_score += 30
    if transactions_24h > 10:
        risk_score += 50

    # Rule 1: demasiadas transacciones
    if transactions_24h >= 10:
        status = "Suspicious"
        action = "Block card and contact user immediately"

    # Rule 2: monto muy alto + frecuencia alta
    elif amount >= 1000 and transactions_24h >= 5:
        status = "Suspicious"
        action = "Flag for manual review - High value + High frequency"

    # Rule extra: cliente nuevo con compra alta
    elif is_new_customer and amount > 1000:
        status = "Suspicious"
        action = "Flag for manual review - New customer high value purchase"

    # Rule extra: risk score > 70
    if risk_score > 70 and status != "Suspicious":
        status = "Suspicious"
        action = f"Flag for manual review - High risk score ({risk_score})"

    # High Value (solo si sigue siendo normal)
    elif status == "Normal" and amount >= 500 and transactions_24h < 10:
        status = "High Value"
        action = "No action - VIP customer behavior"

    return status, action, risk_score

🧪 Test cases incluidos

Ejecutas el script y obtienes resultados como:

txn_001 → Normal
txn_002 → High Value (cliente VIP)
txn_003 → Suspicious (12 transacciones)
txn_004 → Suspicious (1500€ + 7 transacciones)
txn_005 → High Value (compra única grande)
txn_006 → Suspicious (nuevo cliente + compra alta)
txn_007 → Suspicious (risk_score > 70)
txn_008 → Suspicious (frecuencia 11)
txn_009 → Suspicious (nuevo cliente + compra alta)


Esto demuestra cómo las reglas de negocio afectan tanto al estado como al risk_score.

📈 ¿Qué demuestra este proyecto?

Control de flujo y condicionales complejas

Diseño de reglas de negocio

Sistema de clasificación multietapa

Manejo de casos límite

Uso de risk scoring simple (muy usado en fintech)

Documentación clara orientada a negocio

Ideal para recruiters que buscan Junior Data Analyst con enfoque práctico.

👤 Autor

Francesc Cebrián
Transición desde F&B hacia Data Analytics
LinkedIn
 | GitHub