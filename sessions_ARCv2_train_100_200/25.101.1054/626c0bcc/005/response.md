```python
import numpy as np

"""
Transforms an input grid containing white (0) and azure (8) pixels into an 
output grid of the same dimensions. White pixels remain unchanged. Azure pixels 
are recolored to blue (1), red (2), green (3), or yellow (4).

The transformation rule depends on the context of each azure pixel:
1.  If an azure pixel has 7 or 8 azure neighbors (8-way adjacency), it becomes 
    blue (1).
2.  If an azure pixel has fewer than 7 azure neighbors, its color depends on 
    a complex rule involving its local 2x2 pattern (top-left, top-right, 
    bottom-left, bottom-right, with out-of-bounds treated as white/0) and 
    potentially other context (like connected component shape or larger 
    neighborhood). 
3.  Analysis shows that the 2x2 pattern alone, the neighbor count alone, or 
    their simple combination is insufficient to uniquely determine the output 
    color for cases with < 7 neighbors, as conflicts arise in the training data.

This implementation includes the known rule for 7/8 neighbors. For other cases, 
it uses a placeholder mapping based on the first observed output for each 
2x2 pattern, acknowledging that this part of the logic is incomplete and will 
not produce the correct output for all ambiguous cases.
"""

def count_neighbors(grid: np.ndarray, r: int, c: int, target_color: int) -> int:
    """
    Counts the number of neighbors (8-way adjacency) of a specific color 
    around a given cell (r, c). Uses the padded grid.
    """
    count = 0
    # Iterate over the 3x3 neighborhood centered at (r+1, c+1) in the padded grid
    # (which corresponds to (r, c) in the original grid)
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            # Skip the center cell itself
            if i == r + 1 and j == c + 1:
                continue
            # Check if the neighbor has the target color
            if grid[i, j] == target_color:
                count += 1
    return count

def get_2x2_pattern(grid: np.ndarray, r: int, c: int) -> tuple:
    """
    Extracts the 2x2 pattern starting at grid position (r+1, c+1) 
    (corresponding to original grid position (r, c)). Uses the padded grid.
    Returns a flattened tuple: (top-left, top-right, bottom-left, bottom-right).
    """
    # Coordinates are relative to the padded grid
    top_left = grid[r + 1, c + 1]
    top_right = grid[r + 1, c + 2]
    bottom_left = grid[r + 2, c + 1]
    bottom_right = grid[r + 2, c + 2]
    return (top_left, top_right, bottom_left, bottom_right)

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the contextual recoloring transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Pad the input array with 0s (white) by 1 cell on all sides
    # This simplifies neighbor counting and pattern extraction at boundaries
    padded_input = np.pad(input_array, ((1, 1), (1, 1)), mode='constant', constant_values=0)

    # Initialize the output grid with the same dimensions as the input, filled with 0s (white)
    output_array = np.zeros_like(input_array)

    # Define the placeholder mapping for ambiguous cases (< 7 neighbors)
    # This mapping is based on the first observed output for each pattern and is KNOWN TO BE INCORRECT.
    placeholder_pattern_map = {
        (8, 0, 0, 0): 1,  # First seen Ex1 (2,5) -> 1 
                           # Conflicts later map this pattern to 3
        (8, 8, 0, 0): 1,  # First seen Ex1 (3,4) -> 1 
                           # Conflicts later map this pattern to 2, 3
        (8, 0, 8, 0): 2,  # First seen Ex1 (0,1) -> 2
                           # Conflicts later map this pattern to 1, 3, 4
        (8, 0, 0, 8): 1,  # Seems consistent in limited examples? Ex2(4,3)->1. Let's assume 1 for now. Needs recheck.
        (8, 8, 8, 0): 3,  # First seen Ex2 (1,2) -> 3 
                           # Conflicts later map this pattern to 1, 4
        (8, 8, 0, 8): 2,  # First seen Ex1 (1,0) -> 2 
                           # Conflicts later map this pattern to 1, 3, 4
        (8, 0, 8, 8): 4,  # First seen Ex1 (0,4) -> 4 
                           # Conflicts later map this pattern to 1, 2, 3
        (8, 8, 8, 8): 4,  # First seen Ex1 (1,4) -> 4 
                           # Conflicts later map this pattern to 1, 3
    }

    # Iterate through each pixel of the original input grid dimensions
    for r in range(height):
        for c in range(width):
            input_color = input_array[r, c]

            # Handle white background pixels
            if input_color == 0:
                output_array[r, c] = 0
                continue

            # Handle azure pixels
            if input_color == 8:
                # Count 8-way azure neighbors using the padded grid
                # Pass r, c which are indices for the *original* grid.
                # Helper function uses padded grid coordinates (r+1, c+1) internally.
                num_neighbors = count_neighbors(padded_input, r, c, 8)

                # Apply the known rule for 7 or 8 neighbors
                if num_neighbors >= 7:
                    output_array[r, c] = 1 # Blue
                else:
                    # Apply the ambiguous rule for < 7 neighbors
                    # Get the 2x2 pattern using the padded grid
                    pattern = get_2x2_pattern(padded_input, r, c)
                    
                    # Use the placeholder map (known to be incomplete/incorrect)
                    output_color = placeholder_pattern_map.get(pattern, 0) # Default to 0 if somehow pattern not found
                    output_array[r, c] = output_color
            else:
                # Keep any other potential input colors (though only 0 and 8 are expected)
                output_array[r,c] = input_color


    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```