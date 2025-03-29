import numpy as np
from collections import Counter

"""
The transformation identifies the most frequent color in the input grid, considering it the background color.
It then performs a single-step expansion of the non-background colored areas into adjacent background cells.
The rule for expansion is: A background cell changes color if and only if it has at least one non-background neighbor, and all of its non-background neighbors share the same color. 
If these conditions are met, the background cell takes on the color of its non-background neighbor(s).
Cells that are not the background color in the input grid remain unchanged in the output grid.
Background cells adjacent to zero non-background neighbors or adjacent to multiple *different* non-background neighbors retain the background color.
This process occurs in a single pass based on the initial state of the grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by expanding non-background colors by one step 
    into adjacent background cells, conditional on the background cell being 
    adjacent only to non-background cells of a single, uniform color.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input list of lists to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Create a copy of the input grid to store the output
    # Changes will be made to this copy, based on the original input_array
    output_array = np.copy(input_array)

    # Handle edge case: if grid contains only one color, no transformation is needed.
    unique_colors = np.unique(input_array)
    if len(unique_colors) <= 1:
        return input_grid 

    # Determine background color (assumed to be the most frequent color)
    counts = Counter(input_array.flatten())
    # Check for empty grid just in case
    if not counts: 
        return input_grid
    background_color = counts.most_common(1)[0][0]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the *input* grid has the background color
            if input_array[r, c] == background_color:
                # Use a set to store unique non-background colors found in neighbors
                neighbor_colors = set() 

                # Define orthogonal directions
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
                
                # Check orthogonal neighbors in the *input* grid
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Get the color of the neighbor from the input grid
                        neighbor_color = input_array[nr, nc]
                        # If the neighbor is not background color, add it to the set
                        if neighbor_color != background_color:
                            neighbor_colors.add(neighbor_color)

                # Check if there was at least one non-background neighbor AND 
                # exactly one unique non-background neighbor color was found
                if len(neighbor_colors) == 1:
                    # Get the single unique neighbor color
                    new_color = list(neighbor_colors)[0]
                    # Update the cell in the output grid
                    output_array[r, c] = new_color
            
            # If the cell in the input grid was not background color, it remains unchanged
            # (already handled by initializing output_array as a copy of input_array)

    # Convert the final numpy array back to a list of lists for the required output format
    return output_array.tolist()