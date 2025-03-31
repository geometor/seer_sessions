**Analysis of Failure:**

The `tool_code` execution reveals the core problem: the object classification logic failed entirely for Example 1.
*   It classified the top-right and bottom rectangles as 'simple' with color 2 (red), which is correct.
*   Crucially, it *failed* to classify the top-left object (the one with the pattern) as a 'pattern' rectangle. It wasn't classified as 'simple' either, meaning it likely failed the `is_solid_rectangle` check or the subsequent `classify_object` logic for pattern rectangles.

Let's look at the top-left object in Example 1 again:
Rows 5-8, Columns 3-12.

```
6 6 6 6 6 6 6 6 2 2
8 8 8 8 8 8 8 6 2 2
8 8 8 8 8 8 8 6 2 2
6 6 6 6 6 6 6 6 2 2
```

Bounding box seems to be (r=5, c=3) to (r=8, c=12).
Ah, the *actual* pattern rectangle has a frame of red (2).
The object starts at (r=2, c=3). Let's re-run the check starting there.
``` python
import numpy as np
from collections import deque

# --- Helper Functions (Copied from previous attempt) ---
def bfs_find_connected(grid, start_coord, visited):
    q = deque([start_coord])
    coords = set()
    h, w = grid.shape
    start_r, start_c = start_coord
    if not (0 <= start_r < h and 0 <= start_c < w) or \
       grid[start_r, start_c] == 0 or \
       visited[start_r, start_c]:
        return []
    visited[start_r, start_c] = True
    coords.add(start_coord)
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and \
               not visited[nr, nc] and grid[nr, nc] != 0:
                # Check if colors are the same for BFS? No, just non-zero.
                # This might be the issue - BFS connects different colors.
                visited[nr, nc] = True
                coords.add((nr, nc))
                q.append((nr, nc))
    return list(coords)

def bfs_find_connected_same_color(grid, start_coord, visited):
    """Modified BFS to only connect pixels of the *same* starting color."""
    q = deque([start_coord])
    coords = set()
    h, w = grid.shape
    start_r, start_c = start_coord
    start_color = grid[start_r, start_c]

    if start_color == 0 or visited[start_r, start_c]:
        return []

    visited[start_r, start_c] = True
    coords.add(start_coord)

    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and \
               not visited[nr, nc] and grid[nr, nc] == start_color: # Only connect same color
                visited[nr, nc] = True
                coords.add((nr, nc))
                q.append((nr, nc))
    return list(coords)


def get_bounding_box(coords):
    if not coords: return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c, max_r, max_c)

def is_solid_rectangle(grid, coords, bbox):
    if not coords or not bbox: return False
    min_r, min_c, max_r, max_c = bbox
    obj_h = max_r - min_r + 1
    obj_w = max_c - min_c + 1
    if len(coords) != obj_h * obj_w: return False
    coords_set = set(coords)
    # Check if all pixels *within the bounding box* match the object's pixels.
    # This helps confirm rectangularity even if BFS connected weirdly.
    grid_slice = grid[min_r:max_r+1, min_c:max_c+1]
    if grid_slice.size != len(coords): # Check area size first
        return False
    # Check if all points in coords are within bbox (should be by definition)
    # Check if all points in bbox are in coords (critical for rectangularity)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) not in coords_set:
                return False # Hole found
            # Also ensure no background pixels within the bbox
            if grid[r, c] == 0:
                 return False # Background pixel inside object's claimed bbox
    return True


def classify_object(grid, coords, bbox):
    min_r, min_c, max_r, max_c = bbox
    obj_h = max_r - min_r + 1
    obj_w = max_c - min_c + 1
    ref_color = grid[min_r, min_c]

    # Check simple first (all same color)
    is_simple = True
    for r, c in coords: # Check only the coordinates belonging to the object
        if grid[r,c] != ref_color:
            is_simple = False
            break
    if is_simple:
        return {'type': 'simple', 'color': ref_color, 'bbox': bbox}

    # If not simple, check pattern (requires frame & different interior)
    if obj_h >= 3 and obj_w >= 3:
        frame_color = grid[min_r, min_c]
        frame_ok = True
        # Check frame integrity
        for c in range(min_c, max_c + 1): # Top/Bottom
            if grid[min_r, c] != frame_color or grid[max_r, c] != frame_color: frame_ok = False; break
        if frame_ok:
            for r in range(min_r + 1, max_r): # Left/Right (excl corners)
                if grid[r, min_c] != frame_color or grid[r, max_c] != frame_color: frame_ok = False; break

        # Check if interior differs
        interior_differs = False
        if frame_ok:
            for r in range(min_r + 1, max_r):
                for c in range(min_c + 1, max_c):
                    if grid[r, c] != frame_color:
                        interior_differs = True; break
                if interior_differs: break

        if frame_ok and interior_differs:
            inner_pattern = grid[min_r+1 : max_r, min_c+1 : max_c]
            return {'type': 'pattern', 'frame_color': frame_color, 'bbox': bbox, 'inner_pattern_shape': inner_pattern.shape}
    return None # Neither simple nor valid pattern

# Input for train_1
input_grid_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,6,6,6,6,6,6,6,6,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Issue: BFS starting at (2,3)=2 might connect to (5,3)=6
    [0,0,0,8,8,8,8,8,8,8,6,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,8,8,8,8,8,8,8,6,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,6,6,6,6,6,6,6,6,2,2,2,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]
input_grid_np = np.array(input_grid_list, dtype=int)
h, w = input_grid_np.shape
visited = np.zeros_like(input_grid_np, dtype=bool) # Reset visited for new approach

found_objects = []

# Finding objects requires careful definition. Let's redefine based on observation:
# Objects seem to be defined by their rectangular bounding boxes filled with non-zero colors.
# A "pattern" object has a 1-pixel frame of one color, and the inside is different.
# A "simple" object is filled with one color.

# We need to scan for potential top-left corners of rectangles.
potential_corners = set()
for r in range(h):
    for c in range(w):
        if input_grid_np[r,c] != 0:
             # Is it a top-left corner? Check above and left.
             is_top = (r == 0 or input_grid_np[r-1, c] == 0)
             is_left = (c == 0 or input_grid_np[r, c-1] == 0)
             # More robust: Check if pixel above/left belongs to *same* object.
             # Using visited array helps avoid re-processing.
             if not visited[r,c]:
                 potential_corners.add((r,c)) # Add any non-zero unvisited pixel initially

print(f"Initial potential corners: {len(potential_corners)}")

# Let's try the original BFS again but analyze the result for the first object found
visited = np.zeros_like(input_grid_np, dtype=bool) # Reset visited
r, c = 2, 3 # Start of the pattern object
coords = bfs_find_connected(input_grid_np, (r, c), visited)
print(f"\nStarting BFS at ({r},{c}), found {len(coords)} connected pixels.")
if coords:
    bbox = get_bounding_box(coords)
    print(f"Bounding box: {bbox}")
    is_rect = is_solid_rectangle(input_grid_np, coords, bbox)
    print(f"Is solid rectangle? {is_rect}")
    if is_rect:
        obj_info = classify_object(input_grid_np, coords, bbox)
        print(f"Classification: {obj_info}")
    else:
        # Why wasn't it a solid rectangle?
        min_r, min_c, max_r, max_c = bbox
        expected_size = (max_r - min_r + 1) * (max_c - min_c + 1)
        print(f"Reason: Coord count ({len(coords)}) vs Bbox area ({expected_size})")
        # Check for background pixels within the computed bbox
        has_bg = False
        for row in range(min_r, max_r+1):
            for col in range(min_c, max_c+1):
                 if input_grid_np[row, col] == 0:
                     has_bg = True; break
            if has_bg: break
        print(f"Has background pixel in bbox? {has_bg}")


# Let's re-run the full object finding loop with the original BFS to see all objects identified
visited = np.zeros_like(input_grid_np, dtype=bool) # Reset visited
found_objects_orig_bfs = []
for r in range(h):
    for c in range(w):
        if input_grid_np[r, c] != 0 and not visited[r, c]:
            coords = bfs_find_connected(input_grid_np, (r, c), visited)
            if coords:
                bbox = get_bounding_box(coords)
                # We still need to check if it LOOKS like a rectangle, even if BFS grabs neighbors
                # Let's check if the bounding box area contains only non-zero pixels first
                min_r, min_c, max_r, max_c = bbox
                is_dense = True
                for row in range(min_r, max_r+1):
                    for col in range(min_c, max_c+1):
                        if input_grid_np[row,col] == 0:
                            is_dense = False; break
                    if not is_dense: break

                if is_dense and len(coords) == (max_r - min_r + 1) * (max_c - min_c + 1): # Must fill the dense bbox
                     # Now classify based on content
                     obj_info = classify_object(input_grid_np, coords, bbox)
                     if obj_info:
                          found_objects_orig_bfs.append(obj_info)


print(f"\nFound {len(found_objects_orig_bfs)} rectangular objects (Original BFS):")
for i, obj in enumerate(found_objects_orig_bfs):
    print(f"Object {i+1}:")
    print(f"  Type: {obj['type']}")
    if obj['type'] == 'simple':
        print(f"  Color: {obj['color']}")
    else:
        print(f"  Frame Color: {obj['frame_color']}")
        print(f"  Inner Pattern Shape: {obj['inner_pattern_shape']}")
    print(f"  Bbox: {obj['bbox']}")

# Simulate the selection again
simple_rects_test = [o for o in found_objects_orig_bfs if o['type'] == 'simple']
pattern_rect_test = next((o for o in found_objects_orig_bfs if o['type'] == 'pattern'), None)

print("\n--- Simulation (Original BFS) ---")
if pattern_rect_test:
    print(f"Pattern Rect found: Frame Color {pattern_rect_test['frame_color']}, Bbox {pattern_rect_test['bbox']}")
    print(f"Simple Rects found: {len(simple_rects_test)}")
    matching_simple = [o for o in simple_rects_test if o['color'] == pattern_rect_test['frame_color']]
    print(f"Matching Simple Rects (Color {pattern_rect_test['frame_color']}): {len(matching_simple)}")
    for obj in matching_simple:
        print(f"  - Bbox: {obj['bbox']}")
else:
    print("No Pattern Rect found.")

# Conclusion: The original BFS connecting *any* non-zero neighbors breaks the object definition.
# The definition must be: A rectangle is a region defined by a bounding box where all pixels
# inside are non-zero. Then classify that region.

# New strategy: Find bounding boxes of connected components of the *same* color.
# Then, check if multiple such components perfectly align to form a larger rectangle with a frame.
# OR: Find *all* solid non-zero blocks first, then classify.

# Let's try finding all solid blocks first.
visited = np.zeros_like(input_grid_np, dtype=bool) # Reset visited
all_solid_blocks = []
for r in range(h):
    for c in range(w):
         if input_grid_np[r,c] != 0 and not visited[r,c]:
             # Use same-color BFS to find connected components of a single color
             coords = bfs_find_connected_same_color(input_grid_np, (r, c), visited)
             if coords:
                 bbox = get_bounding_box(coords)
                 # Check if this same-color component fills its own bbox (is rectangular itself)
                 if is_solid_rectangle(input_grid_np, coords, bbox):
                     all_solid_blocks.append({'color': input_grid_np[r,c], 'coords': coords, 'bbox': bbox})

print(f"\nFound {len(all_solid_blocks)} solid single-color blocks.")
# for block in all_solid_blocks:
#     print(f"  Color {block['color']}, Bbox {block['bbox']}, Size {len(block['coords'])}")


# Now, reconstruct the actual objects (simple and pattern) from these blocks.
# A simple rectangle is just one of these blocks.
# A pattern rectangle is formed by multiple blocks: one color for the frame, others inside.

final_objects = []
processed_blocks = [False] * len(all_solid_blocks)

for i, block in enumerate(all_solid_blocks):
    if processed_blocks[i]: continue

    min_r, min_c, max_r, max_c = block['bbox']
    obj_h = max_r - min_r + 1
    obj_w = max_c - min_c + 1

    # Could this block be a frame? Check if it surrounds an area.
    is_frame = True
    inner_coords = set()
    # Check if it has the shape of a frame (pixels only on border of bbox)
    for r,c in block['coords']:
        if not (r == min_r or r == max_r or c == min_c or c == max_c):
            is_frame = False; break
    if not is_frame or obj_h < 3 or obj_w < 3: # Not a frame or too small
         # Assume it's a simple rectangle (or part of one if BFS was needed earlier)
         # Since we used same-color BFS and is_solid_rectangle, this block is simple.
         final_objects.append({'type': 'simple', 'color': block['color'], 'bbox': block['bbox']})
         processed_blocks[i] = True
         continue

    # If it looks like a frame, find potential inner blocks
    frame_color = block['color']
    potential_inner_blocks = []
    actual_inner_coords = set()

    # Find other blocks fully contained within this frame's inner area
    inner_min_r, inner_min_c = min_r + 1, min_c + 1
    inner_max_r, inner_max_c = max_r - 1, max_c - 1

    contains_different_color = False
    blocks_forming_object = [i] # Start with the frame block index

    for j, other_block in enumerate(all_solid_blocks):
        if i == j or processed_blocks[j]: continue
        other_min_r, other_min_c, other_max_r, other_max_c = other_block['bbox']
        # Check if other_block is fully inside the potential inner area
        if (other_min_r >= inner_min_r and other_max_r <= inner_max_r and
            other_min_c >= inner_min_c and other_max_c <= inner_max_c):
            potential_inner_blocks.append(other_block)
            actual_inner_coords.update(other_block['coords'])
            if other_block['color'] != frame_color:
                contains_different_color = True
            blocks_forming_object.append(j) # Add index of inner block

    # Now, verify if the frame + inner blocks perfectly fill the frame's bbox
    combined_coords = set(block['coords']) # Start with frame coords
    combined_coords.update(actual_inner_coords)

    total_area = obj_h * obj_w
    filled_area = len(combined_coords)

    # Check if the combined area matches the total bbox area
    # AND if the interior contained something different from the frame
    if filled_area == total_area and contains_different_color:
        # It's a pattern rectangle!
        inner_pattern = input_grid_np[inner_min_r:inner_max_r+1, inner_min_c:inner_max_c+1]
        final_objects.append({'type': 'pattern', 'frame_color': frame_color, 'bbox': block['bbox'], 'inner_pattern_shape': inner_pattern.shape})
        # Mark all constituent blocks as processed
        for block_idx in blocks_forming_object:
             processed_blocks[block_idx] = True
    else:
        # Frame shape didn't combine correctly or interior was same color/empty
        # Treat the initial block as simple
         final_objects.append({'type': 'simple', 'color': block['color'], 'bbox': block['bbox']})
         processed_blocks[i] = True


# Add any remaining unprocessed blocks as simple rectangles
for i, block in enumerate(all_solid_blocks):
     if not processed_blocks[i]:
         final_objects.append({'type': 'simple', 'color': block['color'], 'bbox': block['bbox']})


print(f"\nFound {len(final_objects)} final objects (Reconstruction):")
for i, obj in enumerate(final_objects):
    print(f"Object {i+1}:")
    print(f"  Type: {obj['type']}")
    if obj['type'] == 'simple':
        print(f"  Color: {obj['color']}")
    else:
        print(f"  Frame Color: {obj['frame_color']}")
        print(f"  Inner Pattern Shape: {obj['inner_pattern_shape']}")
    print(f"  Bbox: {obj['bbox']}")


# Simulate the selection again with final objects
simple_rects_final = [o for o in final_objects if o['type'] == 'simple']
pattern_rect_final = next((o for o in final_objects if o['type'] == 'pattern'), None)

print("\n--- Simulation (Reconstruction) ---")
if pattern_rect_final:
    print(f"Pattern Rect found: Frame Color {pattern_rect_final['frame_color']}, Bbox {pattern_rect_final['bbox']}")
    print(f"Simple Rects found: {len(simple_rects_final)}")
    matching_simple = [o for o in simple_rects_final if o['color'] == pattern_rect_final['frame_color']]
    print(f"Matching Simple Rects (Color {pattern_rect_final['frame_color']}): {len(matching_simple)}")
    for obj in matching_simple:
        print(f"  - Bbox: {obj['bbox']}")
else:
    print("No Pattern Rect found.")
```
```
Initial potential corners: 351

Starting BFS at (2,3), found 110 connected pixels.
Bounding box: (2, 3, 11, 13)
Is solid rectangle? True
Classification: None

Found 2 rectangular objects (Original BFS):
Object 1:
  Type: simple
  Color: 2
  Bbox: (8, 19, 16, 27)
Object 2:
  Type: simple
  Color: 2
  Bbox: (19, 5, 28, 20)

--- Simulation (Original BFS) ---
No Pattern Rect found.

Found 3 solid single-color blocks.

Found 3 final objects (Reconstruction):
Object 1:
  Type: simple
  Color: 8
  Bbox: (6, 3, 7, 9)
Object 2:
  Type: simple
  Color: 2
  Bbox: (8, 19, 16, 27)
Object 3:
  Type: simple
  Color: 2
  Bbox: (19, 5, 28, 20)

--- Simulation (Reconstruction) ---
No Pattern Rect found.

```
**General Assessment & Strategy Revision:**

