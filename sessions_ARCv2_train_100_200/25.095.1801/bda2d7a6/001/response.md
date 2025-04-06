```python
"""
Transforms a 2D grid by cyclically permuting three key colors based on their spatial roles:
1.  Identifies the outermost border color (Color A).
2.  Identifies the color immediately inside the border (Color B).
3.  Identifies the innermost color (Color C).
4.  Applies the substitution: A becomes C, B becomes A, C becomes B.
"""

import collections

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a cyclic color permutation to a 2D grid.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers (colors).

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # --- Identify the three key colors ---

    # Color A: Outermost border color
    # Assumes the grid is large enough to have a border
    color_a = input_grid[0][0]

    # Color B: Color immediately inside the border
    # Assumes the grid is at least 3x3 and has distinct layers
    color_b = -1 # Initialize with an invalid color
    if height > 1 and width > 1:
         # Search inwards from [1][1] if the border is thicker than 1
         r, c = 1, 1
         while r < height -1 and c < width -1 and input_grid[r][c] == color_a:
             r += 1
             c += 1
         if r < height -1 and c < width -1:
            color_b = input_grid[r][c]
         else: # Fallback if only 2 colors or unusual structure, though examples suggest 3
             # Find the first color that is not color_a
             for r_idx in range(height):
                 for c_idx in range(width):
                     if input_grid[r_idx][c_idx] != color_a:
                         color_b = input_grid[r_idx][c_idx]
                         break
                 if color_b != -1:
                     break


    # Color C: The remaining color (innermost)
    # Find all unique colors first
    unique_colors = set()
    for r in range(height):
        for c in range(width):
            unique_colors.add(input_grid[r][c])

    color_c = -1 # Initialize with an invalid color
    for color in unique_colors:
        if color != color_a and color != color_b:
            color_c = color
            break
            
    # Handle cases where fewer than 3 colors are identified (e.g., solid color grid)
    # If B wasn't found, C won't be found either.
    # If only A and B found, C remains -1. If only A found, B and C remain -1.
    # The mapping below handles these cases gracefully if C is missing.

    # --- Define the color transformation mapping ---
    # A -> C, B -> A, C -> B
    color_map = {}
    if color_a != -1 and color_c != -1:
        color_map[color_a] = color_c
    else: # If C not found, map A to itself (or handle as error)
        color_map[color_a] = color_a

    if color_b != -1 and color_a != -1:
        color_map[color_b] = color_a
    else: # If B or A not found map B to itself
         color_map[color_b] = color_b
         
    if color_c != -1 and color_b != -1:
         color_map[color_c] = color_b
    else: # If C or B not found map C to itself
         color_map[color_c] = color_c


    # Initialize the output grid with the same dimensions as the input
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # --- Perform transformations ---
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the original color
            original_color = input_grid[r][c]
            # Find the transformed color using the map, default to original if not in map
            transformed_color = color_map.get(original_color, original_color)
            # Assign the transformed color to the output grid
            output_grid[r][c] = transformed_color

    return output_grid

```