
Previous Code:
```python
import numpy as np

"""
This program transforms an input grid based on patterns found in its last row.

1.  Initialize an output grid of the same size as the input, filled with the background color (0, white).
2.  Copy the last row and the last column from the input grid to the corresponding positions in the output grid. This acts as a border or frame.
3.  Analyze the last row of the input grid (excluding the bottom-right corner pixel which belongs to both borders) to identify contiguous horizontal segments (blocks) of identical, non-background colors.
4.  For each identified segment:
    a.  Record its color (C).
    b.  Record its length (n).
    c.  Record the starting column index (idx) of the segment.
    d.  Determine the drawing area for a square based on this segment:
        i.  Top row: `row_start = idx`
        ii. Bottom row (exclusive): `row_end = min(idx + n, height - 1)` (Clip to not overwrite the last row border)
        iii.Left column: `col_start = idx`
        iv. Right column (exclusive): `col_end = min(idx + n, width - 1)` (Clip to not overwrite the last column border)
    e.  If the calculated drawing area has valid dimensions (`row_start < row_end` and `col_start < col_end`), fill this rectangular area `output_grid[row_start : row_end, col_start : col_end]` with the color C. Note that this might not be a perfect square if clipped by the boundaries.
5.  Re-copy the last row and the last column from the input grid to the output grid. This ensures that the border pixels retain their original input values, even if the drawing process in step 4 overwrote them.
6.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by drawing shapes based on color blocks in the last row,
    preserving the last row and column as borders.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_np)
    
    # --- Step 2: Copy initial borders ---
    # Copy the last row and last column from input to output
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
        
    # Handle edge case of 1x1 grid - already copied
    if height <= 1 or width <= 1:
        return output_grid.tolist()

    # --- Step 3 & 4: Analyze last row and draw shapes ---
    last_row = input_np[height - 1, :]
    
    current_color = None
    start_index = -1
    segment_length = 0
    
    # Iterate through the last row to find contiguous blocks
    # Iterate up to width-1 because the last pixel is part of the vertical border
    for col in range(width -1): # Exclude the last column pixel
        color = last_row[col]
        
        # Check if the current segment ends
        if color == 0 or color != current_color:
            # If a non-background segment just ended, process it
            if current_color is not None and current_color != 0:
                # --- Step 4d: Determine drawing area ---
                row_start = start_index
                row_end = min(start_index + segment_length, height - 1)
                col_start = start_index
                col_end = min(start_index + segment_length, width - 1)

                # --- Step 4e: Draw the shape if area is valid ---
                if row_start < row_end and col_start < col_end:
                    output_grid[row_start : row_end, col_start : col_end] = current_color

            # Reset or start a new segment
            if color != 0:
                current_color = color
                start_index = col
                segment_length = 1
            else: # color is 0 (background)
                current_color = None
                start_index = -1
                segment_length = 0
        # Continue the current segment
        elif color == current_color:
            segment_length += 1

    # After the loop, check if the last segment needs to be processed
    if current_color is not None and current_color != 0:
        # --- Step 4d: Determine drawing area ---
        row_start = start_index
        row_end = min(start_index + segment_length, height - 1)
        col_start = start_index
        col_end = min(start_index + segment_length, width - 1)

        # --- Step 4e: Draw the shape if area is valid ---
        if row_start < row_end and col_start < col_end:
             output_grid[row_start : row_end, col_start : col_end] = current_color

    # --- Step 5: Re-copy borders to ensure they are preserved ---
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
            
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 9
5 6 6 7 7 7 8 9 9 9
```
Expected Output:
```
5 0 0 0 0 0 0 0 0 5
0 6 6 0 0 0 0 0 0 6
0 6 6 0 0 0 0 0 0 6
0 0 0 7 7 7 0 0 0 7
0 0 0 7 7 7 0 0 0 7
0 0 0 7 7 7 0 0 0 7
0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 9 9 9
5 6 6 7 7 7 8 9 9 9
```
Transformed Output:
```
5 0 0 0 0 0 0 0 0 5
0 6 6 0 0 0 0 0 0 6
0 6 6 0 0 0 0 0 0 6
0 0 0 7 7 7 0 0 0 7
0 0 0 7 7 7 0 0 0 7
0 0 0 7 7 7 0 0 0 7
0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 9 9 9
5 6 6 7 7 7 8 9 9 9
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 5
9 9 8 8 7 7 6 6 5 5
```
Expected Output:
```
9 9 0 0 0 0 0 0 0 9
9 9 0 0 0 0 0 0 0 9
0 0 8 8 0 0 0 0 0 8
0 0 8 8 0 0 0 0 0 8
0 0 0 0 7 7 0 0 0 7
0 0 0 0 7 7 0 0 0 7
0 0 0 0 0 0 6 6 0 6
0 0 0 0 0 0 6 6 0 6
0 0 0 0 0 0 0 0 5 5
9 9 8 8 7 7 6 6 5 5
```
Transformed Output:
```
9 9 0 0 0 0 0 0 0 9
9 9 0 0 0 0 0 0 0 9
0 0 8 8 0 0 0 0 0 8
0 0 8 8 0 0 0 0 0 8
0 0 0 0 7 7 0 0 0 7
0 0 0 0 7 7 0 0 0 7
0 0 0 0 0 0 6 6 0 6
0 0 0 0 0 0 6 6 0 6
0 0 0 0 0 0 0 0 5 5
9 9 8 8 7 7 6 6 5 5
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 3
8 8 4 4 4 5 5 3 3 3
```
Expected Output:
```
8 8 0 0 0 0 0 0 0 8
8 8 0 0 0 0 0 0 0 8
8 8 0 0 0 0 0 0 0 8
0 0 4 4 4 0 0 0 0 4
0 0 4 4 4 0 0 0 0 4
0 0 0 0 0 5 5 0 0 5
0 0 0 0 0 5 5 0 0 5
0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 3 3 3
8 8 4 4 4 5 5 3 3 3
```
Transformed Output:
```
8 8 0 0 0 0 0 0 0 8
8 8 0 0 0 0 0 0 0 8
0 0 4 4 4 0 0 0 0 8
0 0 4 4 4 0 0 0 0 4
0 0 4 4 4 0 0 0 0 4
0 0 0 0 0 5 5 0 0 5
0 0 0 0 0 5 5 0 0 5
0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 3 3 3
8 8 4 4 4 5 5 3 3 3
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.0
## General Assessment

The previous code successfully implemented the logic derived from the first example, where segments in the last row defined square shapes. However, Example 3 revealed that this assumption was incomplete. The failure occurred because the shapes drawn are not always squares, and their dimensions and positions depend on information from both the last row and the last column.

Specifically, the width of the drawn rectangle corresponds to the length of the segment in the last row, while the height corresponds to the length of the segment of the *same color* in the last column. The top-left corner's coordinates are determined by the starting indices of these corresponding row and column segments.

The strategy is to:
1.  Identify non-background color segments in the last row (excluding the last pixel).
2.  Identify non-background color segments in the last column (excluding the last pixel).
3.  Match segments from the row and column based on their color.
4.  Use the start index and length of the row segment to define the rectangle's column position and width.
5.  Use the start index and length of the corresponding column segment to define the rectangle's row position and height.
6.  Draw the rectangle with the matched color.
7.  Ensure the last row and column borders are preserved from the input.

## Metrics Gathering

Let's analyze the segments in the last row and last column for each example.
Segments are defined by (Color, Start Index, Length).
We exclude the bottom-right corner pixel from both row and column analysis.



*code_execution:*
```python
import numpy as np

