
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 2 2 2 8 0 0
0 0 0 8 2 4 2 8 0 0
0 0 0 8 2 2 2 8 0 0
0 0 0 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 8 0 6 1 6 0 8
0 0 0 0 0 0 0 8 6 1 1 1 6 8
0 0 0 0 0 0 0 8 0 6 1 6 0 8
0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples (train_1 and train_2).

**Perception of Task Elements:**

1.  **Input Grid Structure:** Each input grid contains two distinct, non-overlapping objects placed on a white (0) background.
2.  **Object Types:**
    *   One object consistently appears as a "frame" or "hollow shape". In both examples, this frame is made of azure (8) pixels and encloses a rectangular area of the white background.
    *   The other object is a smaller, potentially multi-colored "pattern". In train_1, it's a red (2) cross with a yellow (4) center. In train_2, it's a magenta (6) diamond/cross shape with a blue (1) center.
3.  **Output Grid Structure:** The output grid retains the original positions and shapes of both the "frame" object and the "pattern" object from the input.
4.  **Transformation:** The core transformation is the *copying* of the "pattern" object and *pasting* it into the empty space *inside* the "frame" object.
5.  **Placement/Alignment:** The copied pattern is aligned such that its top-left pixel (relative to its bounding box) is placed at the top-left position of the white space enclosed by the frame. The original background pixels within the frame are replaced by the corresponding pixels of the pattern.

**YAML Facts:**


```yaml
task_description: "Copy a 'pattern' object into the hollow interior of a 'frame' object."

example_train_1:
  input_features:
    - object_id: 1
      type: pattern
      colors: [red, yellow]
      shape_description: "Red cross with yellow center"
      location: top-left area
      bounding_box: &pattern1_bbox # Anchor for reuse
        rows: [1, 3]
        cols: [1, 3]
    - object_id: 2
      type: frame
      colors: [azure]
      shape_description: "Hollow azure rectangle"
      location: bottom-right area
      bounding_box:
        rows: [5, 9]
        cols: [3, 7]
      enclosed_area: # The white space inside the frame
        top_left_coord: &frame1_inner_tl [6, 4]
        rows: [6, 8]
        cols: [4, 6]
  output_features:
    - object_id: 1 # Original pattern remains
      type: pattern
      colors: [red, yellow]
      location: top-left area
    - object_id: 2 # Original frame remains
      type: frame
      colors: [azure]
      location: bottom-right area
    - object_id: 3 # Copied pattern
      type: pattern_copy
      source_object_id: 1
      colors: [red, yellow]
      location: inside frame object (object_id 2)
      placement_rule: "Top-left of pattern bounding box aligned with top-left of frame's enclosed area."
      bounding_box_in_output:
        top_left_coord: *frame1_inner_tl # Use alias
        rows: [6, 8]
        cols: [4, 6]
  actions:
    - action: identify_objects
      inputs: input_grid
      outputs: [pattern_object, frame_object]
      criteria:
        frame: "Contiguous non-background object enclosing a background region."
        pattern: "The other contiguous non-background object."
    - action: locate_regions
      inputs: [pattern_object, frame_object]
      outputs: [pattern_bbox, frame_inner_top_left]
    - action: copy_paste
      inputs: [input_grid, pattern_object, pattern_bbox, frame_inner_top_left]
      outputs: output_grid
      details: "Copy pixels from pattern_object (relative to pattern_bbox top-left) to output_grid (relative to frame_inner_top_left), overwriting the background inside the frame."

example_train_2:
  input_features:
    - object_id: 1
      type: pattern
      colors: [magenta, blue]
      shape_description: "Magenta diamond/cross with blue center"
      location: top-left area
      bounding_box: &pattern2_bbox
        rows: [1, 4]
        cols: [2, 5]
    - object_id: 2
      type: frame
      colors: [azure]
      shape_description: "Hollow azure rectangle"
      location: bottom-right area
      bounding_box:
        rows: [6, 12]
        cols: [7, 13]
      enclosed_area:
        top_left_coord: &frame2_inner_tl [7, 8]
        rows: [7, 11]
        cols: [8, 12]
  output_features:
    - object_id: 1 # Original pattern remains
      type: pattern
      colors: [magenta, blue]
      location: top-left area
    - object_id: 2 # Original frame remains
      type: frame
      colors: [azure]
      location: bottom-right area
    - object_id: 3 # Copied pattern
      type: pattern_copy
      source_object_id: 1
      colors: [magenta, blue]
      location: inside frame object (object_id 2)
      placement_rule: "Top-left of pattern bounding box aligned with top-left of frame's enclosed area."
      bounding_box_in_output:
        top_left_coord: *frame2_inner_tl # Use alias
        rows: [7, 11] # Adjusted based on pattern size
        cols: [8, 11] # Adjusted based on pattern size
  actions: # Actions are conceptually the same as example 1
    - action: identify_objects
    - action: locate_regions
    - action: copy_paste

```


