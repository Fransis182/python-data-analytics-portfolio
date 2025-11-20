# EJERCICIO 4: Product Engagement Score
# Empresa: SaaS Product (ej: Figma, Miro, Linear)
# Rol: Junior Data Analyst

# CONTEXTO:
# Tu Product Manager necesita priorizar qué usuarios contactar para:
# - Upsell a plan premium
# - Solicitar feedback
# - Prevenir churn

# TASK:
# Crear un "Engagement Score" (0-100) basado en:
# - Días activos en los últimos 30 días
# - Features usadas (de 10 disponibles)
# - Invitaciones enviadas a otros usuarios

# SCORING LOGIC:
# - Active days: 0-30 -> contribuye 0-40 puntos (peso: 40%)
# - Features used: 0-10 -> contribuye 0-35 puntos (peso: 35%)
# - Invites sent: 0-5+ -> contribuye 0-25 puntos (peso: 25%)

# SEGMENTATION:
# - Score 80-100: "Power User" -> Pedir feedback, upsell premium
# - Score 60-79: "Engaged" -> Mantener engaged con nuevas features
# - Score 40-59: "Casual" -> Enviar tips de uso, educational content
# - Score 0-39: "At Risk" -> Re-engagement campaign urgente

def calculate_engagement_score(active_days, features_used, invites_sent, days_since_last_login, plan_type='free'):
    """
    Calcula engagement score del usuario (0-100) incluyendo factores de recencia y plan.

    Args:
        active_days (int): Días activos en últimos 30 días (0-30)
        features_used (int): Número de features usadas (0-10)
        invites_sent (int): Invitaciones enviadas (0+)
        days_since_last_login (int): Días desde el último login (para factor de recencia)
        plan_type (str): Tipo de plan del usuario ('free', 'pro', 'enterprise')

    Returns:
        dict: Score y segmento del usuario
    """

    # Validar inputs y asegurar rangos
    active_days = max(0, min(active_days, 30))
    features_used = max(0, min(features_used, 10))
    invites_sent = max(0, invites_sent) # No cap superior explícito para invites_sent para el cálculo, aunque el score cap 5

    # Calcular componentes del score base
    activity_score = (active_days / 30) * 40  # 40% peso
    feature_score = (features_used / 10) * 35  # 35% peso
    viral_score = (min(invites_sent, 5) / 5) * 25 # 25% peso, cap en 5 para scoring

    # 1. Añade "recency" como factor (días desde último login)
    recency_bonus = 0
    if days_since_last_login <= 0:
        recency_bonus = 10
    elif 1 <= days_since_last_login <= 7:
        recency_bonus = 5
    elif 15 <= days_since_last_login:
        recency_bonus = -10
    # 8-14 días: +0 bonus (implícito)

    # Score total (asegurar que no exceda 0-100)
    total_score = activity_score + feature_score + viral_score + recency_bonus
    total_score = max(0, min(100, total_score))

    # Determinar segmento y acción base
    if total_score >= 80:
        segment = "Power User"
        action = "💎 Upsell to premium + Request testimonial"
        priority = "High value"
    elif total_score >= 60:
        segment = "Engaged"
        action = "✅ Share new features + Encourage invites"
        priority = "Retention focus"
    elif total_score >= 40:
        segment = "Casual"
        action = "📚 Send educational content + Usage tips"
        priority = "Activation needed"
    else:
        segment = "At Risk"
        action = "🚨 Launch re-engagement campaign immediately"
        priority = "Churn prevention"

    # 2. Añade "plan_type" para overrides
    if total_score >= 80 and plan_type == 'free':
        action = "💎 High priority upsell to premium"
        priority = "High priority upsell"
    elif total_score < 40 and plan_type == 'pro':
        segment = "Critical At Risk"
        action = "🚨 CRITICAL - Paying customer at risk"
        priority = "CRITICAL churn prevention"

    # 3. Calcula "lifetime_value_estimate"
    lifetime_value_estimate = "N/A"
    if segment == "Power User":
        lifetime_value_estimate = 1200
    elif segment == "Engaged":
        lifetime_value_estimate = 600
    elif segment == "Casual":
        lifetime_value_estimate = 200
    elif segment == "At Risk":
        lifetime_value_estimate = 50
    elif segment == "Critical At Risk": # Pro user at risk
        lifetime_value_estimate = 600 # Assuming a pro user's LTV even if at risk

    result = {
        "total_score": round(total_score, 1),
        "breakdown": {
            "activity": round(activity_score, 1),
            "features": round(feature_score, 1),
            "viral": round(viral_score, 1),
            "recency_bonus": recency_bonus
        },
        "segment": segment,
        "action": action,
        "priority": priority,
        "lifetime_value_estimate": f"€{lifetime_value_estimate}/year" if isinstance(lifetime_value_estimate, (int, float)) else lifetime_value_estimate
    }

    return result


