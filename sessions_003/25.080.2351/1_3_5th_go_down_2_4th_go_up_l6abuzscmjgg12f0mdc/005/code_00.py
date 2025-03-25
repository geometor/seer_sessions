"""
1. Identify Row Segments: For each row in the input grid, identify contiguous segments of non-zero pixels. Treat each of these as distinct objects.
2. Mirror and Expand: The non-zero section gets mirrored to include itself and the first zero, and the output is mirrored on the other side to reach a similar position to the original.
3. Fill the center: fill in the center zeros with the nearest non-zero neighbor
4. Zero Row Handling: If a row contains only zeros, the output row also contains only zeros.
"""

import numpy as np

def get_row_segments(row):
    """Identifies contiguous segments of non-zero pixels in a row."""
    segments = []
    start = -1
    for i, val in enumerate(row):
        if val != 0 and start == -1:
            start = i
        elif val == 0 and start != -1:
            segments.append((start, i - 1))
            start = -1
    if start != -1:
        segments.append((start, len(row) - 1))
    return segments

def transform(input_grid):
    """Transforms the input grid according to the mirroring and filling logic."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        segments = get_row_segments(input_grid[r])

        if not segments:  # Zero Row Handling
            continue

        for start, end in segments:
            # Mirror and Expand
            segment_length = end - start + 1

            for i in range(segment_length):
              output_grid[r,start + i ] = input_grid[r, start + i]

            if start > 0:
              output_grid[r, start -1] = input_grid[r, start]

            if end < cols -1:
                for i in range(segment_length):
                  if end + 1 + i < cols:
                    output_grid[r, end + 1 + i] = input_grid[r, end -i]

        #fill center with closest non zero
        for c in range(cols):
          if output_grid[r,c] == 0:
             # Find nearest non-zero neighbors
            closest_left = -1
            closest_right = -1

            for i in range(c - 1, -1, -1):
                if output_grid[r, i] != 0:
                    closest_left = i
                    break
            for i in range(c + 1, cols):
                if output_grid[r, i] != 0:
                    closest_right = i
                    break

            if closest_left != -1 and closest_right != -1:
                if (c - closest_left) <= (closest_right - c):
                    output_grid[r, c] = output_grid[r, closest_left]
                else:
                    output_grid[r, c] = output_grid[r, closest_right]
            elif closest_left != -1:
                output_grid[r, c] = output_grid[r, closest_left]
            elif closest_right != -1:
                output_grid[r, c] = output_grid[r, closest_right]


    return output_grid.tolist()