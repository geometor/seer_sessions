import numpy as np

"""
Identifies the two azure (8) pixels in the input grid.
Calculates the shortest Manhattan distance (D) between these two points.
Finds all pixels (r, c) such that the sum of their Manhattan distances 
to the two azure pixels equals D. These pixels represent all points 
lying on any shortest Manhattan path between the two azure points.
Changes the color of these path pixels to green (3), excluding the 
original azure pixels themselves. Returns the modified grid.
"""

# Helper function to find coordinates of pixels with a specific color
def find_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with the given color."""
    # Use np.where to find indices where the grid equals the target color
    rows, cols = np.where(grid == color)
    # Combine row and column indices into a list of (row, col) tuples
    return list(zip(rows, cols))

# Helper function to calculate Manhattan distance
def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points p1=(r1, c1) and p2=(r2, c2)."""
    r1, c1 = p1
    r2, c2 = p2
    # Manhattan distance formula: |r1 - r2| + |c1 - c2|
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid):
    """
    Transforms the input grid by drawing the shortest Manhattan path(s) 
    between two azure pixels in green.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input array to modify, preserving the original
    output_np = np.copy(input_np)
    
    # Define color constants for clarity
    AZURE = 8
    GREEN = 3
    
    # Find the coordinates of the two azure pixels
    azure_pixels = find_pixels(input_np, AZURE)
    
    # Basic validation: Ensure exactly two azure pixels are found as per task examples
    if len(azure_pixels) != 2:
        # If the input doesn't match the expected structure (2 azure pixels), 
        # return the original grid unchanged. This handles unexpected inputs gracefully.
        return input_grid 

    # Assign the found coordinates to p1 and p2
    p1 = azure_pixels[0]
    p2 = azure_pixels[1]
    
    # Calculate the minimum possible Manhattan distance between p1 and p2
    # This is the length of the shortest path using only horizontal/vertical steps.
    min_dist = manhattan_distance(p1, p2)
    
    # Get the dimensions (height, width) of the grid
    height, width = input_np.shape
    
    # Iterate through each cell (pixel) in the grid using its row (r) and column (c) indices
    for r in range(height):
        for c in range(width):
            # Current pixel's coordinates
            current_pos = (r, c)
            
            # Skip processing if the current pixel is one of the original azure pixels (start/end points)
            if current_pos == p1 or current_pos == p2:
                continue
                
            # Calculate the Manhattan distance from the current pixel to the first azure pixel (p1)
            dist_to_p1 = manhattan_distance(current_pos, p1)
            # Calculate the Manhattan distance from the current pixel to the second azure pixel (p2)
            dist_to_p2 = manhattan_distance(current_pos, p2)
            
            # The core logic: A pixel lies on a shortest Manhattan path between p1 and p2 
            # if and only if the sum of its distances to p1 and p2 equals the shortest distance (min_dist).
            if dist_to_p1 + dist_to_p2 == min_dist:
                # Change the color of this pixel to green in the output grid
                output_np[r, c] = GREEN
                
    # Convert the modified NumPy array back to a standard list of lists format for the final output
    output_grid = output_np.tolist()
    
    return output_grid