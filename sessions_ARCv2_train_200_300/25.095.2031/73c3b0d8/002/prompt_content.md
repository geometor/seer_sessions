
Previous Code:
```python
import copy

"""
Simulates gravity on elements marked '4' within a grid.
The grid contains 0s (empty space), 4s (movable objects), and a single horizontal row of 2s (impassable boundary).
Objects (4s) fall downwards within their respective columns until they land on the row immediately above the boundary (2s) or immediately above another settled 4 in the same column.
The boundary row remains static. The process happens independently for each column.
"""

def find_boundary_row(grid: list[list[int]]) -> int:
    """Finds the index of the row consisting entirely of 2s."""
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    for r in range(num_rows):
        if all(grid[r][c] == 2 for c in range(num_cols)):
            return r
    return -1 # Should not happen based on problem description, but good practice

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies gravity to '4' elements in the grid, making them fall
    towards a boundary row of '2's.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid with '4's settled.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Find the boundary row (row of 2s)
    boundary_row_idx = find_boundary_row(output_grid)

    # If no boundary row is found, return the original grid (or handle as error)
    if boundary_row_idx == -1:
        # This case implies invalid input according to the examples
        print("Warning: Boundary row (all 2s) not found.")
        return output_grid 
        
    # Iterate through each column independently
    for c in range(num_cols):
        # Count the number of '4's in this column above the boundary
        fours_count = 0
        for r in range(boundary_row_idx): # Iterate rows above the boundary
            if output_grid[r][c] == 4:
                fours_count += 1
                # Clear the original position of the 4 in the output grid
                output_grid[r][c] = 0

        # Place the counted '4's starting from the row just above the boundary
        # and moving upwards
        landing_row = boundary_row_idx - 1
        for _ in range(fours_count):
            # Ensure we don't try to place a 4 outside the grid bounds (above row 0)
            # or overwrite the boundary itself (though the loop range prevents this)
            if landing_row >= 0:
                output_grid[landing_row][c] = 4
                landing_row -= 1 # Move the next landing spot one row up

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 4
0 0 4 0 0 0 4 0
0 0 0 4 0 4 0 0
0 0 0 0 4 0 0 0
2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 4 0 4 4 0 0
2 2 2 2 2 2 2 2
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 31.25

## Example 2:
Input:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 4 0 0 0 0
0 0 0 0 4 0
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
Expected Output:
```
4 0 0 0 0 0
0 4 0 0 0 0
0 0 4 0 0 0
0 4 0 4 0 4
0 0 0 0 4 0
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 4 0 0 4 0
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 23.333333333333343

## Example 3:
Input:
```
0 0 0
0 4 0
0 0 0
0 0 0
2 2 2
0 0 0
```
Expected Output:
```
0 0 0
0 0 0
0 4 0
0 0 0
2 2 2
0 0 0
```
Transformed Output:
```
0 0 0
0 0 0
0 0 0
0 4 0
2 2 2
0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 11.111111111111114

## Example 4:
Input:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
0 0 0 0 0
2 2 2 2 2
```
Expected Output:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
4 0 0 0 4
0 4 0 4 0
0 0 4 0 0
2 2 2 2 2
```
Transformed Output:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
2 2 2 2 2
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 22.85714285714286