The previous code failed because its definition and identification of objects were flawed. The initial BFS approach, connecting any non-zero neighbors, merged distinct parts of the pattern object and failed to recognize it. Subsequent attempts to refine object detection using same-color BFS or reconstructing from single-color blocks also failed to correctly identify the 'pattern' object in Example 1.

The core issue lies in defining what constitutes an "object" in this context. The key seems to be the structure: rectangles (solid blocks of non-zero pixels) which are either uniformly colored ('simple') or have a 1-pixel frame of one color and a differing interior ('pattern').

**Revised Strategy:**

1.  **Identify Potential Rectangles:** Find *all* rectangular blocks composed entirely of non-background (non-zero) pixels. A simple way is to iterate through all possible top-left (r1, c1) and bottom-right (r2, c2) corners and check if the enclosed grid slice `grid[r1:r2+1, c1:c2+1]` contains only non-zero values. Store these valid rectangular regions (bbox + content). Avoid duplicates (e.g., a smaller rectangle contained within a larger one might be found; need a method to prioritize or filter). A better approach might be flood fill (BFS) *only* on non-zero cells, find bounding boxes, and *then* verify if the component fills the bounding box without any background pixels inside.
2.  **Classify Rectangles:** Iterate through the identified rectangular regions.
    *   **Simple:** Check if all pixels within the rectangle have the same color.
    *   **Pattern:** Check if it's at least 3x3, has a uniform 1-pixel border (frame) of one color, and contains at least one pixel of a *different* color in its interior.
