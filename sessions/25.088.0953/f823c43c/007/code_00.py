import numpy as np
from collections import Counter
import math

"""
Transformation Rule:

1. Identify a 'noise' color, which is consistently magenta (6) in the examples.
2. Analyze the non-noise pixels in the input grid to determine the two most
   dominant colors: C1 (most frequent) and C2 (second most frequent). Handle
   cases where fewer than two non-noise colors exist (defaulting to white=0 or
   using the single color for both C1 and C2).
3. Infer the underlying pattern of the grid based on the non-noise pixels. This
   pattern consists of two parts:
    a. An 'even row' pattern: Determined by observing non-noise pixels in even rows.
       (Based on examples, this is consistently just C1).
    b. An 'odd row' pattern: Determined by observing non-noise pixels in odd rows.
       This pattern involves C1 and potentially C2, often in a repeating sequence
       based on the column index.
4. Create an output grid initialized as a copy of the input grid.
5. Iterate through each pixel (r, c) of the input grid.
6. If the pixel `input_grid[r, c]` is the noise color (6):
    a. Determine the replacement color using the inferred pattern:
        - If the row `r` is even, use the color defined by the 'even row'
          pattern for column `c`.
        - If the row `r` is odd, use the color defined by the 'odd row'
          pattern for column `c`.
    b. Update the `output_grid[r, c]` with the determined replacement color.
7. Pixels that were not the noise color remain unchanged in the output grid.
8. Return the final output grid.

Pattern Inference Details:
- The 'even row' pattern is assumed to be C1 for all columns based on examples.
- The 'odd row' pattern is inferred by finding the first odd row containing
  both C1 and C2 (if C1 and C2 are different). The sequence of non-noise
  colors in this row is analyzed to find the shortest repeating unit. This
  unit is then used to generate the full odd row pattern prototype. If no odd
  row contains both C1 and C2, the pattern defaults to C1 for all columns. If
  only C2 is present in an odd row (and C1 != C2), that might indicate C2 is
  the pattern (though less likely based on examples).
"""

def find_pattern_colors(grid, noise_color):
    """
    Finds the two most frequent colors in the grid, excluding the noise_color.

    Args:
        grid (np.array): The input grid.
        noise_color (int): The color value to exclude from frequency counting.

    Returns:
        tuple: (C1, C2) where C1 is the most frequent and C2 is the second
               most frequent non-noise color. Handles cases where fewer than
               two non-noise colors are present. Defaults to (0, 0) if no
               non-noise colors are found.
    """
    # Flatten the grid to easily count all pixel values
    pixels = grid.flatten()

    # Count the frequency of each color
    color_counts = Counter(pixels)

    # Remove the noise color from the counts if it exists
    if noise_color in color_counts:
        del color_counts[noise_color]

    # Get the colors sorted by frequency (most common first)
    most_common = color_counts.most_common(2)

    # Determine C1 and C2 based on the number of non-noise colors found
    if len(most_common) == 0:
        # No non-noise colors were found
        c1, c2 = 0, 0  # Default to white
    elif len(most_common) == 1:
        # Only one non-noise color was found
        c1 = most_common[0][0]
        c2 = c1  # Use the same color for C2
    else:
        # Two or more non-noise colors were found
        c1 = most_common[0][0]
        c2 = most_common[1][0]

    return (c1, c2)

