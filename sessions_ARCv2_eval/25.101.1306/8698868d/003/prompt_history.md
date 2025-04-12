
## train_1

**input:**
```
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 1 1 4 8 4 4 4 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 8 1 4 4 4 4 8 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
8 8 8 8 8 8 8 3 3 8 3 8 8 8 8
8 8 8 8 8 8 8 3 8 3 3 8 8 8 8
8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
1 1 1 1 1 1 4 4 4 4 4 4
1 2 2 2 2 1 4 3 3 3 3 4
1 2 1 1 2 1 4 3 3 4 3 4
1 2 1 1 2 1 4 3 4 3 3 4
1 2 2 2 2 1 4 3 3 3 3 4
1 1 1 1 1 1 4 4 4 4 4 4
```


## train_2

**input:**
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2
4 4 2 4 4 2 4 4 3 3 3 3 3 2 3 3 2 2 2 9 9 9 9 9 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 2 4 4 4 4 4 3 3 2 3 3 3 3 3 2 2 2 9 9 9 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 9 9 9 9 9 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 2 8 8 1 1 2 1 1 2 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 2 1 1 2 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 1 1 1 1 1 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
4 9 9 9 9 9 9 4 3 7 7 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 3 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 7 7 7 7 7 3
4 9 9 9 9 4 9 4 3 7 3 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 3 7 7 7 7 3
4 9 9 9 9 9 9 4 3 7 7 7 7 7 7 3
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 1 1 1 1 1 1 8 1 5 5 5 5 5 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 8 8 8 8 1 8 1 5 5 5 5 5 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 1 1 1 1 1 8 1 5 5 5 5 5 5 1
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
```

**Perception of Task Elements:**

1.  **Input Structure:** The input grids contain multiple distinct, solid-colored rectangular objects separated by a background/separator color. Some rectangles may contain internal "noise" pixels of a different color.
2.  **Output Structure:** The output grid is smaller than the input and is composed of arrangements of rectangles derived from the input.
3.  **Key Objects:** The primary objects are the solid-colored rectangles. They appear in two distinct sizes within each input grid. The larger rectangles act as 'frames' and the smaller ones provide the 'content'.
4.  **Background/Separators:** A specific color acts as a separator between the key rectangular objects (azure=8 in train\_1, red=2 in train\_2). This separator color does not appear in the output.
5.  **Noise:** Some rectangles in the input contain pixels of a different color internally. This internal noise seems irrelevant to the transformation and is discarded or overwritten in the output.
6.  **Transformation:** The core transformation involves pairing the larger 'frame' rectangles with the smaller 'content' rectangles based on their appearance order (top-to-bottom, left-to-right). The output grid is constructed by taking the border of each frame rectangle and filling its interior with the interior pattern of the corresponding content rectangle. The relative positions of the frame rectangles are preserved in the output grid layout.

**YAML Facts:**


```yaml
Observations:
  - Input grids contain distinct rectangular objects.
  - A separator color divides these objects (azure=8 in train_1, red=2 in train_2).
  - Rectangles appear in two sizes per input: Larger ('frames') and Smaller ('contents').
  - Frame dimensions are exactly 2 units larger than content dimensions (e.g., 6x6 vs 4x4, 8x8 vs 6x6).
  - Some input rectangles contain internal 'noise' pixels which are ignored.
  - Output grids are composed of modified frame rectangles arranged based on their original relative positions.
  - The separator color and surrounding grid space are discarded.
Properties:
  - Objects: Rectangles.
  - Properties: Color, Size (Height, Width), Position (Top-left corner), Type ('frame' or 'content').
  - Relationships:
      - Frames are larger than contents.
      - A one-to-one mapping exists between frames and contents based on reading order.
      - Output layout preserves the relative spatial arrangement of input frames.
Actions:
  - Identify the separator color.
  - Find all non-separator colored rectangles.
  - Categorize rectangles into 'frame' (larger) and 'content' (smaller) groups.
  - Sort frames by reading order (top-left corner).
  - Sort contents by reading order (top-left corner).
  - Pair frames and contents based on sorted order.
  - For each pair:
      - Extract the 1-pixel border from the frame rectangle.
      - Extract the inner core (removing the 1-pixel border) from the content rectangle.
      - Create a new rectangle using the frame's border and the content's core.
  - Assemble these new rectangles into the output grid, maintaining the relative layout of the original frames.
```


**Natural Language Program:**

1.  Identify the separator color, which is the color filling the space between the main rectangular objects (e.g., azure in example 1, red in example 2).
2.  Scan the input grid to find all maximal contiguous rectangular blocks of uniform color, excluding the separator color.
3.  Group these rectangles based on their size. Identify two distinct size categories: larger rectangles ('frames') and smaller rectangles ('contents'). The frame rectangles will be exactly 2 pixels taller and 2 pixels wider than the content rectangles.
4.  Create an ordered list of frame rectangles by sorting them based on their top-left corner coordinates (first by row index, then by column index).
5.  Create a similarly ordered list of content rectangles.
6.  Determine the relative spatial arrangement of the frame rectangles (e.g., side-by-side, 2x2 grid). This defines the layout of the output grid.
7.  Initialize an empty output grid sized to fit the arrangement of frame rectangles.
8.  Iterate through the ordered lists, pairing the i-th frame rectangle with the i-th content rectangle.
9.  For each pair:
    a.  Define the area corresponding to the frame rectangle's position within the output grid.
    b.  Copy the 1-pixel thick border pixels from the frame rectangle to the corresponding border positions in the output grid area.
    c.  Extract the inner core of the content rectangle (i.e., the content rectangle excluding its 1-pixel border).
    d.  Copy this inner core pattern into the interior area (inside the border) of the frame's position in the output grid.
10. Return the completed output grid.
```python
import numpy as np
from collections import defaultdict, deque