3.  **Apply Transformation:** Find the unique 'pattern' rectangle. Extract its frame color and inner pattern. Find all 'simple' rectangles whose color matches the pattern's frame color. Copy the (cropped) inner pattern into the inner area of these matching simple rectangles.

**Metrics & Renewed Investigation (Example 1):**

Let's manually verify the objects in Example 1 based on the revised strategy.

*   **Object 1:** Bbox=(2, 3, 11, 13). Content includes multiple colors (2, 6, 8). Frame check: Top/Bottom rows are color 2. Left/Right columns are color 2. Interior (rows 3-10, cols 4-12) contains colors 6 and 8, different from frame color 2. Size is > 3x3. **Classification: Pattern. Frame=2.** Inner pattern is grid[3:11, 4:12].
*   **Object 2:** Bbox=(8, 19, 16, 27). Content is all color 2. **Classification: Simple. Color=2.**
*   **Object 3:** Bbox=(19, 5, 28, 20). Content is all color 2. **Classification: Simple. Color=2.**

The previous `tool_code` runs failed to identify Object 1 correctly. The BFS was too greedy, and the reconstruction logic was also flawed. The classification logic for 'pattern' rectangles needs to correctly identify the frame and check the interior based on the bounding box, not just connected components.

**Revised YAML Facts:**


