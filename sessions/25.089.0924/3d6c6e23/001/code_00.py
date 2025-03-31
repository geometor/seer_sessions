import numpy as np
import math

"""
Transform the input grid by:
1. Identifying columns containing non-background (non-zero) pixels.
2. For each such column:
    a. Determine the unique non-background colors present.
    b. Count the number of pixels (N) for each color in that column.
    c. Find the topmost row index for each color in that column.
    d. Sort these colors based on their topmost row index in descending order (lowest appears first).
3. Initialize an output grid of the same dimensions as the input, filled with the background color (0).
4. For each processed column, starting from the bottom row of the output grid:
    a. Iterate through the sorted colors for that column.
    b. For each color and its count N:
        i. Calculate the triangle's base width: W = 2 * ceil(sqrt(N)) - 1.
        ii. Calculate the triangle's height: H = (W + 1) / 2.
        iii. Draw an upward-pointing triangle of that color, centered horizontally on the column index, with its base of width W positioned on the current designated base row.
    c. Decrement the designated base row index by 1 for the next color's triangle in the same column stack.
5. Return the completed output grid.
"""

def _draw_triangle(output_grid, color, center_col, base_row, height, width):
    """Draws an upward pointing triangle onto the grid."""
    grid_height, grid_width = output_grid.shape
    top_row = base_row - height + 1

    for r_offset in range(height):
        current_row = top_row + r_offset
        current_width = 2 * r_offset + 1
        start_col = center_col - r_offset
        end_col = center_col + r_offset

        # Ensure drawing stays within grid bounds
        if 0 <= current_row < grid_height:
            for c in range(start_col, end_col + 1):
                if 0 <= c < grid_width:
                    output_grid[current_row, c] = color

def transform(input_grid):
    """
    Transforms the input grid by collecting colors from columns and forming 
    stacked triangles at the bottom.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np)

    # Find columns with non-background pixels
    relevant_cols = np.where(np.any(input_np != 0, axis=0))[0]

    # Process each relevant column
    for c in relevant_cols:
        column_data = input_np[:, c]
        
        # Find unique non-zero colors and their first occurrence (topmost row)
        colors_in_col = []
        unique_colors = np.unique(column_data[column_data != 0])
        
        for color in unique_colors:
            indices = np.where(column_data == color)[0]
            count = len(indices)
            top_row = indices[0] # First index is the topmost
            colors_in_col.append({'color': color, 'count': count, 'top_row': top_row})
            
        # Sort colors by their topmost row index, descending (lowest in grid comes first)
        colors_in_col.sort(key=lambda x: x['top_row'], reverse=True)
        
        # Initialize the base row for the first triangle in this column
        current_base_row = height - 1
        
        # Draw triangles for each color, stacking them upwards
        for color_info in colors_in_col:
            color = color_info['color']
            count = color_info['count']
            
            # Calculate triangle dimensions
            # Ensure count is at least 1 for sqrt
            n = max(1, count) 
            base_width = 2 * math.ceil(math.sqrt(n)) - 1
            tri_height = (base_width + 1) // 2
            
            # Ensure base_width is odd and at least 1
            base_width = int(base_width)
            tri_height = int(tri_height)
            
            # Check if the triangle can fit vertically before drawing
            if current_base_row - tri_height + 1 >= 0:
                 _draw_triangle(output_grid, color, c, current_base_row, tri_height, base_width)
            # Else: triangle is too tall to fit starting at this base row, skip or handle differently?
            # Based on examples, it seems they always fit. If not, they might just be clipped or not drawn.
            # The current implementation clips automatically due to bounds checking in _draw_triangle.

            # Decrement base row for the next triangle in the stack
            current_base_row -= 1 
            
    # The problem statement uses lists of lists, so convert back
    return output_grid.tolist()