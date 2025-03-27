```python
import numpy as np
from typing import List, Tuple, Dict, Set

"""
Identify all distinct objects (connected groups of non-white pixels) in the input grid. 
Determine the color of each object. 
Find the median color value among the unique object colors. 
Locate the object in the input grid that corresponds to this median color. 
Calculate the minimal bounding box containing this object. 
Extract the subgrid defined by this bounding box from the input grid to create the output grid.
"""

def find_objects(grid: np.ndarray) -> Dict[int, List[Tuple[int, int]]]:
    """
    Finds all distinct objects (contiguous non-background pixels of the same color) 
    in the grid using Breadth-First Search (BFS).
    Assumes 4-connectivity (up, down, left, right).

    Args:
        grid: The input numpy array representing the grid.

    Returns:
        A dictionary where keys are the object colors and values are lists of 
        (row, col) tuples representing the pixels belonging to that object.
    """
    height, width = grid.shape
    visited: Set[Tuple[int, int]] = set()
    objects: Dict[int, List[Tuple[int, int]]] = {}

    for r in range(height):
        for c in range(width):
            if (r, c) in visited or grid[r, c] == 0:
                continue

            color = grid[r, c]
            obj_pixels: List[Tuple[int, int]] = []
            q: List[Tuple[int, int]] = [(r, c)]
            visited.add((r, c))

            while q:
                row, col = q.pop(0)
                obj_pixels.append((row, col))

                # Explore neighbors (4-connectivity)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < height and 0 <= nc < width and \
                       (nr, nc) not in visited and grid[nr, nc] == color:
                        visited.add((nr, nc))
                        q.append((nr, nc))
            
            # Store the found object pixels, merging if color already exists (shouldn't happen with distinct objects assumption)
            if color not in objects:
                 objects[color] = []
            objects[color].extend(obj_pixels) # Using extend might be incorrect if objects of the same color aren't connected, but description implies distinct objects. Let's stick to the definition.
            # If the problem implies separate regions of the same color are different objects, the logic needs adjustment.
            # However, based on examples, it seems each color represents one distinct object. So storing by color directly is okay.
            # If colors could repeat for *different* objects, we'd need a different structure, like List[Tuple[int, List[Tuple[int, int]]]].
            # Given the median logic, it seems likely we only care about the unique colors present.

    return objects

def get_bounding_box(pixels: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the minimum bounding box for a list of pixel coordinates.

    Args:
        pixels: A list of (row, col) tuples.

    Returns:
        A tuple (min_row, max_row, min_col, max_col).
    """
    if not pixels:
        return (0, 0, 0, 0) # Should not happen with valid objects

    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    
    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)

    return min_row, max_row, min_col, max_col

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the specified rules:
    1. Finds all objects.
    2. Gets their colors.
    3. Finds the median color.
    4. Selects the object with the median color.
    5. Extracts its bounding box.
    """
    # 1. Identify all distinct objects and their colors
    objects_by_color = find_objects(input_grid)
    
    # 2. Get the unique object colors
    object_colors = list(objects_by_color.keys())
    
    # 3. Sort the colors and find the median
    # Assuming exactly 3 objects as observed in training examples
    if len(object_colors) != 3:
         # Fallback or error handling if assumption is wrong
         # For now, let's proceed assuming 3. If test cases fail, revisit.
         print(f"Warning: Expected 3 objects, found {len(object_colors)}. Using median logic anyway.")
         if not object_colors:
             return np.array([[]]) # Return empty if no objects
         object_colors.sort()
         median_index = len(object_colors) // 2
         median_color = object_colors[median_index]

    else:
        object_colors.sort()
        median_color = object_colors[1] # Median of 3 sorted numbers is the middle one

    # 4. Get the pixels of the object with the median color
    median_object_pixels = objects_by_color[median_color]
    
    # 5. Calculate the bounding box for the median object
    min_row, max_row, min_col, max_col = get_bounding_box(median_object_pixels)
    
    # 6. Extract the subgrid defined by the bounding box
    # Note: Slicing is exclusive of the end index, so add 1 to max values
    output_grid = input_grid[min_row : max_row + 1, min_col : max_col + 1]
    
    return output_grid

```