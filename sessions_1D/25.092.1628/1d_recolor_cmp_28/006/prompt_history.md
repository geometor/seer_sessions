
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
```python
import copy

"""
Identifies all contiguous horizontal segments of yellow (4) pixels within the single-row input grid.
Calculates the length of each segment.
Determines the maximum length found among these yellow segments.
Creates an output grid by copying the input grid.
Modifies the output grid by changing the color of all pixels belonging to yellow segments whose length equals the maximum length to orange (7).
All other pixels (non-yellow or yellow pixels in shorter segments) remain unchanged.
"""

# Define color constants for clarity
YELLOW = 4
ORANGE = 7

def find_yellow_segments(row):
    """
    Finds contiguous segments of yellow (4) pixels in a single row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A list of tuples, where each tuple contains the start index (inclusive),
        end index (exclusive), and length of a yellow segment.
        Returns an empty list if no yellow segments are found.
    """
    segments = []
    start_index = -1
    current_length = 0
    # Iterate through the row with index
    for i, pixel in enumerate(row):
        # Check if the current pixel is yellow
        if pixel == YELLOW:
            # If this is the start of a new segment, record the start index
            if start_index == -1:
                start_index = i
            # Increment the length of the current segment
            current_length += 1
        else:
            # If we were previously tracking a segment (i.e., start_index is not -1),
            # it means the segment has just ended.
            if start_index != -1:
                # Append the found segment's details (start, end, length) to the list
                segments.append((start_index, i, current_length))
                # Reset segment tracking variables
                start_index = -1
                current_length = 0
                
    # After the loop, check if a segment was ongoing until the end of the row
    if start_index != -1:
        # Append the final segment's details
        segments.append((start_index, len(row), current_length))
        
    return segments

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the longest horizontal
    yellow (4) segments to orange (7). Assumes input is a single-row grid.

    Args:
        input_grid: A list of lists representing the input grid (expected to have one row).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Initialize output_grid as a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)

    # Basic validation: Check if the grid is valid (not empty and has at least one row)
    if not output_grid or not output_grid[0]:
        return output_grid # Return the unchanged copy if input is invalid

    # Extract the single row from the grid (we'll modify this row in the copied grid)
    # Since it's a deep copy, modifying output_row modifies output_grid
    output_row = output_grid[0] 

    # Step 1 & 2: Find all yellow segments and their properties (start, end, length)
    yellow_segments = find_yellow_segments(output_row)

    # Step 3: Handle the case where no yellow segments are found
    if not yellow_segments:
        return output_grid # Return the unchanged copy

    # Step 4: Determine the maximum length among all found yellow segments
    max_length = 0
    # Iterate through the lengths of the found segments
    for _, _, length in yellow_segments:
        # Update max_length if the current segment's length is greater
        if length > max_length:
            max_length = length
            
    # If max_length is 0 (only possible if find_yellow_segments returned empty, but safe check)
    if max_length == 0:
         return output_grid # Should not be reached if yellow_segments is not empty

    # Step 5 & 6: Iterate through the identified segments again
    for start, end, length in yellow_segments:
        # Check if the current segment's length is equal to the maximum length
        if length == max_length:
            # Modify the output grid: Change the color of pixels in this segment
            for i in range(start, end):
                # Double-check the pixel is yellow before changing (robustness)
                # Modify the pixel in the output_row (which is part of output_grid)
                if output_row[i] == YELLOW: 
                    output_row[i] = ORANGE 

    # Step 7: Return the modified grid
    return output_grid
```
```python
"""
Identifies all contiguous horizontal segments of yellow (4) pixels within the single-row input grid.
Calculates the length of each segment.
Determines the maximum length found among these yellow segments.
Creates an output grid by copying the input grid.
Modifies the output grid by changing the color of all pixels belonging to yellow segments whose length equals the maximum length to orange (7).
All other pixels (non-yellow or yellow pixels in shorter segments) remain unchanged.
"""

import copy

# Define color constants for clarity
YELLOW = 4
ORANGE = 7
WHITE = 0 # Assuming 0 is the background/separator color

def find_yellow_segments(row):
    """
    Finds contiguous segments of yellow (4) pixels in a single row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A list of tuples, where each tuple contains the start index (inclusive),
        end index (exclusive), and length of a yellow segment.
        Returns an empty list if no yellow segments are found.
    """
    segments = []
    start_index = -1
    current_length = 0
    # Iterate through the row with index
    for i, pixel in enumerate(row):
        # Check if the current pixel is yellow
        if pixel == YELLOW:
            # If this is the start of a new segment, record the start index
            if start_index == -1:
                start_index = i
            # Increment the length of the current segment
            current_length += 1
        else:
            # If we were previously tracking a segment (i.e., start_index is not -1),
            # it means the segment has just ended.
            if start_index != -1:
                # Append the found segment's details (start, end, length) to the list
                segments.append((start_index, i, current_length))
                # Reset segment tracking variables
                start_index = -1
                current_length = 0
                
    # After the loop, check if a segment was ongoing until the end of the row
    if start_index != -1:
        # Append the final segment's details
        segments.append((start_index, len(row), current_length))
        
    return segments

def transform(input_grid):
    # Initialize output_grid as a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)

    # Basic validation: Check if the grid is valid (not empty and has at least one row)
    # Assuming valid inputs based on ARC standard, but good practice.
    if not output_grid or len(output_grid) == 0 or len(output_grid[0]) == 0:
        return output_grid # Return the unchanged copy if input is invalid/empty

    # As per task description, assume input is a single-row grid.
    # Extract the single row we will operate on (from the copied grid).
    output_row = output_grid[0] 
    
    # Find all contiguous horizontal segments of yellow pixels and their lengths
    yellow_segments = find_yellow_segments(output_row)

    # If no yellow segments are found, return the unchanged copy
    if not yellow_segments:
        return output_grid 

    # Determine the maximum length among all found yellow segments
    max_length = 0
    for _, _, length in yellow_segments:
        if length > max_length:
            max_length = length
            
    # If max_length is still 0 (e.g., only non-yellow pixels found, though covered by the 'if not yellow_segments' check)
    if max_length == 0:
         return output_grid 

    # Iterate through the identified segments again
    for start, end, length in yellow_segments:
        # Check if the current segment's length is equal to the maximum length
        if length == max_length:
            # Modify the output grid: Change the color of pixels in this segment
            # Iterate from the start index up to (but not including) the end index
            for i in range(start, end):
                # Change the pixel color in the output row to orange
                # No need to check if it's YELLOW, as find_yellow_segments guarantees it
                output_row[i] = ORANGE 

    # Return the modified grid
    return output_grid
```
