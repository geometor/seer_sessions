```python
import numpy as np

def transform(input_grid):
    """
    Identifies each 2x2 gray (5) square in the input grid and adds four colored
    pixels (blue=1, red=2, green=3, yellow=4) at specific diagonal positions
    relative to the corners of each square.

    1. Initialize the output grid as a copy of the input grid.
    2. Iterate through each possible top-left corner position (r, c) in the input grid.
    3. Check if the 2x2 block starting at (r, c) consists entirely of gray (5) pixels.
    4. If a 2x2 gray square is found:
        a. Place blue (1) at (r-1, c-1) if within grid bounds.
        b. Place red (2) at (r-1, c+2) if within grid bounds.
        c. Place green (3) at (r+2, c-1) if within grid bounds.
        d. Place yellow (4) at (r+2, c+2) if within grid bounds.
    5. Return the modified output grid.
    """

    # Convert input list of lists to a numpy array for easier slicing and modification
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get the dimensions of the grid
    height, width = input_np.shape

    # Helper function to check if coordinates are within grid boundaries
    def is_within_bounds(r, c):
        return 0 <= r < height and 0 <= c < width

    # Iterate through each cell checking if it's the top-left corner of a 2x2 gray square
    # We only need to iterate up to height-2 and width-2 to avoid index errors when checking the 2x2 square
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 area starting at (r, c) is all gray (5)
            if (input_np[r, c] == 5 and
                input_np[r+1, c] == 5 and
                input_np[r, c+1] == 5 and
                input_np[r+1, c+1] == 5):

                # Define the relative positions and colors for the new pixels
                new_pixels = [
                    ((r - 1, c - 1), 1),  # Top-left diagonal, Blue
                    ((r - 1, c + 2), 2),  # Top-right diagonal, Red
                    ((r + 2, c - 1), 3),  # Bottom-left diagonal, Green
                    ((r + 2, c + 2), 4)   # Bottom-right diagonal, Yellow
                ]

                # Place each new pixel if its coordinates are within the grid bounds
                for (nr, nc), color in new_pixels:
                    if is_within_bounds(nr, nc):
                        output_grid[nr, nc] = color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
```