"""
Finds all horizontal or vertical 3-pixel lines. The central pixel expands into a 3x1 block.
Wing pixels are mirrored across the central pixel and also expand to a 3x1 block.
Orange wing pixels change to red, azure wing pixels to magenta.
"""

import numpy as np

def find_3_pixel_objects(grid):
    """Finds horizontal and vertical 3-pixel objects."""
    rows, cols = grid.shape
    objects = []

    # Check for horizontal objects
    for r in range(rows):
        for c in range(cols - 2):
            if grid[r, c] != 0 and grid[r, c] == grid[r, c+1] and grid[r,c] == grid[r, c+2]:
                # all same color
                objects.append({
                    'type': 'horizontal',
                    'central': (r, c+1),
                    'wings': [(r, c), (r, c+2)],
                    'colors': [grid[r,c], grid[r,c+1], grid[r,c+2]]
                })
            elif grid[r, c] != 0 and grid[r, c+1] != 0 and grid[r, c+2] != 0 and grid[r,c] != grid[r,c+1]:
                # different colors
                 objects.append({
                    'type': 'horizontal',
                    'central': (r, c+1),
                    'wings': [(r, c), (r, c+2)],
                    'colors': [grid[r,c], grid[r,c+1], grid[r,c+2]]
                 })


    # Check for vertical objects
    for r in range(rows - 2):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r, c] == grid[r+1, c] and grid[r,c] == grid[r+2,c]:
                # all same color
                objects.append({
                    'type': 'vertical',
                    'central': (r+1, c),
                    'wings': [(r, c), (r+2, c)],
                    'colors': [grid[r,c], grid[r+1,c], grid[r+2,c]]
                })
            elif grid[r, c] != 0 and grid[r+1, c] != 0 and grid[r+2,c] != 0 and grid[r,c] != grid[r+1,c]:
                # different colors.
                objects.append({
                    'type': 'vertical',
                    'central': (r+1, c),
                    'wings': [(r, c), (r+2, c)],
                    'colors' : [grid[r,c], grid[r+1,c], grid[r+2,c]]
                })

    return objects

def transform(input_grid):
    """Transforms the input grid."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    objects = find_3_pixel_objects(input_grid)

    for obj in objects:
        central_row, central_col = obj['central']
        central_color = input_grid[central_row, central_col]

        # Expand central pixel
        output_grid[central_row, max(0, central_col - 1)] = central_color
        output_grid[central_row, central_col] = central_color
        output_grid[central_row, min(output_grid.shape[1] - 1, central_col + 1)] = central_color

        for wing_row, wing_col in obj['wings']:
            wing_color = input_grid[wing_row, wing_col]

            # Mirror and expand wing pixels
            row_offset = wing_row - central_row
            col_offset = wing_col - central_col
            mirrored_row = central_row - row_offset
            mirrored_col = central_col - col_offset

            # Color change
            if wing_color == 7:
                transformed_color = 2
            elif wing_color == 8:
                transformed_color = 6
            else:
                transformed_color = wing_color
            
            # expand the original wing pixel
            output_grid[wing_row, max(0, wing_col - 1)] = transformed_color
            output_grid[wing_row, wing_col] = transformed_color
            output_grid[wing_row, min(output_grid.shape[1] - 1, wing_col + 1)] = transformed_color

            # Expand mirrored wing pixel
            if 0 <= mirrored_row < output_grid.shape[0] and 0 <= mirrored_col < output_grid.shape[1]:
                output_grid[mirrored_row, max(0, mirrored_col - 1)] = transformed_color
                output_grid[mirrored_row, mirrored_col] = transformed_color
                output_grid[mirrored_row, min(output_grid.shape[1] - 1, mirrored_col + 1)] = transformed_color

    return output_grid