def get_segments(line):
    """Finds contiguous segments of non-zero colors in a 1D array."""
    segments = []
    current_color = 0
    start_index = -1
    for i, color in enumerate(line):
        if color != 0 and color == current_color:
            continue # Extend current segment
        elif color != 0 and color != current_color: # Start new segment
            if current_color != 0: # End previous segment
                 segments.append({'color': current_color, 'start': start_index, 'length': i - start_index})
            current_color = color
            start_index = i
        elif color == 0 and current_color != 0: # End segment with background
            segments.append({'color': current_color, 'start': start_index, 'length': i - start_index})
            current_color = 0
            start_index = -1
    # Check for segment ending at the boundary
    if current_color != 0:
        segments.append({'color': current_color, 'start': start_index, 'length': len(line) - start_index})
    return segments

def analyze_example(input_grid):
    """Analyzes segments in the last row and column."""
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    if height <= 1 or width <= 1:
        return {'row_segments': [], 'col_segments': []}

    last_row = input_np[height - 1, :width - 1] # Exclude last pixel
    last_col = input_np[:height - 1, width - 1] # Exclude last pixel
    
    row_segments = get_segments(last_row)
    col_segments = get_segments(last_col)
    
    return {'row_segments': row_segments, 'col_segments': col_segments, 'dims': (height, width)}

