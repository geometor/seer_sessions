"""
1.  **Identify the Outer Object:** Find the bounding box of the largest contiguous red (2) region. This defines the outer boundary.
2.  **Check for Inner Object:** Within the bounding box of the red region, check if there is a contiguous region of any color other than red.
3.  **Handle Inner Object (if present):** If an inner object of a different color exists, replace all pixels of that inner object with black (0). Maintain the original shape and position of the inner object.
4. **Handle No Inner Object:** If no such inner object is found, create a new rectangular black (0) object inside the red region.  The height and width of this new black object should be approximately 1/3 the height and width of the red object, respectively. Center the new black object within the red object.
5.  **Output:** Return the modified grid.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle case where color is not found

    # Calculate bounding box.
    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)
    return (min_y, min_x), (max_y, max_x)

def find_inner_object(grid, outer_color):
    # Find the bounding box of the outer object
    outer_top_left, outer_bottom_right = find_object(grid, outer_color)
    if outer_top_left is None:
        return None

    # Create a mask for the outer object
    mask = np.zeros_like(grid, dtype=bool)
    mask[outer_top_left[0]:outer_bottom_right[0]+1, outer_top_left[1]:outer_bottom_right[1]+1] = True

    # Find all colors within the outer object's bounding box
    inner_colors = np.unique(grid[mask])

    # Exclude the outer color and find any remaining color
    inner_colors = inner_colors[inner_colors != outer_color]
    
    if inner_colors.size > 0:
        inner_color = inner_colors[0]  # Pick the first different color
        return find_object(grid, inner_color)
    else:
        return None



def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the red region (outer object).
    red_top_left, red_bottom_right = find_object(input_grid, 2)

    if red_top_left is None:
      return output_grid

    # Check for inner object.
    inner_object_coords = find_inner_object(output_grid, 2)

    if inner_object_coords is not None:
        inner_top_left, inner_bottom_right = inner_object_coords
        # Replace inner object with black.
        for y in range(inner_top_left[0], inner_bottom_right[0] + 1):
            for x in range(inner_top_left[1], inner_bottom_right[1] + 1):
                output_grid[y, x] = 0
    else:
        # Create black region in the center.
        red_height = red_bottom_right[0] - red_top_left[0] + 1
        red_width = red_bottom_right[1] - red_top_left[1] + 1

        black_height = int(red_height / 3)
        black_width = int(red_width / 3)


        black_top = red_top_left[0] + (red_height - black_height) // 2
        black_left = red_top_left[1] + (red_width - black_width) // 2
        black_bottom = black_top + black_height
        black_right = black_left + black_width

        for y in range(max(0,black_top), min(output_grid.shape[0],black_bottom)):
            for x in range(max(0,black_left), min(output_grid.shape[1], black_right)):
                output_grid[y, x] = 0

    return output_grid