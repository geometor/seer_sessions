import numpy as np
from collections import Counter, deque

"""
Identify all distinct objects (connected groups of same non-white pixels) in the input grid.
Calculate the size (pixel count) of each object.
Determine the frequency of each size.
Count how many sizes appear only once (unique sizes).

Selection Logic:
1. If exactly one unique size exists, select the object with that unique size.
2. If all object sizes are unique, calculate the average size of all objects and select the object whose size is numerically closest to the average.

Output:
Crop the input grid to the minimal bounding box of the selected object.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                if obj_coords:
                    objects.append({'color': color, 'coords': obj_coords})
    return objects

def get_bounding_box(coords):
    """
    Calculates the minimal bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col)
    """
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def crop_grid(grid, bbox):
    """
    Extracts a subgrid defined by the bounding box.

    Args:
        grid (np.array): The input grid.
        bbox (tuple): (min_row, min_col, max_row, max_col)

    Returns:
        np.array: The cropped subgrid.
    """
    min_row, min_col, max_row, max_col = bbox
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Find all objects
    objects = find_objects(input_grid)
    if not objects:
        # Handle edge case: no objects found (return empty or based on convention)
        return np.array([[]])

    # 2. Calculate sizes for each object
    for obj in objects:
        obj['size'] = len(obj['coords'])

    # 3. Analyze sizes
    sizes = [obj['size'] for obj in objects]
    size_counts = Counter(sizes)
    unique_sizes = [size for size, count in size_counts.items() if count == 1]

    selected_object = None

    # 4. Apply selection logic
    if len(unique_sizes) == 1:
        # Case 1: Exactly one unique size
        unique_size_value = unique_sizes[0]
        for obj in objects:
            if obj['size'] == unique_size_value:
                selected_object = obj
                break
    elif len(unique_sizes) == len(objects):
         # Case 2: All sizes are unique
        if len(objects) == 1: # If only one object, it must be selected
             selected_object = objects[0]
        else:
            average_size = sum(sizes) / len(sizes)
            min_diff = float('inf')
            # Find object closest to average size
            for obj in objects:
                diff = abs(obj['size'] - average_size)
                if diff < min_diff:
                    min_diff = diff
                    selected_object = obj
                # Simple tie-breaking: keep the first one found with min_diff
    else:
         # Case 3: Other scenarios (e.g., multiple non-unique sizes, no unique sizes)
         # The provided examples don't cover this. If this occurs, the logic is undefined.
         # Returning an empty grid or raising an error might be appropriate.
         # For now, let's assume the examples cover all expected scenarios.
         # If we must return something, maybe return the largest object? Or smallest?
         # Let's stick to the defined logic for now.
         # If no selection rule matched, selected_object remains None.
         pass # selected_object will remain None


    if selected_object is None:
         # This case should ideally not happen based on the examples,
         # but as a fallback, perhaps return an empty grid or the input?
         # Let's return an empty 1x1 grid with background color for now.
         print("Warning: No selection rule matched. Returning default.")
         return np.array([[0]])


    # 5. Get bounding box of the selected object
    bbox = get_bounding_box(selected_object['coords'])

    # 6. Create output grid by cropping
    # We need to create a new grid based on the object's pixels within its bounding box
    min_row, min_col, max_row, max_col = bbox
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int) # Default to background color

    for r, c in selected_object['coords']:
        output_grid[r - min_row, c - min_col] = selected_object['color']


    return output_grid