# Example Inputs
ex1_in = [[0,0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,9],[0,0,0,0,0,0,0,0,0,9],[5,6,6,7,7,7,8,9,9,9]]
ex2_in = [[0,0,0,0,0,0,0,0,0,9],[0,0,0,0,0,0,0,0,0,9],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,5],[9,9,8,8,7,7,6,6,5,5]]
ex3_in = [[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0,3],[0,0,0,0,0,0,0,0,0,3],[8,8,4,4,4,5,5,3,3,3]]

analysis = {
    "Example 1": analyze_example(ex1_in),
    "Example 2": analyze_example(ex2_in),
    "Example 3": analyze_example(ex3_in),
}

import json
print(json.dumps(analysis, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 53, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type int64 is not JSON serializable

```
Ah, the `int64` from numpy is causing issues with JSON serialization. Let's adjust the `get_segments` function to return standard Python ints.



*code_execution:*
```python
import numpy as np
import json

def get_segments(line):
    """Finds contiguous segments of non-zero colors in a 1D array."""
    segments = []
    current_color = 0
    start_index = -1
    for i, color_val in enumerate(line):
        color = int(color_val) # Convert numpy int to standard int
        if color != 0 and color == current_color:
            continue # Extend current segment
        elif color != 0 and color != current_color: # Start new segment
            if current_color != 0: # End previous segment
                 segments.append({'color': current_color, 'start': start_index, 'length': i - start_index})
            current_color = color
            start_index = i
        elif color == 0 and current_color != 0: # End segment with background
            segments.append({'color': current_color, 'start': start_index, 'length': i - start_index})
            current_color = 0
            start_index = -1
    # Check for segment ending at the boundary
    if current_color != 0:
        segments.append({'color': current_color, 'start': start_index, 'length': len(line) - start_index})
    return segments

def analyze_example(input_grid):
    """Analyzes segments in the last row and column."""
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    if height <= 1 or width <= 1:
        return {'row_segments': [], 'col_segments': [], 'dims': (height, width)}

    last_row = input_np[height - 1, :width - 1] # Exclude last pixel
    last_col = input_np[:height - 1, width - 1] # Exclude last pixel
    
    row_segments = get_segments(last_row)
    col_segments = get_segments(last_col)
    
    return {'row_segments': row_segments, 'col_segments': col_segments, 'dims': (height, width)}

# Example Inputs
ex1_in = [[0,0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,9],[0,0,0,0,0,0,0,0,0,9],[5,6,6,7,7,7,8,9,9,9]]
ex2_in = [[0,0,0,0,0,0,0,0,0,9],[0,0,0,0,0,0,0,0,0,9],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,6],[0,0,0,0,0,0,0,0,0,5],[9,9,8,8,7,7,6,6,5,5]]
ex3_in = [[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0,3],[0,0,0,0,0,0,0,0,0,3],[8,8,4,4,4,5,5,3,3,3]]

analysis = {
    "Example 1": analyze_example(ex1_in),
    "Example 2": analyze_example(ex2_in),
    "Example 3": analyze_example(ex3_in),
}

print(json.dumps(analysis, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{
  "Example 1": {
    "row_segments": [
      {
        "color": 5,
        "start": 0,
        "length": 1
      },
      {
        "color": 6,
        "start": 1,
        "length": 2
      },
      {
        "color": 7,
        "start": 3,
        "length": 3
      },
      {
        "color": 8,
        "start": 6,
        "length": 1
      },
      {
        "color": 9,
        "start": 7,
        "length": 2
      }
    ],
    "col_segments": [
      {
        "color": 5,
        "start": 0,
        "length": 1
      },
      {
        "color": 6,
        "start": 1,
        "length": 2
      },
      {
        "color": 7,
        "start": 3,
        "length": 3
      },
      {
        "color": 8,
        "start": 6,
        "length": 1
      },
      {
        "color": 9,
        "start": 7,
        "length": 2
      }
    ],
    "dims": [
      10,
      10
    ]
  },
  "Example 2": {
    "row_segments": [
      {
        "color": 9,
        "start": 0,
        "length": 2
      },
      {
        "color": 8,
        "start": 2,
        "length": 2
      },
      {
        "color": 7,
        "start": 4,
        "length": 2
      },
      {
        "color": 6,
        "start": 6,
        "length": 2
      },
      {
        "color": 5,
        "start": 8,
        "length": 1
      }
    ],
    "col_segments": [
      {
        "color": 9,
        "start": 0,
        "length": 2
      },
      {
        "color": 8,
        "start": 2,
        "length": 2
      },
      {
        "color": 7,
        "start": 4,
        "length": 2
      },
      {
        "color": 6,
        "start": 6,
        "length": 2
      },
      {
        "color": 5,
        "start": 8,
        "length": 1
      }
    ],
    "dims": [
      10,
      10
    ]
  },
  "Example 3": {
    "row_segments": [
      {
        "color": 8,
        "start": 0,
        "length": 2
      },
      {
        "color": 4,
        "start": 2,
        "length": 3
      },
      {
        "color": 5,
        "start": 5,
        "length": 2
      },
      {
        "color": 3,
        "start": 7,
        "length": 2
      }
    ],
    "col_segments": [
      {
        "color": 8,
        "start": 0,
        "length": 3
      },
      {
        "color": 4,
        "start": 3,
        "length": 2
      },
      {
        "color": 5,
        "start": 5,
        "length": 2
      },
      {
        "color": 3,
        "start": 7,
        "length": 2
      }
    ],
    "dims": [
      10,
      10
    ]
  }
}

```
The metrics confirm the analysis:
-   **Examples 1 & 2:** For every row segment (Color C, Start Sr, Len Lr), there is a perfectly corresponding column segment (Color C, Start Sc, Len Lc) where Sr = Sc and Lr = Lc. The drawn shape in the output is a square of size Lr x Lc (which is Lr x Lr) located at (Sr, Sc) (which is (Sr, Sr)).
-   **Example 3:** The correspondence is based *only* on color.
    -   Row segment (Color 8, Start 0, Len 2) matches Column segment (Color 8, Start 0, Len 3). The drawn shape is Color 8, TopLeft (0, 0), Size 3x2 (Height=Len_Col, Width=Len_Row).
    -   Row segment (Color 4, Start 2, Len 3) matches Column segment (Color 4, Start 3, Len 2). The drawn shape is Color 4, TopLeft (3, 2), Size 2x3 (Height=Len_Col, Width=Len_Row).
    -   Row segment (Color 5, Start 5, Len 2) matches Column segment (Color 5, Start 5, Len 2). The drawn shape is Color 5, TopLeft (5, 5), Size 2x2.
    -   Row segment (Color 3, Start 7, Len 2) matches Column segment (Color 3, Start 7, Len 2). The drawn shape is Color 3, TopLeft (7, 7), Size 2x2.

This confirms the refined hypothesis.

## Facts (YAML)


```yaml
task_context:
  description: The task involves drawing colored rectangles onto a background grid based on patterns found in the grid's borders (last row and last column).
  grid_properties:
    - size: Variable (e.g., 10x10 in examples)
    - background_color: 0 (white)
    - borders: The last row and last column of the input grid define both the transformation rules and are preserved in the output grid.

objects:
  - type: border_segment
    location: Last row (excluding last pixel) or last column (excluding last pixel)
    properties:
      - color: The non-background color of the segment (1-9).
      - start_index: The row or column index where the segment begins.
      - length: The number of contiguous pixels in the segment.
    identified_in: Input grid

  - type: drawn_rectangle
    location: Inner area of the grid (excluding last row and column).
    properties:
      - color: Determined by matching border_segments.
      - top_left_corner: (row, column) coordinates. Determined by the start_indices of matching border_segments.
      - height: Determined by the length of the matching column border_segment.
      - width: Determined by the length of the matching row border_segment.
    created_in: Output grid

actions:
  - name: initialize_output
    description: Create an output grid of the same dimensions as the input, filled with the background color (0).

  - name: preserve_borders
    description: Copy the entire last row and entire last column from the input grid to the output grid.

  - name: identify_row_segments
    input: Last row of the input grid (excluding the last pixel).
    output: A list of border_segments found in the row, each with color, start_index, and length.

  - name: identify_col_segments
    input: Last column of the input grid (excluding the last pixel).
    output: A list of border_segments found in the column, each with color, start_index, and length.

  - name: match_and_draw
    description: |
      For each row_segment:
        Find a col_segment with the same color.
        If a match is found:
          Define a drawn_rectangle:
            - color = matched color
            - top_left_corner = (col_segment.start_index, row_segment.start_index)
            - height = col_segment.length
            - width = row_segment.length
          Draw this rectangle onto the output grid, potentially overwriting previous content but not the borders.

  - name: finalize_borders
    description: Re-copy the entire last row and entire last column from the input grid to the output grid to ensure they are not overwritten by the drawing step.

assumptions:
  - Each non-background color present in the last row's segments (excl. corner) will have exactly one corresponding segment of the same color in the last column's segments (excl. corner).
  - The drawing area for rectangles is clipped by the grid boundaries (excluding the last row/column borders).
```


## Natural Language Program

1.  **Initialization:** Create a new grid (`output_grid`) with the same dimensions as the `input_grid`, filled entirely with the background color (0, white).
2.  **Border Preservation (Initial):** Copy the last row and the last column from the `input_grid` directly onto the `output_grid`.
3.  **Identify Row Segments:** Scan the last row of the `input_grid`, from the first column up to (but not including) the last column. Identify all contiguous horizontal segments (blocks) of identical, non-background colors. For each segment, record its color (`Cr`), starting column index (`Sr`), and length (`Lr`).
4.  **Identify Column Segments:** Scan the last column of the `input_grid`, from the first row up to (but not including) the last row. Identify all contiguous vertical segments (blocks) of identical, non-background colors. For each segment, record its color (`Cc`), starting row index (`Sc`), and length (`Lc`).
5.  **Match Segments and Draw Rectangles:**
    a.  Iterate through each identified `row_segment` (`Cr`, `Sr`, `Lr`).
    b.  For the current `row_segment`, find the unique `col_segment` (`Cc`, `Sc`, `Lc`) such that `Cc` equals `Cr`.
    c.  Define the drawing parameters for a rectangle:
        i.  Color: `C = Cr`
        ii. Top row index: `row_start = Sc`
        iii.Bottom row index (exclusive): `row_end = Sc + Lc`
        iv. Left column index: `col_start = Sr`
        v.  Right column index (exclusive): `col_end = Sr + Lr`
    d.  Fill the area `output_grid[row_start : row_end, col_start : col_end]` with the color `C`. Ensure drawing does not go outside the bounds defined by `height-1` and `width-1`.
6.  **Border Preservation (Final):** Re-copy the last row and the last column from the `input_grid` onto the `output_grid`. This step is crucial to correct any pixels in the border area that might have been overwritten during the rectangle drawing process.
7.  **Return:** Return the final `output_grid`.
