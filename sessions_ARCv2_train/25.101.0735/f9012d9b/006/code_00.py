import collections
import numpy as np
from collections import defaultdict

def parse_grid(grid_str: str) -> list[list[int]]:
    """Parses a string representation of a grid into a list of lists of ints."""
    lines = grid_str.strip().split('\n')
    return [[int(digit) for digit in line.split()] for line in lines]

def get_main_diagonal(grid: list[list[int]]) -> list[int]:
    """Extracts the main diagonal elements from a grid."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    size = min(rows, cols)
    return [grid[i][i] for i in range(size)]

def is_monochromatic(sequence: list[int]) -> bool:
    """Checks if all elements in a sequence are the same."""
    if not sequence: return True
    return all(element == sequence[0] for element in sequence)

def analyze_subgrids_metrics(grid: list[list[int]], subgrid_size: int = 2) -> dict:
    """Finds unique subgrids, calculates sum, frequency, first/last positions."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    subgrid_info = defaultdict(lambda: {'sum': 0, 'freq': 0, 'first_pos': (-1,-1), 'last_pos': (-1, -1)})
    if rows < subgrid_size or cols < subgrid_size: return {}

    for r in range(rows - subgrid_size + 1):
        for c in range(cols - subgrid_size + 1):
            subgrid = [row[c:c+subgrid_size] for row in grid[r:r+subgrid_size]]
            subgrid_tuple = tuple(tuple(row) for row in subgrid)
            current_pos = (r, c)

            if subgrid_info[subgrid_tuple]['freq'] == 0:
                 subgrid_info[subgrid_tuple]['sum'] = int(np.sum(subgrid))
                 subgrid_info[subgrid_tuple]['first_pos'] = current_pos # Set first pos

            subgrid_info[subgrid_tuple]['freq'] += 1
            subgrid_info[subgrid_tuple]['last_pos'] = current_pos # Update last pos

    return dict(subgrid_info)

# --- Apply Revised Hypothesis: Max Sum -> Min Freq -> Earliest Last Pos ---
def apply_revised_hypothesis(grid: list[list[int]]):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Rule 1: Check Diagonal
    diagonal = get_main_diagonal(grid)
    if diagonal and is_monochromatic(diagonal):
        return [[diagonal[0]]]

    # Rule 2: Non-monochromatic diagonal
    if rows < 2 or cols < 2: return []

    analysis = analyze_subgrids_metrics(grid, 2)
    if not analysis: return []

    # Find max sum
    max_sum = max((info['sum'] for info in analysis.values()), default=-1)
    if max_sum == -1: return [] # No patterns found

    # Filter by max sum
    max_sum_patterns = [{'pattern': p, **i} for p, i in analysis.items() if i['sum'] == max_sum]

    # Find min frequency among max_sum patterns
    min_freq = min((item['freq'] for item in max_sum_patterns), default=float('inf'))
    if min_freq == float('inf'): return [] # Should not happen

    # Filter by min frequency
    candidate_patterns = [item for item in max_sum_patterns if item['freq'] == min_freq]

    # Tie-breaker: Earliest Last Position (Min Row, then Min Col)
    candidate_patterns.sort(key=lambda item: item['last_pos']) # Sort ascending by (row, col) tuple

    if not candidate_patterns: return []
    best_pattern_tuple = candidate_patterns[0]['pattern']
    return [list(row) for row in best_pattern_tuple]


# --- Example 1 Verification ---
input_1_str = "8 6 0 6\n6 8 6 8\n8 6 8 6\n6 8 6 8"
input_1_grid = parse_grid(input_1_str)
output_1 = apply_revised_hypothesis(input_1_grid)
expected_1 = [[8]]
print("--- Example 1 ---")
print(f"Input:\n{input_1_str}")
print(f"Expected: {expected_1}")
print(f"Predicted: {output_1}")
print(f"Match: {output_1 == expected_1}")


# --- Example 2 Verification ---
input_2_str = "2 1 2 1 2\n1 1 1 1 1\n2 1 2 1 2\n0 0 1 1 1\n0 0 2 1 2"
input_2_grid = parse_grid(input_2_str)
output_2 = apply_revised_hypothesis(input_2_grid)
expected_2 = [[1, 1], [2, 1]]
print("\n--- Example 2 ---")
print(f"Input:\n{input_2_str}")
analysis_2 = analyze_subgrids_metrics(input_2_grid)
max_sum_2 = max((info['sum'] for info in analysis_2.values()), default=-1)
max_sum_patterns_2 = [{'pattern': p, **i} for p, i in analysis_2.items() if i['sum'] == max_sum_2]
min_freq_2 = min((item['freq'] for item in max_sum_patterns_2), default=float('inf'))
candidate_patterns_2 = [item for item in max_sum_patterns_2 if item['freq'] == min_freq_2]
print("Candidates (Max Sum, Min Freq):")
for item in sorted(candidate_patterns_2, key=lambda x: x['last_pos']): # Sort by last_pos for clarity
    print(f"  Pattern: {item['pattern']}, Sum: {item['sum']}, Freq: {item['freq']}, Last Pos: {item['last_pos']}")
print(f"Expected: {expected_2}")
print(f"Predicted: {output_2}")
print(f"Match: {output_2 == expected_2}")


# --- Example 3 Verification ---
input_3_str = "2 2 5 2 2 5 2\n2 2 5 2 2 5 2\n5 5 5 5 5 5 5\n2 2 5 2 2 5 2\n2 2 5 2 2 5 2\n5 5 5 5 5 0 0\n2 2 5 2 2 0 0"
input_3_grid = parse_grid(input_3_str)
output_3 = apply_revised_hypothesis(input_3_grid)
expected_3 = [[5, 5], [5, 2]]
print("\n--- Example 3 ---")
print(f"Input:\n{input_3_str}")
analysis_3 = analyze_subgrids_metrics(input_3_grid)
max_sum_3 = max((info['sum'] for info in analysis_3.values()), default=-1)
max_sum_patterns_3 = [{'pattern': p, **i} for p, i in analysis_3.items() if i['sum'] == max_sum_3]
min_freq_3 = min((item['freq'] for item in max_sum_patterns_3), default=float('inf'))
candidate_patterns_3 = [item for item in max_sum_patterns_3 if item['freq'] == min_freq_3]
print("Candidates (Max Sum, Min Freq):")
for item in sorted(candidate_patterns_3, key=lambda x: x['last_pos']): # Sort by last_pos for clarity
    print(f"  Pattern: {item['pattern']}, Sum: {item['sum']}, Freq: {item['freq']}, Last Pos: {item['last_pos']}")
print(f"Expected: {expected_3}")
print(f"Predicted: {output_3}")
print(f"Match: {output_3 == expected_3}")