import numpy as np

"""
Reflects all azure (8) pixels in the input grid horizontally based on a condition determined by the overall bounding box of these azure pixels.

1. Find all azure pixels. If none, return the input grid.
2. Determine the overall bounding box (min_row, max_row, min_col, max_col) containing all azure pixels.
3. Calculate the center column index within this bounding box: center_col = min_col + floor((max_col - min_col) / 2).
4. Check the color of the pixel at the bottom-center position of the overall bounding box: (max_row, center_col).
5. If this pixel is azure (8), reflect each original azure pixel horizontally across the vertical line immediately to the right of the overall bounding box (axis x = max_col + 0.5). Reflection formula: reflected_c = 2 * max_col + 1 - original_col.
6. If this pixel is not azure (8), reflect each original azure pixel horizontally across the vertical line immediately to the left of the overall bounding box (axis x = min_col - 0.5). Reflection formula: reflected_c = 2 * min_col - 1 - original_col.
7. The reflected row is the same as the original row.
8. Add the reflected azure pixels to a copy of the input grid. The original azure pixels remain.
"""

def find_all_pixels(grid, color):
    """Finds all pixels of a specific color in the grid."""
    coords = np.argwhere(grid == color)
    # Convert to list of tuples [(row, col), ...]
    return [tuple(coord) for coord in coords]

def get_overall_bounding_box(coords):
    """Calculates the overall bounding box for a list of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    # Check if rows or cols lists ended up empty, which shouldn't happen if coords is not empty
    if not rows or not cols: 
         return None
    # Use numpy's min/max for potential int64 types from argwhere
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    
    return int(min_row), int(max_row), int(min_col), int(max_col)

def transform(input_grid):
    """
    Applies the reflection transformation based on the overall bounding box of azure pixels.
    """
    azure_color = 8
    rows, cols = input_grid.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Identify all azure pixels
    all_azure_coords = find_all_pixels(input_grid, azure_color)

    # If no azure pixels are found, return the original grid
    if not all_azure_coords:
        return output_grid

    # 2. Determine the overall bounding box
    overall_bbox = get_overall_bounding_box(all_azure_coords)
    
    # Should not happen if azure pixels exist, but safety check
    if overall_bbox is None:
        return output_grid 
        
    min_row, max_row, min_col, max_col = overall_bbox

    # 3. Calculate the horizontal center column index within the bounding box
    # Using integer division // for floor behavior
    center_col = min_col + (max_col - min_col) // 2

    # 4. Inspect the color of the pixel at the bottom-center of the bounding box
    pixel_to_check_coord = (max_row, center_col)
    pixel_value_at_check = -1 # Default value if out of bounds
    # Ensure the coordinate is valid before accessing the grid
    if 0 <= pixel_to_check_coord[0] < rows and 0 <= pixel_to_check_coord[1] < cols:
        pixel_value_at_check = input_grid[pixel_to_check_coord]

    # 5. & 6. Determine reflection direction based on the check
    reflect_right = (pixel_value_at_check == azure_color)

    # 7. Create the output grid (already done by copying input)

    # 8. Iterate through each original azure pixel
    for r, c in all_azure_coords:
        
        # 9. Calculate the reflected column coordinate
        if reflect_right:
            # Reflect across axis x = max_col + 0.5
            reflected_c = (2 * max_col) + 1 - c
        else:
            # Reflect across axis x = min_col - 0.5
            reflected_c = (2 * min_col) - 1 - c
            
        # 10. The reflected row coordinate is the same as the original row
        reflected_r = r

        # 11. Check if the reflected coordinate is within the grid boundaries
        if 0 <= reflected_r < rows and 0 <= reflected_c < cols:
            # 12. Set the color of the pixel in the output grid to azure
            output_grid[reflected_r, reflected_c] = azure_color

    # 13. Return the modified output grid
    return output_grid