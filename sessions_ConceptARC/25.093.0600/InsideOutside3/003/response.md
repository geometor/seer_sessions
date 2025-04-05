```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 10x10 grid based on the neighbourhood of the digit 4.

1.  Locate the unique cell containing the digit 4.
2.  Check its 8 immediate neighbours (Moore neighbourhood) for the presence of the digit 2.
3.  **Conditional Transformation:**
    *   If at least one neighbour contains the digit 2: Keep the digit 4 in its position and change all occurrences of the digit 2 in the entire grid to 0.
    *   If none of the neighbours contain the digit 2: Change the digit 4 to 0 and keep all occurrences of the digit 2 unchanged.
4.  Digits 0 remain unchanged in all cases.

*(Note: This rule aligns with most provided examples but contradicts the expected output for train_3 and test_2, where the '4' is kept despite having no '2' neighbours).*
"""

def find_digit_location(grid: np.ndarray, digit: int) -> Optional[Tuple[int, int]]:
    """Finds the coordinates of the first occurrence of a specific digit in the grid."""
    locations = np.where(grid == digit)
    # Check if the digit was found
    if len(locations[0]) > 0:
        # Assuming the target digit (like 4) is unique or we only care about the first one
        return (int(locations[0][0]), int(locations[1][0])) 
    return None # Digit not found

def check_neighbors_for_digit(grid: np.ndarray, center_pos: Tuple[int, int], digit: int) -> bool:
    """Checks the 8 neighbours (Moore neighborhood) of a central cell for a specific digit."""
    rows, cols = grid.shape
    center_r, center_c = center_pos
    
    # Iterate through the 3x3 neighbourhood around the center cell
    for dr in range(-1, 2): # Delta row: -1, 0, 1
        for dc in range(-1, 2): # Delta column: -1, 0, 1
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            # Calculate neighbour coordinates
            nr, nc = center_r + dr, center_c + dc
            
            # Check if the neighbour coordinates are within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbour cell contains the target digit
                if grid[nr, nc] == digit:
                    return True # Found the digit in a neighbour, no need to check further
                    
    return False # Digit not found in any neighbour

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on the neighbours of the digit 4.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid. Modifications will be made to this copy.
    output_grid = grid_np.copy()
    
    # 1. Find the coordinates (r4, c4) of the cell containing the value 4
    pos_4 = find_digit_location(grid_np, 4)
    
    # If 4 is not found in the grid, return the original grid copy
    if pos_4 is None:
        return output_grid.tolist() 

    # 2. Check the 8 neighbouring cells surrounding the location of 4 for the value 2
    found_2_neighbor = check_neighbors_for_digit(grid_np, pos_4, 2)
    
    # 3. Apply conditional transformation based on whether a 2 neighbour was found
    if found_2_neighbor:
        # Condition 1: A neighbour contains 2.
        # Keep the value 4 at its position (it's already in the copied output_grid).
        # Replace all values 2 in the entire output grid with 0.
        output_grid[output_grid == 2] = 0
    else:
        # Condition 2: None of the neighbours contain 2.
        # Replace the value 4 with 0 in the output grid.
        r4, c4 = pos_4
        output_grid[r4, c4] = 0
        # Keep all values 2 at their positions (they are already in the copied output_grid).

    # 4. All cells with value 0 remain 0 (they were copied initially).

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_grid.tolist()
```