```python
import numpy as np

# Define color constants based on the ARC color map
AZURE = 8
YELLOW = 4
WHITE = 0 # Background color

def find_reflection_point(r, c, height, width):
    """
    Calculates the coordinates of a point reflected across the center of the grid.
    The center is considered ((height-1)/2, (width-1)/2).

    Args:
        r (int): Row index of the point.
        c (int): Column index of the point.
        height (int): Height of the grid.
        width (int): Width of the grid.

    Returns:
        tuple (int, int): The reflected row and column indices (r', c').
    """
    # Calculate the reflected row index
    r_reflected = height - 1 - r
    # Calculate the reflected column index
    c_reflected = width - 1 - c
    return r_reflected, c_reflected

def transform(input_grid):
    """
    Transforms the input grid by reflecting azure pixels across the grid's center.
    
    Rule:
    1. Initialize an output grid identical to the input grid.
    2. Iterate through each pixel of the input grid.
    3. If an azure (8) pixel is found at position (r, c):
        a. Calculate its reflection point (r', c') across the grid's center.
        b. Check if the reflection point (r', c') is within the grid boundaries.
        c. Check if the pixel at the reflection point (r', c') in the *original input grid* is white (0).
        d. If both conditions (b and c) are true, change the pixel at (r', c') in the *output grid* to yellow (4).
    4. All other pixels retain their original colors from the input grid. Specifically, 
       original azure pixels remain azure, and original white pixels remain white unless 
       targeted by a reflection from an azure pixel.
    """
    # Convert the input list of lists to a NumPy array for efficient indexing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid. This ensures that
    # all original pixels are preserved unless explicitly overwritten.
    output_grid = np.copy(input_np)
    
    # Get the dimensions (height and width) of the grid
    height, width = input_np.shape
    
    # Define the color constants involved in the transformation
    primary_object_color = AZURE  # The color that triggers the reflection
    added_object_color = YELLOW  # The color placed at the reflected position
    background_color = WHITE     # The color that the reflected position must originally be

    # Iterate through each cell (pixel) of the input grid using its row (r) and column (c) indices
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the *original input grid* is the primary color (azure)
            if input_np[r, c] == primary_object_color:
                # If it is azure, calculate the coordinates reflected across the grid center
                r_reflected, c_reflected = find_reflection_point(r, c, height, width)

                # Check if the calculated reflected coordinates (r', c') fall within the valid bounds of the grid
                if 0 <= r_reflected < height and 0 <= c_reflected < width:
                    # Check if the pixel at the reflected location in the *original input grid* is the background color (white)
                    if input_np[r_reflected, c_reflected] == background_color:
                        # If the reflected point is within bounds AND the original pixel at that point was white,
                        # then update the pixel at the reflected position in the *output grid* to the added color (yellow)
                        output_grid[r_reflected, c_reflected] = added_object_color

    # Convert the final NumPy array back to a list of lists format before returning
    return output_grid.tolist()
```