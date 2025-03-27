import numpy as np

def find_background_color(grid):
  """
  Determines the background color of the grid.
  Assumes the background color is the color present at the corners.
  """
  # Check the color at the top-left corner
  return grid[0, 0]

def transform(input_grid):
  """
  The transformation identifies the background color (typically the color at the corners). 
  It then finds all pixels in the input grid that are *not* the background color, forming a central pattern. 
  An output grid of the same dimensions is created, initially filled with the background color. 
  For each non-background pixel found in the input grid at position (r, c), its color is copied to four locations in the output grid: 
  the original position (r, c), the vertically reflected position (H-1-r, c), the horizontally reflected position (r, W-1-c), 
  and the diagonally reflected position (H-1-r, W-1-c), where H and W are the height and width of the grid. 
  This effectively overlays the central pattern and its three reflections (vertical, horizontal, diagonal/180-degree rotation) 
  onto the background grid.
  """
  # Convert input list of lists to a numpy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)
  H, W = input_np.shape

  # Determine the background color based on the corner pixel
  bg_color = find_background_color(input_np)

  # Initialize the output grid with the background color
  # Using full_like ensures the output has the same shape and type initially
  output_np = np.full_like(input_np, bg_color)

  # Iterate through each pixel of the input grid
  for r in range(H):
    for c in range(W):
      # Check if the current pixel's color is different from the background color
      if input_np[r, c] != bg_color:
        # Get the color of the non-background pixel
        color = input_np[r, c]
        
        # 1. Copy the color to the original position in the output grid
        output_np[r, c] = color
        
        # 2. Copy the color to the vertically reflected position
        # Vertical reflection maps row 'r' to 'H - 1 - r'
        output_np[H - 1 - r, c] = color
        
        # 3. Copy the color to the horizontally reflected position
        # Horizontal reflection maps column 'c' to 'W - 1 - c'
        output_np[r, W - 1 - c] = color
        
        # 4. Copy the color to the diagonally reflected (180-degree rotation) position
        # This combines vertical and horizontal reflection
        output_np[H - 1 - r, W - 1 - c] = color

  # Convert the numpy array back to a list of lists for the final output
  return output_np.tolist()