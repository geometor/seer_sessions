import numpy as np
from collections import Counter
from typing import List, Tuple, Set, Dict

"""
Identifies frame objects (assumed to be blue/color 1 and green/color 3 based on examples) and a single 'target inner color' present within the frames but not part of the background or frames.
Counts the occurrences of the target inner color strictly inside the bounding box of each frame object, excluding the frame pixels themselves.
Constructs a 1D output grid by concatenating repetitions of each frame's color, where the number of repetitions equals the count of inner pixels found inside that frame.
The order in the output corresponds to the frame colors sorted numerically (blue before green). Frames with zero inner pixels are omitted from the output.
"""

def find_objects(grid: np.ndarray) -> List[Tuple[int, Set[Tuple[int, int]]]]:
    """
    Finds connected components of the same non-background color in the grid.

    Args:
        grid: The input numpy array grid.

    Returns:
        A list of tuples, where each tuple contains:
        - color (int): The color of the object.
        - coordinates (Set[Tuple[int, int]]): A set of (row, col) tuples representing the object's pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip background and visited pixels
            if color == 0 or visited[r, c]:
                continue

            # Start BFS for a new object
            obj_coords = set()
            q = [(r, c)]
            visited[r, c] = True

            while q:
                row, col = q.pop(0)
                obj_coords.add((row, col))

                # Check neighbors (4-connectivity: up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    # Check bounds and if neighbor is same color and not visited
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       not visited[nr, nc] and grid[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))
            
            if obj_coords:
                 objects.append((color, obj_coords))

    return objects

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return 0, 0, 0, 0
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on counting inner pixels within frame objects.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the 1D output grid.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Find all non-background objects
    all_objects = find_objects(grid)

    # 2. Identify frame objects (assuming colors 1 and 3 based on examples)
    #    and collect all frame coordinates
    frame_objects: Dict[int, Set[Tuple[int, int]]] = {}
    all_frame_coords: Set[Tuple[int, int]] = set()
    frame_colors_present = set()

    for color, coords in all_objects:
        # Heuristic: Assume frames are colors 1 (blue) or 3 (green) for now
        # If multiple objects of the same frame color exist, merge their coordinates.
        # This might need adjustment if distinct frames of the same color are possible.
        if color in [1, 3]:
            frame_colors_present.add(color)
            if color not in frame_objects:
                frame_objects[color] = set()
            frame_objects[color].update(coords)
            all_frame_coords.update(coords)

    # 3. Identify the 'target inner color'
    potential_inner_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in all_frame_coords:
                potential_inner_pixels.append(grid[r, c])

    target_inner_color = -1 # Default if no inner pixels found
    if potential_inner_pixels:
        # Assume the most frequent non-frame, non-background color is the target
        color_counts = Counter(potential_inner_pixels)
        if color_counts:
            target_inner_color = color_counts.most_common(1)[0][0]

    # If no inner color is found, the output should logically be empty.
    if target_inner_color == -1:
         return [[]] # Represent empty 1D grid

    # 4. Count inner pixels for each frame and build output
    output_pixels = []
    # Process frames in sorted color order (1 then 3)
    for frame_color in sorted(list(frame_colors_present)):
        if frame_color not in frame_objects:
            continue

        frame_coords = frame_objects[frame_color]
        min_r, max_r, min_c, max_c = get_bounding_box(frame_coords)
        inner_pixel_count = 0

        # Iterate within the bounding box
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Check if pixel is inside bounding box, is the target color,
                # AND is not part of the frame itself
                if (r, c) not in frame_coords and grid[r, c] == target_inner_color:
                    inner_pixel_count += 1

        # Append the frame color to the output list 'count' times
        output_pixels.extend([frame_color] * inner_pixel_count)

    # 5. Format output as a 1xN grid (list of lists)
    if not output_pixels:
        return [[]] # Handle cases where no inner pixels were counted for any frame
    else:
        return [output_pixels]
