```python
import numpy as np
from collections import Counter

def find_bounding_box(grid, target_color):
    """
    Finds the minimum bounding box coordinates for a target color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color to find the bounding box for.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if target_color not found.
    """
    rows, cols = np.where(grid == target_color)
    if rows.size == 0:
        return None  # Target color not found
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the minimal bounding box containing all pixels of the non-background color.

    1. Identify the two colors present in the input grid.
    2. Determine the background color (most frequent) and object color (less frequent).
    3. Find the locations (row, column) of all pixels with the object color.
    4. Calculate the minimum and maximum row and column indices (bounding box) for the object pixels.
    5. Extract the subgrid defined by the bounding box from the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    
    # Find unique colors and their counts
    unique_colors, counts = np.unique(grid, return_counts=True)

    if len(unique_colors) == 1:
        # If only one color exists, maybe return the whole grid or an empty one?
        # Based on examples, there are always at least two. Let's assume this.
        # If the single color is the 'object' color somehow, the bounding box is the whole grid.
        # If it's background, maybe return empty? Let's return the original grid for now.
        # Or perhaps, treat the single color as the 'object' and return the full grid.
         return input_grid # Or potentially an empty grid or handle as an error

    if len(unique_colors) > 2:
         # Find the most frequent color (background)
        background_color = unique_colors[np.argmax(counts)]
        # Find the object color(s) - assume the single least frequent? Or all non-background?
        # The prompt implies a single object color. Let's find the least frequent.
        object_color = unique_colors[np.argmin(counts)]
        # This might fail if there are multiple non-background colors with the same count.
        # Let's refine: Find the *second* most frequent, or simply the one that isn't the background.
        counts_dict = {color: count for color, count in zip(unique_colors, counts)}
        background_color = max(counts_dict, key=counts_dict.get)
        # Assume any color that is not the background is the object color.
        # If there are multiple, the problem description is slightly ambiguous.
        # The examples only show one non-background color.
        object_colors = [c for c in unique_colors if c != background_color]
        if len(object_colors) != 1:
             # If more than one non-background color, we need a clearer rule.
             # For now, let's pick the first one found. Or perhaps the least frequent non-bg?
             # Let's stick to the assumption of one object color based on examples.
             # Re-evaluating: Maybe the background is *always* the most frequent,
             # and *all* other colors contribute to the bounding box calculation?
             # Let's try that.
            rows, cols = np.where(grid != background_color)
            if rows.size == 0:
                 return [] # No object pixels found
            min_row = np.min(rows)
            max_row = np.max(rows)
            min_col = np.min(cols)
            max_col = np.max(cols)

        else:
             object_color = object_colors[0]
             # Find bounding box for the single object color
             bbox = find_bounding_box(grid, object_color)
             if bbox is None:
                 return [] # Should not happen if object_color exists
             min_row, max_row, min_col, max_col = bbox

    elif len(unique_colors) == 2:
        # Identify background (most frequent) and object (least frequent) colors
        if counts[0] > counts[1]:
            background_color = unique_colors[0]
            object_color = unique_colors[1]
        else:
            background_color = unique_colors[1]
            object_color = unique_colors[0]
            
        # Find the bounding box coordinates for the object color
        bbox = find_bounding_box(grid, object_color)
        if bbox is None:
            # This case implies the grid only had background color, handled above.
             return []
        min_row, max_row, min_col, max_col = bbox

    # Extract the subgrid using the bounding box coordinates
    # Slicing is inclusive of the start index and exclusive of the end index, so add 1 to max values
    output_grid_np = grid[min_row:max_row + 1, min_col:max_col + 1]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```