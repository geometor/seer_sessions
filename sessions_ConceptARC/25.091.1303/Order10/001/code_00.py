import numpy as np
from collections import deque

"""
Identifies nested layers of non-white colors in the input grid.
Extracts the colors of these layers, starting from the outermost layer 
(adjacent to the white background) and moving inwards.
Returns the sequence of layer colors as a 1-row grid.
"""

def find_neighbors(r, c, height, width):
    """Yields valid neighbor coordinates (up, down, left, right)."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def transform(input_grid):
    """
    Transforms the input grid by extracting the sequence of nested layer colors.

    Args:
        input_grid (list of lists): The input grid representing colors.

    Returns:
        list of lists: A 1xN grid containing the ordered sequence of layer colors.
                       Returns an empty list if no non-white colors are found.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- Find the outermost color (adjacent to white background 0) ---
    outermost_color = None
    found_outer = False
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0: # If it's background
                for nr, nc in find_neighbors(r, c, height, width):
                    neighbor_color = grid[nr, nc]
                    if neighbor_color != 0: # Found a non-background neighbor
                        if outermost_color is None:
                            outermost_color = neighbor_color
                        elif outermost_color != neighbor_color:
                            # This assumes only one distinct color touches the background
                            # Might need adjustment if multiple colors can touch background independently
                            pass # Keep the first one found for now based on examples
                        found_outer = True
                        # Optimization: can potentially break early if sure only one outer color exists
            # Optimization: if outer color found, maybe stop iterating background cells? Depends on complexity.

    if not found_outer or outermost_color is None:
        # Handle cases with no non-white colors or completely enclosed colors (not in examples)
        return np.array([[]], dtype=int) # Return empty 1x0 grid

    # --- Iteratively find inner layers ---
    output_colors = [outermost_color]
    processed_colors = {0, outermost_color} # Keep track of colors already added or background
    current_layer_color = outermost_color

    while True:
        next_inner_color = None
        found_next = False
        potential_next_colors = set()

        # Find colors adjacent to the current layer's color
        for r in range(height):
            for c in range(width):
                if grid[r, c] == current_layer_color:
                    for nr, nc in find_neighbors(r, c, height, width):
                        neighbor_color = grid[nr, nc]
                        # Check if the neighbor is a new, unprocessed color
                        if neighbor_color not in processed_colors:
                            potential_next_colors.add(neighbor_color)
                            found_next = True # Found at least one candidate for the next layer

        if not found_next or not potential_next_colors:
            # No more inner layers found
            break

        # Assume only one distinct color forms the next inner layer based on examples
        if len(potential_next_colors) == 1:
            next_inner_color = potential_next_colors.pop()
        else:
            # Handle ambiguity if multiple different colors are adjacent to the current layer
            # For now, based on examples, assume only one next inner color.
            # If needed, could add logic based on pixel counts, positions etc.
            # Let's just take one if multiple are found, might indicate an issue with assumptions
            # or a more complex rule.
             next_inner_color = potential_next_colors.pop() # Arbitrarily take one


        # Add the found inner color to the output and mark as processed
        output_colors.append(next_inner_color)
        processed_colors.add(next_inner_color)
        current_layer_color = next_inner_color # Move to the next layer

    # --- Format output as a 1xN grid ---
    output_grid = np.array([output_colors], dtype=int)

    return output_grid.tolist() # Return as list of lists
