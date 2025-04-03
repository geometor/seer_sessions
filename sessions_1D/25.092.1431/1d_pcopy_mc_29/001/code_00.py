import numpy as np

def transform(input_grid):
  """
  Transforms the input grid (assumed 3x11) by identifying a single isolated 
  non-white pixel in the first row. This single pixel is then expanded into a 
  horizontal 3-pixel line segment of the same color, centered at the original 
  pixel's location. An existing 3-pixel horizontal line in the first row is 
  preserved. The remaining rows (assumed all white) are unchanged. The input 
  is expected as a flat list of 33 integers and the output is returned in the 
  same format.
  """

  # Define grid dimensions based on the input length (33 = 3 * 11)
  height = 3
  width = 11
  
  # Convert the flat input list into a 2D numpy array
  try:
      input_array = np.array(input_grid).reshape((height, width))
  except ValueError:
      # Handle cases where input might not be exactly 33 elements
      # This is a safeguard, though ARC tasks usually conform to expected structures.
      print(f"Error: Input grid size mismatch. Expected {height * width} elements, got {len(input_grid)}.")
      # Depending on strictness, could return None, empty list, or raise error.
      # For robustness in ARC, often copying input or returning unchanged is safer.
      return input_grid[:] # Return a copy

  # Initialize the output array as a copy of the input
  output_array = input_array.copy()

  # --- Locate the single isolated pixel in the first row ---
  single_pixel_col = -1
  single_pixel_color = -1
  row0 = input_array[0, :] 

  for col in range(width):
      # Check if the current pixel is non-white (not 0)
      if row0[col] != 0:
          # Assume it's single initially
          is_single = True
          
          # Check left neighbor (if it exists and is non-white)
          if col > 0 and row0[col - 1] != 0:
              is_single = False
              
          # Check right neighbor (if it exists and is non-white)
          if col < width - 1 and row0[col + 1] != 0:
              is_single = False
              
          # If it's still considered single, we found it
          if is_single:
              single_pixel_col = col
              single_pixel_color = row0[col]
              # Assuming only one such single pixel per task specification
              break 

  # --- Apply the transformation if a single pixel was found ---
  if single_pixel_col != -1:
      # Calculate the start and end column indices for the new 3-pixel line
      # Ensure indices stay within the grid boundaries [0, width-1]
      start_col = max(0, single_pixel_col - 1)
      # The slice end index is exclusive, so we need single_pixel_col + 2
      # to include the pixel at index single_pixel_col + 1.
      # Ensure the end index doesn't exceed the grid width.
      end_col = min(width, single_pixel_col + 2) 

      # Update the first row of the output array with the new 3-pixel line
      output_array[0, start_col:end_col] = single_pixel_color

  # Convert the 2D numpy output array back to a flat list
  output_grid = output_array.flatten().tolist()

  return output_grid