#!/usr/bin/env python3
"""
Sorting Visualizer
Visualizes different sorting algorithms in the terminal.
Author: Jay Singh (iamjaysingh)
"""

import random
import time
import os


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def visualize(arr, highlight=None, label=""):
    """Visualize array as bar chart in terminal."""
    if highlight is None:
        highlight = set()
    max_val = max(arr) if arr else 1
    height = 20
    width = min(len(arr), 60)

    print(f"\n  {label}")
    print(f"  {'─' * (width * 2 + 2)}")

    for row in range(height, 0, -1):
        line = "  │"
        threshold = (row / height) * max_val
        for i, val in enumerate(arr[:width]):
            if val >= threshold:
                if i in highlight:
                    line += "██"
                else:
                    line += "▓▓"
            else:
                line += "  "
        line += "│"
        print(line)

    print(f"  {'─' * (width * 2 + 2)}")
    nums = "  "
    for v in arr[:width]:
        nums += f"{v:2d}"
    print(nums)


def bubble_sort(arr):
    """Bubble Sort with visualization."""
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return comparisons, swaps


def selection_sort(arr):
    """Selection Sort with counting."""
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    return comparisons, swaps


def insertion_sort(arr):
    """Insertion Sort with counting."""
    comparisons = 0
    swaps = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        comparisons += 1
        arr[j + 1] = key

    return comparisons, swaps


def quick_sort(arr, low=0, high=None, stats=None):
    """Quick Sort with counting."""
    if stats is None:
        stats = {"comparisons": 0, "swaps": 0}
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            stats["comparisons"] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                stats["swaps"] += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        stats["swaps"] += 1
        pi = i + 1

        quick_sort(arr, low, pi - 1, stats)
        quick_sort(arr, pi + 1, high, stats)

    return stats["comparisons"], stats["swaps"]


def main():
    print("=" * 50)
    print("  📊 Sorting Algorithm Visualizer")
    print("=" * 50)

    size = 25
    original = [random.randint(1, 40) for _ in range(size)]

    algorithms = {
        "1": ("Bubble Sort", bubble_sort),
        "2": ("Selection Sort", selection_sort),
        "3": ("Insertion Sort", insertion_sort),
        "4": ("Quick Sort", quick_sort),
        "5": ("Compare All", None),
    }

    visualize(original, label="📊 Original Array (unsorted)")

    print("\n  Algorithms:")
    for key, (name, _) in algorithms.items():
        print(f"    {key}. {name}")

    choice = input("\n  Select: ").strip()

    if choice == "5":
        print(f"\n  {'Algorithm':<20} {'Comparisons':>12} {'Swaps':>8} {'Time (ms)':>10}")
        print(f"  {'─' * 52}")

        for key in ["1", "2", "3", "4"]:
            name, func = algorithms[key]
            arr_copy = original.copy()
            start = time.time()
            comps, swps = func(arr_copy)
            elapsed = (time.time() - start) * 1000
            print(f"  {name:<20} {comps:>12} {swps:>8} {elapsed:>9.2f}ms")

    elif choice in algorithms and algorithms[choice][1]:
        name, func = algorithms[choice]
        arr_copy = original.copy()
        start = time.time()
        comps, swps = func(arr_copy)
        elapsed = (time.time() - start) * 1000

        visualize(arr_copy, label=f"✅ After {name}")
        print(f"\n  📈 Stats: {comps} comparisons, {swps} swaps, {elapsed:.2f}ms")

    else:
        print("  ❌ Invalid option")

    print("\n  👋 Done!")


if __name__ == "__main__":
    main()
