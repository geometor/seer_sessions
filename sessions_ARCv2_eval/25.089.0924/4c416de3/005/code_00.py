import numpy as np
import math
from scipy.ndimage import label
from collections import Counter

"""
Transformation Rule:

1. Identify the background color (BGC) as the most frequent color in the grid, 
   preferring non-white colors if multiple have the same max frequency.
2. Find all distinct contiguous regions of white (0) pixels using connected components labeling.
3. For each white region:
    a. Determine its bounding box (minimum and maximum row and column indices: r_min, c_min, r_max, c_max).
    b. Identify the four potential 'corner anchor' pixels located diagonally outside the bounding box:
       - Top-Left (TL): (r_min - 1, c_min - 1)
       - Top-Right (TR): (r_min - 1, c_max + 1)
       - Bottom-Left (BL): (r_max + 1, c_min - 1)
       - Bottom-Right (BR): (r_max + 1, c_max + 1)
    c. Validate these corner anchors: They must be within the grid boundaries and have the background color (BGC). Keep track of valid anchors.
    d. Find all 'color pixels' associated with the current white region. A color pixel is associated if:
       - It is not white (0) and not the BGC.
       - It is either located within the bounding box of the white region OR is cardinally adjacent (up, down, left, right) to any white pixel belonging to the region.
    e. Assign a color to each valid corner anchor based on proximity to the associated color pixels:
       - For each associated color pixel, calculate its Euclidean distance to each valid corner anchor.
       - For each corner anchor, determine which associated color pixel is closest to it.
       - Assign the color of this closest color pixel to the corner anchor. Ties are broken by the order in which color pixels are processed (the last closest pixel encountered determines the color).
    f. For each corner anchor that received a color assignment, paint a 2x2 block in the output grid using that assigned color. The top-left coordinate of the 2x2 block depends on the corner anchor type:
        - TL anchor at (ar, ac) paints block starting at (ar, ac + 1)
        - TR anchor at (ar, ac) paints block starting at (ar, ac - 1)
        - BL anchor at (ar, ac) paints block starting at (ar - 1, ac + 1)
        - BR anchor at (ar, ac) paints block starting at (ar - 1, ac - 1)
       Ensure the painting stays within grid bounds.
4. Initialize the output grid as a copy of the input grid. The painting of 2x2 blocks modifies this copy. Pixels not part of these painted blocks retain their original color.
"""

# === Helper Functions ===

def find_background_color(grid: np.ndarray) -> int:
    """
    Finds the most frequent color in the grid.
    Prefers non-white if counts are equal.
    """
    colors, counts = np.unique(grid, return_counts=True)
    
    # If only one color exists, it's the background
    if len(colors) == 1:
        return colors[0]

    # Separate white and non-white counts
    white_count = 0
    non_white_colors = []
    non_white_counts = []
    for color, count in zip(colors, counts):
        if color == 0:
            white_count = count
        else:
            non_white_colors.append(color)
            non_white_counts.append(count)

    # Find the most frequent non-white color
    if non_white_counts:
        max_non_white_count = max(non_white_counts)
        most_frequent_non_white = [
            non_white_colors[i] for i, count in enumerate(non_white_counts) if count == max_non_white_count
        ]
        # If the most frequent non-white count is >= white count, return one of them (e.g., the first)
        if max_non_white_count >= white_count:
             # Return the smallest color value among most frequent non-white in case of ties
            return min(most_frequent_non_white)
        else:
            # White is strictly most frequent
            return 0
    else:
        # Only white exists
        return 0


def get_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a list of coordinates."""
    if not coords:
        return None
    rows, cols = zip(*coords)
    return min(rows), min(cols), max(rows), max(cols)

def euclidean_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """Calculates Euclidean distance between two points (r1, c1) and (r2, c2)."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_associated_color_pixels(grid: np.ndarray, 
                                region_coords_set: set[tuple[int, int]], 
                                bbox: tuple[int, int, int, int], 
                                bgc: int) -> list[tuple[tuple[int, int], int]]:
    """
    Finds color pixels (non-white, non-BGC) associated with a white region.
    Association means within the bounding box or cardinally adjacent to the region's white pixels.
    """
    height, width = grid.shape
    r_min, c_min, r_max, c_max = bbox
    associated_pixels = []
    processed_coords = set()  # Avoid duplicates

    # 1. Check inside bounding box (inclusive)
    # Iterate using numpy slicing for potential efficiency if needed, but direct iteration is clearer here.
    for r in range(r_min, r_max + 1):
        for c in range(c_min, c_max + 1):
            coord = (r, c)
             # Ensure coord is valid (though bbox should guarantee this unless 1x1 region)
            if 0 <= r < height and 0 <= c < width:
                color = grid[r, c]
                # Check if it's a color pixel (not white, not BGC)
                if color != 0 and color != bgc:
                    if coord not in processed_coords:
                        associated_pixels.append((coord, color))
                        processed_coords.add(coord)

    # 2. Check cardinal adjacency to white pixels in the region
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # R, L, D, U
    for wr, wc in region_coords_set:
        for dr, dc in directions:
            nr, nc = wr + dr, wc + dc
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                coord = (nr, nc)
                # Check if already processed (could be inside bbox too)
                if coord not in processed_coords:
                    color = grid[nr, nc]
                    # Check if it's a color pixel
                    if color != 0 and color != bgc:
                        associated_pixels.append((coord, color))
                        processed_coords.add(coord)
                        
    return associated_pixels

