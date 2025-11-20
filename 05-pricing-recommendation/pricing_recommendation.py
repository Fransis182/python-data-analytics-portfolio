import math # Importar para usar math.inf si fuera necesario, aunque no lo es con los límites actuales

"""EJERCICIO 5: Pricing Tier Recommendation Engine
Empresa: Freemium SaaS (ej: Notion, Canva, Loom)
Rol: Junior Data Analyst / Growth Analyst

CONTEXTO:
Tu Growth team quiere optimizar conversiones de free → paid.
Necesitas un sistema que recomiende el tier adecuado basado en uso.

PLANS DISPONIBLES:
- Free:  0/month (límites: 5 proyectos, 1 GB storage, 1 user)
- Starter:  12/month (20 proyectos, 10 GB, 3 users)
- Pro:  29/month (Unlimited proyectos, 100 GB, 10 users)
- Enterprise:  99/month (Unlimited todo + soporte prioritario)

TASK:
Analizar uso del usuario y recomendar el plan óptimo que:
1. Cubra sus necesidades actuales
2. Tenga margen de crecimiento (no llegar al límite inmediato)
3. Maximice conversión (no over-sell si no necesita)
"""

def recommend_pricing_tier(projects_created, storage_used_gb, team_members, 
                           support_tickets_last_month):
    """
    Recomienda el plan óptimo basado en patrón de uso
    
    Args:
        projects_created (int): Proyectos creados por el usuario
        storage_used_gb (float): GB de almacenamiento usado
        team_members (int): Miembros del equipo
        support_tickets_last_month (int): Tickets de soporte abiertos
        
    Returns:
        dict: Recomendación de plan + reasoning
    """
    
    # LOGIC: Evaluar qué plan necesita basado en límites
    
    # Caso 1: Uso dentro de Free limits → mantener Free
    if projects_created <= 5 and storage_used_gb <= 1 and team_members <= 1:
        recommended_plan = "Free"
        reasoning = "Current usage fits Free plan limits"
        upsell_trigger = "No action needed"
        confidence = "High"
    
    # Caso 2: Necesita Enterprise (alto soporte o equipos grandes)
    elif team_members > 10 or support_tickets_last_month >= 5:
        recommended_plan = "Enterprise"
        reasoning = "Large team or high support needs require Enterprise"
        upsell_trigger = "Offer dedicated account manager"
        confidence = "High"

    # Caso 3: Necesita Pro (excede límites de Starter)
    elif projects_created > 20 or storage_used_gb > 10 or team_members > 3:
        recommended_plan = "Pro"
        reasoning = "Usage exceeds Starter limits (projects, storage or team). Pro offers more capacity."
        upsell_trigger = "Pro plan benefits presentation & 1-month free trial"
        confidence = "Medium"
        
    # Caso 4: Necesita Starter (excede límites de Free)
    elif projects_created > 5 or storage_used_gb > 1 or team_members > 1:
        recommended_plan = "Starter"
        reasoning = "Usage exceeds Free plan limits. Starter offers necessary growth margin."
        upsell_trigger = "Starter plan trial or discount offer"
        confidence = "High"
        
    else: # Fallback - should ideally not be reached if logic covers all cases
        recommended_plan = "Undefined"
        reasoning = "Usage pattern does not fit any predefined tier, requires manual review."
        upsell_trigger = "Manual review by Sales/Growth team"
        confidence = "Low"
        
    return {
        "recommended_plan": recommended_plan,
        "reasoning": reasoning,
        "upsell_trigger": upsell_trigger,
        "confidence": confidence
    }

# --- Test Cases (optional, for validation) ---
print("=== EJERCICIO 5: Pricing Tier Recommendation ===\n")

tests = [
    (5, 1, 1, 0),    # Free user, fits free limits
    (6, 0.5, 1, 0),  # Exceeds free projects, fits starter
    (15, 8, 2, 0),   # Standard Starter user
    (21, 5, 2, 0),   # Exceeds starter projects, needs Pro
    (10, 15, 2, 0),  # Exceeds starter storage, needs Pro
    (10, 5, 4, 0),   # Exceeds starter team, needs Pro
    (50, 50, 8, 0),  # Standard Pro user
    (5, 1, 12, 0),   # Exceeds Enterprise team members
    (2, 0.5, 1, 5),  # High support tickets, needs Enterprise
    (25, 30, 15, 1), # High usage, high team, already Enterprise level
    (0, 0, 0, 0)     # Minimal usage, should be Free
]

for i, (p, s, t, st) in enumerate(tests):
    result = recommend_pricing_tier(p, s, t, st)
    print(f"--- Test Case {i+1} ---")
    print(f"Input: Projects={p}, Storage={s}GB, Team={t}, SupportTickets={st}")
    print(f"  Recommended Plan: {result['recommended_plan']}")
    print(f"  Reasoning: {result['reasoning']}")
    print(f"  Upsell Trigger: {result['upsell_trigger']}")
    print(f"  Confidence: {result['confidence']}\n")
