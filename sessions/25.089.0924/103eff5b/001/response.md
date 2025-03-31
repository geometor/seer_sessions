```python
import numpy as np
import sys

def calculate_manhattan_distance(p1_row, p1_col, p2_row, p2_col):
    """Calculates the Manhattan distance between two points."""
    return abs(p1_row - p2_row) + abs(p1_col - p2_col)

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify "key" pixels (non-white, non-azure) and "lock" pixels (azure).
    2. For each lock pixel, find the closest key pixel using Manhattan distance.
    3. If there's a tie in distance, use the key pixel that appears first when scanning the grid row by row, then column by column.
    4. Replace the lock pixel's color (azure) with the color of the determined closest key pixel.
    5. Leave all other pixels unchanged.
    """
    # Convert input list of lists to a numpy array for easier indexing
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # 1. Identify key pixels (non-white/0, non-azure/8) and store them with original coordinates and color
    key_pixels = []
    for r in range(rows):
        for c in range(cols):
            color = input_array[r, c]
            if color != 0 and color != 8:
                key_pixels.append({'row': r, 'col': c, 'color': color})

    # 2. Identify lock pixels (azure/8)
    lock_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == 8:
                lock_pixels.append({'row': r, 'col': c})

    # If there are no key pixels or no lock pixels, return the original grid
    if not key_pixels or not lock_pixels:
        return output_array.tolist()

    # 3. For each lock pixel, find the closest key pixel and update the output grid
    for lock_pixel in lock_pixels:
        lr, lc = lock_pixel['row'], lock_pixel['col']
        
        min_distance = sys.maxsize
        closest_key_color = -1 # Placeholder

        # Calculate distances to all key pixels
        distances = []
        for i, key_pixel in enumerate(key_pixels):
            kr, kc = key_pixel['row'], key_pixel['col']
            dist = calculate_manhattan_distance(lr, lc, kr, kc)
            distances.append({'distance': dist, 'index': i, 'color': key_pixel['color']})
            if dist < min_distance:
                min_distance = dist

        # Find all key pixels at the minimum distance
        closest_candidates = [d for d in distances if d['distance'] == min_distance]

        # 4. Tie-breaking: choose the candidate that appeared first in the key_pixels list (row-major order)
        # The 'index' stored in distances corresponds to the original order in key_pixels
        best_candidate = min(closest_candidates, key=lambda x: x['index'])
        closest_key_color = best_candidate['color']

        # 5. Update the output grid at the lock pixel's location
        output_array[lr, lc] = closest_key_color

    # Convert numpy array back to list of lists for the final output
    return output_array.tolist()
```