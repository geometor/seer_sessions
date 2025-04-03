import numpy as np

def find_pivot(grid):
  """Finds the index of the pivot pixel (maroon, 9)."""
  for i, pixel in enumerate(grid):
    if pixel == 9:
      return i
  return -1 # Should not happen based on examples

def find_segment(grid, pivot_index):
  """Finds the segment (color, start_index, end_index)."""
  segment_color = -1
  start_index = -1
  end_index = -1

  for i, pixel in enumerate(grid):
    # Skip background and pivot
    if pixel != 0 and pixel != 9:
      if start_index == -1:
          segment_color = pixel
          start_index = i
      # Continue until the color changes or grid ends
      if i + 1 == len(grid) or grid[i+1] != segment_color:
          end_index = i
          break # Found the end of the segment
  
  if start_index == -1:
      # Handle case where no segment is found (though unlikely based on examples)
      return None, -1, -1
      
  return segment_color, start_index, end_index

def transform(input_grid):
  """
  Reflects a colored line segment across a fixed maroon pivot pixel (9) 
  in a 1D grid. The background is white (0). The length and color of the 
  segment are preserved, but its position is changed based on reflection 
  relative to the pivot.
  """
  
  # Convert list to numpy array for easier manipulation if needed, 
  # but standard list operations are sufficient here.
  input_list = list(input_grid)
  grid_size = len(input_list)
  
  # Initialize output_grid with background color (0)
  output_grid = [0] * grid_size
  
  # 1. Locate the pivot pixel (maroon, 9)
  pivot_index = find_pivot(input_list)
  if pivot_index == -1:
      # If no pivot found, perhaps return input or raise error
      # Based on examples, pivot always exists.
      return input_grid # Or handle error appropriately
      
  # Place the pivot in the output grid
  output_grid[pivot_index] = 9
  
  # 2. Locate the colored segment
  segment_color, start_in, end_in = find_segment(input_list, pivot_index)

  if segment_color == -1:
      # If no segment found (only background and pivot), return grid with just pivot
       return output_grid # Or handle as needed

  # 3. Calculate distances from pivot to segment ends in input
  # Note: end_in is inclusive index
  dist_start_from_pivot = pivot_index - start_in 
  dist_end_from_pivot = pivot_index - end_in 

  # 4. Calculate new segment position based on reflection
  # The new start position's distance from pivot = old end position's distance from pivot
  # The new end position's distance from pivot = old start position's distance from pivot
  start_out = pivot_index + dist_end_from_pivot
  end_out = pivot_index + dist_start_from_pivot

  # 5. Place the reflected segment in the output grid
  # Ensure indices are within bounds (though reflection logic should handle this if grid is large enough)
  # Iterate through the calculated range for the output segment
  # Ensure start_out is the smaller index if reflection crosses the pivot
  min_out = min(start_out, end_out)
  max_out = max(start_out, end_out)
  
  for i in range(min_out, max_out + 1):
      if 0 <= i < grid_size: # Basic boundary check
          # Check if we are overwriting the pivot - shouldn't happen if segment doesn't overlap pivot
          if i != pivot_index: 
              output_grid[i] = segment_color
          # else: handle overlap if necessary based on task rules (not seen in examples)

  return output_grid