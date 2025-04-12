import collections
import numpy as np

def parse_grid(grid_str: str) -> list[list[int]]:
    """Parses a string representation of a grid into a list of lists of ints."""
    lines = grid_str.strip().split('\n')
    return [[int(digit) for digit in line.split()] for line in lines]

def analyze_subgrids_full(grid: list[list[int]], subgrid_size: int = 2):
    """Finds all subgrids, counts frequency, notes first/last positions, and sum."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    # Store: {pattern_tuple: {'freq': int, 'first_pos': (r,c), 'last_pos': (r,c), 'sum': int}}
    subgrid_info = {}

    if rows < subgrid_size or cols < subgrid_size:
        return {}

    for r in range(rows - subgrid_size + 1):
        for c in range(cols - subgrid_size + 1):
            subgrid = [row[c:c+subgrid_size] for row in grid[r:r+subgrid_size]]
            subgrid_tuple = tuple(tuple(row) for row in subgrid)
            current_pos = (r, c)

            if subgrid_tuple not in subgrid_info:
                 current_sum = int(np.sum(subgrid))
                 subgrid_info[subgrid_tuple] = {
                     'freq': 1,
                     'first_pos': current_pos,
                     'last_pos': current_pos, # Initialize last_pos
                     'sum': current_sum,
                 }
            else:
                subgrid_info[subgrid_tuple]['freq'] += 1
                subgrid_info[subgrid_tuple]['last_pos'] = current_pos # Update last_pos

    return subgrid_info

# --- Test Hypothesis ---
def apply_hypothesis(grid: list[list[int]]):
    """Applies the final hypothesis to select the output pattern."""
    # Rule 1: Check Diagonal
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    diag_size = min(rows, cols)
    diagonal = [grid[i][i] for i in range(diag_size)]
    if diagonal and len(set(diagonal)) == 1:
        return [[diagonal[0]]] # Return 1x1 grid

    # Rule 2: Non-monochromatic diagonal
    if rows < 2 or cols < 2: return [] # Cannot form 2x2

    analysis = analyze_subgrids_full(grid, 2)
    if not analysis: return []

    # Find max sum
    max_sum = -1
    for info in analysis.values():
        if info['sum'] > max_sum:
            max_sum = info['sum']

    # Filter by max sum
    max_sum_patterns = []
    for pattern, info in analysis.items():
        if info['sum'] == max_sum:
            max_sum_patterns.append({'pattern': pattern, **info}) # Add pattern to info dict

    if not max_sum_patterns: return [] # Should not happen if analysis is not empty

    # Primary Tie-breaker: Min Frequency
    min_freq = float('inf')
    for item in max_sum_patterns:
        if item['freq'] < min_freq:
            min_freq = item['freq']

    min_freq_patterns = [item for item in max_sum_patterns if item['freq'] == min_freq]

    # Secondary Tie-breaker: Latest Last Position
    min_freq_patterns.sort(key=lambda item: (item['last_pos'][0], item['last_pos'][1]), reverse=True)

    # Select the best pattern
    best_pattern_tuple = min_freq_patterns[0]['pattern']
    return [list(row) for row in best_pattern_tuple]


# --- Example 1 ---
input_1_str = """
8 6 0 6
6 8 6 8
8 6 8 6
6 8 6 8
"""
input_1_grid = parse_grid(input_1_str)
output_1 = apply_hypothesis(input_1_grid)
print("--- Example 1 ---")
print(f"Predicted Output: {output_1}")


# --- Example 2 ---
input_2_str = """
2 1 2 1 2
1 1 1 1 1
2 1 2 1 2
0 0 1 1 1
0 0 2 1 2
"""
expected_output_2_tuple = ((1, 1), (2, 1))
input_2_grid = parse_grid(input_2_str)
analysis_2 = analyze_subgrids_full(input_2_grid)
output_2 = apply_hypothesis(input_2_grid)
print("\n--- Example 2 ---")
print(f"Expected Output: {expected_output_2_tuple}")
# Find max sum
max_sum_2 = max(info['sum'] for info in analysis_2.values())
print(f"Max Sum = {max_sum_2}")
# Find patterns matching max sum
max_sum_patterns_2 = [(p, i) for p, i in analysis_2.items() if i['sum'] == max_sum_2]
print("Patterns with Max Sum:")
for p, i in max_sum_patterns_2: print(f"  {p}: Freq={i['freq']}")
# Find min freq among those
min_freq_2 = min(i['freq'] for p, i in max_sum_patterns_2)
print(f"Min Freq among Max Sum = {min_freq_2}")
# Find patterns matching min freq
min_freq_patterns_2 = [(p, i) for p, i in max_sum_patterns_2 if i['freq'] == min_freq_2]
print("Patterns with Max Sum & Min Freq (Candidates):")
for p, i in min_freq_patterns_2: print(f"  {p}: Last Pos={i['last_pos']}")
print(f"Predicted Output: {output_2}")


# --- Example 3 ---
input_3_str = """
2 2 5 2 2 5 2
2 2 5 2 2 5 2
5 5 5 5 5 5 5
2 2 5 2 2 5 2
2 2 5 2 2 5 2
5 5 5 5 5 0 0
2 2 5 2 2 0 0
"""
expected_output_3_tuple = ((5, 5), (5, 2))
input_3_grid = parse_grid(input_3_str)
analysis_3 = analyze_subgrids_full(input_3_grid)
output_3 = apply_hypothesis(input_3_grid)
print("\n--- Example 3 ---")
print(f"Expected Output: {expected_output_3_tuple}")
# Find max sum
max_sum_3 = max(info['sum'] for info in analysis_3.values())
print(f"Max Sum = {max_sum_3}")
# Find patterns matching max sum
max_sum_patterns_3 = [(p, i) for p, i in analysis_3.items() if i['sum'] == max_sum_3]
print("Patterns with Max Sum:")
for p, i in max_sum_patterns_3: print(f"  {p}: Freq={i['freq']}")
# Find min freq among those
min_freq_3 = min(i['freq'] for p, i in max_sum_patterns_3)
print(f"Min Freq among Max Sum = {min_freq_3}")
# Find patterns matching min freq
min_freq_patterns_3 = [(p, i) for p, i in max_sum_patterns_3 if i['freq'] == min_freq_3]
print("Patterns with Max Sum & Min Freq (Candidates):")
for p, i in min_freq_patterns_3: print(f"  {p}: Last Pos={i['last_pos']}")
print(f"Predicted Output: {output_3}")
