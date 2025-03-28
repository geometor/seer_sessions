import numpy as np

# Helper function to find pixel coordinates of a specific color
def find_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with the specified color."""
    # Use np.argwhere to find indices where grid equals color
    coords = np.argwhere(grid == color)
    # Convert the [row, col] pairs into a list of (row, col) tuples
    return [tuple(coord) for coord in coords]

def transform(input_grid):
    """
    Identifies rectangles defined by four yellow (4) corner pixels in the input grid
    and fills the interior area of these rectangles with red (2) pixels.
    """
    # Initialize output_grid as a copy of the input_grid (assuming input_grid is a numpy array)
    output_grid = np.copy(input_grid)

    # Find all yellow (4) pixels in the original input grid
    yellow_pixels = find_pixels(input_grid, 4)

    # Convert the list of yellow pixel coordinates into a set for efficient O(1) average time lookups
    yellow_pixel_set = set(yellow_pixels)

    # Store identified rectangle boundaries (min_r, max_r, min_c, max_c) to avoid redundant filling
    processed_rectangles = set()

    # Iterate through all found yellow pixels, considering each as a potential top-left corner (r1, c1)
    for r1, c1 in yellow_pixels:
        # Iterate through all yellow pixels again, considering each as a potential bottom-right corner (r2, c2)
        for r2, c2 in yellow_pixels:
            # To form a valid rectangle, the bottom-right corner must be strictly below and to the right of the top-left corner
            if r2 > r1 and c2 > c1:
                # Define the coordinates of the other two potential corners: top-right and bottom-left
                corner_tr = (r1, c2)
                corner_bl = (r2, c1)

                # Check if these other two corners actually exist as yellow pixels in the input grid
                if corner_tr in yellow_pixel_set and corner_bl in yellow_pixel_set:
                    # If all four corners (r1, c1), (r1, c2), (r2, c1), (r2, c2) exist, we've found a rectangle.
                    # Define the bounds of this rectangle
                    rectangle_bounds = (r1, r2, c1, c2) # (min_row, max_row, min_col, max_col)

                    # Check if we have already identified and processed this specific rectangle
                    # This prevents filling the same area multiple times if found via different corner pairs
                    if rectangle_bounds not in processed_rectangles:
                        # Add the bounds to the set to mark this rectangle as processed
                        processed_rectangles.add(rectangle_bounds)

                        # Fill the interior area of this rectangle in the output grid with red (2)
                        # Iterate through rows strictly between the top and bottom rows (from r1+1 up to, but not including, r2)
                        for r in range(r1 + 1, r2):
                            # Iterate through columns strictly between the left and right columns (from c1+1 up to, but not including, c2)
                            for c in range(c1 + 1, c2):
                                output_grid[r, c] = 2 # Set the pixel color to red

    # Return the modified grid as a numpy array
    return output_grid