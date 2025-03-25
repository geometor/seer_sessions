"""
1.  **Identify Repeating Patterns:** For each row, starting from the last row up to the first, identify any repeating sub-pattern within that row. The repeating pattern can start at any point of the row.
2. **Extend Pattern in Row:** If a repeating pattern is found in the row, extend the pattern to fill the full width of the row.
3.  **Propagate to Row Above:** Once a repeating pattern is found and extended in row *n*, examine row *n-1*. If there is a repeating pattern in row *n-1*, extend the pattern across the width of row *n-1*. Repeat the process to the top row.
"""

import numpy as np

def find_repeating_pattern(row):
    """Finds the longest repeating pattern in a row."""
    row = np.array(row)
    n = len(row)
    best_pattern = None
    max_coverage = 0

    for start in range(n):
        for length in range(1, (n - start) // 2 + 1):
            pattern = row[start:start+length]
            repetitions = 0
            current_pos = start
            while current_pos + length <= n:
                if np.array_equal(row[current_pos : current_pos + length], pattern):
                    repetitions += 1
                    current_pos += length
                else:
                    break
            coverage = repetitions * length
            if repetitions > 1 and coverage > max_coverage:
                max_coverage = coverage
                best_pattern = pattern
    return best_pattern


def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through rows from bottom to top.
    for i in range(rows - 1, -1, -1):
        row_pattern = find_repeating_pattern(input_grid[i])

        # Extend the pattern if found.
        if row_pattern is not None:
            pattern_len = len(row_pattern)
            output_grid[i] = np.tile(row_pattern, cols // pattern_len + (cols % pattern_len > 0))[:cols]

    return output_grid.tolist()