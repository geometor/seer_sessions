
Previous Code:
```python
import numpy as np

"""
The transformation identifies all maximal monochromatic rectangles within the input grid.
A rectangle is monochromatic if all its pixels share the same color.
A rectangle is maximal if it cannot be expanded in any of the four cardinal directions (up, down, left, right) 
without either going out of bounds or including a pixel of a different color.

For each maximal monochromatic rectangle found, its area (height * width) is calculated.
If the area is 36 or greater, all pixels within the bounds of that rectangle in the output grid 
are replaced with the color yellow (4). 
If the area is less than 36, the pixels within that rectangle remain unchanged from the input grid.
All pixels outside of any maximal monochromatic rectangle also remain unchanged.
"""

def find_maximal_monochromatic_rectangles(grid):
    """
    Finds all maximal monochromatic rectangles in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing a maximal monochromatic rectangle
              with keys 'r' (row), 'c' (column), 'h' (height), 'w' (width), 'color'.
    """
    rows, cols = grid.shape
    # Keep track of visited cells to avoid redundant checks and overlapping rectangles
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    # Iterate through each cell as a potential top-left corner of a rectangle
    for r in range(rows):
        for c in range(cols):
            # Skip if this cell has already been included in a found rectangle
            if visited[r, c]:
                continue

            color = grid[r, c]

            # Find the initial maximum width starting from (r, c) in the current row
            initial_w = 0
            # Check rightwards from the current column 'c'
            for k in range(c, cols):
                # Only extend width if the cell has the same color and hasn't been visited
                # Note: Checking 'visited' here might prevent finding *maximal* rects
                # if part of it was 'visited' by a suboptimal rect found earlier.
                # A better approach might be to find all possible rectangles first,
                # then filter for maximality. However, this approach attempts to find
                # maximal ones directly by expanding from unvisited cells.
                if grid[r, k] == color:
                    initial_w += 1
                else:
                    # Stop extending width at the first color mismatch
                    break
            
            # This check was added previously but seems redundant if the outer loop iterates correctly
            # if initial_w == 0:
            #     visited[r,c] = True 
            #     continue

            # Determine the maximum possible height for this rectangle
            # The width might shrink as we check lower rows
            final_h = 0
            min_w = initial_w # Start with the width found for the first row
            
            # Iterate downwards from the starting row
            for i in range(r, rows):
                current_row_w = 0
                # Check cells in the current row up to the current minimum width (min_w)
                for j in range(c, c + min_w):
                    # Stop if the cell is out of bounds, or has the wrong color
                    # Crucially, don't stop based on 'visited' here, as we need to check the full
                    # potential extent of the rectangle, even if parts overlap previous checks.
                    if j >= cols or grid[i, j] != color:
                        # The rectangle cannot extend this wide in this row.
                        # Update min_w to the width that *did* match in this row.
                        min_w = j - c 
                        break # Stop checking this row further
                    current_row_w +=1
                
                # If the width shrank to zero, or the loop finished because width became 0, stop extending height
                if min_w == 0:
                    break
                
                # If we successfully checked min_w columns in this row (current_row_w == min_w)
                if current_row_w == min_w:
                     final_h += 1 # Increment the height of the rectangle
                else:
                    # If the row check didn't complete fully up to min_w, stop extending height
                     break


            # We have found a potential maximal rectangle anchored at (r, c)
            # with dimensions (final_h, min_w).
            # Mark only the cells within *this specific* found rectangle as visited.
            if final_h > 0 and min_w > 0:
                is_maximal = True
                # Check for horizontal maximality (can it extend left/right?)
                # Check left boundary
                if c > 0:
                    for row_idx in range(r, r + final_h):
                       if grid[row_idx, c - 1] == color:
                           is_maximal = False
                           break
                # Check right boundary
                if is_maximal and c + min_w < cols:
                    for row_idx in range(r, r + final_h):
                        if grid[row_idx, c + min_w] == color:
                            is_maximal = False
                            break
                
                # Check for vertical maximality (can it extend up/down?)
                # Check top boundary
                if is_maximal and r > 0:
                     for col_idx in range(c, c + min_w):
                        if grid[r - 1, col_idx] == color:
                            is_maximal = False
                            break
                # Check bottom boundary
                if is_maximal and r + final_h < rows:
                    for col_idx in range(c, c + min_w):
                        if grid[r + final_h, col_idx] == color:
                             is_maximal = False
                             break

                # Store the rectangle only if it's maximal
                if is_maximal:
                    # Only mark as visited *after* confirming maximality to allow overlap checks
                    visited[r : r + final_h, c : c + min_w] = True
                    rectangles.append({'r': r, 'c': c, 'h': final_h, 'w': min_w, 'color': color})
                else:
                    # If not maximal, still mark the starting cell visited to avoid re-processing it
                    # as the top-left of the same non-maximal shape. This might need refinement.
                     visited[r,c] = True


            # Ensure the starting point is marked visited even if no rectangle forms from it
            # or if it wasn't part of a maximal rectangle starting there.
            if not visited[r,c]:
                 visited[r,c] = True


    return rectangles


def transform(input_grid):
    """
    Transforms the input grid by filling large monochromatic rectangles with yellow.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to a NumPy array for efficient array operations and slicing
    np_grid = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify, this will be the output
    output_grid = np_grid.copy()

    # --- Refined Area Threshold ---
    # Define the minimum area threshold based on re-evaluation of examples
    min_area = 36 

    # --- Find Rectangles ---
    # Find all maximal monochromatic rectangles in the input grid
    # Using a potentially refined finder function
    rectangles = find_maximal_monochromatic_rectangles(np_grid)

    # --- Apply Transformation ---
    # Process each found maximal rectangle
    for rect in rectangles:
        # Calculate the area of the current rectangle
        area = rect['h'] * rect['w']

        # Check if the area meets the minimum requirement
        if area >= min_area:
            # Get the position (top-left corner) and dimensions
            r, c = rect['r'], rect['c']
            h, w = rect['h'], rect['w']
            
            # Fill the area defined by the rectangle in the output grid with yellow (color 4)
            # NumPy slicing allows efficient modification of the rectangular region
            output_grid[r : r + h, c : c + w] = 4

    # Convert the final NumPy array back to a list of lists format for the output
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
6 8 6 8 8 8 8 6 6 3 8 6 2 3 8 1 2 8 1 3 8 3 3 6 6 1 2 6 2 2
2 3 3 2 2 3 6 2 6 2 8 1 3 8 1 8 1 8 8 8 8 2 2 3 2 1 2 8 6 3
2 3 8 2 3 6 6 6 6 6 6 6 6 6 3 8 2 6 6 2 8 3 8 8 3 2 3 3 3 2
8 6 8 2 3 6 6 6 6 6 6 6 6 6 3 1 1 2 1 2 6 8 2 6 2 1 8 3 3 8
6 8 6 2 3 6 6 6 6 6 6 6 6 6 3 3 3 8 1 1 2 1 8 3 8 2 3 6 8 2
3 8 3 3 6 6 6 6 6 6 6 6 6 6 2 8 6 3 2 6 1 6 6 2 8 8 3 2 6 6
2 6 3 2 8 6 6 6 6 6 6 6 6 6 8 3 8 3 3 6 3 1 8 8 1 2 3 1 8 8
3 8 1 6 1 8 1 3 8 3 2 3 2 8 1 3 1 2 2 8 1 6 3 3 3 6 2 2 8 6
8 3 3 8 3 8 2 2 8 8 8 8 8 1 1 6 3 3 6 2 2 6 1 3 3 6 3 1 3 3
2 3 3 2 3 2 6 2 3 6 8 3 3 8 3 6 1 3 3 8 8 1 6 6 8 8 1 6 2 6
3 6 3 3 3 2 3 6 1 6 3 8 2 8 2 3 2 6 3 6 6 8 3 6 6 1 6 8 8 6
8 3 3 1 2 2 6 8 2 3 6 8 3 2 2 6 3 2 1 2 6 3 6 8 8 8 1 8 1 6
1 8 8 1 6 6 8 2 8 2 1 2 8 8 1 8 2 8 3 8 3 3 8 8 2 3 3 3 3 3
8 8 3 8 3 2 8 6 3 3 1 3 2 1 6 6 8 3 6 6 3 6 3 1 8 1 2 6 3 8
8 6 6 3 2 6 6 8 6 1 3 2 8 3 1 2 8 3 6 2 8 8 3 2 2 6 1 8 6 3
1 8 1 6 2 3 2 2 1 8 2 2 8 3 6 8 8 8 2 8 8 3 3 1 3 2 2 1 3 2
8 1 3 6 8 8 6 6 3 3 2 2 3 8 8 8 8 8 8 8 1 3 3 8 2 3 6 2 8 2
3 3 3 6 3 2 2 2 6 3 2 3 3 8 8 8 8 8 8 8 8 3 3 2 3 2 2 2 2 3
3 2 1 2 2 8 6 3 8 8 8 3 1 8 8 8 8 8 8 8 6 1 8 3 8 3 6 8 1 8
3 6 1 3 2 3 6 6 6 3 2 1 3 8 8 8 8 8 8 8 3 3 2 1 8 3 6 3 2 3
8 1 3 8 6 2 3 3 3 3 2 8 6 8 8 8 8 8 8 8 2 8 8 3 8 2 3 1 3 2
3 6 3 2 8 6 6 3 8 3 1 2 3 8 8 8 8 8 8 8 3 6 8 6 1 2 1 3 3 6
3 8 8 2 3 8 3 6 8 8 3 1 3 3 8 8 2 2 2 2 3 8 1 1 3 3 2 3 1 3
3 3 6 8 1 6 6 2 8 6 6 1 8 1 2 2 1 6 8 3 2 6 8 6 8 8 6 2 8 3
8 3 3 1 8 3 2 3 3 3 8 3 3 3 3 2 3 8 3 1 3 6 6 6 6 6 3 6 2 3
3 6 8 3 2 1 8 6 6 8 6 6 1 6 6 1 3 3 6 2 6 1 3 3 8 1 2 2 3 3
1 8 3 6 3 2 6 8 8 1 6 6 8 6 6 6 2 6 8 3 8 1 3 8 2 6 3 2 6 6
8 8 6 8 1 1 8 2 2 3 6 2 8 3 8 2 1 1 8 6 8 6 8 6 3 3 3 3 2 3
1 3 8 1 3 1 6 3 6 8 2 3 3 8 2 2 2 1 3 2 8 8 3 8 6 6 3 8 3 8
6 2 6 2 8 2 3 3 3 3 1 3 3 3 2 6 3 8 2 3 6 3 3 2 2 3 8 8 1 3
```
Expected Output:
```
6 8 6 8 8 8 8 6 6 3 8 6 2 3 8 1 2 8 1 3 8 3 3 6 6 1 2 6 2 2
2 3 3 2 2 3 6 2 6 2 8 1 3 8 1 8 1 8 8 8 8 2 2 3 2 1 2 8 6 3
2 3 8 2 3 4 4 4 4 4 4 4 4 4 3 8 2 6 6 2 8 3 8 8 3 2 3 3 3 2
8 6 8 2 3 4 4 4 4 4 4 4 4 4 3 1 1 2 1 2 6 8 2 6 2 1 8 3 3 8
6 8 6 2 3 4 4 4 4 4 4 4 4 4 3 3 3 8 1 1 2 1 8 3 8 2 3 6 8 2
3 8 3 3 6 4 4 4 4 4 4 4 4 4 2 8 6 3 2 6 1 6 6 2 8 8 3 2 6 6
2 6 3 2 8 4 4 4 4 4 4 4 4 4 8 3 8 3 3 6 3 1 8 8 1 2 3 1 8 8
3 8 1 6 1 8 1 3 8 3 2 3 2 8 1 3 1 2 2 8 1 6 3 3 3 6 2 2 8 6
8 3 3 8 3 8 2 2 8 8 8 8 8 1 1 6 3 3 6 2 2 6 1 3 3 6 3 1 3 3
2 3 3 2 3 2 6 2 3 6 8 3 3 8 3 6 1 3 3 8 8 1 6 6 8 8 1 6 2 6
3 6 3 3 3 2 3 6 1 6 3 8 2 8 2 3 2 6 3 6 6 8 3 6 6 1 6 8 8 6
8 3 3 1 2 2 6 8 2 3 6 8 3 2 2 6 3 2 1 2 6 3 6 8 8 8 1 8 1 6
1 8 8 1 6 6 8 2 8 2 1 2 8 8 1 8 2 8 3 8 3 3 8 8 2 3 3 3 3 3
8 8 3 8 3 2 8 6 3 3 1 3 2 1 6 6 8 3 6 6 3 6 3 1 8 1 2 6 3 8
8 6 6 3 2 6 6 8 6 1 3 2 8 3 1 2 8 3 6 2 8 8 3 2 2 6 1 8 6 3
1 8 1 6 2 3 2 2 1 8 2 2 8 3 6 8 8 8 2 8 8 3 3 1 3 2 2 1 3 2
8 1 3 6 8 8 6 6 3 3 2 2 3 4 4 4 4 4 4 4 1 3 3 8 2 3 6 2 8 2
3 3 3 6 3 2 2 2 6 3 2 3 3 4 4 4 4 4 4 4 8 3 3 2 3 2 2 2 2 3
3 2 1 2 2 8 6 3 8 8 8 3 1 4 4 4 4 4 4 4 6 1 8 3 8 3 6 8 1 8
3 6 1 3 2 3 6 6 6 3 2 1 3 4 4 4 4 4 4 4 3 3 2 1 8 3 6 3 2 3
8 1 3 8 6 2 3 3 3 3 2 8 6 4 4 4 4 4 4 4 2 8 8 3 8 2 3 1 3 2
3 6 3 2 8 6 6 3 8 3 1 2 3 4 4 4 4 4 4 4 3 6 8 6 1 2 1 3 3 6
3 8 8 2 3 8 3 6 8 8 3 1 3 3 8 8 2 2 2 2 3 8 1 1 3 3 2 3 1 3
3 3 6 8 1 6 6 2 8 6 6 1 8 1 2 2 1 6 8 3 2 6 8 6 8 8 6 2 8 3
8 3 3 1 8 3 2 3 3 3 8 3 3 3 3 2 3 8 3 1 3 6 6 6 6 6 3 6 2 3
3 6 8 3 2 1 8 6 6 8 6 6 1 6 6 1 3 3 6 2 6 1 3 3 8 1 2 2 3 3
1 8 3 6 3 2 6 8 8 1 6 6 8 6 6 6 2 6 8 3 8 1 3 8 2 6 3 2 6 6
8 8 6 8 1 1 8 2 2 3 6 2 8 3 8 2 1 1 8 6 8 6 8 6 3 3 3 3 2 3
1 3 8 1 3 1 6 3 6 8 2 3 3 8 2 2 2 1 3 2 8 8 3 8 6 6 3 8 3 8
6 2 6 2 8 2 3 3 3 3 1 3 3 3 2 6 3 8 2 3 6 3 3 2 2 3 8 8 1 3
```
Transformed Output:
```
6 8 6 8 8 8 8 6 6 3 8 6 2 3 8 1 2 8 1 3 8 3 3 6 6 1 2 6 2 2
2 3 3 2 2 3 6 2 6 2 8 1 3 8 1 8 1 8 8 8 8 2 2 3 2 1 2 8 6 3
2 3 8 2 3 6 6 6 6 6 6 6 6 6 3 8 2 6 6 2 8 3 8 8 3 2 3 3 3 2
8 6 8 2 3 6 6 6 6 6 6 6 6 6 3 1 1 2 1 2 6 8 2 6 2 1 8 3 3 8
6 8 6 2 3 6 6 6 6 6 6 6 6 6 3 3 3 8 1 1 2 1 8 3 8 2 3 6 8 2
3 8 3 3 6 6 6 6 6 6 6 6 6 6 2 8 6 3 2 6 1 6 6 2 8 8 3 2 6 6
2 6 3 2 8 6 6 6 6 6 6 6 6 6 8 3 8 3 3 6 3 1 8 8 1 2 3 1 8 8
3 8 1 6 1 8 1 3 8 3 2 3 2 8 1 3 1 2 2 8 1 6 3 3 3 6 2 2 8 6
8 3 3 8 3 8 2 2 8 8 8 8 8 1 1 6 3 3 6 2 2 6 1 3 3 6 3 1 3 3
2 3 3 2 3 2 6 2 3 6 8 3 3 8 3 6 1 3 3 8 8 1 6 6 8 8 1 6 2 6
3 6 3 3 3 2 3 6 1 6 3 8 2 8 2 3 2 6 3 6 6 8 3 6 6 1 6 8 8 6
8 3 3 1 2 2 6 8 2 3 6 8 3 2 2 6 3 2 1 2 6 3 6 8 8 8 1 8 1 6
1 8 8 1 6 6 8 2 8 2 1 2 8 8 1 8 2 8 3 8 3 3 8 8 2 3 3 3 3 3
8 8 3 8 3 2 8 6 3 3 1 3 2 1 6 6 8 3 6 6 3 6 3 1 8 1 2 6 3 8
8 6 6 3 2 6 6 8 6 1 3 2 8 3 1 2 8 3 6 2 8 8 3 2 2 6 1 8 6 3
1 8 1 6 2 3 2 2 1 8 2 2 8 3 6 8 8 8 2 8 8 3 3 1 3 2 2 1 3 2
8 1 3 6 8 8 6 6 3 3 2 2 3 8 8 8 8 8 8 8 1 3 3 8 2 3 6 2 8 2
3 3 3 6 3 2 2 2 6 3 2 3 3 8 8 8 8 8 8 8 8 3 3 2 3 2 2 2 2 3
3 2 1 2 2 8 6 3 8 8 8 3 1 8 8 8 8 8 8 8 6 1 8 3 8 3 6 8 1 8
3 6 1 3 2 3 6 6 6 3 2 1 3 8 8 8 8 8 8 8 3 3 2 1 8 3 6 3 2 3
8 1 3 8 6 2 3 3 3 3 2 8 6 8 8 8 8 8 8 8 2 8 8 3 8 2 3 1 3 2
3 6 3 2 8 6 6 3 8 3 1 2 3 8 8 8 8 8 8 8 3 6 8 6 1 2 1 3 3 6
3 8 8 2 3 8 3 6 8 8 3 1 3 3 8 8 2 2 2 2 3 8 1 1 3 3 2 3 1 3
3 3 6 8 1 6 6 2 8 6 6 1 8 1 2 2 1 6 8 3 2 6 8 6 8 8 6 2 8 3
8 3 3 1 8 3 2 3 3 3 8 3 3 3 3 2 3 8 3 1 3 6 6 6 6 6 3 6 2 3
3 6 8 3 2 1 8 6 6 8 6 6 1 6 6 1 3 3 6 2 6 1 3 3 8 1 2 2 3 3
1 8 3 6 3 2 6 8 8 1 6 6 8 6 6 6 2 6 8 3 8 1 3 8 2 6 3 2 6 6
8 8 6 8 1 1 8 2 2 3 6 2 8 3 8 2 1 1 8 6 8 6 8 6 3 3 3 3 2 3
1 3 8 1 3 1 6 3 6 8 2 3 3 8 2 2 2 1 3 2 8 8 3 8 6 6 3 8 3 8
6 2 6 2 8 2 3 3 3 3 1 3 3 3 2 6 3 8 2 3 6 3 3 2 2 3 8 8 1 3
```
Match: False
Pixels Off: 87
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 19.333333333333343