def paint_block(grid: np.ndarray, start_r: int, start_c: int, color: int):
    """Paints a 2x2 block starting at (start_r, start_c), checking bounds."""
    height, width = grid.shape
    for r_offset in range(2):
        for c_offset in range(2):
            paint_r, paint_c = start_r + r_offset, start_c + c_offset
            # Check bounds before painting
            if 0 <= paint_r < height and 0 <= paint_c < width:
                grid[paint_r, paint_c] = color


# === Main Transform Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on white regions, corner anchors, 
    and closest associated color pixels, painting 2x2 blocks.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array) # Initialize output grid
    height, width = input_array.shape

    # 1. Identify background color
    bgc = find_background_color(input_array)

    # 2. Find white regions using connected components labeling
    # structure defines connectivity (4-connectivity: cardinal directions)
    structure = np.array([[0,1,0], [1,1,1], [0,1,0]], dtype=bool) 
    white_mask = (input_array == 0)
    labeled_array, num_labels = label(white_mask, structure=structure)

    # 3. Process each distinct white region
    for i in range(1, num_labels + 1):
        # Get coordinates of all pixels in the current region
        region_coords = list(zip(*np.where(labeled_array == i)))
        if not region_coords:
            continue # Skip if region is empty (shouldn't happen with label)
            
        region_coords_set = set(region_coords)

        # a. Calculate bounding box
        bbox = get_bounding_box(region_coords)
        if bbox is None: continue # Should also not happen if region_coords not empty
        r_min, c_min, r_max, c_max = bbox

        # b. & c. Identify and validate corner anchor pixels
        potential_anchors = {
            "TL": (r_min - 1, c_min - 1),
            "TR": (r_min - 1, c_max + 1),
            "BL": (r_max + 1, c_min - 1),
            "BR": (r_max + 1, c_max + 1)
        }
        valid_anchors = {}
        for name, (ar, ac) in potential_anchors.items():
            # Check bounds and if the anchor pixel has the background color
            if 0 <= ar < height and 0 <= ac < width and input_array[ar, ac] == bgc:
                valid_anchors[name] = (ar, ac)

        # If no valid anchors found for this region, skip to the next region
        if not valid_anchors: 
             continue

        # d. Find associated color pixels (non-white, non-BGC) for this region
        color_pixels = get_associated_color_pixels(input_array, region_coords_set, bbox, bgc)
        
        # If no associated color pixels found, skip to the next region
        if not color_pixels: 
            continue

        # e. Assign colors to anchors based on closest color pixel
        # Initialize assignments with infinite distance and no color
        assignments = {name: {'dist': float('inf'), 'color': None} for name in valid_anchors}
        
        # Iterate through each associated color pixel
        for pixel_coord, color in color_pixels:
            # Compare its distance to each valid anchor
            for name, anchor_coord in valid_anchors.items():
                d = euclidean_distance(pixel_coord, anchor_coord)
                # If this pixel is closer than the current closest, update the assignment
                # Using '<=' implicitly handles ties by favoring the last processed pixel
                if d <= assignments[name]['dist']: 
                    assignments[name]['dist'] = d
                    assignments[name]['color'] = color

        # f. Paint 2x2 blocks based on assignments
        for name, anchor_coord in valid_anchors.items():
            assigned_color = assignments[name]['color']
            # Only paint if a color was actually assigned (dist wasn't infinity)
            if assigned_color is not None:
                ar, ac = anchor_coord
                start_r, start_c = -1, -1 # Initialize invalid start coords

                # Determine the top-left corner of the 2x2 block based on anchor type
                if name == "TL":
                    start_r, start_c = ar, ac + 1
                elif name == "TR":
                    start_r, start_c = ar, ac - 1
                elif name == "BL":
                    start_r, start_c = ar - 1, ac + 1
                elif name == "BR":
                    start_r, start_c = ar - 1, ac - 1

                # Paint the 2x2 block using the helper function (handles bounds)
                if start_r != -1: # Check if start coords were set
                    paint_block(output_array, start_r, start_c, assigned_color)

    # Convert the final NumPy array back to a list of lists
    return output_array.tolist()