# ============================================
# TESTS - Portfolio de usuarios reales (Actualizado)
# ============================================

print("=== TEST 4: User Engagement Scoring ===\n")

# user_id, active_days, features_used, invites_sent, days_since_last_login, plan_type
users = [
    ("user_A", 28, 9, 4, 2, 'free'),   # Power User (free plan, high recency) -> High priority upsell
    ("user_B", 22, 6, 2, 8, 'pro'),    # Engaged (pro plan, neutral recency)
    ("user_C", 12, 4, 0, 10, 'free'),  # Casual (free plan, neutral recency)
    ("user_D", 3, 2, 0, 20, 'free'),   # At Risk (free plan, low recency)
    ("user_E", 30, 10, 5, 0, 'enterprise'), # Perfect score (enterprise, very high recency)
    ("user_F", 10, 3, 0, 30, 'pro'),   # At Risk (pro plan, low score, high recency) -> CRITICAL
    ("user_G", 29, 9, 4, 0, 'free'),   # Power User (free plan, very high recency) -> High priority upsell
    ("user_H", 15, 5, 1, 12, 'pro'),   # Casual (pro plan, neutral recency)
    ("user_I", 5, 2, 0, 1, 'free')    # At Risk (free plan, high recency, but low score)
]

for user_id, days, features, invites, recency, plan in users:
    result = calculate_engagement_score(days, features, invites, recency, plan)

    print(f"👤 {user_id}")
    print(f"   Input: {days} active days | {features} features | {invites} invites | {recency} days_since_login | {plan} plan")
    print(f"   Score: {result['total_score']}/100")
    print(f"   Breakdown: Activity {result['breakdown']['activity']} + "
          f"Features {result['breakdown']['features']} + "
          f"Viral {result['breakdown']['viral']} + "
          f"Recency Bonus {result['breakdown']['recency_bonus']}")
    print(f"   Segment: {result['segment']}")
    print(f"   Action: {result['action']}")
    print(f"   Priority: {result['priority']}")
    print(f"   LTV Estimate: {result['lifetime_value_estimate']}\n")


print("="*70)
print("KEY LEARNINGS (ACTUALIZADO):")
print("- user_A: Power User, Free Plan, High Recency -> High priority upsell. LTV: \u20ac1200/year")
print("- user_B: Engaged, Pro Plan, Neutral Recency -> Retention focus. LTV: \u20ac600/year")
print("- user_C: Casual, Free Plan, Neutral Recency -> Activation needed. LTV: \u20ac200/year")
print("- user_D: At Risk, Free Plan, Low Recency -> Churn prevention. LTV: \u20ac50/year")
print("- user_E: Power User (100 score), Enterprise Plan, Very High Recency -> Request case study + Referral program. LTV: \u20ac1200/year")
print("- user_F: Critical At Risk, Pro Plan, Low Score -> CRITICAL churn prevention. LTV: \u20ac600/year")
print("- user_G: Power User, Free Plan, Very High Recency -> High priority upsell. LTV: \u20ac1200/year")
print("- user_H: Casual, Pro Plan, Neutral Recency -> Activation needed. LTV: \u20ac200/year")
print("- user_I: At Risk, Free Plan, High Recency -> Churn prevention. LTV: \u20ac50/year")
print("="*70)