```yaml
Analyzed Objects:
  - type: Background
    color: white (0)
  - type: Rectangle
    description: A rectangular region where all pixels are non-white (non-zero).
    identification: Scan grid for bounding boxes (r1, c1, r2, c2) such that all grid cells within these bounds are != 0.
    subtypes:
      - Simple Rectangle: All pixels within the rectangle have the same color.
        properties:
          - color: The single color value.
          - bbox: (min_r, min_c, max_r, max_c)
          - size: height, width
      - Pattern Rectangle:
        conditions:
          - Must be at least 3x3 pixels.
          - Must have a 1-pixel thick border (frame) consisting of a single, uniform color.
          - The interior region (inside the frame) must contain at least one pixel whose color is different from the frame color.
        properties:
          - frame_color: The color of the 1-pixel border.
          - inner_pattern: A 2D grid representing the pixels inside the frame.
          - bbox: (min_r, min_c, max_r, max_c)
          - size: height, width
        uniqueness: Assume only one Pattern Rectangle exists per input grid.

Relationships & Actions:
  - Identification: Find all Simple and Pattern Rectangles based on the definitions above.
  - Matching: Compare the 'color' of each Simple Rectangle to the 'frame_color' of the unique Pattern Rectangle.
  - Transformation: Pattern Propagation.
    - Condition: A Simple Rectangle's 'color' matches the Pattern Rectangle's 'frame_color', AND the Simple Rectangle is large enough to have an interior (>= 3x3).
    - Action:
      1. Copy the 'inner_pattern' from the Pattern Rectangle.
      2. Determine the inner area of the target Simple Rectangle (bbox excluding the 1-pixel border).
      3. Calculate the dimensions to copy (cropping the source pattern if the target inner area is smaller).
      4. Paste the (potentially cropped) pattern into the target Simple Rectangle's inner area on the output grid, starting at the top-left corner of the inner area.
  - No Change:
    - The original Pattern Rectangle remains unchanged.
    - Simple Rectangles that do not match the frame color remain unchanged.
    - Simple Rectangles that match but are too small (< 3x3) remain unchanged.
    - The background remains unchanged.
```


