import subprocess
import tempfile
import os
import re
import myers

def get_similarity_index(old: str, new: str) -> tuple[str, float]:
    def get_lines(text: str) -> list[str]:
        return text.replace('\r\n', '\n').strip().splitlines()

    def get_changes(old: list[str], new: list[str]) -> list[tuple[str, str]]:
        changes = myers.diff(old, new)
        return changes
    old_lines = get_lines(old)
    new_lines = get_lines(new)
    changes = get_changes(old_lines, new_lines)
    print(changes)
    
    num_unchanged_lines = sum(1 for op, _ in changes if op == 'k')
    
    # Calculate similarity
    total_lines = len(old_lines) + len(new_lines)
    if total_lines == 0:
        similarity = 100.0
    else:
        similarity = round(2 * num_unchanged_lines / total_lines * 100, 2)

    return similarity
# Example usage
code1 = """
def hello():
    print("Hello, World!")
    return True
"""

code2 = """
def hello():
    print("Hello, Python!")
    return True
"""

similarity = get_similarity_index(code1, code2)
print(f"Similarity index: {similarity}%")

# Test with more different codes
code3 = """
def calculate(x, y):
    return x + y
"""

code4 = """
def multiply(a, b):
    return a * b
"""

similarity2 = get_similarity_index(code3, code4)
print(f"Similarity index for different functions: {similarity2}%")