"""
Identifies 'frame' and 'content' rectangular blocks separated by a background color 
in the input grid. The background/separator color is identified as the color 
adjacent to the most diverse set of other colors. The 'frame' blocks are larger 
than the 'content' blocks, typically by 2 units in height and width. 
The transformation constructs an output grid by preserving the relative arrangement 
of the frame blocks. For each frame block, its 1-pixel border is drawn in the output. 
The interior area of the frame in the output is then filled with the pattern found 
in the interior (excluding the 1-pixel border) of the corresponding 'content' block 
from the input grid. Frame and content blocks are paired based on their reading order 
(top-to-bottom, left-to-right).
"""

def get_separator_color(grid: np.ndarray) -> int:
    """
    Identifies the separator color in the grid.
    The separator is assumed to be the color that has the highest number of
    distinct neighboring colors (adjacency diversity). Ties are broken by
    choosing the most frequent color among the candidates with max diversity.
    As a fallback, returns the most frequent color in the grid.
    """
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return 0 # Default for empty grid (white)
        
    neighbor_colors = defaultdict(set)

    # Iterate through grid to find distinct neighbors for each color
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    # Check bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                         neighbor_color = grid[nr, nc]
                         # Add neighbor color if it's different from the cell color
                         if neighbor_color != color:
                             neighbor_colors[color].add(neighbor_color)

    max_diversity = -1
    candidate_separators = []

    # Find the colors with the maximum number of distinct neighbor colors
    for color, neighbors in neighbor_colors.items():
         num_distinct_neighbors = len(neighbors)
         if num_distinct_neighbors > max_diversity:
             max_diversity = num_distinct_neighbors
             candidate_separators = [color] # New maximum found
         elif num_distinct_neighbors == max_diversity:
             candidate_separators.append(color) # Add to candidates with same max diversity

    separator_color = -1
    if len(candidate_separators) == 1:
        # Only one color has the maximum diversity
        separator_color = candidate_separators[0]
    elif len(candidate_separators) > 1:
        # Tie-breaking: Choose the most frequent color among the candidates
        counts = defaultdict(int)
        grid_flat = grid.flatten()
        for pixel_color in grid_flat:
            if pixel_color in candidate_separators:
                counts[pixel_color] += 1
        # Find the color with the max count among candidates
        if counts:
            separator_color = max(counts, key=counts.get)
        else: # Should not happen if candidates exist, but as safety:
            separator_color = candidate_separators[0] 
            
    else: 
         # Fallback: If no diversity found (e.g., solid grid) or other issue
         # guess the most frequent color overall as the separator (less reliable)
        unique_colors, counts = np.unique(grid, return_counts=True)
        if len(counts) > 0:
             separator_color = unique_colors[np.argmax(counts)]
        else:
             separator_color = 0 # Default white for empty grid

    # Ensure a valid color (>= 0) is returned
    if separator_color < 0:
        separator_color = 0

    return separator_color

