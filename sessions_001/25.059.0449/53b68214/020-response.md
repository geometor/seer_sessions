# 53b68214 • 020 • refine_coder

---
```python
"""
1.  **Identify Repeating Column Patterns:** Examine each column of the input grid.  A "repeating column pattern" is defined as a sequence where a single pixel of a specific color appears, followed by one or more empty (0-value) pixels, and then another single pixel of the *same* color appears. The pattern is defined by the color and the number of rows between instances of the colored pixel.
2.  **Extend Grid:** Increase the height of the grid by two rows.
3.  **Replicate Patterns:** For each column that contains a repeating column pattern (as defined in step 1):
    *   Continue the pattern into the new rows. Maintain the same color and the same spacing (number of empty rows) between colored pixels.
4. **Copy Unmodified:** If a column does not contain a repeating column pattern, it will remain unchanged in those rows.
"""

import numpy as np

def find_repeating_patterns(grid):
    """
    Identifies repeating single-pixel patterns in each column.

    Returns:
        A list of dictionaries, one for each column. Each dictionary contains:
        - 'color': The color of the repeating pixel, or None if no pattern is found.
        - 'spacing': The number of rows between repetitions, or None.
        - 'start_row': The row index of the first occurrence of the color.
    """
    height, width = grid.shape
    patterns = []

    for col in range(width):
        column_patterns = {'color': None, 'spacing': None, 'start_row': None}
        first_occurrence = -1
        second_occurrence = -1
        color = None

        for row in range(height):
            if grid[row, col] != 0:
                if first_occurrence == -1:
                    first_occurrence = row
                    color = grid[row, col]
                elif grid[row,col] == color:
                    second_occurrence = row
                    break

        if first_occurrence != -1 and second_occurrence != -1:
            spacing = second_occurrence - first_occurrence
            # Verify the pattern continues
            valid_pattern = True
            
            #check the rest of the column
            next_expected = second_occurrence + spacing
            while next_expected < height:
                if grid[next_expected,col] != color:
                    valid_pattern = False
                    break
                #check for incorrect colors in between
                for in_between in range(next_expected - spacing + 1, next_expected):
                    if grid[in_between,col] != 0:
                        valid_pattern = False
                        break
                if not valid_pattern:
                    break
                next_expected += spacing
            
            if valid_pattern:
                column_patterns['color'] = color
                column_patterns['spacing'] = spacing
                column_patterns['start_row'] = first_occurrence

        patterns.append(column_patterns)

    return patterns


def transform(input_grid):
    # Extend Grid
    input_height, input_width = input_grid.shape
    output_height = input_height + 2
    output_grid = np.zeros((output_height, input_width), dtype=int)
    output_grid[:input_height, :] = input_grid #copy

    # Identify Repeating Column Patterns
    patterns = find_repeating_patterns(input_grid)

    # Replicate Patterns
    for col, pattern in enumerate(patterns):
        if pattern['color'] is not None:
            color = pattern['color']
            spacing = pattern['spacing']
            start_row = pattern['start_row']

            # Determine where to continue the pattern
            last_occurrence = start_row
            
            #find last occurance in input
            next_expected = last_occurrence + spacing
            while next_expected < input_height:          
                last_occurrence = next_expected
                next_expected += spacing
            
            #fill in the new rows
            next_expected = last_occurrence + spacing
            while next_expected < output_height:
                output_grid[next_expected, col] = color
                next_expected += spacing

    return output_grid
```
