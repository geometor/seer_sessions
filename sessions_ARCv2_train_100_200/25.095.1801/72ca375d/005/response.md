```python
import numpy as np
from collections import deque
import math # Although median calculation doesn't strictly need math module here

"""
Identify all distinct connected groups (objects) of the same non-zero digit within the input grid.
Create a list containing the unique digit value associated with each distinct object found.
Sort this list of unique digit values in ascending order.
Determine the median value from this sorted list. (For a list with an odd number of elements, this is the middle element).
Find the specific object identified in step 1 whose digit value is equal to the calculated median value.
Determine the bounding box (minimum and maximum row and column indices) of this selected object.
Extract the rectangular subgrid from the original input grid defined by this bounding box. This subgrid is the final output.
"""

# --- Helper Functions ---

def _find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all connected components of non-zero digits using Breadth-First Search (BFS) 
    and determines their bounding boxes.
    
    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'digit' and 'bbox' [min_row, max_row, min_col, max_col].
        Example: [{'digit': 4, 'bbox': [1, 2, 2, 3]}, ...]
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not visited, start a search (BFS)
            if grid[r, c] != 0 and (r, c) not in visited:
                digit = grid[r, c]
                object_cells = []
                q = deque([(r, c)])
                visited.add((r,c)) # Mark starting cell visited immediately

                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    curr_r, curr_c = q.popleft()
                    object_cells.append((curr_r, curr_c))
                    
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)
                    
                    # Add neighbors to the queue (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, correct digit, and if not visited before adding
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == digit and (nr, nc) not in visited:
                             visited.add((nr, nc)) # Mark visited when adding to queue
                             q.append((nr, nc))

                if object_cells: # Ensure we found at least one cell for the object
                     objects.append({
                         'digit': digit, 
                         'bbox': [min_r, max_r, min_c, max_c]
                     })
                     
    return objects

def _calculate_median(digits: list[int]) -> float | int | None:
    """Calculates the median value of a list of numbers."""
    n = len(digits)
    if n == 0: 
        return None
    sorted_digits = sorted(digits)
    mid_index = n // 2
    if n % 2 == 1:
        # Odd number of elements, median is the middle one
        return sorted_digits[mid_index]
    else:
        # Even number of elements, median is the average of the two middle ones
        # Note: Based on examples, expecting odd count, but handle even for robustness.
        return (sorted_digits[mid_index - 1] + sorted_digits[mid_index]) / 2


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by selecting the object whose digit is the median
    of all unique object digits present, and returning its bounding box.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # 1. Identify all distinct connected non-zero objects and their digits/bboxes
    objects = _find_objects(grid_np)

    # Handle edge case: no objects found
    if not objects:
        return [] 

    # 2. Create a sorted list of unique digit values from all identified objects
    unique_digits = sorted(list(set(obj['digit'] for obj in objects)))

    # 3. Determine the median value from this sorted list
    median_digit = _calculate_median(unique_digits)
    
    # Handle edge case: median couldn't be calculated (e.g., no unique digits)
    if median_digit is None:
        return [] 

    # 4. Find the object whose digit value matches the median
    selected_object = None
    for obj in objects:
        # Use math.isclose for potential floating point medians if needed,
        # but digits are ints, so direct comparison is fine here.
        if obj['digit'] == median_digit:
            selected_object = obj
            break # Assume only one object will match the median based on examples

    # Handle edge case: no object matched the median (shouldn't happen based on examples)
    if selected_object is None:
        return []

    # 5. Determine the bounding box of the selected object
    min_r, max_r, min_c, max_c = selected_object['bbox']

    # 6. Extract the rectangular subgrid defined by the bounding box
    output_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert the output NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```