def find_color_blocks(grid: np.ndarray) -> list[dict]:
    """ 
    Finds all contiguous blocks of the same color using BFS.
    Returns a list of dictionaries, each describing a block: its color,
    bounding box (top, left, bottom, right - inclusive), height, width, 
    and pixel count.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    for r in range(rows):
        for c in range(cols):
             # If cell hasn't been visited yet, start a new block search
             if not visited[r,c]:
                color = grid[r,c]
                q = deque([(r,c)])
                visited[r,c] = True
                pixels = set([(r,c)])
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                # BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    # Update bounding box
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visit status, and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            pixels.add((nr, nc))
                            q.append((nr, nc))
                            
                # Calculate block properties
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                # Store block information
                blocks.append({
                    'color': color,
                    'bounds': (min_r, min_c, max_r, max_c), # top, left, bottom, right (inclusive)
                    'height': height,
                    'width': width,
                    'pixel_count': len(pixels),
                })
    return blocks


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules derived from the examples.
    1. Identifies the separator color.
    2. Finds all contiguous blocks of non-separator colors.
    3. Categorizes blocks into 'frames' (larger) and 'contents' (smaller) based on size,
       preferring pairs where frame_size = content_size + (2, 2).
    4. Sorts frames and contents by reading order.
    5. Constructs the output grid by placing frame borders and content cores according
       to the relative positions of the frames.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return [] # Handle empty input

    # 1. Identify the separator color
    separator_color = get_separator_color(grid)

    # 2. Find all contiguous blocks of solid color
    all_blocks = find_color_blocks(grid)
    
    # 3. Filter out blocks that match the identified separator color
    object_blocks = [b for b in all_blocks if b['color'] != separator_color]
    if not object_blocks:
        return [] # No objects found besides separator

    # 4. Categorize remaining blocks into 'frame' and 'content' based on size
    sizes = defaultdict(list)
    for block in object_blocks:
        # Group blocks by their bounding box dimensions (height, width)
        sizes[(block['height'], block['width'])].append(block)

    frame_size = None
    content_size = None

    # Try to identify frame/content pair based on size relationship (frame = content + 2)
    possible_pairs = []
    sorted_size_keys = sorted(sizes.keys(), key=lambda x: x[0]*x[1], reverse=True) # Sort by area
    for i in range(len(sorted_size_keys)):
        for j in range(len(sorted_size_keys)): # Check all pairs, not just i+1
             if i == j: continue
             s_large = sorted_size_keys[i]
             s_small = sorted_size_keys[j]
             # Check if larger size is exactly 2 units bigger in height and width
             if s_large[0] == s_small[0] + 2 and s_large[1] == s_small[1] + 2:
                  # Check if number of blocks matches for this pair
                  if len(sizes[s_large]) == len(sizes[s_small]):
                      possible_pairs.append({'frame': s_large, 'content': s_small})

    if len(possible_pairs) == 1:
        # Found exactly one pair matching the rule and count
        frame_size = possible_pairs[0]['frame']
        content_size = possible_pairs[0]['content']
    elif len(sizes) >= 2:
         # Fallback: If multiple pairs match or no pair matches rule exactly,
         # assume the most frequent largest size is frame, most frequent second largest is content.
         # Or simply the largest two sizes if counts are equal.
         if len(sorted_size_keys) >= 2:
            frame_size = sorted_size_keys[0]
            content_size = sorted_size_keys[1]
            # Optional: Add check len(sizes[frame_size]) == len(sizes[content_size])
            if len(sizes.get(frame_size,[])) != len(sizes.get(content_size,[])):
                 # Counts don't match, indicates ambiguity
                 return input_grid # Return original grid on failure
    else:
        # Cannot determine frame/content sizes reliably
        return input_grid # Return original grid on failure

    # Ensure sizes were determined
    if frame_size is None or content_size is None:
         return input_grid # Return original grid on failure

    frames = sizes.get(frame_size, [])
    contents = sizes.get(content_size, [])

    # 5. Sort frames and contents by reading order (top-left corner: row, then column)
    frames.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))
    contents.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))

    # Check for equal number of frames and contents after sorting
    if len(frames) != len(contents):
         return input_grid # Error: Mismatch after filtering/sorting
    if not frames:
        return [] # No valid frame/content pairs found

    # 6. Determine output grid layout and size based on frame positions
    min_frame_top = min(f['bounds'][0] for f in frames)
    min_frame_left = min(f['bounds'][1] for f in frames)
    # Calculate max bottom/right coordinates using frame_size for dimensions
    max_frame_bottom_coord = max(f['bounds'][0] + frame_size[0] - 1 for f in frames)
    max_frame_right_coord = max(f['bounds'][1] + frame_size[1] - 1 for f in frames)

    # Calculate output grid dimensions
    output_height = max_frame_bottom_coord - min_frame_top + 1
    output_width = max_frame_right_coord - min_frame_left + 1
    
    # Check for non-positive dimensions
    if output_height <= 0 or output_width <= 0:
        return []

    # 7. Initialize output grid (fill with white=0 by default)
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 8. Assemble the output grid by combining frame borders and content cores
    for frame, content in zip(frames, contents):
        f_top, f_left, _, _ = frame['bounds'] # Frame top-left for positioning
        c_top, c_left, c_bottom, c_right = content['bounds'] # Content bounds for core extraction
        
        frame_h, frame_w = frame_size # Use determined consistent frame size
        content_h, content_w = content_size # Use determined consistent content size

        # Calculate position in output grid based on frame's top-left relative to min top-left
        out_r_start = f_top - min_frame_top
        out_c_start = f_left - min_frame_left
        out_r_end = out_r_start + frame_h # Exclusive index for slicing end
        out_c_end = out_c_start + frame_w # Exclusive index for slicing end

        # Frame color is the color of the contiguous block found
        frame_color = frame['color'] 

        # Draw frame border onto output grid if within bounds
        if 0 <= out_r_start < output_height and 0 <= out_c_start < output_width and \
           out_r_end <= output_height and out_c_end <= output_width:
            output_grid[out_r_start, out_c_start:out_c_end] = frame_color       # Top border
            output_grid[out_r_end - 1, out_c_start:out_c_end] = frame_color     # Bottom border
            output_grid[out_r_start:out_r_end, out_c_start] = frame_color       # Left border
            output_grid[out_r_start:out_r_end, out_c_end - 1] = frame_color     # Right border
        else:
            continue # Skip this frame if it doesn't fit

        # Extract content inner core from the *input* grid using content bounds
        core_r_start_in = c_top + 1
        core_r_end_in = c_bottom # Inclusive bound from find_color_blocks
        core_c_start_in = c_left + 1
        core_c_end_in = c_right # Inclusive bound from find_color_blocks

        # Calculate expected core dimensions based on content_size
        expected_core_h = content_h - 2
        expected_core_w = content_w - 2
        
        # Check if core dimensions are valid and extract
        if expected_core_h > 0 and expected_core_w > 0 and \
           core_r_end_in >= core_r_start_in and core_c_end_in >= core_c_start_in:
            
            # Slice using numpy: end index is exclusive, so add 1 to inclusive bounds
            content_core = grid[core_r_start_in : core_r_end_in + 1, core_c_start_in : core_c_end_in + 1]
            actual_core_h, actual_core_w = content_core.shape
            
            # Place content core into the output grid's inner area
            # Destination indices within the output grid
            out_core_r_start = out_r_start + 1
            out_core_c_start = out_c_start + 1
            out_core_r_end = out_core_r_start + actual_core_h # Exclusive end
            out_core_c_end = out_core_c_start + actual_core_w # Exclusive end
            
            # Final check: ensure extracted core size matches expected size and fits within frame border
            if actual_core_h == expected_core_h and actual_core_w == expected_core_w and \
               out_core_r_end <= (out_r_start + frame_h -1) and \
               out_core_c_end <= (out_c_start + frame_w -1) and \
               out_core_r_start < output_height and out_core_c_start < output_width: # Check placement start is valid
                 output_grid[out_core_r_start : out_core_r_end, out_core_c_start : out_core_c_end] = content_core
            # else: Core size mismatch or doesn't fit, leave the default background (0)

    # 9. Return the final grid as list of lists
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from collections import defaultdict, deque

"""
Identifies 'frame' and 'content' rectangular blocks separated by a background color 
in the input grid. The background/separator color is identified as the color 
adjacent to the most diverse set of other colors. The 'frame' blocks are larger 
than the 'content' blocks, typically by 2 units in height and width. 
The transformation constructs an output grid by preserving the relative arrangement 
of the frame blocks. For each frame block, its 1-pixel border is drawn in the output. 
The interior area of the frame in the output is then filled with the pattern found 
in the interior (excluding the 1-pixel border) of the corresponding 'content' block 
from the input grid. Frame and content blocks are paired based on their reading order 
(top-to-bottom, left-to-right).
"""

def get_separator_color(grid: np.ndarray) -> int:
    """
    Identifies the separator color in the grid.
    The separator is assumed to be the color that has the highest number of
    distinct neighboring colors (adjacency diversity). Ties are broken by
    choosing the most frequent color among the candidates with max diversity.
    As a fallback, returns the most frequent color in the grid.
    """
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return 0 # Default for empty grid (white)
        
    neighbor_colors = defaultdict(set)

    # Iterate through grid to find distinct neighbors for each color
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    # Check bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                         neighbor_color = grid[nr, nc]
                         # Add neighbor color if it's different from the cell color
                         if neighbor_color != color:
                             neighbor_colors[color].add(neighbor_color)

    max_diversity = -1
    candidate_separators = []

    # Find the colors with the maximum number of distinct neighbor colors
    for color, neighbors in neighbor_colors.items():
         num_distinct_neighbors = len(neighbors)
         if num_distinct_neighbors > max_diversity:
             max_diversity = num_distinct_neighbors
             candidate_separators = [color] # New maximum found
         elif num_distinct_neighbors == max_diversity:
             candidate_separators.append(color) # Add to candidates with same max diversity

    separator_color = -1
    if len(candidate_separators) == 1:
        # Only one color has the maximum diversity
        separator_color = candidate_separators[0]
    elif len(candidate_separators) > 1:
        # Tie-breaking: Choose the most frequent color among the candidates
        counts = defaultdict(int)
        grid_flat = grid.flatten()
        for pixel_color in grid_flat:
            if pixel_color in candidate_separators:
                counts[pixel_color] += 1
        # Find the color with the max count among candidates
        if counts:
            separator_color = max(counts, key=counts.get)
        else: # Should not happen if candidates exist, but as safety:
            separator_color = candidate_separators[0] 
            
    else: 
         # Fallback: If no diversity found (e.g., solid grid) or other issue
         # guess the most frequent color overall as the separator (less reliable)
        unique_colors, counts = np.unique(grid, return_counts=True)
        if len(counts) > 0:
             separator_color = unique_colors[np.argmax(counts)]
        else:
             separator_color = 0 # Default white for empty grid

    # Ensure a valid color (>= 0) is returned
    if separator_color < 0:
        separator_color = 0

    return separator_color

def find_color_blocks(grid: np.ndarray) -> list[dict]:
    """ 
    Finds all contiguous blocks of the same color using BFS.
    Returns a list of dictionaries, each describing a block: its color,
    bounding box (top, left, bottom, right - inclusive), height, width, 
    and pixel count.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    for r in range(rows):
        for c in range(cols):
             # If cell hasn't been visited yet, start a new block search
             if not visited[r,c]:
                color = grid[r,c]
                q = deque([(r,c)])
                visited[r,c] = True
                pixels = set([(r,c)])
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                # BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    # Update bounding box
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visit status, and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            pixels.add((nr, nc))
                            q.append((nr, nc))
                            
                # Calculate block properties
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                # Store block information
                blocks.append({
                    'color': color,
                    'bounds': (min_r, min_c, max_r, max_c), # top, left, bottom, right (inclusive)
                    'height': height,
                    'width': width,
                    'pixel_count': len(pixels),
                })
    return blocks


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules derived from the examples.
    1. Identifies the separator color.
    2. Finds all contiguous blocks of non-separator colors.
    3. Categorizes blocks into 'frames' (larger) and 'contents' (smaller) based on size,
       preferring pairs where frame_size = content_size + (2, 2).
    4. Sorts frames and contents by reading order.
    5. Constructs the output grid by placing frame borders and content cores according
       to the relative positions of the frames.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return [] # Handle empty input

    # 1. Identify the separator color
    separator_color = get_separator_color(grid)

    # 2. Find all contiguous blocks of solid color
    all_blocks = find_color_blocks(grid)
    
    # 3. Filter out blocks that match the identified separator color
    object_blocks = [b for b in all_blocks if b['color'] != separator_color]
    if not object_blocks:
        return [] # No objects found besides separator

    # 4. Categorize remaining blocks into 'frame' and 'content' based on size
    sizes = defaultdict(list)
    for block in object_blocks:
        # Group blocks by their bounding box dimensions (height, width)
        sizes[(block['height'], block['width'])].append(block)

    frame_size = None
    content_size = None

    # Try to identify frame/content pair based on size relationship (frame = content + 2)
    possible_pairs = []
    sorted_size_keys = sorted(sizes.keys(), key=lambda x: x[0]*x[1], reverse=True) # Sort by area
    for i in range(len(sorted_size_keys)):
        for j in range(len(sorted_size_keys)): # Check all pairs, not just i+1
             if i == j: continue
             s_large = sorted_size_keys[i]
             s_small = sorted_size_keys[j]
             # Check if larger size is exactly 2 units bigger in height and width
             if s_large[0] == s_small[0] + 2 and s_large[1] == s_small[1] + 2:
                  # Check if number of blocks matches for this pair
                  if len(sizes[s_large]) == len(sizes[s_small]):
                      possible_pairs.append({'frame': s_large, 'content': s_small})

    if len(possible_pairs) == 1:
        # Found exactly one pair matching the rule and count
        frame_size = possible_pairs[0]['frame']
        content_size = possible_pairs[0]['content']
    elif len(sizes) >= 2:
         # Fallback: If multiple pairs match or no pair matches rule exactly,
         # assume the most frequent largest size is frame, most frequent second largest is content.
         # Or simply the largest two sizes if counts are equal.
         if len(sorted_size_keys) >= 2:
            frame_size = sorted_size_keys[0]
            content_size = sorted_size_keys[1]
            # Optional: Add check len(sizes[frame_size]) == len(sizes[content_size])
            if len(sizes.get(frame_size,[])) != len(sizes.get(content_size,[])):
                 # Counts don't match, indicates ambiguity
                 return input_grid # Return original grid on failure
    else:
        # Cannot determine frame/content sizes reliably
        return input_grid # Return original grid on failure

    # Ensure sizes were determined
    if frame_size is None or content_size is None:
         return input_grid # Return original grid on failure

    frames = sizes.get(frame_size, [])
    contents = sizes.get(content_size, [])

    # 5. Sort frames and contents by reading order (top-left corner: row, then column)
    frames.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))
    contents.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))

    # Check for equal number of frames and contents after sorting
    if len(frames) != len(contents):
         return input_grid # Error: Mismatch after filtering/sorting
    if not frames:
        return [] # No valid frame/content pairs found

    # 6. Determine output grid layout and size based on frame positions
    min_frame_top = min(f['bounds'][0] for f in frames)
    min_frame_left = min(f['bounds'][1] for f in frames)
    # Calculate max bottom/right coordinates using frame_size for dimensions
    max_frame_bottom_coord = max(f['bounds'][0] + frame_size[0] - 1 for f in frames)
    max_frame_right_coord = max(f['bounds'][1] + frame_size[1] - 1 for f in frames)

    # Calculate output grid dimensions
    output_height = max_frame_bottom_coord - min_frame_top + 1
    output_width = max_frame_right_coord - min_frame_left + 1
    
    # Check for non-positive dimensions
    if output_height <= 0 or output_width <= 0:
        return []

    # 7. Initialize output grid (fill with white=0 by default)
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 8. Assemble the output grid by combining frame borders and content cores
    for frame, content in zip(frames, contents):
        f_top, f_left, _, _ = frame['bounds'] # Frame top-left for positioning
        c_top, c_left, c_bottom, c_right = content['bounds'] # Content bounds for core extraction
        
        frame_h, frame_w = frame_size # Use determined consistent frame size
        content_h, content_w = content_size # Use determined consistent content size

        # Calculate position in output grid based on frame's top-left relative to min top-left
        out_r_start = f_top - min_frame_top
        out_c_start = f_left - min_frame_left
        out_r_end = out_r_start + frame_h # Exclusive index for slicing end
        out_c_end = out_c_start + frame_w # Exclusive index for slicing end

        # Frame color is the color of the contiguous block found
        frame_color = frame['color'] 

        # Draw frame border onto output grid if within bounds
        if 0 <= out_r_start < output_height and 0 <= out_c_start < output_width and \
           out_r_end <= output_height and out_c_end <= output_width:
            output_grid[out_r_start, out_c_start:out_c_end] = frame_color       # Top border
            output_grid[out_r_end - 1, out_c_start:out_c_end] = frame_color     # Bottom border
            output_grid[out_r_start:out_r_end, out_c_start] = frame_color       # Left border
            output_grid[out_r_start:out_r_end, out_c_end - 1] = frame_color     # Right border
        else:
            continue # Skip this frame if it doesn't fit

        # Extract content inner core from the *input* grid using content bounds
        core_r_start_in = c_top + 1
        core_r_end_in = c_bottom # Inclusive bound from find_color_blocks
        core_c_start_in = c_left + 1
        core_c_end_in = c_right # Inclusive bound from find_color_blocks

        # Calculate expected core dimensions based on content_size
        expected_core_h = content_h - 2
        expected_core_w = content_w - 2
        
        # Check if core dimensions are valid and extract
        if expected_core_h > 0 and expected_core_w > 0 and \
           core_r_end_in >= core_r_start_in and core_c_end_in >= core_c_start_in:
            
            # Slice using numpy: end index is exclusive, so add 1 to inclusive bounds
            content_core = grid[core_r_start_in : core_r_end_in + 1, core_c_start_in : core_c_end_in + 1]
            actual_core_h, actual_core_w = content_core.shape
            
            # Place content core into the output grid's inner area
            # Destination indices within the output grid
            out_core_r_start = out_r_start + 1
            out_core_c_start = out_c_start + 1
            out_core_r_end = out_core_r_start + actual_core_h # Exclusive end
            out_core_c_end = out_core_c_start + actual_core_w # Exclusive end
            
            # Final check: ensure extracted core size matches expected size and fits within frame border
            if actual_core_h == expected_core_h and actual_core_w == expected_core_w and \
               out_core_r_end <= (out_r_start + frame_h -1) and \
               out_core_c_end <= (out_c_start + frame_w -1) and \
               out_core_r_start < output_height and out_core_c_start < output_width: # Check placement start is valid
                 output_grid[out_core_r_start : out_core_r_end, out_core_c_start : out_core_c_end] = content_core
            # else: Core size mismatch or doesn't fit, leave the default background (0)

    # 9. Return the final grid as list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 1 1 4 8 4 4 4 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 8 1 4 4 4 4 8 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
