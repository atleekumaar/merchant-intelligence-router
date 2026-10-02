"""
Main CLI Application for Merchant Intelligence Router (VyaparMitra).
Interactive terminal loop demonstrating Jev Classification, Confidence Routing, and LangGraph.
"""

import sys
import os

# Fix console encoding on Windows for Unicode/Emojis
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


def print_banner():
    threshold = get_confidence_threshold()
    print("=" * 65)
    print("          🛍️  VYAPARMITRA - MERCHANT INTELLIGENCE ROUTER  🛍️")
    print("=" * 65)
    print(" Architecture: Jev Classifier -> Confidence Gate -> LangGraph")
    print(f" Confidence Threshold: {threshold:.2f} (lower scores divert to Support)")
    print(" Sample Queries:")
    print("   1. 'Why were my sales low yesterday?'")
    print("   2. 'Show me my top 5 products.'")
    print("   3. 'Which customers bought from me most?'")
    print("   4. 'How much inventory do I have?'")
    print("   5. 'I need help using the dashboard.'")
    print(" Type 'exit' or 'quit' to terminate.")
    print("=" * 65)
    print()


def main():
    print_banner()
    while True:
        try:
            user_input = input("Merchant AI > ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "q"}:
                print("\nThank you for using VyaparMitra. Have a productive business day! 👋\n")
                break

            state = run_merchant_agent(user_input)
            
            print(f"\n[Intent]     : {state.intent}")
            print(f"[Confidence] : {state.confidence:.2f}")
            if state.structured_query and any(state.structured_query.model_dump().values()):
                print(f"[Extracted]  : {state.structured_query.model_dump()}")
            print("\n[Response]:")
            print(state.reply)
            print("-" * 65 + "\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession terminated by user. Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error processing query: {e}\n")


if __name__ == "__main__":
    main()
