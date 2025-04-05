
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
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


**output:**
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


## train_3

**input:**
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


**output:**
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


## train_4

**input:**
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


**output:**
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

*   **Perception:** The task operates on 10x10 grids containing primarily digits 0, 2, and 4. The input grids usually feature multiple instances of the digit 2 and a single instance of the digit 4. The output grid is derived from the input grid based on a conditional rule involving the spatial relationship between the digit 4 and any adjacent digits 2. Specifically, the transformation depends on whether the cell containing the digit 4 has any neighbouring cells (horizontally, vertically, or diagonally) that contain the digit 2. If such a neighbour exists, the digit 4 is preserved in the output, and all instances of the digit 2 in the grid are changed to 0. Conversely, if the digit 4 has no adjacent neighbours with the digit 2, then all instances of the digit 2 are preserved in the output, and the digit 4 is changed to 0.

*   **YAML Facts:**
    
```yaml
    objects:
      - grid:
          description: A 10x10 matrix of integers.
          properties:
            - dimensions: [10, 10]
            - cells: Contains integer values, primarily 0, 2, and 4.
      - cell:
          description: A single element within the grid.
          properties:
            - position: (row, column) coordinates.
            - value: An integer (0, 2, or 4).
      - target_digit_4:
          description: The cell containing the value 4. Assumed unique per input grid.
          properties:
            - value: 4
            - position: Specific (row, column) coordinates.
      - neighbor_digit_2:
          description: Cells containing the value 2.
          properties:
            - value: 2
            - position: Specific (row, column) coordinates.
    relationships:
      - adjacency:
          description: The spatial relationship between the cell containing 4 and its 8 immediate neighbours (horizontal, vertical, diagonal).
          condition: Check if any neighbour of the cell with value 4 contains the value 2.
    actions:
      - find_digit_4: Locate the coordinates of the cell containing 4.
      - check_neighbors: Examine the 8 neighbours of the cell containing 4 for the presence of the value 2.
      - conditional_replacement:
          if: A neighbour contains 2.
          then: Keep the value 4 at its position, replace all values 2 in the entire grid with 0.
          else: Replace the value 4 with 0, keep all values 2 at their positions.
      - copy_zeros: All cells with value 0 remain 0.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Find the coordinates (row `r4`, column `c4`) of the cell containing the value 4 in the input grid.
    3.  Check the 8 neighbouring cells surrounding (`r4`, `c4`). Determine if any of these neighbours contain the value 2.
    4.  **Condition 1:** If at least one neighbour contains the value 2:
        *   Iterate through all cells in the output grid.
        *   If a cell contains the value 2, change its value to 0.
        *   The cell at (`r4`, `c4`) retains its value 4.
    5.  **Condition 2:** If none of the neighbours contain the value 2:
        *   Change the value of the cell at (`r4`, `c4`) in the output grid to 0.
        *   All cells originally containing 2 retain their value 2.
    6.  All cells originally containing 0 retain their value 0 in both conditions.
    7.  Return the modified output grid.
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
