"""
Processes a grid by applying a 1D cellular automaton rule vertically.
The first row of the input grid serves as the initial state.
Subsequent rows are generated based on the state of the row directly above.
The update rule for a cell at (row r, column c) depends on the states of its diagonal neighbors in the previous row (r-1, c-1) and (r-1, c+1).

Rule Details:
- Active Colors: Red (2), Gray (5).
- Background Color: Orange (7).
- A cell at (r, c) is updated based on the colors of cells L=(r-1, c-1) and R=(r-1, c+1).
- If both L and R are Active Colors:
    - If (L=Gray, R=Red), cell (r, c) becomes Red.
    - If (L=Red, R=Red), cell (r, c) becomes Gray.
    - If (L=Red, R=Gray), cell (r, c) becomes Gray.
    - If (L=Gray, R=Gray), cell (r, c) becomes Red.
- Otherwise (if L or R is Orange or out of bounds), cell (r, c) becomes Orange.
The first row remains unchanged from the input.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a 1D cellular automaton rule vertically down the grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize output grid as a copy of the input grid.
    # The rule application will modify rows starting from the second row.
    output_grid = grid.copy() 

    # Define colors
    orange = 7
    red = 2
    gray = 5
    active_colors = {red, gray}

    # Iterate through the grid rows, starting from the second row (index 1)
    for r in range(1, height):
        # Iterate through the columns for the current row r
        for c in range(width):
            # Get the color of the left neighbor in the previous row (r-1, c-1)
            # Handle boundary condition: if c-1 is out of bounds, treat as orange
            if c - 1 < 0:
                left_neighbor_color = orange
            else:
                left_neighbor_color = output_grid[r - 1, c - 1] # Use output_grid as rules apply sequentially

            # Get the color of the right neighbor in the previous row (r-1, c+1)
            # Handle boundary condition: if c+1 is out of bounds, treat as orange
            if c + 1 >= width:
                right_neighbor_color = orange
            else:
                right_neighbor_color = output_grid[r - 1, c + 1] # Use output_grid as rules apply sequentially

            # Check if both neighbors are active colors
            if left_neighbor_color in active_colors and right_neighbor_color in active_colors:
                # Apply the specific update rules based on neighbor colors
                if left_neighbor_color == gray and right_neighbor_color == red:
                    output_grid[r, c] = red
                elif left_neighbor_color == red and right_neighbor_color == red:
                    output_grid[r, c] = gray
                elif left_neighbor_color == red and right_neighbor_color == gray:
                    output_grid[r, c] = gray
                elif left_neighbor_color == gray and right_neighbor_color == gray:
                    output_grid[r, c] = red
                # This 'else' should theoretically not be reached if both are active
                # else: 
                #    output_grid[r, c] = orange # Default to orange if unexpected combo
            else:
                # If one or both neighbors are not active (orange or out of bounds), set cell to orange
                output_grid[r, c] = orange

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()