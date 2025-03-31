import numpy as np

def find_background_color(grid):
  """
  Identifies the most frequent color in the grid, assuming it's the background.
  """
  values, counts = np.unique(grid, return_counts=True)
  # In case of a tie for most frequent, prioritize lower color index if needed,
  # but usually, there's a clear background. For this task, 7 is consistent.
  return values[np.argmax(counts)] 

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identifies the background color (assumed to be the most frequent, typically orange/7).
    2. Identifies Gray (5) pixels as stationary.
    3. For all other non-background pixels (e.g., Red, Azure, Maroon):
       - Checks if the cell directly below the pixel (in the original input grid) is the background color.
       - If the cell below is background, the pixel "falls" one step down into that cell.
       - The pixel's original location becomes the background color.
       - If the cell below is not background (either another color or the edge of the grid), the pixel remains stationary.
    4. The process iterates from bottom to top to correctly handle pixels potentially falling sequentially.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Determine the background color 
    background_color = find_background_color(input_np)
    # Define the stationary color
    stationary_color = 5 # Gray
    
    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np)

    # Iterate through the grid rows from second-to-last up to the top (height-2 down to 0)
    # Iterating bottom-up ensures that if a pixel A falls into space B, 
    # a pixel C above A can then fall into A's vacated space in the same pass.
    for r in range(height - 2, -1, -1):
        for c in range(width):
            # Get the color of the current pixel in the *original* input grid
            current_color = input_np[r, c]
            
            # Check if the current pixel is background or the designated stationary color
            if current_color == background_color or current_color == stationary_color:
                continue # Skip background and stationary (Gray) pixels

            # Check the color of the cell directly below in the *original* input grid
            below_color = input_np[r + 1, c]
            
            # Check if the cell below is background color
            if below_color == background_color:
                # If yes, move the current pixel down in the *output* grid
                output_np[r + 1, c] = current_color
                # Set the original position in the *output* grid to background color
                output_np[r, c] = background_color
                
    # Return the transformed grid as a standard Python list of lists
    return output_np.tolist()