"""EJERCICIO 3: A/B Test Analysis
Empresa: Tech Product (ej: Spotify, Netflix, Airbnb)
Rol: Junior Data Analyst

CONTEXTO:
El equipo de producto lanzó un A/B test para probar un nuevo botón de CTA.
Necesitas analizar resultados y determinar si la variante B supera a la control (A).

TASK:
Crear función que:
1. Calcule conversion rate para ambas variantes
2. Calcule el uplift (mejora porcentual)
3. Determine el ganador del test
4. Recomiende acción

CRITERIOS:
- Uplift > 5%: "Implementar variante B"
- Uplift entre 2-5%: "Test inconcluso, continuar"
- Uplift < 2%: "Mantener variante A"
- Uplift negativo: "Variante B es peor, descartar"
"""

def analyze_ab_test(variant_a_conversions, variant_a_visitors,
                     variant_b_conversions, variant_b_visitors,
                     minimum_sample_size=1000,
                     average_order_value=None,
                     total_monthly_visitors=None):
    """
    Analiza resultados de A/B test y determina ganador, incluyendo cálculos adicionales.

    Args:
        variant_a_conversions (int): Conversiones en variante A (control)
        variant_a_visitors (int): Visitantes en variante A
        variant_b_conversions (int): Conversiones en variante B (test)
        variant_b_visitors (int): Visitantes en variante B
        minimum_sample_size (int): Tamaño mínimo de muestra requerido para un test válido.
        average_order_value (float): Valor promedio de la orden para calcular impacto en ingresos.
        total_monthly_visitors (int): Visitantes mensuales totales para calcular impacto en ingresos.

    Returns:
        dict: Resultados del análisis
    """

    # 2. Añade un parámetro 'minimum_sample_size' y comprueba
    if variant_a_visitors < minimum_sample_size or variant_b_visitors < minimum_sample_size:
        return {
            "status": "Insufficient data",
            "recommendation": "⚠️ INSUFFICIENT DATA - Increase sample size for a valid test",
            "variant_a_cr": "N/A",
            "variant_b_cr": "N/A",
            "uplift_pct": "N/A",
            "absolute_lift": "N/A",
            "winner": "N/A",
            "confidence": "N/A",
            "revenue_impact": "N/A"
        }

    # Calcular conversion rates
    cr_a = (variant_a_conversions / variant_a_visitors) * 100
    cr_b = (variant_b_conversions / variant_b_visitors) * 100

    # Calcular uplift (mejora porcentual de B vs A)
    uplift = ((cr_b - cr_a) / cr_a) * 100 if cr_a != 0 else 0 # Evitar división por cero

    # 1. Añade cálculo de "absolute_lift"
    absolute_lift = variant_b_conversions - variant_a_conversions

    # Determinar ganador y recomendación
    if uplift > 5:
        winner = "Variant B"
        recommendation = "✅ IMPLEMENT - Clear winner with significant uplift"
        confidence = "High"
    elif uplift >= 2:
        winner = "Inconclusive"
        recommendation = "⚠️ CONTINUE TEST - Positive signal but needs more data"
        confidence = "Medium"
    elif uplift >= -2:
        winner = "No difference"
        recommendation = "➡️ KEEP VARIANT A - No meaningful difference detected"
        confidence = "Medium"
    else:  # uplift < -2
        winner = "Variant A"
        recommendation = "❌ DISCARD B - Variant B performs worse"
        confidence = "High"

    # 3. Calcula el "revenue_impact"
    revenue_impact = "N/A"
    if average_order_value is not None and total_monthly_visitors is not None:
        # La diferencia en CR es en puntos porcentuales, hay que convertirla a proporción
        cr_difference_proportion = (cr_b - cr_a) / 100
        revenue_impact = cr_difference_proportion * total_monthly_visitors * average_order_value

    # Construir resultado
    result = {
        "variant_a_cr": round(cr_a, 2),
        "variant_b_cr": round(cr_b, 2),
        "uplift_pct": round(uplift, 2),
        "absolute_lift": absolute_lift,
        "winner": winner,
        "recommendation": recommendation,
        "confidence": confidence,
        "revenue_impact": round(revenue_impact, 2) if isinstance(revenue_impact, float) else revenue_impact
    }

    return result


# ============================================
# TESTS - Escenarios reales de A/B tests
# ============================================

print("=== TEST 3: A/B Test Results Analysis ===\n")

