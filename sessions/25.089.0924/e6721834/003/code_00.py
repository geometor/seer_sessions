import numpy as np
from collections import Counter
import operator

# --- Helper Functions ---

def find_most_frequent_color(grid_section):
  """
  Finds the most frequent color in a grid section (numpy array).
  Handles ties by returning the smallest color index.
  Returns 0 (white) for empty input.
  """
  if grid_section.size == 0:
      return 0
  colors, counts = np.unique(grid_section, return_counts=True)
  # In case of a tie in counts, np.argmax returns the index of the first max value.
  # Since np.unique returns sorted colors, this effectively selects the smallest color index in a tie.
  most_frequent_color = colors[np.argmax(counts)]
  return most_frequent_color

def count_non_background_pixels(grid_section, background_color):
  """
  Counts the number of pixels in the grid section that are not the background color.
  """
  if grid_section.size == 0:
      return 0
  return np.sum(grid_section != background_color)

# --- Main Transformation Function ---

def transform(input_grid):
  """
  Transforms the input grid based on the following rules:
  1. Split the input grid into two halves (vertically if Width >= Height, horizontally otherwise).
  2. Identify the background color (most frequent) of each half.
  3. Count the number of non-background (foreground) pixels in each half.
  4. Determine the "source" half (the one with strictly more foreground pixels) and the "target" half.
     If counts are equal, the first half (Top or Left) is the source.
  5. Create an output grid with the dimensions of the source half.
  6. Fill the output grid with the background color of the target half.
  7. Overlay the foreground pixels from the source half onto the output grid,
     maintaining their relative positions within the source half.
  """
  input_np = np.array(input_grid, dtype=int)
  H, W = input_np.shape

  # --- 1. Split into Halves ---
  # np.array_split handles odd dimensions; the first array might be smaller.
  if H > W:
      # Split horizontally into Top (A) and Bottom (B)
      axis_split = 0
      half_A, half_B = np.array_split(input_np, 2, axis=axis_split)
  else:
      # Split vertically (includes H == W) into Left (A) and Right (B)
      axis_split = 1
      half_A, half_B = np.array_split(input_np, 2, axis=axis_split)

  # --- 2. Identify Background Colors ---
  bg_A = find_most_frequent_color(half_A)
  bg_B = find_most_frequent_color(half_B)

  # --- 3. Count Foreground Pixels ---
  count_A = count_non_background_pixels(half_A, bg_A)
  count_B = count_non_background_pixels(half_B, bg_B)

  # --- 4. Determine Source and Target Halves ---
  # Source has strictly more foreground pixels. Tie goes to A (Top/Left).
  if count_A >= count_B:
      source_half = half_A
      bg_source = bg_A
      # target_half = half_B # Not explicitly needed for pixel values
      bg_target = bg_B
  else:
      source_half = half_B
      bg_source = bg_B
      # target_half = half_A # Not explicitly needed for pixel values
      bg_target = bg_A

  # --- 5. Create Output Grid ---
  output_shape = source_half.shape
  output_grid = np.full(output_shape, bg_target, dtype=int)

  # --- 6. & 7. Overlay Foreground Pixels ---
  # Iterate through the source half using its local coordinates (r, c)
  for r in range(source_half.shape[0]):
      for c in range(source_half.shape[1]):
          pixel_value = source_half[r, c]
          # Check if the pixel in the source half is a foreground pixel
          if pixel_value != bg_source:
              # Place the foreground pixel onto the output grid at the same relative coordinate
              output_grid[r, c] = pixel_value

  # Convert final numpy array back to list of lists
  return output_grid.tolist()