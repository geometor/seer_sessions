```python
"""
1.  **Identify Repeating Row Pattern:** For each row in the input grid, find the smallest repeating sequence of colors. This is the "repeating row pattern".
2.  **Determine Output Width:** The output grid's width is equal to the length of the repeating pattern detected in the first row, or the majority of rows.
3. **Construct Output rows:** for each input row
   - identify repeating row pattern
   - construct output row by copying the repeating pattern identified
4.  **Assemble Output:** Stack the generated output rows vertically to form the final output grid. The output grid's height matches the input grid's height.
"""

import numpy as np
from collections import Counter

def find_repeating_pattern(row):
    # Find the smallest repeating pattern in a row.
    n = len(row)
    for length in range(1, n // 2 + 1):
        if n % length == 0:
            valid = True
            for i in range(n - length):
                if row[i] != row[i + length]:
                    valid = False
                    break
            if valid:
                return row[:length]
    return row  # No repeating pattern found, return the whole row


def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # Find repeating patterns for all rows
    row_patterns = [find_repeating_pattern(row) for row in input_grid]

    # Determine output width (use length of first row or the most frequent pattern)
    pattern_lengths = [len(pattern) for pattern in row_patterns]

    output_width = Counter(pattern_lengths).most_common(1)[0][0]

    # Construct output grid
    output_grid = []
    for row in input_grid:
        repeating_unit= find_repeating_pattern(row)
        if len(repeating_unit) == output_width:
          output_grid.append(repeating_unit)
        else:
           #print("fixing size")
           new_row = []
           for i in range(output_width):
              new_row.append(repeating_unit[i % len(repeating_unit)]) # handles edge cases of inconsistent patterns
           output_grid.append(new_row)

    return np.array(output_grid).tolist()
```