import numpy as np
from collections import defaultdict, deque

"""
Identifies a 'separator' color and distinct objects in the input grid. Objects 
are contiguous blocks of a single non-separator color. These objects are 
categorized into 'Frames' (larger bounding box, N x M) and 'Contents' 
(smaller bounding box, N-2 x M-2). Assumes a 1-to-1 pairing exists.

The transformation constructs an output grid by preserving the relative 
arrangement of the Frames. Each reconstructed frame in the output consists of:
1. A 1-pixel border using the Frame's main color (Fc).
2. An interior 'core' pattern derived from the paired Content block.

To generate the core pattern:
- Take the rectangular slice of the *original input grid* corresponding to the 
  Content block's bounding box (size N-2 x M-2). Let this be InputPatternSlice.
- Identify the main color (Cc) of the Content block.
- Create an Output Core grid (size N-2 x M-2).
- For each pixel `p` at `(i, j)` in the InputPatternSlice: 
    - If `p` is the separator color, the Output Core pixel `Oc[i, j]` is Fc.
    - Otherwise, the Output Core pixel `Oc[i, j]` is Cc.

Frame and Content blocks are paired based on sorting their top-left bounding box 
corners in reading order (top-to-bottom, left-to-right).
"""

def get_separator_color(grid: np.ndarray) -> int:
    """
    Identifies the separator color in the grid.
    Assumes the separator has the highest number of distinct neighboring colors.
    Ties are broken by choosing the most frequent color among candidates,
    and then by the lowest color value if frequency is also tied.
    Falls back to the overall most frequent color if diversity analysis fails.
    """
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return 0 # Default white for empty grid
        
    neighbor_colors = defaultdict(set)
    color_counts = defaultdict(int)

    # Iterate through grid to find distinct neighbors and count colors
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            color_counts[color] += 1
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
    present_colors = color_counts.keys()

    # Find colors with maximum neighbor diversity
    for color in present_colors:
         neighbors = neighbor_colors[color]
         num_distinct_neighbors = len(neighbors)
         if num_distinct_neighbors > max_diversity:
             max_diversity = num_distinct_neighbors
             candidate_separators = [color]
         elif num_distinct_neighbors == max_diversity:
             candidate_separators.append(color)

    separator_color = -1
    if len(candidate_separators) == 1:
        separator_color = candidate_separators[0]
    elif len(candidate_separators) > 1:
        # Tie-breaking: 1st by frequency, 2nd by lowest color value
        max_count = -1
        best_candidate = -1
        tied_candidates_by_freq = []
        
        for cand_color in candidate_separators:
            count = color_counts.get(cand_color, 0)
            if count > max_count:
                max_count = count
                tied_candidates_by_freq = [cand_color]
            elif count == max_count:
                tied_candidates_by_freq.append(cand_color)
                
        if len(tied_candidates_by_freq) == 1:
             separator_color = tied_candidates_by_freq[0]
        elif len(tied_candidates_by_freq) > 1:
              separator_color = min(tied_candidates_by_freq) # Break final tie with min value
        else: # Should not happen if candidates existed
             separator_color = candidate_separators[0] # Fallback within tie-break
            
    # Fallback if diversity analysis failed
    if separator_color < 0: 
        if color_counts:
             # Sort by count desc, then color asc for tie-breaking
             sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
             separator_color = sorted_colors[0][0]
        else:
             separator_color = 0 # Default white for empty grid

    # Ensure a valid color (>= 0) is returned
    if separator_color < 0:
        separator_color = 0

    return separator_color


