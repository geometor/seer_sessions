```python
"""
Transformation rule:
1. Identify the primary non-white color (C) and the single contiguous object made of this color in the input grid.
2. Determine if the object is "solid" or "hollow".
    - An object is "solid" if at least one pixel of color C has all 8 of its neighbors also being color C.
    - Otherwise, the object is "hollow".
3. If the object is "solid", create an "outline" of the object.
    - The outline consists of only those pixels of color C from the input that were adjacent (8 directions) to at least one background pixel (0). All other pixels become background (0).
4. If the object is "hollow", create a "filled" version of the shape.
    - Start with the input grid.
    - Change any background pixel (0) to color C if it has pixels of color C both to its left and right on the same row, OR if it has pixels of color C both above and below it in the same column.
"""

import numpy as np
from typing import List, Tuple, Set

def _get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Get valid 8-directional neighbor coordinates."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def _find_object_pixels(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]]]:
    """Find the non-background color and the set of coordinates for the object."""
    object_color = -1
    object_pixels = set()
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                if object_color == -1:
                    object_color = grid[r, c]
                elif grid[r, c] != object_color:
                    # Assuming only one object color besides background
                    # This case shouldn't happen based on examples, but good practice
                    pass # Or raise an error
                
                if grid[r, c] == object_color:
                     object_pixels.add((r, c))

    if object_color == -1: # Handle case of all background
        object_color = 0 # Default to background if no object found

    return object_color, object_pixels

def _is_solid(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> bool:
    """Check if any object pixel has all 8 neighbors of the same object color."""
    height, width = grid.shape
    for r, c in object_pixels:
        neighbors = _get_neighbors(r, c, height, width)
        if len(neighbors) < 8: # Pixel on the edge cannot be fully surrounded
             continue
        
        all_neighbors_are_object_color = True
        for nr, nc in neighbors:
            if grid[nr, nc] != object_color:
                all_neighbors_are_object_color = False
                break
        
        if all_neighbors_are_object_color:
            return True # Found an interior pixel, so it's solid
            
    return False # No interior pixel found

def _create_outline(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> np.ndarray:
    """Keep only object pixels adjacent to background."""
    height, width = grid.shape
    output_grid = np.zeros_like(grid) # Start with all background

    for r, c in object_pixels:
        is_boundary = False
        neighbors = _get_neighbors(r, c, height, width)
        for nr, nc in neighbors:
            if grid[nr, nc] == 0: # Check if adjacent to background
                is_boundary = True
                break
        
        if is_boundary:
            output_grid[r, c] = object_color
            
    return output_grid

def _fill_shape(grid: np.ndarray, object_color: int) -> np.ndarray:
    """Fill the shape defined by the hollow object."""
    height, width = grid.shape
    output_grid = grid.copy() # Start with the input grid

    for r in range(height):
        for c in range(width):
            if output_grid[r, c] == 0: # Only consider filling background pixels
                # Check horizontal containment
                found_left = any(output_grid[r, j] == object_color for j in range(c))
                found_right = any(output_grid[r, j] == object_color for j in range(c + 1, width))
                horizontal_contained = found_left and found_right

                # Check vertical containment
                found_up = any(output_grid[i, c] == object_color for i in range(r))
                found_down = any(output_grid[i, c] == object_color for i in range(r + 1, height))
                vertical_contained = found_up and found_down

                # Fill if horizontally OR vertically contained
                if horizontal_contained or vertical_contained:
                    output_grid[r, c] = object_color
                    
    return output_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by either filling a hollow shape or creating an outline 
    of a solid shape.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Find the object's color and pixel coordinates
    object_color, object_pixels = _find_object_pixels(grid_np)

    # Handle edge case: no object found or empty grid
    if object_color == 0 or not object_pixels:
        return input_grid # Return original grid if no object pixels

    # Determine if the object is solid or hollow
    solid = _is_solid(grid_np, object_pixels, object_color)

    # Apply the corresponding transformation
    if solid:
        # If solid, create the outline
        output_grid_np = _create_outline(grid_np, object_pixels, object_color)
    else:
        # If hollow, fill the shape
        # Note: The fill logic needs the original pixel locations, 
        # so we pass the original grid_np, not just object_pixels
        output_grid_np = _fill_shape(grid_np, object_color)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid

```