def find_repeating_pattern(seq):
    """
    Finds the shortest repeating pattern unit in a sequence.

    Args:
        seq (list): The input sequence of colors.

    Returns:
        list or None: The shortest repeating unit if found, otherwise None.
                      Returns None if seq is empty. Returns [seq[0]] if only one distinct element.
    """
    if not seq:
        return None
        
    unique_elements = set(seq)
    if len(unique_elements) <= 1:
         return [seq[0]] # Pattern is just the single element

    n = len(seq)
    for length in range(1, n // 2 + 1):
        unit = seq[:length]
        
        # Check if the sequence is formed by repeating this unit
        is_match = True
        for i in range(0, n, length):
            segment = seq[i : min(i + length, n)]
            expected_segment = unit[:len(segment)]
            if segment != expected_segment:
                is_match = False
                break
        
        if is_match:
            # Check if a shorter unit (divisor of current length) also works
            # Example: If seq=[1,1,1,1], unit=[1,1] works, but unit=[1] is shorter.
            shorter_pattern_found = False
            if length > 1:
                for sub_len in range(1, length):
                    if length % sub_len == 0:
                         sub_unit = unit[:sub_len]
                         is_sub_match = True
                         for i in range(0, length, sub_len):
                              segment = unit[i : min(i+sub_len, length)]
                              expected_segment = sub_unit[:len(segment)]
                              if segment != expected_segment:
                                   is_sub_match = False
                                   break
                         if is_sub_match: # Found a shorter repeating unit for the current unit
                              shorter_pattern_found = True
                              break # No need to check other sub_lengths
            
            if not shorter_pattern_found:
                 return unit # Found shortest repeating unit for the sequence

    # If no repeating pattern shorter than the sequence itself is found
    # but the sequence contains multiple colors, maybe the pattern is just the sequence?
    # For this problem, we expect simple repeating patterns. If none found, default.
    # Let's return None if no *repeating* pattern is clearly identified.
    return None


def infer_prototype_rows(grid, noise_color, c1, c2):
    """
    Infers the prototype pattern for even and odd rows based on non-noise pixels.

    Args:
        grid (np.array): The input grid.
        noise_color (int): The noise color to ignore.
        c1 (int): The most frequent non-noise color.
        c2 (int): The second most frequent non-noise color.

    Returns:
        tuple: (even_prototype, odd_prototype) where each is a list
               representing the color pattern for a row of width cols.
    """
    rows, cols = grid.shape
    
    # Assume even rows are always C1 based on examples
    even_prototype = [c1] * cols
    
    # Default odd prototype is C1
    odd_prototype = [c1] * cols
    
    # Try to find a more specific pattern for odd rows
    representative_odd_row_idx = -1
    found_c1_c2_row = False
    found_any_non_noise_odd_row = False
    
    # Prioritize finding an odd row with both C1 and C2 (if they differ)
    if c1 != c2:
        for r in range(1, rows, 2):
            row_colors = set(grid[r, grid[r, :] != noise_color])
            if c1 in row_colors and c2 in row_colors:
                representative_odd_row_idx = r
                found_c1_c2_row = True
                break
                
    # If no C1/C2 row, find any odd row with non-noise pixels
    if representative_odd_row_idx == -1:
         for r in range(1, rows, 2):
             if np.any(grid[r, :] != noise_color):
                  representative_odd_row_idx = r
                  found_any_non_noise_odd_row = True
                  break

    # If we found a representative odd row, analyze its pattern
    if representative_odd_row_idx != -1:
        r = representative_odd_row_idx
        # Extract the sequence of non-noise colors in this row
        observed_seq = [grid[r, c] for c in range(cols) if grid[r, c] != noise_color]
        
        if observed_seq:
            pattern_unit = find_repeating_pattern(observed_seq)
            
            if pattern_unit:
                unit_len = len(pattern_unit)
                # Generate prototype by repeating the unit
                odd_prototype = [pattern_unit[c % unit_len] for c in range(cols)]
            else:
                # No simple repeating pattern found in the representative row.
                # Fallback: use observed values and fill gaps with C1.
                observed_colors_map = {c: grid[r, c] for c in range(cols) if grid[r, c] != noise_color}
                odd_prototype = [observed_colors_map.get(c, c1) for c in range(cols)]
        # else: row had only noise, keep default odd_prototype = [c1]*cols
        
    # Handle the case where C1 == C2. Prototypes should just be C1.
    if c1 == c2:
        even_prototype = [c1] * cols
        odd_prototype = [c1] * cols
        
    return even_prototype, odd_prototype


def transform(input_grid):
    """
    Transforms the input grid by replacing noise pixels (magenta=6) based on
    an inferred underlying pattern derived from non-noise pixels. The pattern
    consists of potentially different repeating sequences for even and odd rows,
    determined by the two most frequent non-noise colors (C1, C2).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with noise pixels replaced according
                       to the inferred pattern.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original non-noise pixels
    output_grid_np = grid_np.copy()
    rows, cols = grid_np.shape

    # Define the noise color to be identified and replaced
    noise_color = 6

    # Determine the primary (C1) and secondary (C2) pattern colors globally
    c1, c2 = find_pattern_colors(grid_np, noise_color)

    # Infer the pattern prototypes for even and odd rows
    even_prototype, odd_prototype = infer_prototype_rows(grid_np, noise_color, c1, c2)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel in the original grid is the noise color
            if grid_np[r, c] == noise_color:
                # Apply the inferred pattern based on row parity
                if r % 2 == 0:
                    # Use the even row pattern prototype
                    replacement_color = even_prototype[c]
                else:
                    # Use the odd row pattern prototype
                    replacement_color = odd_prototype[c]
                
                # Update the pixel in the output grid
                output_grid_np[r, c] = replacement_color

    # Convert the NumPy array back to a list of lists for the final output format
    output_grid = output_grid_np.tolist()

    return output_grid