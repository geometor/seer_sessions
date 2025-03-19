# 75b8110e • 020 • refine_coder

---
```python
"""
Transforms an 8x8 input grid to a 4x4 output grid by reducing each 2x2 block of pixels in the input to a single pixel in the output. The color of the output pixel is determined by the most frequent color in the corresponding 2x2 input block. If there's a tie, the largest color value wins.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate over each 2x2 block in the input grid
    for i in range(0, 8, 2):
        for j in range(0, 8, 2):
            # Extract the 2x2 block
            block = input_grid[i:i+2, j:j+2]

            # Count the occurrences of each color in the block
            color_counts = {}
            for color in block.flatten():
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1

            # Find the most frequent color(s)
            max_count = 0
            dominant_colors = []
            for color, count in color_counts.items():
                if count > max_count:
                    max_count = count
                    dominant_colors = [color]
                elif count == max_count:
                    dominant_colors.append(color)
            
            # Determine output pixel
            if len(dominant_colors) > 0:
                if len(dominant_colors) > 1:
                  output_grid[i//2, j//2] = max(dominant_colors)
                else:
                  output_grid[i//2, j//2] = dominant_colors[0]
            else:
                output_grid[i // 2, j // 2] = 0

    return output_grid
```