**Revised Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all maximal rectangular blocks in the input grid that contain only non-white pixels. Store their bounding boxes and content.
3.  Find the unique "Pattern Rectangle" among these blocks:
    a.  It must be at least 3x3.
    b.  It must have a 1-pixel border (frame) composed of a single, uniform color.
    c.  Its interior (inside the frame) must contain at least one pixel with a color different from the frame color.
    d.  If found, store its frame color and extract its inner pattern (the grid slice inside the frame). If not found, return the initial output grid.
4.  Identify all "Simple Rectangles":
    a.  These are rectangular blocks where all pixels share the same single color.
5.  For each "Simple Rectangle":
    a.  Check if its color matches the frame color of the "Pattern Rectangle".
    b.  Check if the Simple Rectangle is at least 3x3 in size (to have an interior).
    c.  If both conditions are true:
        i.  Determine the bounding box of the Simple Rectangle's inner area (bbox excluding the 1-pixel border). Let the dimensions be `target_h` and `target_w`.
        ii. Let the dimensions of the Pattern Rectangle's inner pattern be `source_h` and `source_w`.
        iii. Calculate the copy dimensions: `copy_h = min(target_h, source_h)` and `copy_w = min(target_w, source_w)`.
        iv. If `copy_h > 0` and `copy_w > 0`:
            - Extract the top-left `copy_h` x `copy_w` subgrid from the Pattern Rectangle's inner pattern.
            - Overwrite the corresponding top-left portion of the Simple Rectangle's inner area in the output grid with the extracted subgrid.
6.  Return the modified output grid.