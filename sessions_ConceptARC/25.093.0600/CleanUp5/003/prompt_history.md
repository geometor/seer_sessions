
## train_1

**input:**
```
0 0 0 0 0 2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 3 0 2 0 0 0 2 0 3 0 0 0 2 0 0 0 2 0 0 3
0 0 2 0 0 0 0 0 2 0 0 0 3 0 0 0 0 0 3 0 0
0 2 0 3 0 0 0 0 0 2 0 2 0 0 0 3 0 0 0 2 0
2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


## train_2

**input:**
```
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 4 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0
```

Okay, I will analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) containing single-digit non-negative integers.
2.  **Grid Size:** The grid dimensions can vary between examples (6x21 in train\_1, 6x24 in train\_2), but the output grid always has the same dimensions as the corresponding input grid.
3.  **Values:** The grids contain the value 0 and other non-zero digits (2, 3 in train\_1; 4 in train\_2).
4.  **Transformation:** The core transformation involves selectively changing some non-zero digits in the input grid to 0 in the output grid. Other digits (including existing 0s and some non-zero digits) remain unchanged.
5.  **Pattern:**
    *   In `train_1`, all instances of the digit '3' are changed to '0', while all instances of '2' remain unchanged.
    *   In `train_2`, *some* instances of the digit '4' are changed to '0', while others remain '4'.
    *   Observing the positions, the non-zero digits that are changed to 0 appear to be those that do not have any adjacent cells (including diagonals - Moore neighborhood) containing the *same* non-zero digit. Conversely, non-zero digits that *do* have at least one neighbor with the same value are preserved in the output.

**YAML Facts:**


```yaml
task_description: "Filter a 2D grid of digits, setting non-zero digits to zero if they lack neighbors of the same value."
elements:
  - object: grid
    properties:
      - type: 2D array (matrix)
      - content: non-negative single digits
      - dimensionality: [rows, columns] (variable)
  - object: cell
    properties:
      - value: integer (0-9)
      - position: [row_index, column_index]
      - neighbors: set of 8 adjacent cells (Moore neighborhood)
relationships:
  - type: adjacency
    between: cell
    details: A cell is adjacent to up to 8 other cells (horizontally, vertically, diagonally). Boundary cells have fewer neighbors.
actions:
  - action: process_grid
    actor: system
    input: input_grid
    output: output_grid
    rule: "Iterate through each cell of the input grid."
  - action: evaluate_cell
    actor: system
    input: current_cell (value, position), input_grid
    output: output_cell_value
    rule: |
      1. Get the value (v) and position of the current cell.
      2. If v is 0, the output_cell_value is 0.
      3. If v is non-zero:
         a. Examine the values of the 8 neighboring cells (Moore neighborhood) in the input_grid. Handle boundary conditions (ignore non-existent neighbors).
         b. Check if any neighbor has the same value v.
         c. If at least one neighbor has value v, the output_cell_value is v.
         d. If no neighbor has value v, the output_cell_value is 0.
  - action: construct_output
    actor: system
    input: results of evaluate_cell for all cells
    output: output_grid
    rule: "Assemble the output_cell_values into a new grid with the same dimensions as the input grid."

```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Iterate through each cell `(r, c)` of the input grid. Let the value of the input cell be `v`.
3.  If `v` is 0, set the corresponding cell `(r, c)` in the output grid to 0.
4.  If `v` is not 0:
    a.  Check all 8 neighboring cells (including diagonals) of `(r, c)` within the bounds of the input grid.
    b.  Determine if any of these neighboring cells in the *input* grid has the same value `v`.
    c.  If at least one neighbor has the value `v`, set the corresponding cell `(r, c)` in the output grid to `v`.
    d.  If *none* of the neighbors have the value `v`, set the corresponding cell `(r, c)` in the output grid to 0.
5.  Return the completed output grid.
```python
import copy

"""
Filters a 2D grid of digits. For each non-zero cell in the input grid,
it checks its 8 neighbors (Moore neighborhood). If at least one neighbor
in the input grid has the same value as the cell, the cell's value is 
kept in the output grid. Otherwise (if the cell value is 0 or if it's 
non-zero but has no neighbors with the same value), the corresponding 
cell in the output grid is set to 0.
"""

def _is_valid(r, c, num_rows, num_cols):
    """
    Helper function to check if coordinates (r, c) are within the grid boundaries.

    Args:
        r (int): Row index.
        c (int): Column index.
        num_rows (int): Total number of rows in the grid.
        num_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if the coordinates are valid, False otherwise.
    """
    return 0 <= r < num_rows and 0 <= c < num_cols