**Natural Language Program:**

1.  Initialize the output grid as a direct copy of the input grid.
2.  Identify all distinct contiguous objects composed of non-background colors (colors 1 through 9) in the input grid. There should be exactly two such objects.
3.  Determine which of these two objects is the 'frame'. The frame object is characterized by completely enclosing a rectangular region consisting only of the background color (white, 0).
4.  Identify the other object as the 'pattern'.
5.  Find the bounding box of the 'pattern' object. Determine its top-left corner coordinates (min_row_pattern, min_col_pattern) and its dimensions (height_pattern, width_pattern).
6.  Find the rectangular region of background color enclosed by the 'frame' object. Determine the top-left coordinates (target_row, target_col) of this enclosed region.
7.  Iterate through each pixel within the bounding box of the 'pattern' object in the input grid. For each pixel at `(r, c)` where `min_row_pattern <= r < min_row_pattern + height_pattern` and `min_col_pattern <= c < min_col_pattern + width_pattern`:
    a.  Get the color `color_pattern` of the pixel `input[r][c]`.
    b.  Calculate the corresponding target coordinates in the output grid: `output_r = target_row + (r - min_row_pattern)` and `output_c = target_col + (c - min_col_pattern)`.
    c.  If the `color_pattern` is *not* the background color (0), update the pixel in the *output grid* at `(output_r, output_c)` with `color_pattern`. (This overwrites the background pixels within the frame's interior).
8.  Return the modified output grid.
```python
import numpy as np
from typing import List, Tuple, Dict, Set

"""
Identify two distinct non-background objects in the input grid.
One object acts as a 'frame', characterized by enclosing a rectangular area of the background color (0).
The other object acts as a 'pattern'.
Copy the 'pattern' object (preserving its shape and colors, ignoring its background pixels) into the background area enclosed by the 'frame' object.
The top-left corner of the pattern's bounding box should align with the top-left corner of the frame's enclosed background area.
The original pattern and frame objects remain in their initial positions in the output.
"""

def find_objects(grid: np.ndarray, background_color: int = 0) -> List[Dict]:
    """
    Finds contiguous objects of non-background colors in the grid.

    Args:
        grid: The input numpy array representing the grid.
        background_color: The integer value representing the background color.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color' (int) and 'pixels' (Set[Tuple[int, int]]).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited.add((r, c))
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append({'color': color, 'pixels': obj_pixels})
                    
    return objects

def get_bounding_box(pixels: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the bounding box of a set of pixels.

    Args:
        pixels: A set of (row, col) tuples.

    Returns:
        A tuple (min_row, min_col, max_row, max_col).
    """
    if not pixels:
        return (0, 0, 0, 0)
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def find_frame_and_pattern(grid: np.ndarray, objects: List[Dict], background_color: int = 0) -> Tuple[Dict, Dict, Tuple[int, int]]:
    """
    Identifies the frame and pattern objects from a list of objects.
    Determines the top-left corner of the background area inside the frame.

    Args:
        grid: The input numpy array representing the grid.
        objects: A list of objects found by find_objects.
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing:
        - The frame object dictionary.
        - The pattern object dictionary.
        - The (row, col) tuple for the top-left corner of the frame's inner area.
        Returns None for any element if identification fails.
    """
    if len(objects) != 2:
        # print(f"Error: Expected 2 objects, found {len(objects)}")
        return None, None, None

    potential_frames = []

    for i, obj in enumerate(objects):
        obj_pixels = obj['pixels']
        min_r, min_c, max_r, max_c = get_bounding_box(obj_pixels)
        
        is_potential_frame = True
        inner_bg_pixels = set()
        
        # Check if the area strictly inside the bounding box contains only background
        # or pixels belonging to the object itself. Must contain at least one background pixel.
        found_inner_bg = False
        if max_r > min_r + 1 and max_c > min_c + 1: # Potential for interior space
             for r in range(min_r + 1, max_r):
                 for c in range(min_c + 1, max_c):
                     if (r, c) not in obj_pixels:
                         if grid[r, c] == background_color:
                             inner_bg_pixels.add((r,c))
                             found_inner_bg = True
                         else:
                             # Found a non-background, non-object pixel inside BB
                             is_potential_frame = False
                             break
                 if not is_potential_frame:
                     break
        else: # Too small to have an interior
            is_potential_frame = False

        # A frame must enclose at least one background pixel
        if is_potential_frame and found_inner_bg:
             # Find the top-left coordinate of the inner background area
            inner_min_r = min(r for r, c in inner_bg_pixels)
            inner_min_c = min(c for r, c in inner_bg_pixels)
            potential_frames.append({'index': i, 'object': obj, 'inner_top_left': (inner_min_r, inner_min_c)})

    if len(potential_frames) == 1:
        frame_info = potential_frames[0]
        frame_object = frame_info['object']
        inner_top_left = frame_info['inner_top_left']
        pattern_object = objects[1 - frame_info['index']] # The other object is the pattern
        return frame_object, pattern_object, inner_top_left
    else:
        # print(f"Error: Found {len(potential_frames)} potential frames, expected 1.")
        # Handle ambiguity or error - perhaps check connectivity of the frame border etc.
        # For this specific task structure, assume exactly one object fits the frame criteria.
         return None, None, None


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by finding a 'frame' object and a 'pattern' object,
    then copying the pattern into the hollow area inside the frame.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    background_color = 0

    # 1. Find all distinct objects
    objects = find_objects(input_np, background_color)
    
    # Ensure exactly two objects are found as per task description
    if len(objects) != 2:
        # print(f"Warning: Expected 2 objects, found {len(objects)}. Returning original grid.")
        return input_grid # Or raise an error, depending on desired behavior

    # 2. Identify the frame and the pattern
    frame_obj, pattern_obj, frame_inner_tl = find_frame_and_pattern(input_np, objects, background_color)

    if frame_obj is None or pattern_obj is None or frame_inner_tl is None:
        # print("Warning: Could not definitively identify frame and pattern. Returning original grid.")
        return input_grid # Identification failed

    # 3. Get bounding box of the pattern
    pattern_pixels = pattern_obj['pixels']
    pat_min_r, pat_min_c, _, _ = get_bounding_box(pattern_pixels)
    
    # 4. Get top-left coordinate of the frame's inner area
    target_r_start, target_c_start = frame_inner_tl

    # 5. Copy pattern pixels into the frame's inner area in the output grid
    for r, c in pattern_pixels:
        # Calculate relative position within the pattern's bounding box
        relative_r = r - pat_min_r
        relative_c = c - pat_min_c
        
        # Calculate target position in the output grid
        target_r = target_r_start + relative_r
        target_c = target_c_start + relative_c
        
        # Get the color of the pattern pixel
        pattern_color = input_np[r, c] # Color is stored in the object, but reading from input ensures consistency

        # Ensure the target position is within the grid bounds (safety check)
        if 0 <= target_r < output_np.shape[0] and 0 <= target_c < output_np.shape[1]:
             # Only copy non-background pixels from the pattern source area
             # Note: find_objects already filters for non-background, but this is explicit
             if pattern_color != background_color:
                 output_np[target_r, target_c] = pattern_color

    # Convert back to list of lists for the required output format
    return output_np.tolist()

```
