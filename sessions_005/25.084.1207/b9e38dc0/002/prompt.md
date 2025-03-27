
Previous Code:
```python
import numpy as np
from collections import Counter, deque

"""
Identifies a background color (most frequent) and a fill color (least frequent non-background color).
Performs a flood fill starting from the background pixels adjacent to the grid border,
replacing the background color with the fill color. The fill stops at non-background pixels.
Connectivity is 4-directional (up, down, left, right).
"""

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    # Flatten the grid and count color occurrences
    counts = Counter(grid.flatten())
    # If the grid is empty or has no colors, return a default (e.g., 0 or handle error)
    if not counts:
        return 0 # Default to white/0 if grid is empty
    # Return the color with the highest frequency
    most_common = counts.most_common(1)
    return most_common[0][0]

def find_fill_color(grid, background_color):
    """
    Finds the color to use for filling.
    It's assumed to be the non-background color with the fewest occurrences.
    If there's a tie for the minimum count, the color with the smallest numerical value is chosen.
    """
    counts = Counter()
    # Iterate through the grid to count non-background colors
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            # Only count colors that are not the background
            if color != background_color:
                counts[color] += 1

    # If there are no non-background colors, return the background color itself
    if not counts:
        return background_color

    # Find the minimum count among non-background colors
    min_count = float('inf')
    for count in counts.values():
        if count < min_count:
            min_count = count

    # Collect all colors that have this minimum count
    min_colors = []
    for color, count in counts.items():
        if count == min_count:
            min_colors.append(color)

    # Apply tie-breaking rule: return the smallest color value among those with the minimum count
    if min_colors:
        return min(min_colors)
    else:
        # This case should not be reached if counts is not empty
        return background_color


def transform(input_grid):
    """
    Transforms the input grid by flood-filling the outer background region.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input state for checks
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # If grid is empty, return it as is
    if height == 0 or width == 0:
        return output_grid.tolist()

    # 1. Identify the background color (most frequent)
    background_color = find_most_frequent_color(input_grid_np)

    # 2. Identify the fill color (least frequent non-background color)
    fill_color = find_fill_color(input_grid_np, background_color)

    # If the identified fill color is the same as the background,
    # it implies either only one color exists or something unexpected.
    # In this scenario, no transformation should occur.
    if fill_color == background_color:
        return output_grid.tolist()

    # 3. Perform flood fill starting from background pixels connected to the border
    visited = set()  # Keep track of visited cells to avoid cycles and redundant work
    queue = deque()  # Queue for BFS

    # Initialize the queue with all background-colored pixels located on the grid's border
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on the border
            is_border = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            # Check if it's the background color
            if is_border and input_grid_np[r, c] == background_color:
                # If not already visited, add to queue and visited set
                if (r, c) not in visited:
                    visited.add((r, c))
                    queue.append((r, c))

    # Perform Breadth-First Search (BFS) based flood fill
    while queue:
        r, c = queue.popleft()

        # Change the color of the current background pixel to the fill color in the output grid
        output_grid[r, c] = fill_color

        # Explore 4-directional neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a background pixel and has not been visited yet
                if input_grid_np[nr, nc] == background_color and (nr, nc) not in visited:
                    # Mark as visited and add to the queue for processing
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 3 3 3 3 3 3 1 1 1
1 1 1 1 1 3 1 1 9 1 1 1 3 1 1
1 1 1 1 3 1 1 1 1 3 3 3 1 1 1
1 1 1 1 3 1 1 1 3 1 1 1 1 1 1
1 1 1 1 1 3 1 1 3 1 1 1 1 1 1
1 1 1 1 1 1 3 1 1 3 1 1 1 1 1
1 1 1 1 1 3 1 1 1 1 3 1 1 1 1
1 1 1 1 3 1 1 1 1 1 1 3 1 1 1
1 1 1 1 1 1 1 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 3 3 3 3 3 3 1 1 1
1 1 1 1 1 3 9 9 9 9 9 9 3 1 1
1 1 1 1 3 9 9 9 9 3 3 3 1 1 1
1 1 1 1 3 9 9 9 3 1 1 1 1 1 1
1 1 1 1 1 3 9 9 3 1 1 1 1 1 1
1 1 1 1 1 1 3 9 9 3 1 1 1 1 1
1 1 1 1 1 3 9 9 9 9 3 1 1 1 1
1 1 1 1 3 9 9 9 9 9 9 3 1 1 1
1 1 1 1 9 9 9 5 5 9 9 9 1 1 1
1 1 1 9 9 9 9 1 1 9 9 9 9 1 1
1 1 9 9 9 9 9 1 1 9 9 9 9 9 1
1 9 9 9 9 9 9 1 1 9 9 9 9 9 9
```
Transformed Output:
```
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 3 3 3 3 3 3 9 9 9
9 9 9 9 9 3 9 9 9 1 1 1 3 9 9
9 9 9 9 3 9 9 9 9 3 3 3 9 9 9
9 9 9 9 3 9 9 9 3 9 9 9 9 9 9
9 9 9 9 9 3 9 9 3 9 9 9 9 9 9
9 9 9 9 9 9 3 9 9 3 9 9 9 9 9
9 9 9 9 9 3 9 9 9 9 3 9 9 9 9
9 9 9 9 3 9 9 9 9 9 9 3 9 9 9
9 9 9 9 9 9 9 5 5 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
```
Match: False
Pixels Off: 141
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 125.33333333333333

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 4 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 5 0 5 5 5 5 0
```
Expected Output:
```
4 4 4 4 4 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 5 0 0 0 5 5 5 0
4 4 4 4 4 4 4 4 5 0 5 4 4 5 0
4 4 4 4 4 4 4 4 4 5 4 4 4 5 0
4 4 4 4 4 4 4 4 4 4 4 4 4 5 0
4 4 4 4 4 4 4 4 4 5 4 4 4 5 0
4 4 4 4 4 4 4 4 5 0 5 5 5 5 0
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 5 4 4 4 5 5 5 4
4 4 4 4 4 4 4 4 5 4 5 4 4 5 4
4 4 4 4 4 4 4 4 4 5 4 4 4 5 4
4 4 4 4 4 4 4 4 4 4 4 4 4 5 4
4 4 4 4 4 4 4 4 4 5 4 4 4 5 4
4 4 4 4 4 4 4 4 5 4 5 5 5 5 4
```
Match: False
Pixels Off: 30
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 3:
Input:
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 6 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 9 7 7 7 7 7 9 7 7 7 7 7
7 7 7 7 9 7 7 6 7 7 9 7 7 7 7 7
7 7 7 7 7 9 7 7 7 9 7 7 7 7 7 7
7 7 7 7 7 9 7 7 7 9 7 7 7 7 7 7
7 7 7 7 7 7 9 7 9 7 7 7 7 7 7 7
7 7 7 7 7 7 9 7 9 7 7 7 7 7 7 7
7 7 7 7 7 9 7 7 9 9 9 7 7 7 7 7
7 7 7 7 9 7 7 7 7 3 9 7 7 7 7 7
7 7 7 7 9 7 7 3 3 3 9 7 7 7 7 7
7 7 7 7 7 9 7 3 3 9 7 7 7 7 7 7
7 7 7 7 7 7 9 9 9 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 6 7 7
7 7 6 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 3 3 7 3 7 3 3 3 3 7 7 7 7
7 7 7 7 3 6 3 7 3 3 3 7 7 7 7 7
7 7 7 7 3 3 3 7 3 3 3 7 7 7 7 7
7 7 7 7 9 3 3 7 3 3 9 7 7 7 7 7
7 7 7 7 9 3 3 6 3 3 9 7 7 7 7 7
7 7 7 7 7 9 3 3 3 9 7 7 7 7 7 7
7 7 7 7 7 9 3 3 3 9 7 7 7 7 7 7
7 7 7 7 7 7 9 3 9 7 7 7 7 7 7 7
7 7 7 7 7 7 9 3 9 7 7 7 7 7 7 7
7 7 7 7 7 9 3 3 9 9 9 7 7 7 7 7
7 7 7 7 9 3 3 3 3 3 9 7 7 7 7 7
7 7 7 7 9 3 3 3 3 3 9 7 7 7 7 7
7 7 7 7 7 9 3 3 3 9 7 7 7 7 7 7
7 7 7 7 7 7 9 9 9 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 6 7 7
7 7 6 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 9 8 8 8 8 8 9 8 8 8 8 8
8 8 8 8 9 8 8 6 8 8 9 8 8 8 8 8
8 8 8 8 8 9 8 8 8 9 8 8 8 8 8 8
8 8 8 8 8 9 8 8 8 9 8 8 8 8 8 8
8 8 8 8 8 8 9 8 9 8 8 8 8 8 8 8
8 8 8 8 8 8 9 8 9 8 8 8 8 8 8 8
8 8 8 8 8 9 8 8 9 9 9 8 8 8 8 8
8 8 8 8 9 8 8 8 8 3 9 8 8 8 8 8
8 8 8 8 9 8 8 3 3 3 9 8 8 8 8 8
8 8 8 8 8 9 8 3 3 9 8 8 8 8 8 8
8 8 8 8 8 8 9 9 9 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8
8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 252
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 175.0
