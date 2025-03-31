```python
import numpy as np
from collections import Counter
import math

"""
Identify the background color (assumed to be 7 based on examples).
Count the occurrences of all other non-background colors in the input grid.
For each non-background color:
  - Find the total count N.
  - Determine the dimensions (h, w) of a rectangle such that h * w = N and the dimensions are as close as possible (minimizing h + w).
  - Create a solid block of size h x w filled with that color.
Sort these generated blocks based on their total pixel count N in ascending order.
Determine the output grid dimensions:
  - Height (H) is the maximum height among all generated blocks.
  - Width (W) is the sum of the widths of all blocks plus a single column of background color between adjacent blocks.
Create the output grid initialized with the background color.
Place the sorted blocks horizontally from left to right, bottom-aligned, separated by single columns of the background color.
"""

def get_factors(n):
    """Find all factor pairs (h, w) of n."""
    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add((i, n // i))
            factors.add((n // i, i))
    return list(factors)

def find_closest_factors(n):
    """Find the factor pair (h, w) of n that minimizes h + w."""
    if n == 0:
        return (0, 0)
    if n == 1:
        return (1, 1)
        
    factors = get_factors(n)
    if not factors: # Should not happen for n > 0, but defensively
         return (1, n) # or handle as error

    best_pair = factors[0]
    min_sum = sum(best_pair)

    for h, w in factors:
        if h + w < min_sum:
            min_sum = h + w
            best_pair = (h, w)
        # Tie-breaking: prefer the squarer shape if sums are equal
        elif h + w == min_sum:
             if abs(h - w) < abs(best_pair[0] - best_pair[1]):
                 best_pair = (h, w)
            
    # Further tie-breaking: prefer taller rectangle if sums and abs differences are equal
    if sum(best_pair) == sum((best_pair[1], best_pair[0])) and abs(best_pair[0]-best_pair[1]) == abs(best_pair[1]-best_pair[0]):
       if best_pair[0] < best_pair[1]: # if height is less than width
          best_pair = (best_pair[1], best_pair[0]) # make it taller

    # Final tie-breaking: if still tied (e.g. perfect square), use the pair where h <= w as conventionally done by get_factors initially finding smaller factor first
    # Or simply return the one found, the logic above tends to favor taller first now. 
    # Let's ensure h >= w consistently if possible after minimizing sum and abs diff
    if best_pair[0] < best_pair[1]:
         best_pair = (best_pair[1], best_pair[0])


    return best_pair


def transform(input_grid):
    """
    Transforms the input grid by counting non-background pixels, forming blocks,
    sorting them by size, and arranging them horizontally, bottom-aligned,
    separated by background color columns.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Identify Background Color (assuming 7 based on examples)
    background_color = 7
    
    # 2. Isolate and Count Non-Background Pixels
    color_counts = Counter()
    for r in range(input_np.shape[0]):
        for c in range(input_np.shape[1]):
            color = input_np[r, c]
            if color != background_color:
                color_counts[color] += 1
                
    # Handle empty case
    if not color_counts:
         # Return a 1x1 grid of background color if no non-background pixels found
         return [[background_color]] 

    # 3. Create Color Blocks
    blocks_info = []
    for color, count in color_counts.items():
        h, w = find_closest_factors(count)
        block = np.full((h, w), color, dtype=int)
        blocks_info.append({'color': color, 'count': count, 'height': h, 'width': w, 'block': block})
        
    # 4. Sort Blocks by count (N)
    blocks_info.sort(key=lambda x: x['count'])
    
    # 5. Determine Output Grid Dimensions
    if not blocks_info:
         # This case is already handled above, but defensively
         return [[background_color]]
         
    max_h = 0
    total_w = 0
    num_blocks = len(blocks_info)
    
    for i, info in enumerate(blocks_info):
        max_h = max(max_h, info['height'])
        total_w += info['width']
        if i < num_blocks - 1: # Add gap width if not the last block
            total_w += 1 
            
    if max_h == 0 or total_w == 0: # Should not happen if blocks_info is not empty
        return [[background_color]]

    # 6. Construct Output Grid (initialized with background)
    output_grid = np.full((max_h, total_w), background_color, dtype=int)
    
    # 7. Place Blocks
    current_col = 0
    for i, info in enumerate(blocks_info):
        h = info['height']
        w = info['width']
        block = info['block']
        
        # Calculate start row for bottom-alignment
        start_row = max_h - h
        
        # Place the block
        output_grid[start_row : start_row + h, current_col : current_col + w] = block
        
        # Update cursor, adding gap if not the last block
        current_col += w
        if i < num_blocks - 1:
            current_col += 1 # Move past the gap column

    # 8. Finalize and return as list of lists
    return output_grid.tolist()

```