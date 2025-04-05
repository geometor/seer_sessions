
Previous Code:
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Processes a 10x10 grid containing integers (primarily 0, 2, and 4).
The transformation rule depends on the spatial relationship between the unique digit 4 and any adjacent digits 2.

1. Locate the cell containing the digit 4.
2. Check its 8 immediate neighbours (horizontal, vertical, diagonal).
3. If any neighbour contains the digit 2:
    - Keep the digit 4 in its original position.
    - Change all occurrences of the digit 2 in the entire grid to 0.
4. If none of the neighbours contain the digit 2:
    - Change the digit 4 to 0.
    - Keep all occurrences of the digit 2 in their original positions.
5. Digits 0 remain unchanged in all cases.
"""

def find_digit_location(grid: np.ndarray, digit: int) -> Optional[Tuple[int, int]]:
    """Finds the first occurrence of a specific digit in the grid."""
    locations = np.where(grid == digit)
    if len(locations[0]) > 0:
        return (locations[0][0], locations[1][0]) # Return coordinates of the first found digit
    return None # Digit not found

def check_neighbors_for_digit(grid: np.ndarray, center_pos: Tuple[int, int], digit: int) -> bool:
    """Checks the 8 neighbours of a central cell for a specific digit."""
    rows, cols = grid.shape
    center_r, center_c = center_pos
    # Iterate through the 3x3 neighbourhood around the center
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = center_r + dr, center_c + dc
            
            # Check if the neighbour coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbour cell contains the target digit
                if grid[nr, nc] == digit:
                    return True # Found the digit in a neighbour
    return False # Digit not found in any neighbour

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """Applies the transformation rule based on the neighbours of digit 4."""
    # Convert input list of lists to a NumPy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid_np.copy()
    
    # 1. Find the coordinates (r4, c4) of the cell containing the value 4
    pos_4 = find_digit_location(grid_np, 4)
    
    # If 4 is not found (unlikely based on examples, but good practice to check)
    if pos_4 is None:
        return output_grid.tolist() # Return the original grid if 4 is missing

    # 2. Check the 8 neighbouring cells surrounding (r4, c4) for the value 2
    found_2_neighbor = check_neighbors_for_digit(grid_np, pos_4, 2)
    
    # 3. Apply conditional replacement based on whether a 2 neighbour was found
    if found_2_neighbor:
        # Condition 1: A neighbour contains 2.
        # Keep the value 4 at its position (already copied).
        # Replace all values 2 in the entire grid with 0.
        output_grid[output_grid == 2] = 0
    else:
        # Condition 2: None of the neighbours contain 2.
        # Replace the value 4 with 0.
        r4, c4 = pos_4
        output_grid[r4, c4] = 0
        # Keep all values 2 at their positions (already copied).

    # 4. All cells with value 0 remain 0 (already copied).

    # Convert the NumPy array back to a list of lists for the final output
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
