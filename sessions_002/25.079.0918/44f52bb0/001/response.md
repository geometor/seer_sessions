```python
"""
Counts the number of red pixels (value 2) in the input grid.
If the count is odd, the output is 1.
If the count is even, the output is 7.
"""

def transform(input_grid):
    # Count red pixels.
    red_pixel_count = 0
    for row in input_grid:
        for pixel in row:
            if pixel == 2:
                red_pixel_count += 1

    # Determine output based on parity.
    if red_pixel_count % 2 == 1:
        output = 1
    else:
        output = 7

    return output
```
