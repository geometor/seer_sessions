import numpy as np
from collections import Counter

def find_most_frequent_color(grid_array):
    """
    Counts the frequency of each color in the grid and returns the most frequent one.
    Handles ties by returning the first one encountered by Counter.most_common().
    
    Args:
        grid_array (np.ndarray): The input grid as a numpy array.

    Returns:
        int: The color value that appears most frequently in the grid.
    """
    # Flatten the 2D grid array into a 1D array to count all pixels
    pixels = grid_array.flatten()
    
    # Count occurrences of each color using collections.Counter
    counts = Counter(pixels)
    
    # Check if counts is empty (e.g., empty grid), though ARC constraints likely prevent this
    if not counts:
        # Define default behavior for empty grid, e.g., return background color 0
        # Based on ARC, grids are 1x1 to 30x30, so this shouldn't happen.
        # If it did, maybe returning 0 (white) or raising an error is appropriate.
        # Let's assume valid grids based on ARC specs.
        return 0 

    # .most_common(1) returns a list containing a single tuple: [(most_frequent_item, count)]
    most_frequent_color, _ = counts.most_common(1)[0]
    
    return most_frequent_color

def transform(input_grid):
    """
    Transforms the input grid by replacing all instances of the magenta color (6) 
    with the single most frequent color found in the input grid. All other pixels 
    remain unchanged.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    
    # Convert the input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # --- Determine the replacement color ---
    # Find the color that appears most frequently in the input grid
    replacement_color = find_most_frequent_color(input_array)
    
    # Define the color that needs to be replaced
    color_to_replace = 6 # magenta
    
    # --- Create and modify the output grid ---
    # Initialize the output grid as a copy of the input grid.
    # This ensures pixels not matching 'color_to_replace' keep their original value.
    output_array = np.copy(input_array)
    
    # Find all coordinates (pixels) in the input grid where the color is 'color_to_replace' (magenta)
    replace_mask = (input_array == color_to_replace)
    
    # In the output grid, update the pixels identified by the mask to the 'replacement_color'
    output_array[replace_mask] = replacement_color
    
    # Convert the resulting numpy array back to a list of lists format
    return output_array.tolist()
