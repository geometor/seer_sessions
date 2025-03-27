import numpy as np

def count_color(grid, color):
  """Counts the occurrences of a specific color in the grid."""
  count = 0
  for r in range(grid.shape[0]):
    for c in range(grid.shape[1]):
      if grid[r, c] == color:
        count += 1
  return count

def transform(input_grid):
    """
    Transforms the input grid based on a cycling color replacement rule.

    1. Identifies all pixels in the input grid that are not the background color orange (7).
    2. Counts the number of blue (1) pixels in the input grid.
    3. Selects a target color cycle based on this count:
       - If the count of blue pixels is 3 or more, the cycle is (red(2), gray(5), azure(8)).
       - Otherwise (count is 0, 1, or 2), the cycle is (red(2), azure(8), gray(5)).
    4. Iterates through the input grid in reading order (top-to-bottom, left-to-right).
    5. For each non-orange pixel encountered, replaces its color in the output grid
       with the next color from the selected sequence, cycling through the sequence.
    6. Orange (7) pixels remain unchanged.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)

    # Define the background color and the cycle-determining color
    background_color = 7
    cycle_determining_color = 1 # blue

    # Count the occurrences of the blue color
    # blue_count = np.sum(input_array == cycle_determining_color) # numpy way
    blue_count = count_color(input_array, cycle_determining_color) # explicit count

    # Determine the color cycle based on the count of blue pixels
    if blue_count >= 3:
        # Cycle: red(2), gray(5), azure(8)
        color_cycle = [2, 5, 8]
    else:
        # Cycle: red(2), azure(8), gray(5)
        color_cycle = [2, 8, 5]

    # Initialize cycle index
    cycle_index = 0
    cycle_len = len(color_cycle)

    # Get grid dimensions
    height, width = input_array.shape

    # Iterate through the grid in reading order (top-to-bottom, left-to-right)
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is NOT the background color
            if input_array[r, c] != background_color:
                # Get the target color from the determined cycle
                target_color = color_cycle[cycle_index % cycle_len]
                # Update the corresponding pixel in the output grid
                output_array[r, c] = target_color
                # Increment the cycle index for the next non-background pixel
                cycle_index += 1

    # Convert the numpy array back to a standard list of lists format
    output_grid = output_array.tolist()
    return output_grid