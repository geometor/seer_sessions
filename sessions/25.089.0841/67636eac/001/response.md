```python
import numpy as np
from typing import List, Tuple

"""
Identifies all 3x3 "plus-sign" shapes in the input grid. 
A plus-sign shape is defined as a 3x3 area with a white center (0), four 
orthogonally adjacent pixels of the same non-white color, and four white 
corner pixels.
Extracts these 3x3 shapes.
Determines the primary spatial arrangement (vertical or horizontal) of these 
shapes in the input grid based on the range of their top-left corner coordinates.
Sorts the extracted shapes based on their original position: top-to-bottom 
(then left-to-right) if vertically arranged, or left-to-right (then top-to-bottom) 
if horizontally arranged.
Concatenates the sorted shapes accordingly (vertically stacked or horizontally 
aligned) to form the output grid.
"""

def find_plus_shapes(grid: np.ndarray) -> List[Tuple[int, int, np.ndarray]]:
    """
    Finds all unique 3x3 plus-sign shapes in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple contains:
        - The top row index of the shape's bounding box.
        - The top column index of the shape's bounding box.
        - A 3x3 numpy array representing the shape.
    """
    h, w = grid.shape
    found_shapes = {} # Use dict keyed by (row, col) to store unique shapes

    # Iterate through potential center cells (r, c)
    # The center of a 3x3 shape cannot be on the border
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            # Check if the potential center is white
            if grid[r, c] == 0:
                # Get neighbor colors
                center_color = 0 # grid[r, c]
                up_color = grid[r - 1, c]
                down_color = grid[r + 1, c]
                left_color = grid[r, c - 1]
                right_color = grid[r, c + 1]
                
                # Check if orthogonal neighbors are the same non-white color
                if up_color != 0 and up_color == down_color == left_color == right_color:
                    shape_color = up_color
                    # Check if corner neighbors are white
                    tl_color = grid[r - 1, c - 1]
                    tr_color = grid[r - 1, c + 1]
                    bl_color = grid[r + 1, c - 1]
                    br_color = grid[r + 1, c + 1]
                    
                    if tl_color == 0 and tr_color == 0 and bl_color == 0 and br_color == 0:
                        # Valid plus shape found
                        top_row, top_col = r - 1, c - 1
                        # Extract the 3x3 subgrid
                        shape_grid = grid[top_row : top_row + 3, top_col : top_col + 3]
                        # Store it using its top-left coordinate as the key to avoid duplicates
                        found_shapes[(top_row, top_col)] = shape_grid
                        
    # Convert the dictionary items to the desired list format
    shapes_list = [(r, c, shape) for (r, c), shape in found_shapes.items()]
    return shapes_list


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by extracting 3x3 plus-sign shapes and 
    concatenating them either vertically or horizontally based on their 
    original spatial arrangement.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)
    
    # Find all 3x3 plus shapes and their top-left coordinates
    shapes = find_plus_shapes(input_np)

    # If no shapes are found, return an empty grid or handle as needed
    if not shapes:
        # Based on examples, this case doesn't seem to occur, but return empty for safety
        return [] 
        
    # If only one shape, return it directly
    if len(shapes) == 1:
         return shapes[0][2].tolist()

    # Determine the spatial arrangement (vertical or horizontal dominance)
    rows = [r for r, c, s in shapes]
    cols = [c for r, c, s in shapes]
    
    # Calculate the range of rows and columns
    # Add 1 to avoid division by zero or issues if all shapes are aligned perfectly
    row_range = max(rows) - min(rows) 
    col_range = max(cols) - min(cols)
    
    # Decide stacking direction: stack vertically if row range is >= column range
    stack_vertically = row_range >= col_range

    # Sort the shapes based on the determined arrangement
    if stack_vertically:
        # Sort primarily by row (top-to-bottom), then column (left-to-right)
        sorted_shapes = sorted(shapes, key=lambda x: (x[0], x[1]))
    else:
        # Sort primarily by column (left-to-right), then row (top-to-bottom)
        sorted_shapes = sorted(shapes, key=lambda x: (x[1], x[0]))

    # Extract just the 3x3 shape grids in the sorted order
    shape_grids = [s[2] for s in sorted_shapes]

    # Concatenate the grids
    if stack_vertically:
        output_np = np.vstack(shape_grids)
    else:
        output_np = np.hstack(shape_grids)

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```