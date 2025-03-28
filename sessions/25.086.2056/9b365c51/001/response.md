```python
import numpy as np
import collections

"""
Identify vertical lines of distinct non-white, non-azure colors on the left.
Identify groups of contiguous columns containing azure pixels on the right.
Map the i-th vertical line color (ordered left-to-right) to the i-th azure column group (ordered left-to-right).
Create an output grid, initially white. For every azure pixel in the input at (r, c), find the column group 'c' belongs to, determine the corresponding color from the vertical lines, and place that color at (r, c) in the output grid.
"""

def find_vertical_lines(input_grid):
    """Finds vertical lines of a single non-white, non-azure color."""
    height, width = input_grid.shape
    lines = []
    for c in range(width):
        col = input_grid[:, c]
        first_color = col[0]
        if first_color != 0 and first_color != 8: # Must not be white or azure
            is_line = True
            for r in range(1, height):
                if col[r] != first_color:
                    is_line = False
                    break
            if is_line:
                lines.append({'color': first_color, 'col_index': c})
    # Sort lines by column index
    lines.sort(key=lambda x: x['col_index'])
    return lines

def find_azure_column_groups(input_grid):
    """Finds groups of contiguous columns containing azure pixels."""
    height, width = input_grid.shape
    azure_cols = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 8:
                azure_cols.add(c)

    if not azure_cols:
        return []

    sorted_azure_cols = sorted(list(azure_cols))

    groups = []
    if not sorted_azure_cols:
        return groups

    current_group = [sorted_azure_cols[0]]
    for i in range(1, len(sorted_azure_cols)):
        if sorted_azure_cols[i] == sorted_azure_cols[i-1] + 1:
            current_group.append(sorted_azure_cols[i])
        else:
            groups.append(current_group)
            current_group = [sorted_azure_cols[i]]
    groups.append(current_group) # Add the last group

    return groups


def transform(input_grid):
    """
    Transforms the input grid by recoloring azure areas based on vertical color lines.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    
    # Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # Step 2 & 3: Find and sort vertical color lines
    vertical_lines = find_vertical_lines(input_grid)
    sorted_colors = [line['color'] for line in vertical_lines]

    # Step 4, 5 & 6: Find and sort groups of contiguous azure columns
    azure_column_groups = find_azure_column_groups(input_grid)

    # Ensure the number of lines matches the number of groups (as per assumption)
    if len(sorted_colors) != len(azure_column_groups):
        # This case might indicate a misunderstanding or an edge case not covered.
        # For now, return the empty grid or handle error appropriately.
        print(f"Warning: Mismatch between number of color lines ({len(sorted_colors)}) and azure groups ({len(azure_column_groups)}).")
        # Depending on expected behavior, might return input, empty grid, or raise error
        return output_grid.tolist() 

    # Step 7 & 8a, 8b, 8c: Create mapping from column index to target color
    col_to_color_map = {}
    for i, group in enumerate(azure_column_groups):
        color_to_assign = sorted_colors[i]
        for col_index in group:
            col_to_color_map[col_index] = color_to_assign

    # Step 8 & 8d: Iterate through the input grid and populate the output grid
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 8: # If the pixel is azure in the input
                # Find the corresponding color from the map
                if c in col_to_color_map:
                    output_grid[r, c] = col_to_color_map[c]
                # else: # Handle case where an azure pixel is not in a mapped group (shouldn't happen with current logic)
                #     pass # Keep it white (0) in the output

    return output_grid.tolist()
```