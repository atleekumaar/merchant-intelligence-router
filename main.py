"""
Main CLI Application for Merchant Intelligence Router (VyaparMitra).
Interactive terminal demonstrating Local Jev-Compatible Classifier, Confidence Routing, and LangGraph.

NOTE: Uses a local scikit-learn (TF-IDF + Cosine Similarity) classifier at zero cost.
"""

import sys
import os

# Ensure clean UTF-8 console encoding on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.graph import run_merchant_agent
from app.router import get_confidence_threshold
from app.classifier import default_classifier


def print_banner():
    threshold = get_confidence_threshold()
    print("=" * 68)
    print("   🛍️  VYAPARMITRA — MERCHANT INTELLIGENCE ROUTER  🛍️")
    print("   Architecture: Local Jev-Compatible Classifier -> LangGraph")
    print("=" * 68)
    print(f" Confidence Threshold: {threshold:.2f} (lower scores divert to Support)")
    print(" Commands:")
    print("   - Type your natural query (e.g. 'How much did I sell today?')")
    print("   - Type 'explain <query>' to view TF-IDF similarity distribution")
    print("   - Type 'exit' or 'quit' to terminate")
    print("=" * 68)
    print()


def main():
    print_banner()
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "q"}:
                print("\nThank you for using VyaparMitra. Have a productive business day! 👋\n")
                break

            # Debug / Explain mode
            if user_input.lower().startswith("explain "):
                query = user_input[8:].strip()
                explanation = default_classifier.explain(query)
                print(f"\n🔍 [EXPLAIN MODE for '{query}']")
                print("Intent Similarity Scores:")
                for intent_name, score in explanation["intent_scores"].items():
                    bar = "█" * int(score * 20)
                    print(f"  {intent_name:<12} : {score:.4f}  {bar}")
                print(f"Selected Intent   : {explanation['selected_intent']}")
                print(f"Confidence        : {explanation['confidence']:.2f}")
                print(f"Passes Threshold  : {explanation['passes_threshold']} (Threshold: {explanation['threshold']})\n")
                continue

            state = run_merchant_agent(user_input)
            
            intent_val = state.intent.value if hasattr(state.intent, "value") else state.intent
            print(f"\nIntent: {intent_val}")
            print(f"Confidence: {state.confidence:.2f}")
            
            if state.structured_query and any(state.structured_query.model_dump().values()):
                clean_extracted = {k: v for k, v in state.structured_query.model_dump().items() if v is not None}
                if clean_extracted:
                    print(f"Extracted: {clean_extracted}")
                    
            print(f"\nAssistant:\n{state.reply}")
            print("-" * 68 + "\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession terminated by user. Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error processing query: {e}\n")


if __name__ == "__main__":
    main()
