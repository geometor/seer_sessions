```python
import numpy as np
import copy

# Color mapping for reference (not used directly in code)
# COLOR_MAP = {
#     0: 'white', 1: 'blue', 2: 'red', 3: 'green',
#     4: 'yellow', 5: 'gray', 6: 'magenta', 7: 'orange',
#     8: 'azure', 9: 'maroon'
# }
BLUE = 1
MAGENTA = 6
ORANGE = 7
AZURE = 8

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    coords = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color:
                coords.append((r, c))
    return coords

def transform(input_grid):
    """
    Transforms the input grid based on the relative positions of blue (1)
    and magenta (6) pixels.

    For each blue pixel, find a unique corresponding magenta pixel located
    in the same row or column. Calculate the vector from the blue pixel
    to the magenta pixel (dr, dc). Rotate this vector -90 degrees to get
    (-dc, dr). Place an orange (7) pixel at the location determined by
    adding this rotated vector to the blue pixel's coordinates, if the
    location is within the grid bounds. The original magenta pixel is
    replaced with the background color azure (8). Blue pixels remain
    unchanged.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # Find coordinates of all blue and magenta pixels
    blue_coords = find_pixels(input_np, BLUE)
    magenta_coords = find_pixels(input_np, MAGENTA)

    # Keep track of magenta pixels that have been paired and processed
    processed_magenta = set()

    # Iterate through each blue pixel to find its corresponding magenta partner
    for r_b, c_b in blue_coords:
        found_match = None
        # Search for a magenta pixel in the same row or column
        for r_m, c_m in magenta_coords:
            # Skip if this magenta pixel has already been processed
            if (r_m, c_m) in processed_magenta:
                continue

            # Check for row or column alignment
            if r_m == r_b or c_m == c_b:
                # Assuming a unique match exists for each blue pixel based on examples
                found_match = (r_m, c_m)
                break # Found the partner for this blue pixel

        # If a unique, unprocessed partner was found
        if found_match:
            r_m, c_m = found_match
            # Mark this magenta pixel as processed
            processed_magenta.add(found_match)

            # Calculate the delta vector from blue to magenta
            dr = r_m - r_b
            dc = c_m - c_b

            # Calculate the target coordinates for the orange pixel (-90 degree rotation)
            # New vector is (-dc, dr) relative to blue
            r_o = r_b - dc
            c_o = c_b + dr

            # Remove the original magenta pixel by setting it to azure
            output_grid[r_m, c_m] = AZURE

            # Place the orange pixel if the target coordinates are within grid bounds
            if 0 <= r_o < height and 0 <= c_o < width:
                output_grid[r_o, c_o] = ORANGE

    # Return the modified grid as a list of lists (standard ARC format)
    return output_grid.tolist()
```