def _has_same_neighbor(grid, r, c, value, num_rows, num_cols):
    """
    Helper function to check if any of the 8 neighbors of cell (r, c) 
    in the grid has the specified value.

    Args:
        grid (list[list[int]]): The input grid.
        r (int): Row index of the cell to check neighbors for.
        c (int): Column index of the cell to check neighbors for.
        value (int): The value to look for in the neighbors.
        num_rows (int): Total number of rows in the grid.
        num_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if at least one neighbor has the specified value, False otherwise.
    """
    # Define relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    # Iterate through all potential neighbor positions
    for dr, dc in neighbor_deltas:
        nr, nc = r + dr, c + dc
        
        # Check if the neighbor coordinates are valid (within grid bounds)
        if _is_valid(nr, nc, num_rows, num_cols):
            # Check if the neighbor cell in the grid has the target value
            if grid[nr][nc] == value:
                return True # Found a neighbor with the same value

    # If the loop completes without finding a matching neighbor
    return False

def transform(input_grid):
    """
    Transforms the input grid based on neighbor values.

    A non-zero cell retains its value if at least one of its 8 neighbors 
    has the same value. Otherwise, the cell becomes 0. Zero cells remain 0.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A new 2D list representing the transformed grid.
    """
    # Handle empty or invalid input grid
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        # Or raise an error, depending on desired behavior
        return [] 

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize the output grid with the same dimensions, filled with zeros
    # Using list comprehension for initialization
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            cell_value = input_grid[r][c]

            # Process only non-zero cells
            if cell_value != 0:
                # Check if the current cell has at least one neighbor with the same value
                # Pass the original input_grid to the helper function for checking neighbors
                if _has_same_neighbor(input_grid, r, c, cell_value, num_rows, num_cols):
                    # If it has a matching neighbor, retain the value in the output grid
                    output_grid[r][c] = cell_value
                # Else: The cell value becomes 0 (already initialized)

            # If cell_value is 0, the output_grid[r][c] remains 0 (as initialized)

    # Return the newly constructed output grid
    return output_grid
```

Previous Code:
```python
import copy

"""
Filters a 2D grid of digits. For each non-zero cell in the input grid,
it checks its 8 neighbors (Moore neighborhood). If at least one neighbor
in the input grid has the same value as the cell, the cell's value is 
kept in the output grid. Otherwise (if the cell value is 0 or if it's 
non-zero but has no neighbors with the same value), the corresponding 
cell in the output grid is set to 0.
"""

def _is_valid(r, c, num_rows, num_cols):
    """
    Helper function to check if coordinates (r, c) are within the grid boundaries.

    Args:
        r (int): Row index.
        c (int): Column index.
        num_rows (int): Total number of rows in the grid.
        num_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if the coordinates are valid, False otherwise.
    """
    return 0 <= r < num_rows and 0 <= c < num_cols

def _has_same_neighbor(grid, r, c, value, num_rows, num_cols):
    """
    Helper function to check if any of the 8 neighbors of cell (r, c) 
    in the grid has the specified value.

    Args:
        grid (list[list[int]]): The input grid.
        r (int): Row index of the cell to check neighbors for.
        c (int): Column index of the cell to check neighbors for.
        value (int): The value to look for in the neighbors.
        num_rows (int): Total number of rows in the grid.
        num_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if at least one neighbor has the specified value, False otherwise.
    """
    # Define relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    # Iterate through all potential neighbor positions
    for dr, dc in neighbor_deltas:
        nr, nc = r + dr, c + dc
        
        # Check if the neighbor coordinates are valid (within grid bounds)
        if _is_valid(nr, nc, num_rows, num_cols):
            # Check if the neighbor cell in the grid has the target value
            if grid[nr][nc] == value:
                return True # Found a neighbor with the same value

    # If the loop completes without finding a matching neighbor
    return False

def transform(input_grid):
    """
    Transforms the input grid based on neighbor values.

    A non-zero cell retains its value if at least one of its 8 neighbors 
    has the same value. Otherwise, the cell becomes 0. Zero cells remain 0.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A new 2D list representing the transformed grid.
    """
    # Handle empty or invalid input grid
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        # Or raise an error, depending on desired behavior
        return [] 

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize the output grid with the same dimensions, filled with zeros
    # Using list comprehension for initialization
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            cell_value = input_grid[r][c]

            # Process only non-zero cells
            if cell_value != 0:
                # Check if the current cell has at least one neighbor with the same value
                # Pass the original input_grid to the helper function for checking neighbors
                if _has_same_neighbor(input_grid, r, c, cell_value, num_rows, num_cols):
                    # If it has a matching neighbor, retain the value in the output grid
                    output_grid[r][c] = cell_value
                # Else: The cell value becomes 0 (already initialized)

            # If cell_value is 0, the output_grid[r][c] remains 0 (as initialized)

    # Return the newly constructed output grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 2:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

