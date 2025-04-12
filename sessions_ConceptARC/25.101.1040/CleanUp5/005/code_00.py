import numpy as np
from scipy.ndimage import label

"""
Transforms an input grid based on the number and values of distinct non-white colors present.

Transformation Rules:

1.  **Analyze Input Colors**: Identify all distinct non-white (non-zero) colors in the input grid. Count the number of distinct non-white colors, `N`.
2.  **Conditional Transformation**: Apply rules based on the value of `N`:
    *   **If `N` equals 1 (Single Non-White Color `C`):**
        1.  Find all connected components (8-way adjacency) of color `C`.
        2.  Identify pixels to change:
            *   Any pixel belonging to a component containing only 1 pixel (an isolated pixel).
            *   The pixel with the smaller column index (leftmost) in any component consisting of exactly two pixels positioned horizontally adjacent to each other.
        3.  Change the color of all identified pixels to white (0). Other pixels remain unchanged.
    *   **If `N` is greater than 1 (Multiple Non-White Colors):**
        1.  Identify the non-white color with the highest numerical value (`C_max`) and the non-white color with the second-highest numerical value (`C_next`).
        2.  Examine each pixel `p` at location `(r, c)` that has the color `C_max`.
        3.  Determine the final color for pixel `p` based on these conditions:
            *   Check if the pixel's row index `r` is exactly 3.
            *   Check if the pixel `p` is "isolated" with respect to `C_max` (none of its 8 neighbors have color `C_max`).
            *   Check if the pixel `p` is part of a "horizontal pair" with respect to `C_max` (exactly one of its horizontal neighbors, `(r, c-1)` or `(r, c+1)`, has color `C_max`, and no other neighbors have color `C_max`).
            *   **If** the pixel is on row 3 **AND** (it is isolated **OR** it is part of a horizontal pair), then change the color of this pixel to `C_next`.
            *   **Else**, change the color of this pixel to white (0).
        4.  Pixels that *do not* have the color `C_max` retain their original color.
    *   **If `N` equals 0 (No Non-White Colors):**
        1.  The output grid is identical to the input grid.
"""


def _get_neighbor_coords(r, c, height, width):
    """Generates valid 8-way neighbor coordinates."""
    coords = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                coords.append((nr, nc))
    return coords

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    # Create a copy to modify for the output
    output_array = np.copy(input_array)

    # Find unique non-zero colors in the grid
    non_zero_colors = sorted(np.unique(input_array[input_array != 0]), reverse=True) # Sort descending
    num_distinct_colors = len(non_zero_colors)

    # --- Apply transformation based on the number of distinct non-white colors ---

    if num_distinct_colors == 0:
        # Case 0: No non-white colors, return input as is
        pass # Output array is already a copy

    elif num_distinct_colors == 1:
        # Case 1: Exactly one non-white color present
        single_color = non_zero_colors[0]

        # Create a boolean mask where the grid matches the single color
        mask = input_array == single_color

        # Define the connectivity structure for finding components (8-way adjacency)
        structure = np.array([[1, 1, 1],
                              [1, 1, 1],
                              [1, 1, 1]], dtype=bool)

        # Find connected components in the boolean mask
        labeled_array, num_features = label(mask, structure=structure)

        # Keep track of pixel coordinates that need to be removed (set to white)
        pixels_to_remove = set()

        # Iterate through each component found (labels are 1-based)
        for i in range(1, num_features + 1):
            # Get the coordinates (row, column) of all pixels belonging to the current component
            component_coords = np.argwhere(labeled_array == i)
            component_size = len(component_coords)

            if component_size == 1:
                # Rule: Remove components of size 1 (isolated pixels)
                pixel_coord = tuple(component_coords[0])
                pixels_to_remove.add(pixel_coord)

            elif component_size == 2:
                # Rule: For components of size 2, check if they form a horizontal line
                p1 = component_coords[0] # Coordinates of the first pixel
                p2 = component_coords[1] # Coordinates of the second pixel

                # Check if rows are the same and columns differ by exactly 1
                if p1[0] == p2[0] and abs(p1[1] - p2[1]) == 1:
                    # This is a horizontal line of size 2
                    # Find the leftmost pixel (the one with the smaller column index)
                    leftmost_pixel_coord = tuple(p1) if p1[1] < p2[1] else tuple(p2)
                    # Add the leftmost pixel to the removal set
                    pixels_to_remove.add(leftmost_pixel_coord)

        # Apply the removals: Iterate through the collected coordinates and set them to white
        for r, c in pixels_to_remove:
            output_array[r, c] = 0

    elif num_distinct_colors > 1:
        # Case 2: More than one non-white color present
        c_max = non_zero_colors[0]  # Highest color value
        c_next = non_zero_colors[1] # Second highest color value

        # Iterate through each pixel potentially affected (only C_max pixels)
        for r in range(height):
            for c in range(width):
                if input_array[r, c] == c_max:
                    # This pixel has the max color, determine its fate
                    
                    # Check neighbors for C_max
                    cmax_neighbors = 0
                    cmax_horizontal_neighbors = 0
                    neighbor_coords = _get_neighbor_coords(r, c, height, width)

                    for nr, nc in neighbor_coords:
                        if input_array[nr, nc] == c_max:
                            cmax_neighbors += 1
                            # Check if it's a horizontal neighbor
                            if nr == r and abs(nc - c) == 1:
                                cmax_horizontal_neighbors += 1

                    # Determine conditions
                    is_isolated = (cmax_neighbors == 0)
                    # Check if it's a horizontal pair element (exactly one horizontal neighbor, and no others)
                    is_horizontal_pair_element = (cmax_neighbors == 1 and cmax_horizontal_neighbors == 1)

                    # Apply the specific rule for row 3
                    if r == 3 and (is_isolated or is_horizontal_pair_element):
                        output_array[r, c] = c_next # Change to second highest color
                    else:
                        output_array[r, c] = 0 # Change to white

    # Convert the final NumPy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid