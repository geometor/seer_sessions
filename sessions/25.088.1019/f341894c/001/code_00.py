import numpy as np

def find_adjacent_pairs(grid, color1, color2):
    """
    Finds all unique pairs of adjacent cells with specified colors.
    Checks right and down neighbors only to avoid duplicates.
    Returns a list of pairs of coordinates: [((r1, c1), (r2, c2)), ...].
    """
    pairs = []
    height, width = grid.shape
    processed = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if processed[r, c]:
                continue

            current_color = grid[r, c]

            # Check right neighbor
            if c + 1 < width:
                right_neighbor_color = grid[r, c + 1]
                if not processed[r, c + 1]:
                    if (current_color == color1 and right_neighbor_color == color2) or \
                       (current_color == color2 and right_neighbor_color == color1):
                        pairs.append(((r, c), (r, c + 1)))
                        processed[r, c] = True
                        processed[r, c + 1] = True
                        continue # Move to next cell once paired

            # Check down neighbor (only if not already paired horizontally)
            if r + 1 < height:
                down_neighbor_color = grid[r + 1, c]
                if not processed[r + 1, c]:
                     if (current_color == color1 and down_neighbor_color == color2) or \
                        (current_color == color2 and down_neighbor_color == color1):
                        pairs.append(((r, c), (r + 1, c)))
                        processed[r, c] = True
                        processed[r + 1, c] = True
                        continue # Move to next cell once paired
            
            # Mark as processed even if no pair found starting here
            # This isn't strictly necessary with the continue statements, 
            # but doesn't hurt. The key is marking pairs as processed.
            # processed[r, c] = True 

    return pairs

def transform(input_grid):
    """
    Transforms the input grid by swapping the positions of adjacent blue (1) and magenta (6) pixels.
    All other pixels remain unchanged.
    The adjacency considered is horizontal (left-right) and vertical (up-down).
    Each pair of adjacent blue and magenta pixels swaps exactly once.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to modify
    output_grid = input_array.copy()
    
    # Define the colors to swap
    color1 = 1 # blue
    color2 = 6 # magenta
    
    # Find all adjacent pairs of color1 and color2
    # Using a helper function that prevents double counting/processing
    # Note: The original find_adjacent_pairs had a slight logic flaw.
    # A simpler approach is to iterate and swap directly in the output grid,
    # using a processed marker to avoid double swaps. Let's use that instead.

    height, width = input_array.shape
    processed = np.zeros_like(input_array, dtype=bool)

    for r in range(height):
        for c in range(width):
            # Skip if this cell was already part of a swap
            if processed[r, c]:
                continue

            current_color = input_array[r, c]

            # Check only if the current cell is one of the colors of interest
            if current_color == color1 or current_color == color2:
                # Check right neighbor
                if c + 1 < width and not processed[r, c + 1]:
                    right_neighbor_color = input_array[r, c + 1]
                    if (current_color == color1 and right_neighbor_color == color2) or \
                       (current_color == color2 and right_neighbor_color == color1):
                        # Perform swap in the output grid
                        output_grid[r, c] = right_neighbor_color
                        output_grid[r, c + 1] = current_color
                        # Mark both cells as processed
                        processed[r, c] = True
                        processed[r, c + 1] = True
                        # Move to the next cell in the main loop
                        continue 

                # Check down neighbor (only if not already swapped horizontally)
                if r + 1 < height and not processed[r + 1, c]:
                    down_neighbor_color = input_array[r + 1, c]
                    if (current_color == color1 and down_neighbor_color == color2) or \
                       (current_color == color2 and down_neighbor_color == color1):
                         # Perform swap in the output grid
                        output_grid[r, c] = down_neighbor_color
                        output_grid[r + 1, c] = current_color
                        # Mark both cells as processed
                        processed[r, c] = True
                        processed[r + 1, c] = True
                        # Move to the next cell in the main loop
                        continue
            
            # No swap initiated from this cell, mark as processed (optional but clarifies)
            # processed[r, c] = True # This line is not strictly needed due to the continue statements

    # Return the modified grid as a list of lists
    return output_grid.tolist()