def find_color_blocks(grid: np.ndarray, ignore_color: int) -> list[dict]:
    """ 
    Finds all contiguous blocks of the same color using BFS, ignoring ignore_color.
    Returns a list of dictionaries, each describing a block: its main color,
    bounding box (top, left, bottom, right - inclusive), height, and width.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip if already visited or if it's the ignore_color
            if not visited[r, c] and color != ignore_color:
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                # BFS to find all connected pixels of the same color
                # Only need to track bounds, not all pixels
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
                            q.append((nr, nc))
                            
                # Calculate block properties
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                
                # Store block information
                blocks.append({
                    'color': color, # The main color of the contiguous block
                    'bounds': (min_r, min_c, max_r, max_c), # top, left, bottom, right (inclusive)
                    'height': height,
                    'width': width,
                })
    return blocks


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the specified rules: identifies 
    frame/content pairs, extracts patterns, and assembles them into an output grid.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return [] # Handle empty input

    # 1. Identify the separator color
    separator_color = get_separator_color(grid)

    # 2. Find all contiguous non-separator blocks
    all_blocks = find_color_blocks(grid, ignore_color=separator_color)
    if not all_blocks:
        return [] # No objects found

    # 3. Categorize blocks into 'frame' and 'content' based on bounding box size
    sizes = defaultdict(list)
    for block in all_blocks:
        size_key = (block['height'], block['width'])
        sizes[size_key].append(block)

    frame_size = None
    content_size = None
    possible_pairs = []
    
    # Sort potential sizes by area (descending)
    sorted_size_keys = sorted(sizes.keys(), key=lambda x: x[0]*x[1], reverse=True) 

    # Identify frame/content pair based on size relationship (frame = content + 2)
    for i in range(len(sorted_size_keys)):
        s_large = sorted_size_keys[i]
        for j in range(len(sorted_size_keys)):
            if i == j: continue
            s_small = sorted_size_keys[j]
            # Check if larger size is exactly 2 units bigger in height and width
            if s_large[0] == s_small[0] + 2 and s_large[1] == s_small[1] + 2:
                # Check if number of blocks matches for this pair
                if len(sizes[s_large]) == len(sizes[s_small]):
                    possible_pairs.append({'frame': s_large, 'content': s_small})
                    break # Found a potential content size for this frame size

    # Select the best pair 
    if len(possible_pairs) == 1:
        frame_size = possible_pairs[0]['frame']
        content_size = possible_pairs[0]['content']
    elif len(possible_pairs) > 1:
         # Ambiguous: Default to the pair with the largest frame size.
         possible_pairs.sort(key=lambda p: p['frame'][0]*p['frame'][1], reverse=True)
         frame_size = possible_pairs[0]['frame']
         content_size = possible_pairs[0]['content']
    # No fallback implemented if N vs N-2 rule fails

    # Ensure sizes were determined
    if frame_size is None or content_size is None:
        return [] # Cannot determine sizes reliably

    frames = sizes.get(frame_size, [])
    contents = sizes.get(content_size, [])

    # 4. Sort frames and contents by reading order (top-left corner)
    frames.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))
    contents.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))

    # Check for equal number of frames and contents after sorting
    if len(frames) != len(contents) or not frames:
        return [] # Mismatch or no pairs found

    # 5. Determine output grid layout and size
    min_frame_top = min(f['bounds'][0] for f in frames)
    min_frame_left = min(f['bounds'][1] for f in frames)
    # Use Frame size for calculating max bounds, not just bounds[2]/bounds[3]
    # which might be affected if the found block wasn't perfectly rectangular initially
    max_frame_bottom = max(f['bounds'][0] + frame_size[0] - 1 for f in frames)
    max_frame_right = max(f['bounds'][1] + frame_size[1] - 1 for f in frames)

    output_height = max_frame_bottom - min_frame_top + 1
    output_width = max_frame_right - min_frame_left + 1
    
    if output_height <= 0 or output_width <= 0:
        return [] # Invalid dimensions

    # 6. Initialize output grid (filled with white=0)
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 7. Process pairs and construct output
    for frame, content in zip(frames, contents):
        frame_color = frame['color']    # Fc
        content_color = content['color']  # Cc
        
        f_top, f_left, _, _ = frame['bounds'] # Use top-left for positioning
        c_top, c_left, c_bottom, c_right = content['bounds'] 
        
        frame_h, frame_w = frame_size 
        content_h, content_w = content_size 

        # Calculate target top-left position in output grid
        out_r_start = f_top - min_frame_top
        out_c_start = f_left - min_frame_left
        out_r_end = out_r_start + frame_h # Exclusive index for slicing
        out_c_end = out_c_start + frame_w # Exclusive index for slicing

        # Ensure target position is within bounds of output grid
        if not (0 <= out_r_start < output_height and 0 <= out_c_start < output_width and \
                out_r_end <= output_height and out_c_end <= output_width):
            continue # Skip if frame placement is out of bounds

        # Extract the InputPatternSlice from the original grid using Content bounds
        # Slicing uses exclusive end index, so add 1 to inclusive bounds
        input_pattern_slice = grid[c_top : c_bottom + 1, c_left : c_right + 1]
        
        # Verify extracted slice matches expected content dimensions
        if input_pattern_slice.shape != (content_h, content_w):
             # Content block bounds did not match expected size, skip.
             continue

        # Generate the Output Core based on the mapping rule
        output_core = np.zeros_like(input_pattern_slice)
        for r_idx in range(content_h):
            for c_idx in range(content_w):
                source_pixel = input_pattern_slice[r_idx, c_idx]
                if source_pixel == separator_color:
                    output_core[r_idx, c_idx] = frame_color # Use Frame color (Fc)
                else:
                    output_core[r_idx, c_idx] = content_color # Use Content color (Cc)
        
        # Draw frame border onto output grid
        output_grid[out_r_start, out_c_start:out_c_end] = frame_color       # Top border
        output_grid[out_r_end - 1, out_c_start:out_c_end] = frame_color     # Bottom border
        output_grid[out_r_start:out_r_end, out_c_start] = frame_color       # Left border
        output_grid[out_r_start:out_r_end, out_c_end - 1] = frame_color     # Right border

        # Place the generated Output Core into the output grid's inner area
        out_core_r_start = out_r_start + 1
        out_core_c_start = out_c_start + 1
        out_core_r_end = out_core_r_start + content_h # Exclusive end for slicing
        out_core_c_end = out_core_c_start + content_w # Exclusive end for slicing

        # Ensure placement fits within the frame border area in the output grid
        if out_core_r_end <= (out_r_end - 1) and \
           out_core_c_end <= (out_c_end - 1) and \
           out_core_r_start >= out_r_start and \
           out_core_c_start >= out_c_start:
                output_grid[out_core_r_start : out_core_r_end, out_core_c_start : out_core_c_end] = output_core
        # Else: Core doesn't fit - logic assumes N vs N-2 holds, so this shouldn't normally fail.

    # 8. Return the final grid as list of lists
    return output_grid.tolist()