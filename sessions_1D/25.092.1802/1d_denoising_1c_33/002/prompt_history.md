
## train_1

**input:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 8 0 0 8 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves processing a 1-dimensional grid (represented as a single row). Each input grid contains white pixels (0) and pixels of one other color (e.g., azure=8 or orange=7). The non-white pixels appear in one or more contiguous horizontal segments, and potentially as isolated single pixels. The output grid retains only the *longest* contiguous horizontal segment of the non-white color found in the input. All other pixels in the output grid, including shorter segments or isolated pixels of the non-white color, become white (0). The dimensions of the grid remain unchanged.

## Facts


```yaml
task_type: filtering
grid_dimensionality: 1D # Effectively 1xN grids
color_usage:
  - background: white (0)
  - foreground: one other color per example (e.g., azure=8, orange=7)
objects:
  - type: contiguous_horizontal_segment
    color: non-white color present in the input
    properties:
      - length
      - color_value
  - type: isolated_pixel
    color: non-white color present in the input
relationships:
  - multiple segments of the same non-white color can exist in the input
actions:
  - identify: the single non-white color present
  - find: all contiguous horizontal segments of this non-white color
  - measure: the length of each segment
  - select: the segment with the maximum length (if multiple have the same max length, the examples don't show this case, but implicitly any one of the longest would work, though typically the first encountered might be selected)
  - generate_output: create a new grid of the same size, filled with the background color (white)
  - copy: place the selected longest segment into the output grid at its original position
transformation: keep only the longest contiguous horizontal block of the non-background color, changing all other cells to the background color (white).
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid, but filled entirely with white pixels (0).
2.  Identify the primary non-white color present in the input grid.
3.  Scan the input grid to find all contiguous horizontal segments composed solely of this non-white color.
4.  Determine the length of each identified segment.
5.  Identify the segment(s) with the greatest length. If there's a tie, select the first one encountered (or any one of them).
6.  Copy the pixels corresponding to this longest segment from their original positions in the input grid to the same positions in the output grid.
7.  Return the modified output grid.
```python
import numpy as np
from itertools import groupby

"""
Keep only the longest contiguous horizontal block of the non-background color, 
changing all other cells to the background color (white=0).
"""

def find_segments(row, target_color):
    """Finds contiguous segments of a target color in a 1D list."""
    segments = []
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment
            segments.append({'start': start_index, 'end': i - 1, 'length': i - start_index, 'color': target_color})
            start_index = -1
    # Handle segment ending at the last pixel
    if start_index != -1:
        segments.append({'start': start_index, 'end': len(row) - 1, 'length': len(row) - start_index, 'color': target_color})
    return segments

# Alternative using groupby (often more concise)
def find_segments_groupby(row):
    """Finds contiguous segments of any color using groupby."""
    segments = []
    index = 0
    for color, group in groupby(row):
        length = len(list(group))
        if color != 0: # Only track non-background segments
             segments.append({'start': index, 'end': index + length - 1, 'length': length, 'color': color})
        index += length
    return segments


def transform(input_grid):
    """
    Transforms the input grid by keeping only the longest contiguous horizontal 
    segment of the non-white color. All other pixels become white (0).

    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # Assuming input is always 1xN, extract the single row
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input
        
    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    background_color = 0

    # Initialize output grid with background color
    output_row = [background_color] * width

    # Find all non-background segments
    all_segments = find_segments_groupby(input_row)

    # If no non-background segments exist, return the background grid
    if not all_segments:
        return [output_row] # Return as list of lists

    # Find the longest segment
    longest_segment = max(all_segments, key=lambda s: s['length'])

    # Copy the longest segment to the output row
    start = longest_segment['start']
    end = longest_segment['end']
    color = longest_segment['color']
    for i in range(start, end + 1):
        output_row[i] = color

    # Return the output grid (as a list of lists)
    return [output_row]

```
