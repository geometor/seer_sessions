
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 1 0 0 0 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 7 7 7 7 7 7 7 0 0 1 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 7 7 7 1 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 1 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 0
```

Okay, let's analyze the provided examples.

**Perception of Elements:**

Each task example consists of a single row (1D grid) of pixels.
The key elements appear to be:
1.  A contiguous block of pixels of a single color (red in train_1, orange in train_2, azure in train_3). Let's call this the "main colored block".
2.  Immediately following this main colored block, there are always exactly two white pixels.
3.  Immediately following these two white pixels, there is always a single blue pixel.
4.  The rest of the pixels in the row are white. These can appear before the main colored block and/or after the blue pixel.

The transformation seems to involve rearranging the positions of the main colored block and the two white pixels that follow it. Specifically, the main colored block moves two positions to the right, and the two white pixels shift to occupy the two positions immediately preceding the new location of the main colored block. The blue pixel and all other white pixels (those initially before the main block and those after the blue pixel) remain in their original absolute positions.

**YAML Facts:**


```yaml
Grid:
  Type: 1D array (single row)
  Content: Pixels with colors (0-9)

Objects:
  - Type: Main_Block
    Properties:
      - Color: Any color except white (0) and blue (1)
      - Shape: Contiguous horizontal segment
      - Variable: Color, Length, Start_Position
  - Type: Separator
    Properties:
      - Color: White (0)
      - Shape: Contiguous horizontal segment
      - Fixed: Length (always 2 pixels)
      - Position: Immediately follows Main_Block
  - Type: Marker
    Properties:
      - Color: Blue (1)
      - Shape: Single pixel
      - Fixed: Color
      - Position: Immediately follows Separator
  - Type: Background
    Properties:
      - Color: White (0)
      - Shape: Pixels or contiguous segments
      - Position: Can be before Main_Block and/or after Marker

Relationships:
  - Adjacency: Main_Block -> Separator -> Marker are directly adjacent in sequence in the input.

Transformation:
  - Action: Positional Swap
    - Target1: Main_Block
    - Target2: Separator
    - Rule: The sequence [Main_Block, Separator] in the input becomes [Separator, Main_Block] in the output.
  - Invariance:
    - Background pixels before the original Main_Block maintain their absolute positions.
    - Marker pixel maintains its absolute position.
    - Background pixels after the Marker maintain their absolute positions.
```


**Natural Language Program:**

1.  Identify the single blue pixel (the "Marker"). Note its position.
2.  Identify the two white pixels immediately preceding the Marker (the "Separator").
3.  Identify the contiguous block of non-white, non-blue pixels immediately preceding the Separator (the "Main Block"). Note its color, length, and starting position.
4.  Identify any white pixels preceding the Main Block ("Leading Background") and any white pixels following the Marker ("Trailing Background").
5.  Construct the output row by concatenating the following elements in order:
    a. The Leading Background pixels (if any).
    b. The Separator (two white pixels).
    c. The Main Block (using its original color and length).
    d. The Marker (the blue pixel).
    e. The Trailing Background pixels (if any).
    The resulting row is the output grid.
```python
"""
Identifies a sequence of [Main Block, Separator, Marker] in the input row,
where the Marker is a single blue pixel (1), the Separator is two adjacent
white pixels (0, 0), and the Main Block is a contiguous sequence of identical
pixels (neither white nor blue) preceding the Separator. The transformation
swaps the position of the Main Block and the Separator, keeping all other
pixels (leading white background, the marker, and trailing white background)
in their original absolute positions relative to the grid boundaries.

1. Find the index of the blue pixel (Marker, value 1).
2. Identify the two pixels immediately before the Marker; these are the Separator (value 0, 0).
3. Identify the contiguous block of identical, non-white, non-blue pixels immediately before the Separator; this is the Main Block.
4. Identify any white pixels before the Main Block (Leading Background).
5. Identify any white pixels after the Marker (Trailing Background).
6. Construct the output row by concatenating: Leading Background, Separator, Main Block, Marker, Trailing Background.
"""

import numpy as np
from typing import List

