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