8 8 8 8 8 8 8 3 3 8 3 8 8 8 8
8 8 8 8 8 8 8 3 8 3 3 8 8 8 8
8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
1 1 1 1 1 1 4 4 4 4 4 4
1 2 2 2 2 1 4 3 3 3 3 4
1 2 1 1 2 1 4 3 3 4 3 4
1 2 1 1 2 1 4 3 4 3 3 4
1 2 2 2 2 1 4 3 3 3 3 4
1 1 1 1 1 1 4 4 4 4 4 4
```
Transformed Output:
```
1 1 1 1 1 1 4 4 4 4 4 4
1 0 0 0 0 1 4 0 0 0 0 4
1 0 0 0 0 1 4 0 0 0 0 4
1 0 0 0 0 1 4 0 0 0 0 4
1 0 0 0 0 1 4 0 0 0 0 4
1 1 1 1 1 1 4 4 4 4 4 4
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 177.77777777777777

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2
4 4 2 4 4 2 4 4 3 3 3 3 3 2 3 3 2 2 2 9 9 9 9 9 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 2 4 4 4 4 4 3 3 2 3 3 3 3 3 2 2 2 9 9 9 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 9 9 9 9 9 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 2 8 8 1 1 2 1 1 2 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 2 1 1 2 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 1 1 1 1 1 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
4 9 9 9 9 9 9 4 3 7 7 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 3 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 7 7 7 7 7 3
4 9 9 9 9 4 9 4 3 7 3 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 3 7 7 7 7 3
4 9 9 9 9 9 9 4 3 7 7 7 7 7 7 3
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 1 1 1 1 1 1 8 1 5 5 5 5 5 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 8 8 8 8 1 8 1 5 5 5 5 5 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 1 1 1 1 1 8 1 5 5 5 5 5 5 1
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
```
Transformed Output:
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
4 0 0 0 0 0 0 4 3 0 0 0 0 0 0 3
4 0 0 0 0 0 0 4 3 0 0 0 0 0 0 3
4 0 0 0 0 0 0 4 3 0 0 0 0 0 0 3
4 0 0 0 0 0 0 4 3 0 0 0 0 0 0 3
4 0 0 0 0 0 0 4 3 0 0 0 0 0 0 3
4 0 0 0 0 0 0 4 3 0 0 0 0 0 0 3
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 0 0 0 0 0 0 8 1 0 0 0 0 0 0 1
8 0 0 0 0 0 0 8 1 0 0 0 0 0 0 1
8 0 0 0 0 0 0 8 1 0 0 0 0 0 0 1
8 0 0 0 0 0 0 8 1 0 0 0 0 0 0 1
8 0 0 0 0 0 0 8 1 0 0 0 0 0 0 1
8 0 0 0 0 0 0 8 1 0 0 0 0 0 0 1
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 144
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 225.0
**General Assessment:**

The initial code correctly identified the core components: separator color, frame blocks (larger rectangles), and content blocks (smaller rectangles, exactly 2 units smaller in height/width). It also correctly determined the output grid structure based on the relative positions of the frame blocks and applied the frame borders.

The primary failure occurred in generating the *interior* of the frames in the output. The code attempted a direct copy of the pixels found within the bounding box of the content block (minus its border), resulting in incorrect patterns (often filled with the default background color '0' in the failed examples).

The analysis reveals a more complex transformation for the interior:
1.  **Pattern Source:** The pattern originates from the pixels within the bounding box of the identified content block (size N-2 x N-2).
2.  **Color Mapping Rule:** The output core pixels are determined by mapping the colors from the content pattern source. The most likely rule (based on 7/8 successful pair transformations across both examples) is:
    *   If the pattern source pixel is the `Separator Color`, the output pixel becomes the `Frame Color`.
    *   Otherwise (if the pattern source pixel is the `Content Color` or any other `Noise Color` *except* the separator), the output pixel becomes the `Content Color` (defined as the dominant non-separator color within the pattern source block).
3.  **Pairing:** While simple reading order (top-to-bottom, left-to-right) for both frames and content blocks worked for `train_1`, it failed for `train_2`. `train_2` required a specific pairing: Frame1->Content1, Frame2->Content4, Frame3->Content3, Frame4->Content2 (using reading-order indices). The logic behind this specific pairing in `train_2` is not immediately obvious (neither simple reading order, quadrant mapping, nor proximity worked consistently) and might require further examples or insight. However, the pattern transformation rule itself seems consistent once the correct pairs are established.

**Strategy:**

1.  Modify the code to implement the Color Mapping Rule described above for generating the output core.
2.  Refine the process of determining the `Content Color` for the rule (e.g., use the mode of non-separator colors in the pattern source block).
3.  Address the pairing issue. Implement the simple reading order pairing as a default, but note its failure in `train_2` and the specific pairing required there. A more robust solution might involve trying different pairing strategies or finding a consistent underlying logic. For now, the focus will be on correcting the core generation logic, assuming correct pairing can be determined.

**Metrics:**


*code_execution:*
```python
import numpy as np

