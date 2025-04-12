```python
"""
Transformation Rule Description (Hypothesis 8: Strict Bound + Row/Column Alignment):

1.  **Identify Background:** Determine the most frequent color in the input grid; this is the background color.
2.  **Find Solid Blocks:** Locate all solid 3x3 squares composed of a single non-background color. Record their color, coordinates, and bounding box (min/max row/col).
3.  **Find Noise Pixels:** Identify all non-background pixels that are not part of any solid 3x3 block. Group these noise pixels by their color.
4.  **Initialize Output:** Create an output grid of the same dimensions as the input, filled entirely with the background color.
5.  **Copy Blocks:** Copy the identified solid 3x3 blocks from the input grid to the output grid at their original locations.
6.  **Determine Block Expansion (Hypothesis 8 Rule):**
    a.  For each solid block `b` with color `c`, bounds (`r_min`, `r_max`, `c_min`, `c_max`), and corresponding noise pixels `P_c`:
        i.  Find all background pixels `n = (r_n, c_n)` in the *input* grid orthogonally adjacent to any *edge* pixel of block `b`.
        ii. For each candidate `n`, determine the side(s) `S` it is adjacent to relative to block `b` ("Above", "Below", "Left", "Right").
        iii. Check if `n` should change color: Iterate through each side `s` in `S`. Does there exist *at least one* noise pixel `p = (r_p, c_p)` in `P_c` such that `p` is strictly outside the block boundary on side `s` AND `p` is strictly aligned with `n` (same column for Above/Below sides, same row for Left/Right sides)?
        iv. If the condition in (iii) is met for *any* side `s` in `S`, mark pixel `n` to change to color `c`.
7.  **Apply Expansion:** Update the output grid by changing the color of all marked pixels.
8.  **Return Output:** The final output grid contains the preserved blocks and the expanded regions. Noise pixels are implicitly removed.

(Self-correction note: Acknowledge that this program based on H8 is expected to fail on train_2 pixels (2,3), (6,5), and (8,5) based on the metrics analysis.)
"""

import numpy as np
from collections import Counter
from typing import List, Tuple, Dict, Set

# === Helper Functions ===

def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default for empty grid
    # Ensure key is standard int
    return int(counts.most_common(1)[0][0])

def find_solid_blocks_and_noise(grid: np.ndarray) -> tuple[int, list[tuple[int, tuple[int, int, int, int], set[tuple[int, int]]]], dict[int, set[tuple[int, int]]]]:
    """
    Finds the background color, all solid 3x3 blocks, and noise pixels.

    Returns:
        - background_color (int)
        - list_of_blocks: List of (color, (r_min, r_max, c_min, c_max), coords_set)
        - noise_pixels_by_color: Dict {color: set_of_noise_coords}
    """
    H, W = grid.shape
    background_color = find_background_color(grid)
    list_of_blocks = []
    all_block_coords = set()
    visited_block_pixels = set() # To handle potential overlaps or faster checks

    # Find blocks
    for r in range(H - 2):
        for c in range(W - 2):
            if (r, c) in visited_block_pixels: continue
            color = grid[r, c]
            if color == background_color: continue

            is_solid_block = True
            current_block_coords = set()
            for i in range(3):
                for j in range(3):
                    coord = (r + i, c + j)
                    # Check bounds explicitly
                    if r+i >= H or c+j >= W or grid[r + i, c + j] != color or coord in visited_block_pixels:
                        is_solid_block = False
                        break
                    current_block_coords.add(coord)
                if not is_solid_block: break

            if is_solid_block:
                bounds = (r, r + 2, c, c + 2)
                # Ensure color is standard int
                list_of_blocks.append((int(color), bounds, current_block_coords))
                all_block_coords.update(current_block_coords)
                visited_block_pixels.update(current_block_coords)

    # Find noise
    noise_pixels_by_color = {}
    for r in range(H):
        for c in range(W):
            coord = (r, c)
            color = grid[r, c]
            if color != background_color and coord not in all_block_coords:
                noise_color_key = int(color) # Ensure key is standard int
                if noise_color_key not in noise_pixels_by_color:
                    noise_pixels_by_color[noise_color_key] = set()
                noise_pixels_by_color[noise_color_key].add(coord)

    return background_color, list_of_blocks, noise_pixels_by_color

def get_edge_adjacent_background_candidates(grid: np.ndarray, background_color: int, block_bounds: tuple[int, int, int, int], block_coords: set[tuple[int, int]]) -> dict[tuple[int, int], set[str]]:
    """
    Finds background pixels orthogonally adjacent to block edges and notes which side(s).

    Returns:
        Dict {(r, c): set_of_sides} e.g., {(3, 0): {"Below"}}
    """
    H, W = grid.shape
    r_min, r_max, c_min, c_max = block_bounds
    candidates = {} # {(r, c): {"Above", "Below", "Left", "Right"}}

    # Identify edge pixels of the block
    edge_pixels = {
        (r, c) for r, c in block_coords
        if r == r_min or r == r_max or c == c_min or c == c_max
    }

    # Check orthogonal neighbors of edge pixels
    for r_edge, c_edge in edge_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Orthogonal steps
            r_n, c_n = r_edge + dr, c_edge + dc
            coord_n = (r_n, c_n)

            # Check bounds, ensure it's background color in INPUT, and not part of the block itself
            if 0 <= r_n < H and 0 <= c_n < W and grid[r_n, c_n] == background_color and coord_n not in block_coords:
                if coord_n not in candidates:
                    candidates[coord_n] = set()
                # Determine side(s) n is on relative to block bounds
                if r_n < r_min: candidates[coord_n].add("Above")
                if r_n > r_max: candidates[coord_n].add("Below")
                if c_n < c_min: candidates[coord_n].add("Left")
                if c_n > c_max: candidates[coord_n].add("Right")

    # Filter out any candidates that didn't end up on a side
    final_candidates = {coord: sides for coord, sides in candidates.items() if sides}
    return final_candidates

def check_expansion_condition_h8(candidate_coord: tuple[int, int], candidate_sides: set[str], block_bounds: tuple[int, int, int, int], noise_coords: set[tuple[int, int]]) -> bool:
    """
    Checks if a candidate background pixel should change color based on H8:
    Strict Bound + Row/Column Alignment with noise.
    """
    r_n, c_n = candidate_coord
    r_min, r_max, c_min, c_max = block_bounds

    if not noise_coords: return False # No noise, no expansion

    # Check each side the candidate is adjacent to
    for side in candidate_sides:
        # Check if any noise pixel satisfies the condition for this side
        for r_p, c_p in noise_coords:
            # Condition 1: Noise is strictly outside the boundary on this side
            # Condition 2: Noise is strictly aligned with candidate (same col for Above/Below, same row for Left/Right)
            if side == "Above" and r_p < r_min and c_p == c_n: return True
            if side == "Below" and r_p > r_max and c_p == c_n: return True
            if side == "Left"  and c_p < c_min and r_p == r_n: return True
            if side == "Right" and c_p > c_max and r_p == r_n: return True

    return False # No noise pixel satisfied the condition for any adjacent side

# === Main Transformation Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation based on Hypothesis 8.
    """
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape
    if H == 0 or W == 0: # Handle empty input case
        return []

    # Step 1, 2, 3: Find background, blocks, and noise
    background_color, solid_blocks_list, noise_pixels_by_color = find_solid_blocks_and_noise(input_np)

    # Step 4: Initialize Output Grid with the background color
    output_np = np.full_like(input_np, background_color)

    # Step 5: Preserve Solid Blocks by copying them to the output grid
    for color, bounds, block_coords in solid_blocks_list:
        for r, c in block_coords:
            # Bounds check might be redundant if find_solid_blocks is correct, but safe
            if 0 <= r < H and 0 <= c < W:
                output_np[r, c] = color

    # Step 6: Determine Expansion based on H8
    expansion_updates = {} # Store updates as {(r, c): color}

    # Iterate through each solid block found
    for block_color, block_bounds, block_coords in solid_blocks_list:
        # Get noise pixels matching the current block's color
        current_noise_set = noise_pixels_by_color.get(block_color, set())
        if not current_noise_set:
            continue # Skip if no relevant noise exists for this block color

        # Find candidate background pixels adjacent to the block's edges
        candidate_pixels = get_edge_adjacent_background_candidates(input_np, background_color, block_bounds, block_coords)

        # Check each candidate against the expansion condition (H8)
        for coord_n, adjacent_sides in candidate_pixels.items():
            # Check if the H8 condition is met using the relevant noise set
            if check_expansion_condition_h8(coord_n, adjacent_sides, block_bounds, current_noise_set):
                # If the condition is met, mark this pixel for update
                expansion_updates[coord_n] = block_color

    # Step 7: Apply the collected expansion updates to the output grid
    for (r, c), color in expansion_updates.items():
        output_np[r, c] = color

    # Step 8: Convert the final NumPy array back to list of lists
    return output_np.tolist()
```