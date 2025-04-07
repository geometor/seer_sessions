import numpy as np
from collections import Counter, defaultdict
import copy

"""
Identifies the two non-background colors based on object count and total area, then swaps them.

1. Determine the background color (most frequent color).
2. Identify all non-background colors present in the grid.
3. For each non-background color:
    a. Find all distinct contiguous objects of that color.
    b. Count the number of objects found.
    c. Calculate the total number of pixels (area) for that color.
4. Group the non-background colors by their object count.
5. Determine the minimum object count found.
6. Among the colors with the minimum object count, select the one with the smallest total pixel area. If there's a tie in area, select the color with the highest numerical color value. This is 'color1'.
7. Determine the second minimum object count found.
8. Among the colors with the second minimum object count, select the one with the smallest total pixel area. If there's a tie in area, select the color with the highest numerical color value. This is 'color2'.
9. Create a copy of the input grid.
10. Iterate through the copied grid and swap all occurrences of 'color1' with 'color2'.
11. Return the modified grid.
If there are fewer than two non-background colors, return the original grid unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented by a set
              of (row, col) tuples. Returns an empty list if the color
              is not found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    current_object.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    # Convert input grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # Flatten the array to count color frequencies
    flat_array = input_array.flatten()

    # Count the occurrences of each color
    color_counts = Counter(flat_array)

    # If there are fewer than 3 unique colors (background + 2 others),
    # no swap is possible/needed
    if len(color_counts) < 3:
        return output_array.tolist()

    # Find the most frequent color (background)
    # If there's a tie for most frequent, np.argmax will pick the first one encountered.
    # This usually doesn't matter if the background is dominant.
    background_color = color_counts.most_common(1)[0][0]

    # Identify non-background colors and store their properties
    color_properties = {}
    for color, count in color_counts.items():
        if color != background_color:
            objects = find_objects(input_array, color)
            num_objects = len(objects)
            total_area = count # Total pixels of this color
            if num_objects > 0: # Only consider colors actually forming objects
                 color_properties[color] = {'obj_count': num_objects, 'area': total_area}

    # If there are fewer than 2 non-background colors after analysis,
    # no swap is possible/needed
    if len(color_properties) < 2:
         return output_array.tolist()

    # Group colors by object count
    grouped_by_obj_count = defaultdict(list)
    for color, props in color_properties.items():
        grouped_by_obj_count[props['obj_count']].append({'color': color, 'area': props['area']})

    # Sort object counts to find min and second min
    sorted_obj_counts = sorted(grouped_by_obj_count.keys())

    if len(sorted_obj_counts) < 2:
        # This case handles scenarios where all non-background colors have the same object count.
        # Although the problem description implies finding *two* colors based on *different* counts,
        # let's handle this gracefully by not performing a swap if we can't identify two distinct groups.
        # Alternatively, one could define a tie-breaking rule here too, but sticking to the
        # interpretation derived from Example 1 (min count vs second min count).
        return output_array.tolist()

    min_obj_count = sorted_obj_counts[0]
    second_min_obj_count = sorted_obj_counts[1]

    # Find color1: from the group with min_obj_count
    min_count_group = grouped_by_obj_count[min_obj_count]
    # Sort by area (ascending), then by color value (descending for tie-break)
    min_count_group.sort(key=lambda x: (x['area'], -x['color']))
    color1 = min_count_group[0]['color']

    # Find color2: from the group with second_min_obj_count
    second_min_count_group = grouped_by_obj_count[second_min_obj_count]
    # Sort by area (ascending), then by color value (descending for tie-break)
    second_min_count_group.sort(key=lambda x: (x['area'], -x['color']))
    color2 = second_min_count_group[0]['color']

    # Iterate through the grid and swap the identified colors
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == color1:
                output_array[r, c] = color2
            elif input_array[r, c] == color2:
                output_array[r, c] = color1

    # Return the transformed grid as a list of lists
    return output_array.tolist()