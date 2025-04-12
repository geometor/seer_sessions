"""
Identifies the non-white color (1-9) that appears the least number of times (minimum pixel frequency) in the input grid.
If there is a tie for the minimum pixel frequency, the tie is broken by selecting the color among the tied candidates that forms the maximum number of distinct contiguous objects (connected horizontally/vertically).
The output is the single integer value of the selected color.
"""

from collections import Counter, deque
import math

def find_objects(grid: list[list[int]], color: int) -> int:
    """
    Counts the number of distinct contiguous objects of a given color in the grid.
    Objects are formed by pixels connected horizontally or vertically.

    Args:
        grid: The input grid (list of lists of integers).
        color: The color of the objects to count.

    Returns:
        The total number of distinct objects of the specified color.
    """
    height = len(grid)
    if height == 0:
        return 0
    width = len(grid[0])
    if width == 0:
        return 0

    visited = set()
    object_count = 0

    for r in range(height):
        for c in range(width):
            # Check if the pixel is the target color and not already visited
            if grid[r][c] == color and (r, c) not in visited:
                # Found the start of a new object
                object_count += 1
                # Perform BFS or DFS to find all connected pixels of this object
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    row, col = q.popleft()
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
    return object_count


def transform(input_grid: list[list[int]]) -> int:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid of colors (0-9).

    Returns:
        An integer representing the selected color based on minimum pixel frequency
        and maximum object count tie-breaker. Returns 0 if no non-white colors exist.
    """
    # 1. Calculate pixel frequencies for non-white colors
    pixel_counts = Counter()
    height = len(input_grid)
    width = len(input_grid[0])
    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]
            if color != 0:
                pixel_counts[color] += 1

    # Handle edge case: grid contains only white or is empty
    if not pixel_counts:
        return 0 # Return 0 as per common ARC practice for empty/no-feature cases

    # 2. Find the minimum pixel frequency
    min_frequency = min(pixel_counts.values())

    # 3. Identify colors with this minimum frequency (primary candidates)
    frequency_candidates = [color for color, count in pixel_counts.items() if count == min_frequency]

    # 4. Check if there's only one candidate
    if len(frequency_candidates) == 1:
        return frequency_candidates[0]

    # 5. Tie-breaker: Count objects for each tied candidate
    object_counts = {}
    max_objects = -1
    selected_color = -1

    for candidate_color in frequency_candidates:
        count = find_objects(input_grid, candidate_color)
        object_counts[candidate_color] = count
        # Keep track of the color with the maximum object count found so far
        # If counts are equal, the logic implicitly favors the first one checked,
        # but the problem implies a unique winner from this rule. Let's refine.
        # We need the color corresponding to the *absolute maximum* object count.
        
    # Find the maximum object count among the candidates
    max_object_count_among_candidates = -1
    for color in frequency_candidates:
        if object_counts[color] > max_object_count_among_candidates:
            max_object_count_among_candidates = object_counts[color]
            
    # Identify the color(s) with that maximum object count
    final_candidates = [color for color in frequency_candidates if object_counts[color] == max_object_count_among_candidates]

    # In case of a tie *even after* the object count tie-breaker (unlikely based on examples, but possible),
    # the original problem description for Example 4 suggested picking the smallest color value.
    # Let's assume the object count tie-breaker is sufficient as per the refined hypothesis.
    # If not, we would add `return min(final_candidates)` here.
    # Based on the analysis matching all examples, the object count tie-breaker should be unique.
    if len(final_candidates) == 1:
         return final_candidates[0]
    else:
        # If there's still a tie after the object count tie-breaker,
        # fall back to the smallest color value among the remaining candidates.
        # This handles potential edge cases not explicitly covered by the training examples.
        return min(final_candidates)
