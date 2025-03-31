import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on adjacent pixel interactions.

    For each non-white pixel in the input grid:
    1. Examine its 8 adjacent neighbors (horizontal, vertical, and diagonal).
    2. If any neighbor has a non-white color with a *lower* color index value 
       than the current pixel, the current pixel's corresponding position in 
       the output grid is changed to white (0).
    3. Otherwise (if all non-white neighbors have a higher or equal color index, 
       or if there are no non-white neighbors), the pixel retains its original color 
       in the output grid.
    White background pixels remain unchanged.
    """

    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)  # Initialize output grid as a copy of the input
    rows, cols = input_array.shape

    # Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_array[r, c]

            # Skip background pixels
            if current_color == 0:
                continue

            should_turn_white = False
            # Check all 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the center pixel itself
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_color = input_array[nr, nc]

                        # Check if neighbor is non-white and has a different color
                        if neighbor_color != 0 and neighbor_color != current_color:
                            # Apply the rule: if any neighbor has a lower color index, mark current pixel to turn white
                            if neighbor_color < current_color:
                                should_turn_white = True
                                break  # Found a lower-indexed neighbor, no need to check others
                if should_turn_white:
                    break # Exit outer neighbor loop as well

            # If marked, change the corresponding pixel in the output grid to white
            if should_turn_white:
                output_array[r, c] = 0

    # Convert back to list of lists if necessary, though numpy array is often preferred
    return output_array.tolist()