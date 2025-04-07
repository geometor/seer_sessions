```python
import numpy as np
import copy

"""
Transforms a 10x10 grid containing a single 3x3 hollow square object made of a 
non-zero digit. The transformation moves the object to a new location determined 
by the object's color (digit), preserving the object's shape and color.

Movement Rules:
- If the object's color is 8, move it horizontally so its top-left corner's 
  column index becomes 7. The row index remains unchanged.
- If the object's color is 4, move it vertically so its top-left corner's 
  row index becomes 7. The column index remains unchanged.
- If the object's color is 6, move it vertically so its top-left corner's 
  row index becomes 0. The column index remains unchanged.
The background remains zero.
"""

def find_object_top_left(grid: np.ndarray) -> tuple[int, int, int]:
    """
    Finds the top-left corner coordinates and color of the 3x3 hollow square object.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (top_row, top_col, color) if the object is found, 
        otherwise raises ValueError.
    """
    rows, cols = grid.shape
    for r in range(rows - 2):  # Iterate potential top-left rows
        for c in range(cols - 2):  # Iterate potential top-left columns
            color = grid[r, c]
            # Check if it's the top-left corner of a potential object
            if color != 0:
                # Check the 3x3 hollow square pattern
                if (grid[r, c+1] == color and
                    grid[r, c+2] == color and
                    grid[r+1, c] == color and
                    grid[r+1, c+1] == 0 and    # Center must be zero
                    grid[r+1, c+2] == color and
                    grid[r+2, c] == color and
                    grid[r+2, c+1] == color and
                    grid[r+2, c+2] == color):
                    # Check if this object is isolated (no other non-zero adjacent)
                    # This check might be overly strict for ARC but good for robustness
                    # For this specific problem, we assume only one object exists.
                    return r, c, color
    raise ValueError("Could not find the 3x3 hollow square object in the input grid.")

def place_object(grid: np.ndarray, top_row: int, top_col: int, color: int):
    """
    Places the 3x3 hollow square object onto the grid at the specified location.

    Args:
        grid: The grid (numpy array) to modify.
        top_row: The target row index for the top-left corner.
        top_col: The target column index for the top-left corner.
        color: The color (digit) of the object.
    """
    # Define the hollow square pattern relative coordinates
    pattern_coords = [
        (0, 0), (0, 1), (0, 2),
        (1, 0),         (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]
    
    rows, cols = grid.shape
    for dr, dc in pattern_coords:
        nr, nc = top_row + dr, top_col + dc
        # Check bounds before placing
        if 0 <= nr < rows and 0 <= nc < cols:
            grid[nr, nc] = color
        else:
            # Handle cases where the target position would place part of the object
            # outside the grid (though not expected based on examples).
            print(f"Warning: Object placement at ({top_row},{top_col}) goes out of bounds.")


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A 10x10 list of lists representing the input grid.

    Returns:
        A 10x10 list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output grid with zeros
    output_np = np.zeros_like(input_np)

    try:
        # Find the object's top-left corner and color
        start_row, start_col, color = find_object_top_left(input_np)

        # Determine the target top-left corner based on color
        target_row, target_col = start_row, start_col # Default to original if no rule matches

        if color == 8:
            target_row = start_row
            target_col = 7
        elif color == 4:
            target_row = 7
            target_col = start_col
        elif color == 6:
            target_row = 0
            target_col = start_col
        
        # Place the object in the output grid at the target location
        place_object(output_np, target_row, target_col, color)

    except ValueError as e:
        # If no object is found, return the empty grid (or handle as needed)
        print(f"Error processing grid: {e}")
        # Returning the empty grid initialized earlier
        pass 

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```