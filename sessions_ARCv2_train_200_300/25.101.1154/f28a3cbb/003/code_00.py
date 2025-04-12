import numpy as np
from collections import Counter
from typing import List, Tuple, Dict, Set

"""
Transformation Rule Description:

1.  **Identify Background:** Determine the most frequent color in the input grid; this is the background color.
2.  **Find Solid Blocks:** Locate all solid 3x3 squares composed of a single non-background color. Record their color, coordinates, and bounding box (min/max row/col).
3.  **Find Noise Pixels:** Identify all non-background pixels that are not part of any solid 3x3 block. Group these noise pixels by their color.
4.  **Initialize Output:** Create an output grid of the same dimensions as the input, filled entirely with the background color.
5.  **Copy Blocks:** Copy the identified solid 3x3 blocks from the input grid to the output grid at their original locations.
6.  **Determine Block Expansion (Hypothesis 7):**
    a.  For each solid block:
        i.  Identify the noise pixels that share the same color as the block.
        ii. Determine the "active directions" (Up, Down, Left, Right) relative to the block's bounding box based on whether any same-colored noise pixels exist strictly outside the block's boundaries in those directions.
        iii. Find all background pixels in the *input* grid that are orthogonally adjacent to any *edge* pixel of the current block. These are the "candidate" pixels for expansion. For each candidate, note which side(s) of the block it is adjacent to (Above, Below, Left, Right).
        iv. A candidate pixel changes color in the output grid if at least one of the sides it's adjacent to matches an "active direction" determined in step ii. The pixel's new color is the color of the adjacent block.
7.  **Apply Expansion:** Update the output grid by changing the color of the identified candidate pixels according to the rule in step 6.iv.
8.  **Return Output:** The final output grid contains the preserved blocks and the expanded regions. Noise pixels are implicitly removed as they are not copied, and non-expanded background pixels remain as background.
"""

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
                # Candidate is "Above" if its row is less than block's min row, etc.
                if r_n < r_min: candidates[coord_n].add("Above")
                if r_n > r_max: candidates[coord_n].add("Below")
                if c_n < c_min: candidates[coord_n].add("Left")
                if c_n > c_max: candidates[coord_n].add("Right")

    # Filter out any candidates that didn't end up on a side (e.g. inside a concave region - shouldn't happen for 3x3)
    final_candidates = {coord: sides for coord, sides in candidates.items() if sides}
    return final_candidates

def get_active_directions(noise_coords: set[tuple[int, int]], block_bounds: tuple[int, int, int, int]) -> set[str]:
    """
    Determines active expansion directions based on noise pixels existing strictly outside block bounds.

    Returns:
        Set of directions: {"Up", "Down", "Left", "Right"}
    """
    r_min, r_max, c_min, c_max = block_bounds
    active_dirs = set()
    if not noise_coords: # Handle case with no noise
        return active_dirs
    for r_p, c_p in noise_coords:
        if r_p < r_min: active_dirs.add("Up")
        if r_p > r_max: active_dirs.add("Down")
        if c_p < c_min: active_dirs.add("Left")
        if c_p > c_max: active_dirs.add("Right")
    return active_dirs


# === Main Transformation Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by preserving 3x3 blocks and expanding them based
    on adjacent background pixels that are 'activated' by nearby noise pixels
    of the same color existing beyond the block's boundaries.
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
            # Check bounds just in case, though find_solid_blocks should ensure this
            if 0 <= r < H and 0 <= c < W:
                output_np[r, c] = color

    # Step 6 & 7: Determine and Apply Expansion based on Hypothesis 7
    expansion_updates = {} # Store updates as {(r, c): color} to handle potential overlaps if needed

    # Iterate through each solid block found
    for block_color, block_bounds, block_coords in solid_blocks_list:
        # Get noise pixels matching the current block's color
        current_noise_set = noise_pixels_by_color.get(block_color, set())

        # Determine active directions based on this noise and block bounds
        active_directions = get_active_directions(current_noise_set, block_bounds)
        if not active_directions:
            continue # Skip if no noise activates any direction

        # Find candidate background pixels adjacent to the block's edges
        candidate_pixels = get_edge_adjacent_background_candidates(input_np, background_color, block_bounds, block_coords)

        # Check each candidate against the active directions
        for (r_n, c_n), adjacent_sides in candidate_pixels.items():
            coord_n = (r_n, c_n)
            should_change = False
            # Check if any side the candidate is adjacent to matches an active direction
            for side in adjacent_sides:
                # Map the side name ("Above", "Below", "Left", "Right") to the direction name ("Up", "Down", "Left", "Right")
                direction = side
                if side == "Above": direction = "Up"
                elif side == "Below": direction = "Down"
                # Left and Right map directly

                if direction in active_directions:
                    should_change = True
                    break # Found a matching active direction, no need to check other sides

            # If the candidate should change, record the update
            if should_change:
                # Store the coordinate and the color it should change to (block's color)
                # Using dict handles cases where a pixel might be candidate for multiple blocks (unlikely here)
                # or adjacent to multiple sides activated by different directions (possible).
                expansion_updates[coord_n] = block_color

    # Apply the collected expansion updates to the output grid
    for (r, c), color in expansion_updates.items():
        output_np[r, c] = color

    # Step 8: Convert the final NumPy array back to list of lists
    return output_np.tolist()