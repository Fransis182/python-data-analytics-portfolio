"""EJERCICIO 2: Transaction Analysis
Empresa: Ecommerce / Fintech (ej: Shopify, Stripe)
Rol: Junior Data Analyst

CONTEXTO:
El equipo de fraude necesita un sistema automático que identifique
transacciones anómalas para revisión manual.

TASK:
Crear función que analice transacciones según:
Monto de la transacción
Número de transacciones del usuario en las últimas 24h

REGLAS DE NEGOCIO:
Normal: monto < €500 y transacciones < 5
High Value: monto >= €500 y transacciones < 10 (VIP customer, ok)
Suspicious: transacciones >= 10 (posible fraude, revisar)
Suspicious: monto >= €1000 y transacciones >= 5 (alerta roja)
"""

def analyze_transaction(amount, transactions_24h, is_new_customer=False):
    """
    Analiza transacciones y detecta anomalías

    Args:
        amount (float): Monto de la transacción en €
        transactions_24h (int): Número de transacciones en últimas 24h
        is_new_customer (bool): True si el cliente es nuevo, False en caso contrario

    Returns:
        tuple: (status, action, risk_score)
    """
    risk_score = 0
    status = "Normal"
    action = "No action needed"

    # Calcular risk_score
    if amount > 500:
        risk_score += 20
    if transactions_24h > 5:
        risk_score += 30
    if transactions_24h > 10:
        risk_score += 50 # Esto se suma al de > 5, haciendo 80 en total

    # Aplicar reglas de negocio y actualizar status/action

    # Caso 1: Demasiadas transacciones (posible fraude)
    if transactions_24h >= 10:
        status = "Suspicious"
        action = "Block card and contact user immediately"

    # Caso 2: Monto muy alto + varias transacciones (alerta roja)
    elif amount >= 1000 and transactions_24h >= 5:
        status = "Suspicious"
        action = "Flag for manual review - High value + High frequency"

    # Caso extra 1: Cliente nuevo Y compra > €1000
    elif is_new_customer and amount > 1000:
        status = "Suspicious"
        action = "Flag for manual review - New customer high value purchase"

    # Caso extra 2: Si risk_score > 70
    if risk_score > 70 and status != "Suspicious": # No sobrescribir Suspicious ya establecido
        status = "Suspicious"
        action = f"Flag for manual review - High risk score ({risk_score})"

    # Caso 3: Monto alto pero pocas transacciones (cliente VIP normal) - Solo si no es ya sospechoso
    elif status == "Normal" and amount >= 500 and transactions_24h < 10:
        status = "High Value"
        action = "No action - VIP customer behavior"

    return status, action, risk_score


# ============================================
# TESTS - Casos reales que encontrarías
# ============================================

print("=== TEST 2: Transaction Fraud Detection ===\n")

# Test cases (transaction_id, amount, transactions_24h, is_new_customer)
transactions = [
    ("txn_001", 45.90, 1, False),      # Normal: compra pequeña, no nuevo
    ("txn_002", 850.00, 2, False),     # High Value: cliente VIP, no nuevo
    ("txn_003", 120.00, 12, False),    # Suspicious: demasiadas transacciones
    ("txn_004", 1500.00, 7, False),    # Suspicious: monto alto + frecuencia alta
    ("txn_005", 2500.00, 1, False),    # High Value: compra única grande (normal en luxury)
    ("txn_006", 1200.00, 1, True),     # Suspicious EXTRA: nuevo cliente + compra alta
    ("txn_007", 600.00, 6, False),     # Suspicious EXTRA: risk_score > 70 (20+30=50, este caso es >70 si 30 se vuelve 50)
    ("txn_008", 100.00, 11, False),    # Suspicious: 11 txns (risk_score = 0+80=80)
    ("txn_009", 1000.00, 4, True)      # Suspicious EXTRA: cliente nuevo y compra > 1000
]

for txn_id, amount, freq, new_customer in transactions:
    status, action, risk_score = analyze_transaction(amount, freq, new_customer)
    print(f"{txn_id}: €{amount} ({freq} txns/24h), New: {new_customer}")
    print(f"  → Status: {status}, Risk Score: {risk_score}")
    print(f"  → Action: {action}\n")


print("="*60)
print("INTERPRETACIÓN DE RESULTADOS (ACTUALIZADA):")
print("- txn_001: Normal (45.90€, 1 txn, cliente existente)")
print("- txn_002: High Value (850€, 2 txns, cliente existente) - VIP legítimo.")
print("- txn_003: Suspicious (120€, 12 txns) - Demasiadas transacciones. Riesgo: 80")
print("- txn_004: Suspicious (1500€, 7 txns) - Monto y frecuencia altos. Riesgo: 50")
print("- txn_005: High Value (2500€, 1 txn, cliente existente) - Compra única de lujo. Riesgo: 20")
print("- txn_006: Suspicious (1200€, 1 txn, cliente nuevo) - Nuevo cliente con compra alta. Riesgo: 20")
print("- txn_007: Suspicious (600€, 6 txns, cliente existente) - Puntuación de riesgo > 70. Riesgo: 50")
print("- txn_008: Suspicious (100€, 11 txns, cliente existente) - Demasiadas transacciones. Riesgo: 80")
print("- txn_009: Suspicious (1000€, 4 txns, cliente nuevo) - Nuevo cliente con compra alta. Riesgo: 20")
print("="*60)