Test Set Results:

## Example 1:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 2:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

## Example 3:
Error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
**General Assessment and Strategy**

The error message "The truth value of an array with more than one element is ambiguous" clearly indicates that the input data is being treated as a NumPy array rather than a standard Python list of lists. The previous code assumed list-of-lists semantics, leading to errors when performing comparisons within conditional statements (`if grid[nr][nc] == value:`).

The core logic identified previously – keeping a non-zero cell's value if and only if it has at least one neighbor (including diagonals) with the same value – appears consistent with the examples. The strategy is to adapt the implementation to correctly handle NumPy arrays, ensuring that neighbor checks and value comparisons work as expected within the NumPy framework.

**Metrics and Verification**


*code_execution:*
```python
import numpy as np

# Example train_1 data
input_1_str = """
0 0 0 0 0 2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 3 0 2 0 0 0 2 0 3 0 0 0 2 0 0 0 2 0 0 3
0 0 2 0 0 0 0 0 2 0 0 0 3 0 0 0 0 0 3 0 0
0 2 0 3 0 0 0 0 0 2 0 2 0 0 0 3 0 0 0 2 0
2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0 0 0 0 0 2
"""
output_1_str = """
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2
"""

# Example train_2 data
input_2_str = """
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 4 0 0 4 0 0 0 0 0
"""
output_2_str = """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0
"""

def parse_grid(grid_str):
    return np.array([[int(x) for x in row.split()] for row in grid_str.strip().split('\n')])

input_1 = parse_grid(input_1_str)
output_1 = parse_grid(output_1_str)
input_2 = parse_grid(input_2_str)
output_2 = parse_grid(output_2_str)

# Verification of data types and shapes
print(f"Input 1 type: {type(input_1)}, shape: {input_1.shape}, dtype: {input_1.dtype}")
print(f"Output 1 type: {type(output_1)}, shape: {output_1.shape}, dtype: {output_1.dtype}")
print(f"Input 2 type: {type(input_2)}, shape: {input_2.shape}, dtype: {input_2.dtype}")
print(f"Output 2 type: {type(output_2)}, shape: {output_2.shape}, dtype: {output_2.dtype}")

# Manual Check: Cell (2, 1) in train_1 input is 3. Check neighbors.
r, c = 2, 1
value = input_1[r, c]
num_rows, num_cols = input_1.shape
has_neighbor = False
for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
        if dr == 0 and dc == 0:
            continue
        nr, nc = r + dr, c + dc
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            if input_1[nr, nc] == value:
                has_neighbor = True
                break
    if has_neighbor:
        break

print(f"\nManual Check train_1[2, 1] (value={value}):")
print(f"  Has same neighbor? {has_neighbor}")
print(f"  Expected output value: {output_1[r, c]}")
print(f"  Logic correct for this cell? {output_1[r, c] == (value if has_neighbor else 0)}")

# Manual Check: Cell (1, 6) in train_1 input is 2. Check neighbors.
r, c = 1, 6
value = input_1[r, c]
num_rows, num_cols = input_1.shape
has_neighbor = False
for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
        if dr == 0 and dc == 0:
            continue
        nr, nc = r + dr, c + dc
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            if input_1[nr, nc] == value:
                has_neighbor = True
                break
    if has_neighbor:
        break

print(f"\nManual Check train_1[1, 6] (value={value}):")
print(f"  Has same neighbor? {has_neighbor}")
print(f"  Expected output value: {output_1[r, c]}")
print(f"  Logic correct for this cell? {output_1[r, c] == (value if has_neighbor else 0)}")


# Manual Check: Cell (0, 0) in train_2 input is 4. Check neighbors.
r, c = 0, 0
value = input_2[r, c]
num_rows, num_cols = input_2.shape
has_neighbor = False
for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
        if dr == 0 and dc == 0:
            continue
        nr, nc = r + dr, c + dc
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            if input_2[nr, nc] == value:
                has_neighbor = True
                break
    if has_neighbor:
        break

print(f"\nManual Check train_2[0, 0] (value={value}):")
print(f"  Has same neighbor? {has_neighbor}")
print(f"  Expected output value: {output_2[r, c]}")
print(f"  Logic correct for this cell? {output_2[r, c] == (value if has_neighbor else 0)}")

# Manual Check: Cell (3, 2) in train_2 input is 4. Check neighbors.
r, c = 3, 2
value = input_2[r, c]
num_rows, num_cols = input_2.shape
has_neighbor = False
for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
        if dr == 0 and dc == 0:
            continue
        nr, nc = r + dr, c + dc
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            if input_2[nr, nc] == value:
                has_neighbor = True
                break
    if has_neighbor:
        break

print(f"\nManual Check train_2[3, 2] (value={value}):")
print(f"  Has same neighbor? {has_neighbor}")
print(f"  Expected output value: {output_2[r, c]}")
print(f"  Logic correct for this cell? {output_2[r, c] == (value if has_neighbor else 0)}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Input 1 type: <class 'numpy.ndarray'>, shape: (6, 21), dtype: int64
Output 1 type: <class 'numpy.ndarray'>, shape: (6, 21), dtype: int64
Input 2 type: <class 'numpy.ndarray'>, shape: (6, 24), dtype: int64
Output 2 type: <class 'numpy.ndarray'>, shape: (6, 24), dtype: int64

Manual Check train_1[2, 1] (value=3):
  Has same neighbor? False
  Expected output value: 0
  Logic correct for this cell? True

Manual Check train_1[1, 6] (value=2):
  Has same neighbor? True
  Expected output value: 2
  Logic correct for this cell? True

Manual Check train_2[0, 0] (value=4):
  Has same neighbor? False
  Expected output value: 0
  Logic correct for this cell? True

Manual Check train_2[3, 2] (value=4):
  Has same neighbor? True
  Expected output value: 4
  Logic correct for this cell? True

```
**YAML Facts**


