import numpy as np
from collections import Counter

"""
The transformation identifies the most frequent color in the input grid, considering it the background color.
It then iteratively expands the non-background colored areas into adjacent background cells.
In each iteration, it examines every cell that currently holds the background color.
If such a background cell has exactly one unique non-background color among its four orthogonal neighbors in the grid state from the *previous* iteration (or initial state for the first iteration), that cell's color is changed to match the neighbor's color in the *next* iteration's grid state.
This process repeats until an iteration occurs where no background cells change color.
Cells that are not background color remain unchanged throughout the process.
Background cells adjacent to zero non-background neighbors or adjacent to multiple *different* non-background neighbors retain the background color.
"""

def transform(input_grid):
    """
    Transforms the input grid by iteratively expanding non-background colors 
    by one step into adjacent background cells, conditional on the background 
    cell being adjacent to exactly one unique non-background color in the 
    previous state. The process repeats until no further changes occur.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input list of lists to numpy array for easier handling
    current_grid = np.array(input_grid, dtype=int)
    height, width = current_grid.shape

    # Handle edge case: if grid contains only one color, no transformation is possible or needed.
    unique_colors = np.unique(current_grid)
    if len(unique_colors) <= 1:
        return input_grid 

    # Determine background color (assumed to be the most frequent color)
    counts = Counter(current_grid.flatten())
    # Check for empty grid just in case, although ARC constraints likely prevent this.
    if not counts: 
        return input_grid
    background_color = counts.most_common(1)[0][0]

    while True: # Loop until no changes are made in an iteration
        changed = False
        # Create a copy to store the results of this iteration
        # Changes are based on current_grid, but applied to next_grid
        next_grid = np.copy(current_grid) 

        # Iterate through each cell of the grid
        for r in range(height):
            for c in range(width):
                # Check if the current cell in the *current state* has the background color
                if current_grid[r, c] == background_color:
                    # Use a set to store unique non-background colors found in neighbors
                    neighbor_colors = set() 

                    # Define orthogonal directions
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
                    
                    # Check orthogonal neighbors in the *current state*
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc

                        # Check if the neighbor coordinates are within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Get the color of the neighbor from the current grid
                            neighbor_color = current_grid[nr, nc]
                            # If the neighbor is not background color, add it to the set
                            if neighbor_color != background_color:
                                neighbor_colors.add(neighbor_color)

                    # Check if exactly one unique non-background neighbor color was found
                    if len(neighbor_colors) == 1:
                        # Get the single unique neighbor color
                        new_color = list(neighbor_colors)[0]
                        # If the cell in next_grid is not already this color, update it
                        # This check prevents infinite loops if a cell could flip back and forth (though unlikely here)
                        # and ensures 'changed' is only True if a meaningful change occurred
                        if next_grid[r, c] != new_color:
                            next_grid[r, c] = new_color
                            changed = True
        
        # After checking all cells, update current_grid for the next iteration
        current_grid = next_grid

        # If no cells were changed in this iteration, the process has stabilized
        if not changed:
            break

    # Convert the final numpy array back to a list of lists for the required output format
    return current_grid.tolist()