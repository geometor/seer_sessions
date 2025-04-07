import numpy as np

def transform(input_grid):
  """
    Transforms the input grid by filtering out pixels of a specific color (Yellow 4)
    and preserving all other non-background pixels (Azure 8) in their original positions.

    1. Initialize an output grid with the same dimensions as the input, filled with the background color (Azure 8).
    2. Iterate through each pixel of the input grid.
    3. If the input pixel's color is neither the background color (Azure 8) nor the discard color (Yellow 4),
       copy its color to the corresponding position in the output grid.
    4. Otherwise, the output grid retains the background color at that position.
    5. Return the final output grid.
  """

  # Convert input list of lists to a numpy array for easier manipulation
  input_array = np.array(input_grid, dtype=int)
  
  # Get grid dimensions
  height, width = input_array.shape
  
  # Define key colors
  background_color = 8  # Azure
  discard_color = 4     # Yellow
  
  # Initialize output_grid with the background color
  output_array = np.full((height, width), background_color, dtype=int)
  
  # Iterate through each cell of the input grid
  for r in range(height):
    for c in range(width):
      # Get the color of the current input pixel
      current_color = input_array[r, c]
      
      # Check if the color should be preserved
      if current_color != background_color and current_color != discard_color:
        # If it's not background or the discard color, copy it to the output grid
        output_array[r, c] = current_color
        
  # Convert the output numpy array back to a list of lists for the expected format
  output_grid = output_array.tolist()
  
  return output_grid
