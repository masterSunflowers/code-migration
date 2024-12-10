import subprocess
import tempfile
import os
import re

def get_similarity_index(code1, code2):
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f1:
        f1.write(code1)
        file1_path = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f2:
        f2.write(code2)
        file2_path = f2.name
    
    try:
        # Run git diff with rename detection
        cmd = ['git', 'diff', '--no-index', '--find-renames=1%', file1_path, file2_path]
        result = subprocess.run(cmd, text=True, stderr=subprocess.STDOUT)
        
        output = result.stdout or result.stderr
        
        # Look for rename pattern: rename from ... rename to ... (XX%)
        rename_match = re.search(r'rename from.*\nrename to.*\((\d+)%\)', output)
        if rename_match:
            return int(rename_match.group(1))
            
        # If files are identical
        if 'Files ' + file1_path + ' and ' + file2_path + ' are identical' in output:
            return 100
            
        # Calculate similarity based on added/removed lines
        added_lines = len([line for line in output.split('\n') if line.startswith('+')])
        removed_lines = len([line for line in output.split('\n') if line.startswith('-')])
        total_lines = len(code1.split('\n'))
        
        if total_lines == 0:
            return 0
            
        changed_lines = max(added_lines, removed_lines)
        similarity = ((total_lines - changed_lines) / total_lines) * 100
        return round(similarity)
        
    finally:
        # Clean up temporary files
        os.unlink(file1_path)
        os.unlink(file2_path)

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