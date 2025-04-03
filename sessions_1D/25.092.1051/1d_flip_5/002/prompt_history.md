
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 4 3 3 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 4 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 2 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 3 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 4 4 4 4 4 4 4 3 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception:**

1.  **Input/Output Structure:** The input and output are both single rows (1D arrays) of pixels represented by integers.
2.  **Key Elements:** Each input row contains a contiguous segment of non-white (non-zero) pixels surrounded by white (zero) pixels.
3.  **Segment Composition:** Within the non-white segment, there's one pixel of a specific color (e.g., yellow in train_1, red in train_2, green in train_3) and multiple pixels of another single color (e.g., green in train_1, blue in train_2, yellow in train_3). The single pixel appears at one end of the segment.
4.  **Transformation:** The transformation involves moving the single, unique-colored pixel from one end of the multi-pixel block to the other end. The colors themselves and the surrounding white pixels remain unchanged.
5.  **General Rule:** The core operation is relocating the uniquely colored pixel within the non-white segment to the opposite end of that segment.

**Facts:**


```yaml
Task: Move a unique colored pixel to the other end of its segment.

Input:
  - type: grid (1D array)
  - contains:
    - background: white pixels (0)
    - segment:
      - type: contiguous block of non-white pixels
      - composition:
        - unique_pixel:
          - count: 1
          - color: non-white (e.g., 4, 2, 3)
          - position: one end of the segment
        - repeated_pixels:
          - count: multiple
          - color: single non-white color, different from unique_pixel (e.g., 3, 1, 4)
          - position: adjacent to unique_pixel, forming the rest of the segment

Output:
  - type: grid (1D array)
  - derived_from: input grid
  - changes:
    - segment:
      - unique_pixel:
        - action: moved
        - destination: opposite end of the segment
      - repeated_pixels:
        - position: shifted to accommodate the moved unique_pixel
    - background: unchanged

Relationships:
  - The unique_pixel is defined by its color being different from the adjacent pixels within the segment.
  - The transformation preserves the colors and the overall length of the non-white segment.
  - The transformation only affects the order of pixels within the non-white segment.
```


**Natural Language Program:**

1.  Identify the start and end indices of the contiguous segment of non-white (non-zero) pixels in the input row.
2.  Extract this segment from the row.
3.  Within the extracted segment, identify the single pixel whose color is unique compared to the others in the segment. Note its color and the color of the repeated pixels.
4.  Determine if the unique pixel is currently at the beginning or the end of the segment.
5.  Construct the new segment by placing the block of repeated-color pixels first, followed by the unique-color pixel if the unique pixel was originally at the beginning, OR place the unique-color pixel first, followed by the block of repeated-color pixels if the unique pixel was originally at the end. Effectively, move the unique pixel to the opposite end of the segment.
6.  Create the output row by replacing the original segment in the input row with the newly constructed segment at the same start and end indices. Keep the surrounding white pixels unchanged.
```python
import collections

"""
Transformation Rule:
1. Identify the contiguous segment of non-white (non-zero) pixels in the input row.
2. Within this segment, find the single pixel with a unique color compared to the others.
3. Move this unique pixel to the opposite end of the segment, shifting the other pixels accordingly.
4. Keep the surrounding white (zero) pixels and the colors within the segment unchanged.
"""

def find_segment_indices(row):
    """Finds the start and end indices of the first contiguous non-zero segment."""
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            end_index = i
    return start_index, end_index

def transform(input_grid):
    """
    Moves a unique colored pixel within a contiguous non-zero segment 
    to the opposite end of that segment in a 1D grid (represented as a list).

    Args:
        input_grid: A list containing a single list (the row) of integers.

    Returns:
        A list containing a single list (the transformed row) of integers.
    """
    # Assume input is always a single row grid
    if not input_grid or not input_grid[0]:
        return input_grid # Handle empty input
        
    input_row = list(input_grid[0]) # Work with a mutable copy
    output_row = list(input_row) # Initialize output as a copy

    # 1. Find the start and end indices of the non-white segment
    start, end = find_segment_indices(input_row)

    # If no segment is found, return the original row
    if start == -1:
        return [output_row]

    # 2. Extract the segment
    segment = input_row[start:end+1]
    
    # If segment is too small to have a unique element to move, return original
    if len(segment) <= 1:
        return [output_row]

    # 3. Identify unique and repeated colors within the segment
    color_counts = collections.Counter(segment)
    unique_color = -1
    repeated_color = -1
    
    # Check if the segment conforms to the expected pattern (one unique, one repeated)
    if len(color_counts) == 2:
        for color, count in color_counts.items():
            if count == 1:
                unique_color = color
            else:
                repeated_color = color
    
    # If the pattern doesn't match (e.g., all same color, >2 colors, no unique), return original
    if unique_color == -1 or repeated_color == -1:
        return [output_row] 

    # 4. Determine if the unique pixel is at the beginning or end
    is_unique_at_start = (segment[0] == unique_color)
    is_unique_at_end = (segment[-1] == unique_color)

    # If unique color is not at either end (shouldn't happen based on examples, but good check)
    if not is_unique_at_start and not is_unique_at_end:
        # Or handle unexpected internal position if needed by task rules
         return [output_row] # Return original if unique is not at an end

    # 5. Construct the new segment
    new_segment = []
    num_repeated = len(segment) - 1
    
    if is_unique_at_start:
        # Move unique pixel to the end
        new_segment.extend([repeated_color] * num_repeated)
        new_segment.append(unique_color)
    elif is_unique_at_end:
        # Move unique pixel to the start
        new_segment.append(unique_color)
        new_segment.extend([repeated_color] * num_repeated)
        
    # 6. Replace the original segment with the new segment in the output row
    output_row[start:end+1] = new_segment

    # Return the transformed row within a list structure
    return [output_row]
```