## Example 2:
Input:
```
3 3 2 6 3 6 8 8 8 2 3 3 3 3 3 6 3 3 8 8 1 2 2 6 3 3 2 8 1 1
8 2 1 6 3 1 8 3 1 8 3 8 8 1 3 2 8 3 8 8 3 1 3 1 8 3 2 6 2 6
1 8 3 1 8 8 8 8 8 8 1 3 2 3 3 6 6 2 3 6 2 2 2 2 2 2 2 3 2 3
1 2 8 1 8 8 8 8 8 8 3 8 1 2 1 1 2 3 8 3 2 2 2 2 2 2 2 2 1 3
1 3 8 1 8 8 8 8 8 8 3 2 3 3 8 3 1 1 3 3 2 2 2 2 2 2 2 6 8 3
3 3 8 2 8 8 8 8 8 8 3 3 1 3 2 3 6 1 1 2 2 2 2 2 2 2 2 3 6 2
8 2 1 1 8 8 8 8 8 8 3 3 6 1 3 1 8 1 2 1 2 2 2 2 2 2 2 2 3 8
1 3 3 6 8 8 8 8 8 8 8 1 2 8 2 8 2 1 3 3 2 2 2 2 2 2 2 2 8 6
3 1 3 8 3 2 3 8 1 3 1 8 1 3 1 2 3 1 8 6 2 1 3 1 1 8 3 1 6 3
2 8 6 3 1 3 8 2 1 3 2 3 3 3 3 1 8 3 3 6 2 8 2 2 6 2 1 6 2 3
8 8 2 2 3 1 1 3 2 3 3 8 2 3 3 8 8 6 6 2 1 2 6 2 3 3 3 2 6 3
6 3 2 2 8 3 2 3 3 1 3 2 2 3 2 6 3 2 2 1 1 2 1 8 6 3 2 1 8 2
8 6 2 8 2 2 2 3 3 8 1 1 3 1 6 1 3 2 8 3 8 3 3 3 3 3 3 1 8 1
8 8 2 8 8 6 8 6 3 8 6 1 3 2 8 3 6 6 2 6 3 8 3 3 3 3 3 3 8 1
1 8 2 6 2 8 1 3 6 3 8 2 2 3 6 1 6 2 8 3 8 3 3 3 3 3 3 2 2 3
3 2 8 1 1 3 2 2 2 6 8 3 8 8 1 2 8 6 1 3 1 2 3 3 3 3 3 2 2 2
8 3 8 1 2 3 8 6 3 3 3 1 6 3 1 2 1 3 2 3 2 8 3 3 3 3 3 8 3 3
6 2 3 8 6 2 2 1 8 8 1 1 1 1 1 1 1 6 6 2 1 6 3 1 6 8 3 1 2 3
2 1 2 1 8 2 3 2 6 8 1 1 1 1 1 1 1 1 1 1 3 6 2 1 2 2 2 3 3 1
1 8 8 2 8 2 2 2 3 1 1 1 1 1 1 1 1 8 2 3 2 3 6 6 2 3 3 3 6 3
2 6 8 3 6 1 3 8 3 6 1 1 1 1 1 1 1 2 3 3 3 1 6 3 3 6 1 3 2 2
6 8 6 2 3 2 6 3 3 1 1 1 1 1 1 1 1 3 3 8 1 6 3 3 3 8 1 8 2 3
6 3 1 3 6 6 1 6 3 8 1 1 1 1 1 1 1 1 2 1 6 3 3 8 1 8 3 8 2 1
3 2 2 3 1 1 2 3 8 6 1 3 3 1 8 3 1 8 8 3 8 3 1 8 8 1 1 2 1 8
3 2 3 6 1 8 3 6 3 3 2 2 1 3 6 3 2 3 8 3 8 3 2 2 2 2 3 3 1 6
2 8 6 2 2 1 8 3 1 6 8 2 3 2 3 2 3 3 3 3 2 2 2 8 6 8 3 6 1 3
6 2 3 2 3 3 8 3 3 6 2 2 3 3 8 8 1 3 1 2 8 3 8 3 3 3 6 1 2 2
2 3 2 1 2 6 3 1 8 3 1 6 2 3 8 2 6 1 1 1 3 6 8 1 2 8 6 2 3 2
2 1 8 2 6 3 8 2 3 6 8 8 2 8 8 3 2 3 1 6 8 2 6 3 2 3 2 1 8 3
1 6 3 1 6 6 3 1 2 8 8 1 8 1 3 3 1 2 6 8 3 1 6 8 3 8 3 1 1 8
```
Expected Output:
```
3 3 2 6 3 6 8 8 8 2 3 3 3 3 3 6 3 3 8 8 1 2 2 6 3 3 2 8 1 1
8 2 1 6 3 1 8 3 1 8 3 8 8 1 3 2 8 3 8 8 3 1 3 1 8 3 2 6 2 6
1 8 3 1 4 4 4 4 4 4 1 3 2 3 3 6 6 2 3 6 4 4 4 4 4 4 4 3 2 3
1 2 8 1 4 4 4 4 4 4 3 8 1 2 1 1 2 3 8 3 4 4 4 4 4 4 4 2 1 3
1 3 8 1 4 4 4 4 4 4 3 2 3 3 8 3 1 1 3 3 4 4 4 4 4 4 4 6 8 3
3 3 8 2 4 4 4 4 4 4 3 3 1 3 2 3 6 1 1 2 4 4 4 4 4 4 4 3 6 2
8 2 1 1 4 4 4 4 4 4 3 3 6 1 3 1 8 1 2 1 4 4 4 4 4 4 4 2 3 8
1 3 3 6 4 4 4 4 4 4 8 1 2 8 2 8 2 1 3 3 4 4 4 4 4 4 4 2 8 6
3 1 3 8 3 2 3 8 1 3 1 8 1 3 1 2 3 1 8 6 2 1 3 1 1 8 3 1 6 3
2 8 6 3 1 3 8 2 1 3 2 3 3 3 3 1 8 3 3 6 2 8 2 2 6 2 1 6 2 3
8 8 2 2 3 1 1 3 2 3 3 8 2 3 3 8 8 6 6 2 1 2 6 2 3 3 3 2 6 3
6 3 2 2 8 3 2 3 3 1 3 2 2 3 2 6 3 2 2 1 1 2 1 8 6 3 2 1 8 2
8 6 2 8 2 2 2 3 3 8 1 1 3 1 6 1 3 2 8 3 8 3 4 4 4 4 4 1 8 1
8 8 2 8 8 6 8 6 3 8 6 1 3 2 8 3 6 6 2 6 3 8 4 4 4 4 4 3 8 1
1 8 2 6 2 8 1 3 6 3 8 2 2 3 6 1 6 2 8 3 8 3 4 4 4 4 4 2 2 3
3 2 8 1 1 3 2 2 2 6 8 3 8 8 1 2 8 6 1 3 1 2 4 4 4 4 4 2 2 2
8 3 8 1 2 3 8 6 3 3 3 1 6 3 1 2 1 3 2 3 2 8 4 4 4 4 4 8 3 3
6 2 3 8 6 2 2 1 8 8 4 4 4 4 4 4 4 6 6 2 1 6 3 1 6 8 3 1 2 3
2 1 2 1 8 2 3 2 6 8 4 4 4 4 4 4 4 1 1 1 3 6 2 1 2 2 2 3 3 1
1 8 8 2 8 2 2 2 3 1 4 4 4 4 4 4 4 8 2 3 2 3 6 6 2 3 3 3 6 3
2 6 8 3 6 1 3 8 3 6 4 4 4 4 4 4 4 2 3 3 3 1 6 3 3 6 1 3 2 2
6 8 6 2 3 2 6 3 3 1 4 4 4 4 4 4 4 3 3 8 1 6 3 3 3 8 1 8 2 3
6 3 1 3 6 6 1 6 3 8 4 4 4 4 4 4 4 1 2 1 6 3 3 8 1 8 3 8 2 1
3 2 2 3 1 1 2 3 8 6 1 3 3 1 8 3 1 8 8 3 8 3 1 8 8 1 1 2 1 8
3 2 3 6 1 8 3 6 3 3 2 2 1 3 6 3 2 3 8 3 8 3 2 2 2 2 3 3 1 6
2 8 6 2 2 1 8 3 1 6 8 2 3 2 3 2 3 3 3 3 2 2 2 8 6 8 3 6 1 3
6 2 3 2 3 3 8 3 3 6 2 2 3 3 8 8 1 3 1 2 8 3 8 3 3 3 6 1 2 2
2 3 2 1 2 6 3 1 8 3 1 6 2 3 8 2 6 1 1 1 3 6 8 1 2 8 6 2 3 2
2 1 8 2 6 3 8 2 3 6 8 8 2 8 8 3 2 3 1 6 8 2 6 3 2 3 2 1 8 3
1 6 3 1 6 6 3 1 2 8 8 1 8 1 3 3 1 2 6 8 3 1 6 8 3 8 3 1 1 8
```
Transformed Output:
```
3 3 2 6 3 6 8 8 8 2 3 3 3 3 3 6 3 3 8 8 1 2 2 6 3 3 2 8 1 1
8 2 1 6 3 1 8 3 1 8 3 8 8 1 3 2 8 3 8 8 3 1 3 1 8 3 2 6 2 6
1 8 3 1 8 8 8 8 8 8 1 3 2 3 3 6 6 2 3 6 2 2 2 2 2 2 2 3 2 3
1 2 8 1 8 8 8 8 8 8 3 8 1 2 1 1 2 3 8 3 2 2 2 2 2 2 2 2 1 3
1 3 8 1 8 8 8 8 8 8 3 2 3 3 8 3 1 1 3 3 2 2 2 2 2 2 2 6 8 3
3 3 8 2 8 8 8 8 8 8 3 3 1 3 2 3 6 1 1 2 2 2 2 2 2 2 2 3 6 2
8 2 1 1 8 8 8 8 8 8 3 3 6 1 3 1 8 1 2 1 2 2 2 2 2 2 2 2 3 8
1 3 3 6 8 8 8 8 8 8 8 1 2 8 2 8 2 1 3 3 2 2 2 2 2 2 2 2 8 6
3 1 3 8 3 2 3 8 1 3 1 8 1 3 1 2 3 1 8 6 2 1 3 1 1 8 3 1 6 3
2 8 6 3 1 3 8 2 1 3 2 3 3 3 3 1 8 3 3 6 2 8 2 2 6 2 1 6 2 3
8 8 2 2 3 1 1 3 2 3 3 8 2 3 3 8 8 6 6 2 1 2 6 2 3 3 3 2 6 3
6 3 2 2 8 3 2 3 3 1 3 2 2 3 2 6 3 2 2 1 1 2 1 8 6 3 2 1 8 2
8 6 2 8 2 2 2 3 3 8 1 1 3 1 6 1 3 2 8 3 8 3 3 3 3 3 3 1 8 1
8 8 2 8 8 6 8 6 3 8 6 1 3 2 8 3 6 6 2 6 3 8 3 3 3 3 3 3 8 1
1 8 2 6 2 8 1 3 6 3 8 2 2 3 6 1 6 2 8 3 8 3 3 3 3 3 3 2 2 3
3 2 8 1 1 3 2 2 2 6 8 3 8 8 1 2 8 6 1 3 1 2 3 3 3 3 3 2 2 2
8 3 8 1 2 3 8 6 3 3 3 1 6 3 1 2 1 3 2 3 2 8 3 3 3 3 3 8 3 3
6 2 3 8 6 2 2 1 8 8 1 1 1 1 1 1 1 6 6 2 1 6 3 1 6 8 3 1 2 3
2 1 2 1 8 2 3 2 6 8 1 1 1 1 1 1 1 1 1 1 3 6 2 1 2 2 2 3 3 1
1 8 8 2 8 2 2 2 3 1 1 1 1 1 1 1 1 8 2 3 2 3 6 6 2 3 3 3 6 3
2 6 8 3 6 1 3 8 3 6 1 1 1 1 1 1 1 2 3 3 3 1 6 3 3 6 1 3 2 2
6 8 6 2 3 2 6 3 3 1 1 1 1 1 1 1 1 3 3 8 1 6 3 3 3 8 1 8 2 3
6 3 1 3 6 6 1 6 3 8 1 1 1 1 1 1 1 1 2 1 6 3 3 8 1 8 3 8 2 1
3 2 2 3 1 1 2 3 8 6 1 3 3 1 8 3 1 8 8 3 8 3 1 8 8 1 1 2 1 8
3 2 3 6 1 8 3 6 3 3 2 2 1 3 6 3 2 3 8 3 8 3 2 2 2 2 3 3 1 6
2 8 6 2 2 1 8 3 1 6 8 2 3 2 3 2 3 3 3 3 2 2 2 8 6 8 3 6 1 3
6 2 3 2 3 3 8 3 3 6 2 2 3 3 8 8 1 3 1 2 8 3 8 3 3 3 6 1 2 2
2 3 2 1 2 6 3 1 8 3 1 6 2 3 8 2 6 1 1 1 3 6 8 1 2 8 6 2 3 2
2 1 8 2 6 3 8 2 3 6 8 8 2 8 8 3 2 3 1 6 8 2 6 3 2 3 2 1 8 3
1 6 3 1 6 6 3 1 2 8 8 1 8 1 3 3 1 2 6 8 3 1 6 8 3 8 3 1 1 8
```
Match: False
Pixels Off: 145
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.22222222222223