def find_first_occurrence(arr: np.ndarray, value: int) -> int:
    """Finds the index of the first occurrence of a value in a numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) == 0:
        raise ValueError(f"Value {value} not found in the array.")
    return indices[0]

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid by swapping a specific colored block with the
    two white pixels that follow it, keeping a trailing blue marker fixed.
    
    Args:
        input_grid: A list of integers representing the input row.

    Returns:
        A list of integers representing the transformed output row.
    """
    
    # Convert input list to numpy array for easier processing
    input_array = np.array(input_grid)
    
    # --- Locate Key Elements ---
    
    # 1. Find the Marker (blue pixel, value 1)
    try:
        marker_idx = find_first_occurrence(input_array, 1)
    except ValueError:
        # Handle cases where the marker is not found (though expected by examples)
        print("Warning: Blue marker (1) not found in input grid.")
        return input_grid # Return original if pattern not found

    # 2. Identify the Separator (two white pixels before marker)
    # Check if there are enough elements before the marker
    if marker_idx < 2:
        print("Warning: Not enough elements before marker for separator.")
        return input_grid # Pattern not matched
        
    separator_start_idx = marker_idx - 2
    separator_end_idx = marker_idx - 1
    separator = [0, 0] # Expected separator
    
    # Verify the separator pixels are white
    if not np.array_equal(input_array[separator_start_idx : marker_idx], separator):
        print(f"Warning: Expected separator [0, 0] not found at indices {separator_start_idx}, {separator_end_idx}.")
        return input_grid # Pattern not matched

    # 3. Identify the Main Block (contiguous non-white/non-blue block before separator)
    # Check if there's anything before the separator
    if separator_start_idx == 0:
         print("Warning: No elements found before the separator.")
         # This could be valid if the block is meant to be empty, but based on examples,
         # there's always a colored block. Assume pattern mismatch for now.
         return input_grid

    main_block_end_idx = separator_start_idx - 1
    main_block_color = input_array[main_block_end_idx]

    # Check if the block color is valid (not white or blue)
    if main_block_color == 0 or main_block_color == 1:
        print(f"Warning: Invalid color ({main_block_color}) for main block found at index {main_block_end_idx}.")
        return input_grid # Pattern not matched

    # Find the start of the main block by searching backwards
    main_block_start_idx = main_block_end_idx
    while main_block_start_idx > 0 and input_array[main_block_start_idx - 1] == main_block_color:
        main_block_start_idx -= 1
        
    # Extract the main block
    main_block = input_array[main_block_start_idx : main_block_end_idx + 1].tolist()

    # 4. Identify Leading Background (white pixels before Main Block)
    leading_bg = input_array[0 : main_block_start_idx].tolist()
    # Optional: Verify leading background is all white (0)
    # if not all(p == 0 for p in leading_bg):
    #    print("Warning: Non-white pixels found in leading background area.")
        # Decide whether to proceed or return original based on strictness

    # 5. Identify Trailing Background (white pixels after Marker)
    trailing_bg = input_array[marker_idx + 1 :].tolist()
    # Optional: Verify trailing background is all white (0)
    # if not all(p == 0 for p in trailing_bg):
    #    print("Warning: Non-white pixels found in trailing background area.")
        # Decide whether to proceed or return original based on strictness

    # --- Construct Output ---

    # 6. Concatenate elements in the new order
    output_grid_list = leading_bg + separator + main_block + [1] + trailing_bg
    
    return output_grid_list

```
```python
"""
Transforms an input 1D grid (list of integers) based on a specific pattern.
The pattern consists of a contiguous block of identical, non-white/non-blue pixels
("Main Block"), followed immediately by two white pixels ("Separator"), followed
immediately by a single blue pixel ("Marker"). Any white pixels before the Main
Block are "Leading Background", and any white pixels after the Marker are
"Trailing Background".

The transformation swaps the positions of the Main Block and the Separator,
while keeping the Leading Background, Marker, and Trailing Background in their
original absolute positions.

1.  Scan the input row to locate the unique blue pixel (color 1); this is the "Marker". Record its index.
2.  Identify the two pixels immediately preceding the Marker's index. Verify they are both white (color 0); these form the "Separator".
3.  Identify the contiguous block of pixels immediately preceding the Separator. Verify these pixels are all the same color and that the color is *not* white (0) or blue (1). This block is the "Main Block". Record its start index, end index, color, and length.
4.  Identify the sequence of pixels from the start of the row up to (but not including) the start index of the Main Block. This is the "Leading Background".
5.  Identify the sequence of pixels from the index immediately after the Marker to the end of the row. This is the "Trailing Background".
6.  Construct the output row by concatenating the identified components in the following specific order: Leading Background, Separator, Main Block, Marker, Trailing Background.
7.  The resulting concatenated row is the final output grid. If the pattern is not found at any step, the original input grid is returned.
"""

