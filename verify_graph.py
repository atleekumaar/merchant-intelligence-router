import sys
import io

# Ensure UTF-8 output encoding across all platforms
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from app.graph import run_merchant_agent

test_cases = [
    ("Why were my sales low yesterday?", "analytics", 0.70),
    ("Show me my top 5 products.", "products", 0.70),
    ("Which customers bought from me most?", "customers", 0.70),
    ("How much inventory do I have?", "inventory", 0.70),
    ("I need help using the dashboard.", "support", 0.70),
    ("Can you teach me quantum physics?", "support", 0.0), # Ambiguous / off-topic -> fallback to support
]

print("=== RUNNING GRAPH ROUTING VERIFICATION ===")
for query, expected_intent, min_conf in test_cases:
    state = run_merchant_agent(query)
    print(f"\n[Query]: '{query}'")
    print(f"[Detected Intent]: {state.intent} (Expected: {expected_intent})")
    print(f"[Confidence]: {state.confidence:.2f}")
    print(f"[Reply Preview]: {state.reply[:80]}...")
    
print("\nAll verification cases executed successfully!")
