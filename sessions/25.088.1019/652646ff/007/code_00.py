import numpy as np
from collections import Counter
from skimage.measure import label, regionprops

"""
Transforms an input grid based on the following rules:

1.  **Identify Background:** Determine the `background_color` as the most frequent color in the input grid.
2.  **Identify Relevant Pixels:** Create a mask identifying 'relevant' pixels. A pixel is relevant if its color is NOT the background color, NOT Gray (5), NOT Orange (7), and NOT Maroon (9). Additionally, if the background color is Azure (8), then Red (2) pixels are also NOT relevant.
3.  **Find Conceptual Shapes:** Find connected components (using 4-connectivity, meaning only horizontal and vertical neighbors are considered connected) within the `relevant_mask`. These components represent the conceptual shapes.
4.  **Characterize Shapes:** For each connected component (shape):
    *   Determine its bounding box (`min_row`, `min_col`, `max_row`, `max_col`).
    *   Calculate its height `h = max_row - min_row + 1`.
    *   Find the coordinates of the top-most, left-most pixel belonging to this component within the original input grid.
    *   Determine the `representative_color` which is the original color of this top-left pixel in the input grid.
    *   Store the shape's `height`, `representative_color`, and `top_left` coordinate (`min_row`, `min_col`).
5.  **Sort Shapes:** Sort the characterized shapes primarily by their `min_row` (top coordinate) and secondarily by their `min_col` (left coordinate).
6.  **Conditional Reverse:** If the `background_color` is Yellow (4), reverse the order of the sorted shapes.
7.  **Determine Output Dimensions:**
    *   Calculate `max_shape_height` which is the maximum height (`h`) among all identified shapes. If no shapes are found, default to 0.
    *   The `output_width` will be equal to `max_shape_height`.
    *   The `output_height` will be the sum of the heights (`h`) of all identified shapes.
    *   If either dimension is 0 (e.g., no shapes found), return an empty grid.
8.  **Construct Output Grid:**
    *   Create a new grid initialized with the `background_color`, with dimensions `output_height` x `output_width`.
    *   Initialize `current_row = 0`.
    *   Iterate through the sorted (and potentially reversed) shapes. For each shape with height `h` and `representative_color`:
        *   Calculate the starting column for horizontal centering: `start_col = (output_width - h) // 2`.
        *   Draw a solid square block of size `h` x `h` using the `representative_color` in the output grid. The top-left corner of this square will be at `(current_row, start_col)`.
        *   Update `current_row` by adding `h` to position the next shape below the current one.
9.  **Return:** The constructed output grid as a list of lists.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    if grid.size == 0:
        return 0 # Default to white
    counts = Counter(grid.flatten())
    if not counts:
        return 0
    background_color = counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    input_np = np.array(input_grid, dtype=int)
    if input_np.size == 0:
        return [[]]

    # 1. Identify Background
    background_color = find_background_color(input_np)

    # 2. Identify Relevant Pixels
    rows, cols = input_np.shape
    relevant_mask = np.ones_like(input_np, dtype=bool)
    always_ignored_colors = {5, 7, 9} # Gray, Orange, Maroon

    relevant_mask[input_np == background_color] = False
    for color in always_ignored_colors:
        relevant_mask[input_np == color] = False
    if background_color == 8: # If background is Azure
        relevant_mask[input_np == 2] = False # Ignore Red

    # 3. Find Conceptual Shapes using skimage.measure.label
    # connectivity=1 means 4-connectivity (rook's moves)
    labeled_grid, num_labels = label(relevant_mask, connectivity=1, background=0, return_num=True)

    shapes = []
    # 4. Characterize Shapes
    # Skip label 0 as it represents the background/non-relevant areas
    for i in range(1, num_labels + 1):
        coords = np.argwhere(labeled_grid == i)
        if coords.size == 0:
            continue

        min_row = np.min(coords[:, 0])
        min_col = np.min(coords[:, 1])
        max_row = np.max(coords[:, 0])
        max_col = np.max(coords[:, 1])

        height = max_row - min_row + 1
        #width = max_col - min_col + 1 # Width not directly used for output square size

        # Find the top-most, left-most pixel *of this component*
        top_left_component_pixel_coord = min(coords, key=lambda x: (x[0], x[1]))
        representative_color = input_np[top_left_component_pixel_coord[0], top_left_component_pixel_coord[1]]

        shapes.append({
            'min_row': min_row,
            'min_col': min_col, # Keep min_col for sorting
            'height': height,
            'representative_color': representative_color
        })

    # Handle case with no relevant shapes found
    if not shapes:
        return [[]] # Return empty grid as per rule 7

    # 5. Sort Shapes
    # Sort by min_row (top coordinate), then min_col (left coordinate)
    sorted_shapes = sorted(shapes, key=lambda s: (s['min_row'], s['min_col']))

    # 6. Conditional Reverse
    if background_color == 4: # Yellow background
        sorted_shapes.reverse()

    # 7. Determine Output Dimensions
    if not sorted_shapes: # Double check after potential filtering/sorting issues
         return [[]]

    max_shape_height = max(s['height'] for s in sorted_shapes) if sorted_shapes else 0
    output_width = max_shape_height
    output_height = sum(s['height'] for s in sorted_shapes)

    # Additional check for zero dimensions
    if output_height <= 0 or output_width <= 0:
        return [[]]

    # 8. Construct Output Grid
    output_grid = np.full((output_height, output_width), background_color, dtype=int)
    current_row = 0

    for shape in sorted_shapes:
        h = shape['height']
        rep_color = shape['representative_color']

        # Calculate start column for horizontal centering of the h x h square
        start_col = (output_width - h) // 2

        # Define the slice for the h x h square
        row_slice = slice(current_row, current_row + h)
        col_slice = slice(start_col, start_col + h)

        # Draw the solid square block
        output_grid[row_slice, col_slice] = rep_color

        # Update the starting row for the next shape
        current_row += h

    # 9. Return as list of lists
    return output_grid.tolist()