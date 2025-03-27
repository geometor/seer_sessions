import numpy as np

"""
Transforms an input grid containing a single central pattern on a uniform background.
The transformation involves extracting the pattern, creating four transformed versions
(original, rotated 90 degrees clockwise, rotated 90 degrees counter-clockwise, rotated 180 degrees),
and placing them onto an output grid of the same size, initially filled with the background color.
The placement is determined by aligning the center of each transformed pattern with a corner
of the bounding box of the original pattern in the input grid. Overlapping pixels are overwritten,
with later placements taking precedence. The specific alignment is:
- Rotated 90 CW: Center aligns with BBox Top-Left.
- Rotated 90 CCW: Center aligns with BBox Top-Right.
- Rotated 180: Center aligns with BBox Bottom-Left.
- Original: Center aligns with BBox Bottom-Right.
"""

# --- Helper Functions ---

def find_background_color(grid):
  """
  Determines the background color of the grid.
  Assumes the background color is the color present at the top-left corner.

  Args:
    grid: A numpy array representing the input grid.

  Returns:
    The integer color value of the background.
  """
  if grid.size == 0:
      raise ValueError("Input grid is empty")
  return grid[0, 0]

def find_pattern_bbox(grid, bg_color):
  """
  Finds the bounding box of non-background pixels.

  Args:
    grid: A numpy array representing the input grid.
    bg_color: The background color integer.

  Returns:
    A tuple (min_r, max_r, min_c, max_c) representing the bounding box
    of non-background pixels, or None if no non-background pixels are found.
  """
  non_bg_pixels = np.where(grid != bg_color)

  if len(non_bg_pixels[0]) == 0:
    return None

  min_r = np.min(non_bg_pixels[0])
  max_r = np.max(non_bg_pixels[0])
  min_c = np.min(non_bg_pixels[1])
  max_c = np.max(non_bg_pixels[1])

  return int(min_r), int(max_r), int(min_c), int(max_c) # Cast to int

def extract_pattern(grid, bbox):
   """
   Extracts the subgrid (pattern) defined by the bounding box.

   Args:
     grid: A numpy array representing the input grid.
     bbox: A tuple (min_r, max_r, min_c, max_c) defining the bounding box.

   Returns:
     A numpy array representing the extracted pattern.
   """
   if bbox is None:
       return np.array([[]], dtype=int) # Return empty array if no bbox
   min_r, max_r, min_c, max_c = bbox
   # Slice the grid using the bounding box coordinates
   # Note: slicing is exclusive of the end index, so add 1 to max_r and max_c
   return grid[min_r:max_r+1, min_c:max_c+1]

def place_pattern(output_grid, pattern, r_start, c_start):
    """
    Places a pattern onto the output grid at the specified top-left corner.
    Overwrites existing pixels in the output grid. Handles partial placements
    if the pattern goes out of bounds (clipping).

    Args:
      output_grid: The numpy array representing the grid to place the pattern onto.
      pattern: The numpy array representing the pattern to place.
      r_start: The starting row index for the top-left corner of the placement.
      c_start: The starting column index for the top-left corner of the placement.
    """
    if pattern.size == 0: # Do nothing if the pattern is empty
        return

    pH, pW = pattern.shape
    H, W = output_grid.shape

    # Determine the slice of the output grid to modify
    out_r_start = max(0, r_start)
    out_c_start = max(0, c_start)
    out_r_end = min(H, r_start + pH)
    out_c_end = min(W, c_start + pW)

    # Determine the corresponding slice of the pattern to use
    pattern_r_start = max(0, -r_start)
    pattern_c_start = max(0, -c_start)
    pattern_r_end = pattern_r_start + (out_r_end - out_r_start)
    pattern_c_end = pattern_c_start + (out_c_end - out_c_start)

    # Place the pattern slice if the slice dimensions are positive
    if out_r_end > out_r_start and out_c_end > out_c_start:
        output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = \
            pattern[pattern_r_start:pattern_r_end, pattern_c_start:pattern_c_end]


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation based on the natural language program.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)

    # Handle potentially empty input grid gracefully
    if input_np.size == 0:
        return [] # Return empty list for empty input

    H, W = input_np.shape

    # 1. Identify Background color
    bg_color = find_background_color(input_np)

    # 2. Initialize the output grid filled with the background color
    output_np = np.full_like(input_np, bg_color)

    # 3. Find the bounding box enclosing all non-background pixels
    bbox = find_pattern_bbox(input_np, bg_color)

    # If no non-background pattern is found, return the grid filled with background color
    if bbox is None:
      return output_np.tolist()

    min_r, max_r, min_c, max_c = bbox

    # 4. Extract the pattern P based on the bounding box
    pattern_P = extract_pattern(input_np, bbox)

    # Check if pattern extraction resulted in an empty pattern (shouldn't happen if bbox is not None, but safe check)
    if pattern_P.size == 0:
        return output_np.tolist() # Return background grid if pattern is empty

    pH, pW = pattern_P.shape # Get height and width of the pattern

    # Ensure pattern dimensions are valid
    if pH <= 0 or pW <= 0:
        return output_np.tolist()

    # 5. Calculate Pattern Center (relative to the pattern's top-left)
    # Using integer division for center calculation
    center_r = (pH - 1) // 2
    center_c = (pW - 1) // 2

    # 6. Create geometrically transformed versions of the pattern
    P_rot90_cw = np.rot90(pattern_P, k=-1)   # Rotate 90 degrees clockwise
    P_rot90_ccw = np.rot90(pattern_P, k=1)   # Rotate 90 degrees counter-clockwise
    P_rot180 = np.rot90(pattern_P, k=2)      # Rotate 180 degrees
    P_original = pattern_P                   # Original pattern

    # --- 7. Calculate Placement Origins (top-left corner for each pattern placement) ---
    # These origins ensure the center of the placed pattern aligns with the target bbox corner

    # Origin for P_rot90_cw (aligns center with bbox top-left: min_r, min_c)
    origin_cw_r = min_r - center_r
    origin_cw_c = min_c - center_c

    # Origin for P_rot90_ccw (aligns center with bbox top-right: min_r, max_c)
    origin_ccw_r = min_r - center_r
    origin_ccw_c = max_c - center_c

    # Origin for P_rot180 (aligns center with bbox bottom-left: max_r, min_c)
    origin_180_r = max_r - center_r
    origin_180_c = min_c - center_c

    # Origin for P_original (aligns center with bbox bottom-right: max_r, max_c)
    origin_orig_r = max_r - center_r
    origin_orig_c = max_c - center_c

    # --- 8. Place the transformed patterns onto the output grid ---
    # The order determines which pattern's pixels overwrite others in case of overlap.
    # Using the order: CW, CCW, 180, Original as specified in analysis.
    place_pattern(output_np, P_rot90_cw, origin_cw_r, origin_cw_c)
    place_pattern(output_np, P_rot90_ccw, origin_ccw_r, origin_ccw_c)
    place_pattern(output_np, P_rot180, origin_180_r, origin_180_c)
    place_pattern(output_np, P_original, origin_orig_r, origin_orig_c)

    # 9. Convert the final numpy array back to a list of lists for the required output format
    return output_np.tolist()
