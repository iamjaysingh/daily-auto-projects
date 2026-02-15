#!/usr/bin/env python3
"""
CLI Calculator
A feature-rich command-line calculator with history and memory.
Author: Jay Singh (iamjaysingh)
"""

import math
import sys


class Calculator:
    """A CLI calculator with history, memory, and scientific functions."""

    def __init__(self):
        self.history = []
        self.memory = 0.0

    def calculate(self, expression):
        """Evaluate a mathematical expression safely."""
        # Define allowed functions
        safe_funcs = {
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "log": math.log, "log10": math.log10,
            "abs": abs, "pow": pow, "round": round,
            "pi": math.pi, "e": math.e, "ans": self.last_answer,
            "mem": self.memory,
        }

        try:
            result = eval(expression, {"__builtins__": {}}, safe_funcs)
            self.history.append({"expr": expression, "result": result})
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {e}"

    @property
    def last_answer(self):
        """Get the last calculated answer."""
        return self.history[-1]["result"] if self.history else 0

    def show_history(self):
        """Display calculation history."""
        if not self.history:
            print("  📭 No history yet.")
            return
        print("\n  📜 Calculation History:")
        for i, item in enumerate(self.history[-10:], 1):
            print(f"    {i}. {item['expr']} = {item['result']}")

    def store_memory(self, value):
        """Store a value in memory."""
        self.memory = value
        print(f"  💾 Stored {value} in memory")

    def recall_memory(self):
        """Recall stored memory value."""
        print(f"  💾 Memory: {self.memory}")
        return self.memory


def main():
    calc = Calculator()
    print("=" * 50)
    print("  🧮 CLI Calculator v1.0")
    print("=" * 50)
    print("  Functions: sqrt, sin, cos, tan, log, abs, pow")
    print("  Constants: pi, e, ans (last answer), mem")
    print("  Commands:  history, store <n>, recall, clear, quit")
    print("=" * 50)

    while True:
        try:
            expr = input("\n  ▶ ").strip()
            if not expr:
                continue
            if expr.lower() in ("quit", "exit", "q"):
                print("\n  👋 Goodbye!")
                break
            elif expr.lower() == "history":
                calc.show_history()
            elif expr.lower().startswith("store"):
                val = float(expr.split()[1]) if len(expr.split()) > 1 else calc.last_answer
                calc.store_memory(val)
            elif expr.lower() == "recall":
                calc.recall_memory()
            elif expr.lower() == "clear":
                calc.history.clear()
                print("  🗑️  History cleared")
            else:
                result = calc.calculate(expr)
                print(f"  = {result}")
        except (EOFError, KeyboardInterrupt):
            print("\n  👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