```yaml
task_description: "Filter a 2D NumPy array of digits, setting non-zero digits to zero if they lack neighbors of the same value."
elements:
  - object: grid
    properties:
      - type: 2D NumPy array
      - content: non-negative single digits (integers)
      - dimensionality: [rows, columns] (variable)
      - dtype: typically int (e.g., int64)
  - object: cell
    properties:
      - value: integer (0-9)
      - position: [row_index, column_index]
      - neighbors: set of up to 8 adjacent cells (Moore neighborhood), considering grid boundaries.
relationships:
  - type: adjacency
    between: cell
    details: A cell is adjacent to up to 8 other cells (horizontally, vertically, diagonally). Boundary cells have fewer neighbors within the grid.
actions:
  - action: process_grid
    actor: system
    input: input_grid (NumPy array)
    output: output_grid (NumPy array)
    rule: "Iterate through each cell of the input grid."
  - action: evaluate_cell
    actor: system
    input: current_cell_value, current_cell_position (r, c), input_grid
    output: output_cell_value
    rule: |
      1. Get the value (v) and position (r, c) of the current cell.
      2. If v is 0, the output_cell_value is 0.
      3. If v is non-zero:
         a. Examine the values of the 8 neighboring cells (Moore neighborhood) in the input_grid. Check boundaries to only consider valid neighbor indices.
         b. Check if any valid neighbor in the input_grid has the same value v.
         c. If at least one neighbor has value v, the output_cell_value is v.
         d. If no neighbor has value v, the output_cell_value is 0.
  - action: construct_output
    actor: system
    input: results of evaluate_cell for all cells
    output: output_grid (NumPy array)
    rule: "Assemble the output_cell_values into a new NumPy array with the same shape and dtype as the input grid."

```


**Natural Language Program**

1.  Receive the input grid as a 2D NumPy array.
2.  Determine the dimensions (number of rows and columns) of the input grid.
3.  Create a new output grid (as a NumPy array) of the same dimensions and data type as the input grid, initialized with zeros.
4.  Iterate through each cell of the *input* grid using its row index `r` (from 0 to rows-1) and column index `c` (from 0 to columns-1).
5.  Get the value `v` of the current cell `input_grid[r, c]`.
6.  If `v` is not 0:
    a.  Initialize a flag `found_same_neighbor` to `False`.
    b.  Iterate through the relative neighbor offsets `dr` from -1 to 1 and `dc` from -1 to 1.
    c.  Skip the current cell itself (where `dr` is 0 and `dc` is 0).
    d.  Calculate the neighbor coordinates `nr = r + dr` and `nc = c + dc`.
    e.  Check if the neighbor coordinates (`nr`, `nc`) are within the valid bounds of the grid (0 <= `nr` < rows and 0 <= `nc` < columns).
    f.  If the neighbor coordinates are valid and the value of the neighbor cell `input_grid[nr, nc]` is equal to `v`:
        i.  Set `found_same_neighbor` to `True`.
        ii. Break the inner loops (checking neighbors), as only one match is needed.
    g.  After checking all neighbors, if `found_same_neighbor` is `True`, set the corresponding cell in the *output* grid `output_grid[r, c]` to `v`.
    h.  (Implicitly, if `found_same_neighbor` is `False`, the `output_grid[r, c]` remains 0 from initialization).
7.  (Implicitly, if `v` was 0 initially, the `output_grid[r, c]` remains 0 from initialization).
8.  After iterating through all cells, return the completed output grid.
