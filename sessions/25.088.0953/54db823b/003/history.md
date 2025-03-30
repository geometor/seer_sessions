
Previous Code:
```python
import numpy as np
from scipy.ndimage import label, find_objects as scipy_find_objects

"""
Identifies all connected components (objects) of non-white pixels (colors 3-green and 9-maroon) using 8-way connectivity.
Calculates the number of maroon (9) pixels within each object ('maroon_count') and the total size of the object ('size').
Determines the median 'maroon_count' across all objects (using the lower median if the number of objects is even).
Selects the object(s) whose 'maroon_count' matches this median value.
If multiple objects match the median count, selects the one with the largest 'size'.
If there's still a tie in size, selects the object whose top-most, then left-most pixel occurs first in grid scan order (row-major).
Removes the selected object by changing all its pixels to white (0) in the output grid.
If no non-white objects are found, returns the input grid unchanged.
"""

def get_objects_properties(grid):
    """
    Finds all connected non-background objects (value != 0) in the grid
    using 8-way connectivity and calculates their properties.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (list of (r, c) tuples), 'maroon_count' (int),
              'size' (int), and 'top_left' (tuple (min_row, min_col)).
              Returns an empty list if no non-background objects are found.
    """
    # Define connectivity for 8-way (including diagonals)
    structure = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]], dtype=bool)

    # Create a boolean mask where True indicates non-background pixels
    mask = grid != 0

    # Label connected components
    labeled_array, num_features = label(mask, structure=structure)

    if num_features == 0:
        return []

    # Find the bounding boxes and coordinates for each labeled object
    objects_slices = scipy_find_objects(labeled_array)
    objects_properties = []

    for i in range(num_features):
        obj_label = i + 1
        coords = list(zip(*np.where(labeled_array == obj_label)))

        if not coords: # Should not happen with scipy_find_objects result but safety check
            continue

        maroon_count = 0
        size = len(coords)
        min_row = float('inf')
        min_col_at_min_row = float('inf')

        for r, c in coords:
            if grid[r, c] == 9: # Count maroon pixels
                maroon_count += 1
            # Determine the top-most, left-most coordinate for tie-breaking
            if r < min_row:
                min_row = r
                min_col_at_min_row = c
            elif r == min_row and c < min_col_at_min_row:
                min_col_at_min_row = c

        objects_properties.append({
            'coords': coords,
            'maroon_count': maroon_count,
            'size': size,
            'top_left': (min_row, min_col_at_min_row) # Store for tie-breaking
        })

    return objects_properties

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Identify all distinct non-white objects and their properties
    objects = get_objects_properties(output_grid)

    # If no objects found, return the original grid
    if not objects:
        return output_grid

    # 2. Calculate maroon_count and size (done in get_objects_properties)

    # 3. Create a list of maroon_counts
    maroon_counts = [obj['maroon_count'] for obj in objects]

    # 4. Determine the target median maroon_count
    sorted_counts = sorted(maroon_counts)
    n = len(sorted_counts)
    if n % 2 == 1:
        median_index = n // 2
        target_maroon_count = sorted_counts[median_index]
    else:
        # Use the lower median for even number of objects
        median_index = n // 2 - 1
        target_maroon_count = sorted_counts[median_index]

    # 5. Identify all objects matching the target_maroon_count
    matching_objects = [obj for obj in objects if obj['maroon_count'] == target_maroon_count]

    # 6. & 7. Select the object to remove based on criteria
    object_to_remove = None
    if len(matching_objects) == 1:
        object_to_remove = matching_objects[0]
    elif len(matching_objects) > 1:
        # Tie-breaker 1: Largest size
        max_size = -1
        potential_objects = []
        for obj in matching_objects:
            if obj['size'] > max_size:
                max_size = obj['size']
                potential_objects = [obj]
            elif obj['size'] == max_size:
                potential_objects.append(obj)

        if len(potential_objects) == 1:
             object_to_remove = potential_objects[0]
        else:
             # Tie-breaker 2: Top-most, then left-most pixel
             potential_objects.sort(key=lambda obj: (obj['top_left'][0], obj['top_left'][1]))
             object_to_remove = potential_objects[0]


    # 8. Create output grid (already done by copying input)

    # 9. Remove the selected object by setting its pixels to white (0)
    if object_to_remove:
        for r, c in object_to_remove['coords']:
            output_grid[r, c] = 0

    # 10. Return the modified output grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 3 3 9 3 3 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 3 9 3 3 0 0 0 0
0 9 3 3 9 3 0 3 3 3 9 0 0 0 0
0 0 0 0 0 0 0 9 3 9 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0 0
3 3 9 0 0 0 0 0 0 0 0 0 0 0 0
9 3 3 0 0 3 9 3 0 0 0 3 3 9 3
3 9 3 0 0 3 3 9 0 0 0 9 3 3 3
3 3 3 0 0 0 0 0 0 0 0 3 3 9 3
9 3 3 0 0 0 0 0 0 0 0 3 9 3 3
3 3 9 0 3 3 3 9 3 0 0 3 3 9 3
0 0 0 0 9 3 9 3 3 0 0 3 3 3 9
0 0 0 0 3 3 3 3 3 0 0 9 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 3 3 9 3 3 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 3 9 3 3 0 0 0 0
0 9 3 9 3 3 0 3 3 3 9 0 0 0 0
0 0 0 0 0 0 0 9 3 9 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0 0
3 3 9 0 0 0 0 0 0 0 0 0 0 0 0
9 3 3 0 0 0 0 0 0 0 0 3 3 9 3
3 9 3 0 0 0 0 0 0 0 0 9 3 3 3
3 3 3 0 0 0 0 0 0 0 0 3 3 9 3
9 3 3 0 0 0 0 0 0 0 0 3 9 3 3
3 3 9 0 3 3 3 9 3 0 0 3 3 9 3
0 0 0 0 9 3 9 3 3 0 0 3 3 3 9
0 0 0 0 3 3 3 3 3 0 0 9 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 9 3 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 9 0 0 0 0
0 0 0 0 0 0 0 9 3 9 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0 0
3 3 9 0 0 0 0 0 0 0 0 0 0 0 0
9 3 3 0 0 3 9 3 0 0 0 3 3 9 3
3 9 3 0 0 3 3 9 0 0 0 9 3 3 3
3 3 3 0 0 0 0 0 0 0 0 3 3 9 3
9 3 3 0 0 0 0 0 0 0 0 3 9 3 3
3 3 9 0 3 3 3 9 3 0 0 3 3 9 3
0 0 0 0 9 3 9 3 3 0 0 3 3 3 9
0 0 0 0 3 3 3 3 3 0 0 9 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.666666666666686

## Example 2:
Input:
```
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 9 3 9 0 0 3 3 3 3 3 0 0 0 0
0 3 9 3 0 0 3 3 3 9 3 0 0 0 0
0 3 3 9 0 0 3 3 3 3 3 0 0 0 0
0 3 3 3 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 3 9 3 0 0 0 0 0 0 0 0 0 0
0 0 9 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 3 3 3 3 3 0 0 3 3 3 3 3 3 3
0 3 3 3 3 3 0 0 3 9 3 9 9 3 3
0 3 9 3 3 3 0 0 3 3 3 3 3 3 3
0 3 3 3 3 3 0 0 3 3 9 3 3 3 3
0 3 3 3 9 3 0 0 3 3 3 3 3 3 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 9 3 9 0 0 0 0 0 0 0 0 0 0 0
0 3 9 3 0 0 0 0 0 0 0 0 0 0 0
0 3 3 9 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 9 3 0 0 0 0 0 0 0 0 0 0
0 0 9 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 3 3 3 3 3 0 0 3 3 3 3 3 3 3
0 3 3 3 3 3 0 0 3 9 3 9 9 3 3
0 3 9 3 3 3 0 0 3 3 3 3 3 3 3
0 3 3 3 3 3 0 0 3 3 9 3 3 3 3
0 3 3 3 9 3 0 0 3 3 3 3 3 3 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 9 3 9 0 0 3 3 3 3 3 0 0 0 0
0 3 9 3 0 0 3 3 3 9 3 0 0 0 0
0 3 3 9 0 0 3 3 3 3 3 0 0 0 0
0 3 3 3 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 3 9 3 0 0 0 0 0 0 0 0 0 0
0 0 9 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 9 3 9 9 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 9 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 50
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 44.44444444444443

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3
0 3 3 3 3 3 0 0 0 0 0 0 3 9 3
0 3 3 9 3 3 0 3 3 3 3 0 3 9 3
0 3 9 3 3 3 0 3 9 9 3 0 3 3 9
0 0 0 0 0 0 0 3 3 3 3 0 9 3 3
0 0 0 0 0 0 0 3 3 9 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 9 3 3 3 0 0 0 0 0 0 0 3 3 0
3 3 3 9 3 0 0 0 0 0 0 0 3 9 0
3 9 3 3 3 0 0 3 3 3 3 0 3 3 0
3 3 3 9 3 0 0 3 9 3 9 0 3 9 0
0 0 0 0 0 0 0 3 3 3 3 0 9 3 0
0 0 0 0 0 0 0 3 9 9 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 3 9 3
0 0 0 0 0 0 0 3 3 3 3 0 3 9 3
0 0 0 0 0 0 0 3 9 9 3 0 3 3 9
0 0 0 0 0 0 0 3 3 3 3 0 9 3 3
0 0 0 0 0 0 0 3 3 9 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 9 3 3 3 0 0 0 0 0 0 0 3 3 0
3 3 3 9 3 0 0 0 0 0 0 0 3 9 0
3 9 3 3 3 0 0 3 3 3 3 0 3 3 0
3 3 3 9 3 0 0 3 9 3 9 0 3 9 0
0 0 0 0 0 0 0 3 3 3 3 0 9 3 0
0 0 0 0 0 0 0 3 9 9 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3
0 3 3 3 3 3 0 0 0 0 0 0 3 9 3
0 3 3 9 3 3 0 0 0 0 0 0 3 9 3
0 3 9 3 3 3 0 0 0 0 0 0 3 3 9
0 0 0 0 0 0 0 0 0 0 0 0 9 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 9 3 3 3 0 0 0 0 0 0 0 3 3 0
3 3 3 9 3 0 0 0 0 0 0 0 3 9 0
3 9 3 3 3 0 0 3 3 3 3 0 3 3 0
3 3 3 9 3 0 0 3 9 3 9 0 3 9 0
0 0 0 0 0 0 0 3 3 3 3 0 9 3 0
0 0 0 0 0 0 0 3 9 9 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 31
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 27.555555555555543

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 9 3 3 3 3 0 0 0 3 3 9 3 9
3 3 3 3 3 9 3 0 0 0 3 3 3 3 3
3 9 3 9 3 3 3 0 0 0 3 9 3 3 9
3 3 3 3 9 3 3 0 0 0 3 3 3 3 3
3 3 9 3 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 0 3 3 3 3 3 9 3 0 0
0 3 9 3 9 0 3 9 3 3 3 3 3 0 0
0 3 3 3 9 0 3 3 3 9 3 3 3 0 0
0 9 3 9 3 0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 9 3 3 3 3 0 0 0 3 3 9 3 9
3 3 3 3 3 9 3 0 0 0 3 3 3 3 3
3 9 3 9 3 3 3 0 0 0 3 9 3 3 9
3 3 3 3 9 3 3 0 0 0 3 3 3 3 3
3 3 9 3 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 9 3 9 0 0 0 0 0 0 0 0 0 0
0 3 3 3 9 0 0 0 0 0 0 0 0 0 0
0 9 3 9 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 9 3 3 3 3 0 0 0 0 0 0 0 0
3 3 3 3 3 9 3 0 0 0 0 0 0 0 0
3 9 3 9 3 3 3 0 0 0 0 0 0 0 0
3 3 3 3 9 3 3 0 0 0 0 0 0 0 0
3 3 9 3 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 0 3 3 3 3 3 9 3 0 0
0 3 9 3 9 0 3 9 3 3 3 3 3 0 0
0 3 3 3 9 0 3 3 3 9 3 3 3 0 0
0 9 3 9 3 0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 55
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 48.888888888888886
