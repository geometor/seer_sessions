
## train_1

**input:**
```
0 4 4 0 0 0 4 4 0 0 4 4 4 0 4 4 4 0 0 0 4 4 4 4 4 0 4 4 0 4 0 0 0
```


**output:**
```
0 4 4 0 0 0 4 4 0 0 4 4 4 0 4 4 4 0 0 0 7 7 7 7 7 0 4 4 0 4 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 0 0 0 4 4 4 4 4 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 4 0 0 4 0 0 0 4 4 4 0 0 0 4 4 4 4 0 0 4 0 0 4 4 4 4 0 0 4 0 0
```


**output:**
```
0 0 4 0 0 4 0 0 0 4 4 4 0 0 0 7 7 7 7 0 0 4 0 0 7 7 7 7 0 0 4 0 0
```

## Perception

The input and output are single-row grids (or effectively 1D arrays) containing pixels of primarily white (0) and yellow (4). The output grid is largely identical to the input grid, with the key difference being that some yellow (4) pixels are changed to orange (7) pixels.

Observing the examples provided:
1.  **train_1:** The input has contiguous horizontal groups of yellow pixels with lengths [2, 2, 3, 3, 5, 2, 1]. The maximum length is 5. The group of 5 yellow pixels in the input is changed to orange in the output.
2.  **train_2:** The input has contiguous horizontal groups of yellow pixels with lengths [7, 5, 6]. The maximum length is 7. The group of 7 yellow pixels in the input is changed to orange in the output.
3.  **train_3:** The input has contiguous horizontal groups of yellow pixels with lengths [1, 1, 3, 4, 1, 4, 1]. The maximum length is 4. Both groups of 4 yellow pixels in the input are changed to orange in the output.

The core transformation involves identifying horizontal segments of yellow pixels, determining their lengths, finding the maximum length among these segments, and then changing the color of all yellow pixels that belong to segments of that maximum length to orange. Pixels not meeting this criterion (white pixels or yellow pixels in shorter segments) remain unchanged.

## Facts


```yaml
Grid:
  - type: 1D array or single-row 2D array
  - colors_present: white (0), yellow (4) in input; white (0), yellow (4), orange (7) in output

Objects:
  - type: contiguous horizontal segments
  - color: yellow (4)
  - property: length (number of pixels in the segment)

Relationships:
  - Segments are separated by white (0) pixels.
  - Multiple segments can exist within a single grid.

Actions:
  - Identify all yellow (4) segments.
  - Calculate the length of each segment.
  - Determine the maximum length among all identified segments.
  - For every segment whose length equals the maximum length:
    - Change the color of all pixels within that segment from yellow (4) to orange (7).
  - Pixels not part of a maximum-length yellow segment remain unchanged.
```


## Natural Language Program

1.  Scan the input grid horizontally to identify all contiguous segments composed entirely of yellow (4) pixels.
2.  For each identified yellow segment, calculate its length (the number of pixels it contains).
3.  Find the maximum length among all calculated segment lengths. If no yellow segments exist, the maximum length is 0.
4.  Create the output grid as a copy of the input grid.
5.  Iterate through the input grid again, identifying the yellow segments.
6.  If a yellow segment's length matches the maximum length found in step 3, change the color of all pixels corresponding to that segment in the output grid from yellow (4) to orange (7).
7.  Leave all other pixels in the output grid unchanged from their input values (white pixels remain white, yellow pixels in segments shorter than the maximum length remain yellow).
```python
import copy

"""
Identify all contiguous horizontal segments of yellow (4) pixels in the input grid (which is a single row).
Calculate the length of each yellow segment.
Find the maximum length among all identified yellow segments.
Create the output grid by copying the input grid.
For every yellow segment whose length equals the maximum length, change the color of those pixels in the output grid to orange (7).
Leave all other pixels unchanged.
"""

def find_yellow_segments(row):
    """
    Finds contiguous segments of yellow (4) pixels in a single row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index, length).
        end_index is exclusive.
    """
    segments = []
    start_index = -1
    current_length = 0
    for i, pixel in enumerate(row):
        if pixel == 4:
            if start_index == -1:
                start_index = i
            current_length += 1
        else:
            if start_index != -1:
                segments.append((start_index, i, current_length))
                start_index = -1
                current_length = 0
    # Handle segment extending to the end of the row
    if start_index != -1:
        segments.append((start_index, len(row), current_length))
    return segments

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the longest horizontal
    yellow (4) segments to orange (7).

    Args:
        input_grid: A list of lists of integers representing the input grid.
                    Expected to be a single-row grid.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    # Ensure input is a single row grid, extract the row
    if not input_grid or len(input_grid) != 1:
         # Or handle error appropriately if multi-row grids are possible but unexpected
        return copy.deepcopy(input_grid) 
    
    input_row = input_grid[0]

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    output_row = output_grid[0]

    # Find all yellow segments in the input row
    yellow_segments = find_yellow_segments(input_row)

    # If no yellow segments, return the copy of the input
    if not yellow_segments:
        return output_grid

    # Find the maximum length among the segments
    max_length = 0
    for _, _, length in yellow_segments:
        if length > max_length:
            max_length = length

    # If max_length is 0 (shouldn't happen if segments exist, but safe check)
    if max_length == 0:
        return output_grid
        
    # Iterate through the segments again and change colors in the output row
    for start, end, length in yellow_segments:
        if length == max_length:
            # Change pixels in the output row from yellow (4) to orange (7)
            for i in range(start, end):
                if output_row[i] == 4: # Check just in case, though segment finder ensures this
                   output_row[i] = 7

    return output_grid
```