import numpy as np
from typing import List, Optional, Tuple

def find_first_occurrence(arr: np.ndarray, value: int) -> Optional[int]:
    """Finds the index of the first occurrence of a value in a numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) == 0:
        return None # Value not found
    return indices[0]

def find_main_block_before(arr: np.ndarray, end_exclusive_idx: int) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous block of identical, non-white/non-blue pixels
    ending just before the specified index.

    Args:
        arr: The numpy array representing the grid row.
        end_exclusive_idx: The index immediately *after* the desired block.

    Returns:
        A tuple (start_idx, end_idx, color) if found, otherwise None.
        end_idx is inclusive.
    """
    # Check if there's anything before the target index
    if end_exclusive_idx <= 0:
        return None

    main_block_end_idx = end_exclusive_idx - 1
    main_block_color = arr[main_block_end_idx]

    # Check if the block color is valid (not white 0 or blue 1)
    if main_block_color == 0 or main_block_color == 1:
        return None # Invalid color for main block

    # Find the start of the main block by searching backwards
    main_block_start_idx = main_block_end_idx
    while main_block_start_idx > 0 and arr[main_block_start_idx - 1] == main_block_color:
        main_block_start_idx -= 1
        
    return main_block_start_idx, main_block_end_idx, main_block_color


def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A list of integers representing the input row.

    Returns:
        A list of integers representing the transformed output row,
        or the original input_grid if the required pattern is not found.
    """
    
    # Convert input list to numpy array for easier processing
    input_array = np.array(input_grid)
    n = len(input_array)

    # 1. Find the Marker (blue pixel, value 1)
    marker_idx = find_first_occurrence(input_array, 1)
    if marker_idx is None:
        # print("Debug: Marker (1) not found.")
        return input_grid # Pattern not found: No marker

    # 2. Identify and verify the Separator (two white pixels before marker)
    if marker_idx < 2:
        # print(f"Debug: Not enough elements before marker at index {marker_idx} for separator.")
        return input_grid # Pattern not matched: Not enough space for separator
        
    separator_start_idx = marker_idx - 2
    separator_content = [0, 0] # Expected separator
    
    # Verify the separator pixels are white
    if not np.array_equal(input_array[separator_start_idx : marker_idx], separator_content):
        # print(f"Debug: Expected separator [0, 0] not found at indices {separator_start_idx}-{marker_idx-1}.")
        return input_grid # Pattern not matched: Separator content incorrect

    # 3. Identify the Main Block (contiguous non-white/non-blue block before separator)
    block_info = find_main_block_before(input_array, separator_start_idx)
    if block_info is None:
        # print(f"Debug: Main block pattern not found before index {separator_start_idx}.")
        return input_grid # Pattern not matched: Main block requirements not met
        
    main_block_start_idx, main_block_end_idx, _ = block_info
        
    # Extract the main block content
    main_block = input_array[main_block_start_idx : main_block_end_idx + 1].tolist()

    # 4. Identify Leading Background (pixels before Main Block)
    leading_bg = input_array[0 : main_block_start_idx].tolist()
    # Optional check: Verify leading background is all white (0)
    # if not all(p == 0 for p in leading_bg): return input_grid 

    # 5. Identify Trailing Background (pixels after Marker)
    trailing_bg = input_array[marker_idx + 1 :].tolist()
    # Optional check: Verify trailing background is all white (0)
    # if not all(p == 0 for p in trailing_bg): return input_grid

    # 6. Construct Output by concatenating in the new order
    # Order: Leading BG, Separator, Main Block, Marker, Trailing BG
    output_grid_list = leading_bg + separator_content + main_block + [1] + trailing_bg
    
    # 7. Return the result
    return output_grid_list
```
