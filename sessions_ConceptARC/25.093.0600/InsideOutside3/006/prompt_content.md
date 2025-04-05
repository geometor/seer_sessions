
Previous Code:
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 10x10 grid based on the adjacency of the digit 2 to the unique digit 4.

1.  Locates the unique cell containing the digit 4.
2.  Checks its 8 immediate neighbours (Moore neighbourhood) for the presence of the digit 2.
3.  Conditional Transformation Rule:
    *   If at least one neighbour contains the digit 2: 
        - Keep the digit 4 in its original position.
        - Change all occurrences of the digit 2 in the entire grid to 0.
    *   If none of the neighbours contain the digit 2:
        - Change the digit 4 to 0.
        - Keep all occurrences of the digit 2 unchanged.
4.  Digits 0 remain unchanged in all cases.

*(Note: This rule describes the transformation observed in 5 out of the 7 provided examples. Examples `train_3` and `test_2` are inconsistent with the "If none of the neighbours contain the digit 2" step, as their expected outputs follow the logic of the "If at least one neighbour contains the digit 2" step despite having no adjacent 2.)*
"""

def find_digit_location(grid: np.ndarray, digit: int) -> Optional[Tuple[int, int]]:
    """Finds the coordinates (row, col) of the first occurrence of a specific digit."""
    locations = np.where(grid == digit)
    # Check if the digit was found
    if len(locations[0]) > 0:
        # Return the coordinates of the first instance found
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
    """Applies the transformation rule based on the neighbours of the digit 4."""
    
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Initialization: Create a copy of the input grid to serve as the output grid.
    output_grid = grid_np.copy()
    
    # 2. Locate Target: Find the coordinates (r4, c4) of the cell containing the value 4.
    pos_4 = find_digit_location(grid_np, 4)
    
    # If 4 is not found in the grid, return the original grid copy (as list of lists).
    if pos_4 is None:
        return output_grid.tolist() 

    # 3. Check Adjacency: Determine if any neighbours of the cell at pos_4 contain the value 2.
    has_adjacent_2 = check_neighbors_for_digit(grid_np, pos_4, 2)
    
    # 4. Conditional Transformation: Apply changes based on the adjacency check.
    if has_adjacent_2:
        # If a '2' neighbour exists: Keep '4', change all '2's to '0' globally.
        # '4' is already preserved in the copy.
        # Change all cells with value 2 to 0 in the output grid.
        output_grid[output_grid == 2] = 0
    else:
        # If no '2' neighbour exists: Change '4' to '0', keep all '2's.
        # Change the value at the position of '4' to 0 in the output grid.
        r4, c4 = pos_4
        output_grid[r4, c4] = 0
        # '2's are already preserved in the copy.

    # 5. Finalize: Convert the NumPy array back to a list of lists for the return value.
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 2 0
2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 36.0

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 4 0 0 0 0
0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 44.0

## Example 3:
Input:
```
0 2 0 2 0 2 0 2 0 4
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 2 0 2 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 2 0 2 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
