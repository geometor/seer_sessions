import numpy as np

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify all yellow (4) and gray (5) pixels.
    2. For each yellow pixel Y:
        a. Find the gray pixel(s) G with the minimum Manhattan distance to Y.
        b. Among these closest gray pixels, calculate a potential square size S' = 2 * max(|Y_row - G_row|, |Y_col - G_col|) - 1 for each.
        c. Determine the final square side length S as the minimum of these calculated S'.
        d. Draw a square of side length S centered at Y.
        e. Fill the area of this square with red (2) pixels, but only overwrite white (0) background pixels. Existing non-white pixels remain unchanged.
    3. Return the modified grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find coordinates of yellow (4) and gray (5) pixels
    yellow_pixels = find_pixels(input_grid, 4)
    gray_pixels = find_pixels(input_grid, 5)

    # If there are no yellow or no gray pixels, return the original grid
    if not yellow_pixels or not gray_pixels:
        return output_grid

    # Process each yellow pixel
    for yr, yc in yellow_pixels:
        min_dist = float('inf')
        closest_grays = []

        # Calculate distances to all gray pixels and find the minimum distance
        for gr, gc in gray_pixels:
            dist = manhattan_distance((yr, yc), (gr, gc))
            if dist < min_dist:
                min_dist = dist
                closest_grays = [(gr, gc)]
            elif dist == min_dist:
                closest_grays.append((gr, gc))

        # Determine the square size based on the closest gray(s)
        min_calculated_size = float('inf')
        if not closest_grays: # Should not happen if gray_pixels is not empty, but safety check
             continue

        for gr, gc in closest_grays:
            delta_r = abs(yr - gr)
            delta_c = abs(yc - gc)
            potential_size = 2 * max(delta_r, delta_c) - 1
            if potential_size < min_calculated_size:
                min_calculated_size = potential_size

        # Ensure size is at least 1
        side_length = max(1, min_calculated_size)

        # Calculate the drawing radius (half side length, integer floor)
        radius = (side_length - 1) // 2

        # Determine the bounds of the square
        start_row = yr - radius
        end_row = yr + radius
        start_col = yc - radius
        end_col = yc + radius

        # Draw the square, changing only white pixels to red
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                # Check if the coordinates are within the grid bounds
                if 0 <= r < height and 0 <= c < width:
                    # If the pixel is background (white), change it to red
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 2

    return output_grid