def analyze_example(input_grid_list, expected_output_list, transformed_output_list):
    input_grid = np.array(input_grid_list)
    expected_output = np.array(expected_output_list)
    transformed_output = np.array(transformed_output_list)

    metrics = {}
    metrics['input_dims'] = input_grid.shape
    metrics['expected_output_dims'] = expected_output.shape

    if transformed_output.size == 0:
        metrics['transformed_output_dims'] = (0, 0)
        metrics['size_match'] = False
        metrics['pixel_diff'] = expected_output.size
        metrics['palette_match'] = False
    else:
        metrics['transformed_output_dims'] = transformed_output.shape
        metrics['size_match'] = (expected_output.shape == transformed_output.shape)
        if metrics['size_match']:
            metrics['pixel_diff'] = int(np.sum(expected_output != transformed_output))
            metrics['palette_match'] = set(np.unique(expected_output)) == set(np.unique(transformed_output))
        else:
            # Cannot compare pixels if sizes differ
            metrics['pixel_diff'] = None # Or some indicator of size mismatch
            metrics['palette_match'] = False # Palettes can't match if shapes differ fundamentally

    # Placeholder for separator color identified by the previous code (assuming it was consistent)
    # This would require running the 'get_separator_color' part of the original code
    # For now, manually note based on description: 8 for ex1, 2 for ex2
    metrics['identified_separator'] = None # Needs code execution context

    # Placeholder for frame/content info (also needs code execution context)
    metrics['identified_frame_size'] = None
    metrics['identified_content_size'] = None
    metrics['num_pairs'] = None

    return metrics

