"""EJERCICIO 1: Customer Segmentation
Empresa: Startup SaaS (ej: Notion, Slack, HubSpot)
Rol: Junior Data Analyst

CONTEXTO:
Tu equipo necesita clasificar usuarios según días desde último login
para identificar usuarios en riesgo de churn y activar campañas de re-engagement.

TASK:
Crear función que clasifique usuarios en:
- "Active": último login hace menos de 7 días
- "At Risk": último login entre 7-30 días
- "Churned": último login hace más de 30 días
"""

def classify_user_status(days_since_last_login):
    """
    Clasifica usuarios según actividad reciente y recomienda una acción.

    Args:
        days_since_last_login (int): Días desde el último login

    Returns:
        tuple: (Estado del usuario, Recomendación de acción)
    """
    if days_since_last_login < 1: # Menos de 24 horas
        status = "Highly Active"
        action = "Offer special promotion"
    elif days_since_last_login < 7:
        status = "Active"
        action = "No action needed"
    elif days_since_last_login <= 30:
        status = "At Risk"
        action = "Send re-engagement email"
    else:
        status = "Churned"
        action = "Add to win-back campaign"

    return status, action


# ============================================
# TESTS - Ejecuta y verifica resultados
# ============================================

print("=== TEST 1: User Activity Classification ===\n")

# Test cases
users = [
    ("user_001", 3),   # Active user
    ("user_002", 15),  # At risk
    ("user_003", 45),  # Churned
    ("user_004", 0),   # Just logged in (Highly Active)
    ("user_005", 30),  # Edge case: exactly 30 days (At Risk)
    ("user_006", 0.5) # Test Highly Active with float
]

for user_id, days in users:
    status, action = classify_user_status(days)
    print(f"{user_id}: {days} days \u2192 {status} ({action})")


print("\n" + "="*50)
print("RESULTADO ESPERADO:")
print("user_001: 3 days \u2192 Active (No action needed)")
print("user_002: 15 days \u2192 At Risk (Send re-engagement email)")
print("user_003: 45 days \u2192 Churned (Add to win-back campaign)")
print("user_004: 0 days \u2192 Highly Active (Offer special promotion)")
print("user_005: 30 days \u2192 At Risk (Send re-engagement email)")
print("user_006: 0.5 days \u2192 Highly Active (Offer special promotion)")
print("="*50)