# Escenario 1: B gana claramente
print("📊 SCENARIO 1: New CTA button (Clear Winner)")
print("-" * 50)
test1 = analyze_ab_test(
    variant_a_conversions=450,
    variant_a_visitors=10000,
    variant_b_conversions=580,
    variant_b_visitors=10000
)
print(f"Variant A CR: {test1['variant_a_cr']}%")
print(f"Variant B CR: {test1['variant_b_cr']}%")
print(f"Uplift: {test1['uplift_pct']}%")
print(f"Absolute Lift (Conversions): {test1['absolute_lift']}")
print(f"Winner: {test1['winner']}")
print(f"Recommendation: {test1['recommendation']}")
print(f"Confidence: {test1['confidence']}")
print(f"Revenue Impact: {test1['revenue_impact']}\n")


# Escenario 2: Resultado incierto
print("📊 SCENARIO 2: Headline change (Inconclusive)")
print("-" * 50)
test2 = analyze_ab_test(
    variant_a_conversions=320,
    variant_a_visitors=8000,
    variant_b_conversions=335,
    variant_b_visitors=8000
)
print(f"Variant A CR: {test2['variant_a_cr']}%")
print(f"Variant B CR: {test2['variant_b_cr']}%")
print(f"Uplift: {test2['uplift_pct']}%")
print(f"Absolute Lift (Conversions): {test2['absolute_lift']}")
print(f"Winner: {test2['winner']}")
print(f"Recommendation: {test2['recommendation']}")
print(f"Confidence: {test2['confidence']}")
print(f"Revenue Impact: {test2['revenue_impact']}\n")


# Escenario 3: B es peor que A
print("📊 SCENARIO 3: New checkout flow (B is worse)")
print("-" * 50)
test3 = analyze_ab_test(
    variant_a_conversions=890,
    variant_a_visitors=12000,
    variant_b_conversions=720,
    variant_b_visitors=12000
)
print(f"Variant A CR: {test3['variant_a_cr']}%")
print(f"Variant B CR: {test3['variant_b_cr']}%")
print(f"Uplift: {test3['uplift_pct']}%")
print(f"Absolute Lift (Conversions): {test3['absolute_lift']}")
print(f"Winner: {test3['winner']}")
print(f"Recommendation: {test3['recommendation']}")
print(f"Confidence: {test3['confidence']}")
print(f"Revenue Impact: {test3['revenue_impact']}\n")

# Nuevo Escenario 4: Datos insuficientes
print("📊 SCENARIO 4: Insufficient Sample Size")
print("-" * 50)
test4 = analyze_ab_test(
    variant_a_conversions=50,
    variant_a_visitors=500,
    variant_b_conversions=60,
    variant_b_visitors=550,
    minimum_sample_size=1000
)
print(f"Status: {test4['status']}")
print(f"Recommendation: {test4['recommendation']}\n")

# Nuevo Escenario 5: Cálculo de impacto en ingresos (B gana)
print("📊 SCENARIO 5: Revenue Impact Calculation (B wins)")
print("-" * 50)
test5 = analyze_ab_test(
    variant_a_conversions=450,
    variant_a_visitors=10000,
    variant_b_conversions=580,
    variant_b_visitors=10000,
    average_order_value=50.00,
    total_monthly_visitors=100000
)
print(f"Variant A CR: {test5['variant_a_cr']}%")
print(f"Variant B CR: {test5['variant_b_cr']}%")
print(f"Uplift: {test5['uplift_pct']}%")
print(f"Absolute Lift (Conversions): {test5['absolute_lift']}")
print(f"Winner: {test5['winner']}")
print(f"Recommendation: {test5['recommendation']}")
print(f"Confidence: {test5['confidence']}")
print(f"Revenue Impact: {test5['revenue_impact']}€\n")

print("="*60)
print("KEY LEARNINGS (ACTUALIZADO):")
print("- Scenario 1: Uplift +28.89% \u2192 Ship variant B immediately")
print("- Scenario 2: Uplift +3.73% \u2192 Need more data to decide")
print("- Scenario 3: Uplift -19.10% \u2192 Variant B hurt conversions, revert")
print("- Scenario 4: Insufficient data \u2192 Test is not valid yet")
print("- Scenario 5: Uplift +28.89%, Revenue Impact: +65000.00€ \u2192 Clear financial win for Variant B")
print("="*60)