# Example 1 Data
input_1 = [
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 8, 8, 8],
    [1, 1, 1, 1, 1, 1, 4, 8, 4, 4, 4, 4, 8, 8, 8],
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 8, 8, 8],
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 8, 8, 8],
    [1, 1, 1, 1, 8, 1, 4, 4, 4, 4, 8, 4, 8, 8, 8],
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 2, 2, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 2, 8, 8, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 2, 8, 8, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 2, 2, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 3, 3, 3, 3, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 3, 3, 8, 3, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 3, 8, 3, 3, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 3, 3, 3, 3, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
]
expected_1 = [
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4],
    [1, 2, 2, 2, 2, 1, 4, 3, 3, 3, 3, 4],
    [1, 2, 1, 1, 2, 1, 4, 3, 3, 4, 3, 4],
    [1, 2, 1, 1, 2, 1, 4, 3, 4, 3, 3, 4],
    [1, 2, 2, 2, 2, 1, 4, 3, 3, 3, 3, 4],
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4]
]
transformed_1 = [
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4],
    [1, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 4],
    [1, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 4],
    [1, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 4],
    [1, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 4],
    [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4]
]

# Example 2 Data
input_2 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [4, 4, 2, 4, 4, 2, 4, 4, 3, 3, 3, 3, 3, 2, 3, 3, 2, 2, 2, 9, 9, 9, 9, 9, 9, 2, 2, 2, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 9, 2, 2, 9, 2, 9, 2, 2, 2, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 9, 2, 2, 9, 2, 9, 2, 2, 2, 2, 2],
    [4, 4, 2, 4, 4, 4, 4, 4, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 9, 9, 9, 9, 2, 9, 2, 2, 2, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 9, 2, 2, 9, 2, 9, 2, 2, 2, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 9, 9, 9, 9, 9, 9, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 2, 8, 8, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 5, 2, 5, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 5, 2, 5, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 5, 2, 5, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 7, 2, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
expected_2 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 9, 9, 9, 9, 9, 9, 4, 3, 7, 7, 7, 7, 7, 7, 3],
    [4, 9, 4, 4, 9, 4, 9, 4, 3, 7, 3, 7, 7, 7, 7, 3],
    [4, 9, 4, 4, 9, 4, 9, 4, 3, 7, 7, 7, 7, 7, 7, 3],
    [4, 9, 9, 9, 9, 4, 9, 4, 3, 7, 3, 7, 7, 7, 7, 3],
    [4, 9, 4, 4, 9, 4, 9, 4, 3, 7, 3, 7, 7, 7, 7, 3],
    [4, 9, 9, 9, 9, 9, 9, 4, 3, 7, 7, 7, 7, 7, 7, 3],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1],
    [8, 1, 1, 1, 1, 1, 1, 8, 1, 5, 5, 5, 5, 5, 5, 1],
    [8, 1, 8, 8, 8, 8, 1, 8, 1, 5, 1, 1, 5, 1, 5, 1],
    [8, 1, 8, 8, 8, 8, 1, 8, 1, 5, 1, 1, 5, 1, 5, 1],
    [8, 1, 8, 8, 8, 8, 1, 8, 1, 5, 5, 5, 5, 5, 5, 1],
    [8, 1, 8, 8, 8, 8, 1, 8, 1, 5, 1, 1, 5, 1, 5, 1],
    [8, 1, 1, 1, 1, 1, 1, 8, 1, 5, 5, 5, 5, 5, 5, 1],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1]
]
transformed_2 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 3],
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1],
    [8, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1],
    [8, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1],
    [8, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1],
    [8, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1],
    [8, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1],
    [8, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1],
    [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1]
]

