```python
import numpy as np
from collections import defaultdict, deque
from scipy import stats as ss

"""
Identifies a 'separator' color and distinct rectangular objects ('frames' and 'contents') in the input grid. 
Frames are larger (N x M) and Contents are smaller (N-2 x M-2).
The transformation constructs an output grid preserving the relative arrangement of the Frames.
Each Frame's 1-pixel border (using its main color, Fc) is copied to the output.
The interior (core) of each Frame in the output is filled based on a pattern derived from its paired Content block.
To generate the core:
1. Identify the dominant color (Cc) of the paired Content block (most frequent non-separator color).
2. Take the rectangular slice of the *input grid* corresponding to the Content block's area (size N-2 x M-2).
3. For each pixel in this slice: if it's the separator color, the output core pixel is Fc; otherwise, it's Cc.
Frame and Content blocks are paired based on their reading order (top-to-bottom, left-to-right).
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
        max_count = -1
        tied_candidates = []
        for cand_color in candidate_separators:
            count = color_counts.get(cand_color, 0)
            if count > max_count:
                max_count = count
                tied_candidates = [cand_color]
            elif count == max_count:
                tied_candidates.append(cand_color)
        # If still tied after frequency, just pick the first one
        if tied_candidates:
             separator_color = tied_candidates[0]
            
    # Fallback if no diversity or tie-breaking failed
    if separator_color < 0: 
        unique_colors, counts = np.unique(grid, return_counts=True)
        if len(counts) > 0:
            # Avoid picking black (0) as separator if possible, unless it's the only color
            most_frequent_idx = np.argsort(counts)[::-1]
            for idx in most_frequent_idx:
                if unique_colors[idx] != 0 or len(unique_colors) == 1:
                    separator_color = unique_colors[idx]
                    break
            if separator_color < 0: # Should only happen if grid was all black
                 separator_color = 0 
        else:
             separator_color = 0 # Default white for empty grid

    # Ensure a valid color (>= 0) is returned
    if separator_color < 0:
        separator_color = 0

    return separator_color

def find_color_blocks(grid: np.ndarray, ignore_color: int = -1) -> list[dict]:
    """ 
    Finds all contiguous blocks of the same color using BFS, optionally ignoring one color.
    Returns a list of dictionaries, each describing a block: its main color,
    bounding box (top, left, bottom, right - inclusive), height, width, 
    pixel coordinates, and pixel count.
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
                pixels = set([(r, c)])
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
                    'color': color, # The main color of the contiguous block
                    'bounds': (min_r, min_c, max_r, max_c), # top, left, bottom, right (inclusive)
                    'height': height,
                    'width': width,
                    'pixels': pixels, # Set of (row, col) tuples
                    'pixel_count': len(pixels),
                })
    return blocks

def get_dominant_color(grid_slice: np.ndarray, ignore_color: int) -> int:
    """Finds the most frequent color in a grid slice, ignoring a specific color."""
    unique_elements, counts = np.unique(grid_slice, return_counts=True)
    # Filter out the ignore_color
    mask = unique_elements != ignore_color
    filtered_elements = unique_elements[mask]
    filtered_counts = counts[mask]
    
    if len(filtered_elements) == 0:
        # If only the ignored color was present, return it as a fallback
        # Or perhaps return a default like 0? Let's return ignore_color's opposite if simple?
        # For now, let's default to 0 (white) if no other color found.
        return 0 
    else:
        # Return the element with the highest count
        return filtered_elements[np.argmax(filtered_counts)]

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid by identifying frame/content pairs, extracting
    patterns, and assembling them into an output grid based on the described rules.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return [] # Handle empty input

    # 1. Identify the separator color
    separator_color = get_separator_color(grid)

    # 2. Find all contiguous blocks, excluding the separator color
    all_blocks = find_color_blocks(grid, ignore_color=separator_color)
    if not all_blocks:
        return [] # No objects found besides separator

    # 3. Categorize remaining blocks into 'frame' and 'content' based on size
    #    We expect rectangular bounding boxes for frames/contents.
    sizes = defaultdict(list)
    for block in all_blocks:
         # Use bounding box dimensions for categorization
         size_key = (block['height'], block['width'])
         sizes[size_key].append(block)

    frame_size = None
    content_size = None
    possible_pairs = []
    
    # Sort potential sizes by area (descending) to check larger ones first
    sorted_size_keys = sorted(sizes.keys(), key=lambda x: x[0]*x[1], reverse=True) 

    # Try to identify frame/content pair based on size relationship (frame = content + 2)
    for i in range(len(sorted_size_keys)):
        for j in range(len(sorted_size_keys)):
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
    elif len(sizes) >= 2 and not possible_pairs:
        # Fallback: If no pair matches rule exactly, but >= 2 sizes exist,
        # assume the most frequent largest size is frame, most frequent second largest is content.
        # This is less robust.
        size_counts = {size: len(blocks) for size, blocks in sizes.items()}
        sorted_by_freq_then_area = sorted(
            sizes.keys(), 
            key=lambda x: (size_counts[x], x[0]*x[1]), 
            reverse=True
        )
        if len(sorted_by_freq_then_area) >= 2:
            frame_size = sorted_by_freq_then_area[0]
            content_size = sorted_by_freq_then_area[1]
            # Add a check if counts match even in fallback
            if size_counts[frame_size] != size_counts[content_size]:
                 frame_size, content_size = None, None # Reset if counts mismatch

    # Check if sizes were successfully determined
    if frame_size is None or content_size is None:
        # Cannot determine sizes reliably, return empty or original? Let's return empty.
        return [] 

    frames = sizes.get(frame_size, [])
    contents = sizes.get(content_size, [])

    # 4. Sort frames and contents by reading order (top-left corner: row, then column)
    frames.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))
    # *** Assumption: Simple reading order pairing works. This might fail for some tasks. ***
    contents.sort(key=lambda x: (x['bounds'][0], x['bounds'][1]))

    # Check for equal number of frames and contents after sorting
    if len(frames) != len(contents):
        return [] # Error: Mismatch after filtering/sorting
    if not frames:
        return [] # No valid frame/content pairs found

    # 5. Determine output grid layout and size based on frame positions
    min_frame_top = min(f['bounds'][0] for f in frames)
    min_frame_left = min(f['bounds'][1] for f in frames)
    # Use the determined frame_size for dimensions
    max_frame_bottom_coord = max(f['bounds'][0] + frame_size[0] - 1 for f in frames)
    max_frame_right_coord = max(f['bounds'][1] + frame_size[1] - 1 for f in frames)

    # Calculate output grid dimensions
    output_height = max_frame_bottom_coord - min_frame_top + 1
    output_width = max_frame_right_coord - min_frame_left + 1
    
    # Check for non-positive dimensions
    if output_height <= 0 or output_width <= 0:
        return []

    # 6. Initialize output grid (fill with a default, e.g., white=0 or separator?) Use white=0.
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 7. Assemble the output grid by combining frame borders and content cores
    for frame, content in zip(frames, contents):
        frame_color = frame['color'] # Fc: Main color of the contiguous frame block
        content_color = content['color'] # Cc: Main color of the contiguous content block
        
        f_top, f_left, _, _ = frame['bounds'] # Frame top-left for positioning
        c_top, c_left, c_bottom, c_right = content['bounds'] # Content bounds for pattern extraction

        # Frame dimensions N x M
        frame_h, frame_w = frame_size 
        # Content dimensions (N-2) x (M-2)
        content_h, content_w = content_size 

        # Calculate position in output grid based on frame's top-left relative to min top-left
        out_r_start = f_top - min_frame_top
        out_c_start = f_left - min_frame_left
        out_r_end = out_r_start + frame_h # Exclusive index for slicing end
        out_c_end = out_c_start + frame_w # Exclusive index for slicing end

        # Check if the calculated output position is valid
        if not (0 <= out_r_start < output_height and 0 <= out_c_start < output_width and \
                out_r_end <= output_height and out_c_end <= output_width):
            continue # Skip this frame if it doesn't fit

        # Draw frame border onto output grid
        output_grid[out_r_start, out_c_start:out_c_end] = frame_color       # Top border
        output_grid[out_r_end - 1, out_c_start:out_c_end] = frame_color     # Bottom border
        output_grid[out_r_start:out_r_end, out_c_start] = frame_color       # Left border
        output_grid[out_r_start:out_r_end, out_c_end - 1] = frame_color     # Right border
        
        # Extract the rectangular content pattern source from the *input* grid
        # using the content block's bounding box. Remember bounds are inclusive.
        # Expected slice size is content_h x content_w
        if c_bottom - c_top + 1 == content_h and c_right - c_left + 1 == content_w:
             content_pattern_source = grid[c_top : c_bottom + 1, c_left : c_right + 1]
        else:
             # Bounding box doesn't match expected content size, maybe noise distorted it?
             # Try to fallback to expected size centered? Or skip? For now, skip.
             continue 

        # Generate the output core based on the mapping rule
        output_core = np.zeros_like(content_pattern_source)
        for r_idx in range(content_h):
            for c_idx in range(content_w):
                source_pixel = content_pattern_source[r_idx, c_idx]
                if source_pixel == separator_color:
                    output_core[r_idx, c_idx] = frame_color # Fc
                else:
                    output_core[r_idx, c_idx] = content_color # Cc
        
        # Place the generated output core into the output grid's inner area
        out_core_r_start = out_r_start + 1
        out_core_c_start = out_c_start + 1
        out_core_r_end = out_core_r_start + content_h # Exclusive end
        out_core_c_end = out_core_c_start + content_w # Exclusive end

        # Ensure the placement fits within the frame border area
        if out_core_r_end <= (out_r_start + frame_h - 1) and \
           out_core_c_end <= (out_c_start + frame_w - 1):
             output_grid[out_core_r_start : out_core_r_end, out_core_c_start : out_core_c_end] = output_core
        # Else: Core doesn't fit (shouldn't happen if sizes N and N-2 match), leave the default background (0)

    # 8. Return the final grid as list of lists
    return output_grid.tolist()
```