metrics_1 = analyze_example(input_1, expected_1, transformed_1)
# Manually add context from previous run / analysis
metrics_1['identified_separator'] = 8
metrics_1['identified_frame_size'] = (6, 6)
metrics_1['identified_content_size'] = (4, 4)
metrics_1['num_pairs'] = 2

metrics_2 = analyze_example(input_2, expected_2, transformed_2)
# Manually add context from previous run / analysis
metrics_2['identified_separator'] = 2
metrics_2['identified_frame_size'] = (8, 8)
metrics_2['identified_content_size'] = (6, 6)
metrics_2['num_pairs'] = 4


print("--- Metrics Example 1 ---")
print(metrics_1)
print("\n--- Metrics Example 2 ---")
print(metrics_2)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Metrics Example 1 ---
{'input_dims': (20, 15), 'expected_output_dims': (6, 12), 'transformed_output_dims': (6, 12), 'size_match': True, 'pixel_diff': 32, 'palette_match': False, 'identified_separator': 8, 'identified_frame_size': (6, 6), 'identified_content_size': (4, 4), 'num_pairs': 2}

--- Metrics Example 2 ---
{'input_dims': (30, 30), 'expected_output_dims': (16, 16), 'transformed_output_dims': (16, 16), 'size_match': True, 'pixel_diff': 144, 'palette_match': False, 'identified_separator': 2, 'identified_frame_size': (8, 8), 'identified_content_size': (6, 6), 'num_pairs': 4}

```
**YAML Facts:**


```yaml
Observations:
  - Input grids contain multiple rectangular objects separated by a single 'separator' color.
  - Rectangular objects appear primarily in two sizes: 'Frames' (larger, size N x M) and 'Contents' (smaller, size N-2 x M-2).
  - Both Frame and Content blocks in the input may contain internal pixels ('noise') of colors different from their main color. The separator color is frequently used as noise.
  - The output grid arranges the Frame blocks, preserving their relative positions from the input.
  - The output preserves the 1-pixel border of each Frame block, using the Frame block's main color.
  - The interior (core) of each Frame block in the output is filled with a pattern derived from its paired Content block.
  - The core pattern generation involves a color mapping rule applied to the pixels within the Content block's bounding box.
Properties:
  - Separator Color: Color separating the main rectangular objects. Identified by adjacency diversity or frequency.
  - Objects: Rectangular blocks (Frames, Contents).
  - Object Properties: Color (main color), Size (Height, Width), Position (Top-left corner), Type ('frame' or 'content'), Pattern (pixels within bounds).
  - Frame Properties: Size (N x M), Color (Fc), Border (1px thick).
  - Content Properties: Size (N-2 x M-2), Location (Top-left), PatternSource (Pixels within N-2 x M-2 bounding box in input grid), DominantColor (Cc - most frequent non-separator color in PatternSource).
  - Relationships:
      - Frames are paired 1-to-1 with Contents.
      - Pairing mechanism: Simple reading order works for Train 1. Train 2 requires a specific permutation (F1->C1, F2->C4, F3->C3, F4->C2 based on reading order indices). The general rule is unclear.
      - Output layout mirrors the relative spatial arrangement of input Frames.
Transformation Rule (Core Generation):
  - For a given Frame (Color Fc) paired with a Content (PatternSource Cp, DominantColor Cc):
  - Iterate through each pixel `p` at `(i, j)` in the `Cp`:
  - The corresponding output core pixel `Oc[i, j]` is `Fc` if `p` is the `SeparatorColor`.
  - Otherwise, the output core pixel `Oc[i, j]` is `Cc`.
Actions:
  - Identify the Separator Color.
  - Find all non-separator colored rectangular blocks and determine their properties (color, bounds, size).
  - Categorize blocks into Frames (size N x M) and Contents (size N-2 x M-2).
  - Create an ordered list of Frames (sorted by reading order: top-to-bottom, left-to-right).
  - Create an ordered list of Contents (method depends on pairing rule - potentially reading order, potentially requires permutation like in Train 2).
  - Determine the output grid dimensions based on the relative positions and sizes of the Frames.
  - Initialize the output grid.
  - Iterate through the paired Frames (F) and Contents (C):
      - Determine Frame Color (Fc) and Content Dominant Color (Cc).
      - Extract Content Pattern Source (Cp) slice from the input grid based on C's bounds.
      - Calculate the Output Core (Oc) by applying the Transformation Rule (Core Generation) pixel by pixel to Cp.
      - Determine the position for F in the output grid relative to the top-leftmost Frame.
      - Draw the Frame border (Fc) in the output grid at the calculated position.
      - Place the calculated Output Core (Oc) inside the border in the output grid.
  - Return the completed output grid.
```


**Natural Language Program:**

1.  **Identify Separator:** Analyze the input grid to determine the single 'separator' color that primarily occupies the space between distinct rectangular objects. This color often has the most diverse neighbors or is the most frequent background color.
2.  **Find Blocks:** Locate all contiguous blocks of non-separator colors in the input grid and determine their bounding boxes, dominant color, and dimensions (height, width).
3.  **Categorize Blocks:** Group the found blocks based on their dimensions. Identify two main categories: 'Frames' (larger size, N x M) and 'Contents' (smaller size, N-2 x M-2).
4.  **Order Frames:** Create an ordered list of Frame blocks, sorted by their top-left corner coordinates (top-to-bottom, then left-to-right).
5.  **Identify and Order Contents:** Create a list of Content blocks. Determine the correct pairing between Frames and Contents. *(Note: For some tasks like train_2, simple reading order for Contents is insufficient, and a specific permutation or pairing rule is required. If the rule is unknown, assume reading order first.)* Ensure the final list of Contents is ordered according to the determined pairing rule, corresponding to the sorted Frame list.
6.  **Determine Output Layout:** Calculate the required dimensions of the output grid based on the minimum and maximum row/column coordinates spanned by the Frame blocks in the input, preserving their relative arrangement. Initialize an empty output grid (e.g., filled with white=0).
7.  **Process Pairs:** Iterate through the corresponding Frame (F) and Content (C) blocks from the ordered lists:
    a.  **Get Properties:** Identify the Frame Color (Fc) (main color of F) and the top-left position of F (`f_top`, `f_left`). Find the top-left position of C (`c_top`, `c_left`).
    b.  **Extract Content Pattern:** Define the Content Pattern source (Cp) as the rectangular slice of the *original input grid* corresponding to the Content block's bounding box (size N-2 x M-2, starting at `c_top`, `c_left`).
    c.  **Determine Content Color:** Find the Content Color (Cc) by identifying the most frequent color within the Content Pattern source (Cp), excluding the Separator Color.
    d.  **Generate Output Core:** Create a new grid, the Output Core (Oc), of the same dimensions as Cp (N-2 x M-2). For each pixel `Cp[i, j]` in the Content Pattern source:
        i.  If `Cp[i, j]` is the Separator Color, set `Oc[i, j]` to the Frame Color (Fc).
        ii. Otherwise (if `Cp[i, j]` is Cc or any other non-separator color), set `Oc[i, j]` to the Content Color (Cc).
    e.  **Place in Output:** Calculate the target top-left position (`out_r`, `out_c`) for the current Frame in the output grid based on its relative position to the top-leftmost Frame.
    f.  Draw the 1-pixel border of the Frame using the Frame Color (Fc) at the target location (`out_r`, `out_c`) in the output grid.
    g.  Place the generated Output Core (Oc) into the interior area (inside the border) at the target location in the output grid.
8.  **Return Output:** Return the completed output grid.
