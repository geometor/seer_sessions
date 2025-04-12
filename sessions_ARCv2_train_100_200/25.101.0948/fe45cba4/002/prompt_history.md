
## train_1

**input:**
```
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
2 7 7 7 7 9 9 9
2 2 2 7 7 7 7 7
2 2 2 7 7 2 2 2
2 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
```


**output:**
```
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
7 7 7 7 7 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
```


## train_2

**input:**
```
7 7 7 7 7 9 9 9
9 7 7 7 7 7 9 9
9 9 7 7 7 9 9 9
9 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
```


**output:**
```
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
```

*   **Perception:**
    The task involves grids containing three colors: a background color (orange/7) and two other foreground colors (red/2 and maroon/9). In each example, one of the foreground colors is selected, and its pixels are rearranged into a solid rectangle placed in one of the four corners of the grid. The other foreground color remains unchanged. The background color fills the remaining space.

*   **Observations:**
    *   **Color Selection:** The foreground color chosen for rearrangement appears to be the one whose pixels, in the input grid, touch the most unique edges (Top, Bottom, Left, Right) of the grid.
        *   Example 1: Red (2) touches Left, Bottom, Right (3 edges). Maroon (9) touches Top, Right (2 edges). Red is chosen.
        *   Example 2: Red (2) touches Bottom, Right (2 edges). Maroon (9) touches Top, Left, Right (3 edges). Maroon is chosen.
    *   **Pixel Count:** The total number of pixels of the selected color remains the same between input and output.
    *   **Rectangle Shape:** The pixels are rearranged into a solid rectangle. The dimensions (Height R, Width C) of this rectangle are factors of the total pixel count (N), such that R * C = N, and the difference `abs(R - C)` is minimized. If multiple factor pairs minimize this difference, the pair with the smaller height (R) is chosen.
        *   Example 1: Red count = 16. Factors: (1,16), (2,8), (4,4), (8,2), (16,1). Min diff `abs(R-C)` is 0 for (4,4). Shape is 4x4.
        *   Example 2: Maroon count = 12. Factors: (1,12), (2,6), (3,4), (4,3), (6,2), (12,1). Min diff `abs(R-C)` is 1 for (3,4) and (4,3). Smaller R is 3, so choose (3,4). Shape is 3x4.
    *   **Rectangle Placement:** The rectangle is placed in one of the four corners. The corner seems determined by the two grid edges that the selected color's pixels touched most frequently in the input. The frequency is the count of pixels adjacent to that edge. Ties for the second most frequent edge seem broken by the order: Top > Bottom > Left > Right.
        *   Example 1: Red touches T=0, B=4, L=4, R=6. Highest counts are R(6) and B(4)/L(4). Tie-break B>L. Edges are Right and Bottom. Corner is Bottom-Right.
        *   Example 2: Maroon touches T=3, B=0, L=3, R=5. Highest counts are R(5) and T(3)/L(3). Tie-break T>L. Edges are Right and Top. Corner is Top-Right.
    *   **Other Color:** The foreground color *not* selected for rearrangement remains in its original position.
    *   **Background:** The background color (orange/7) fills all cells not occupied by the rearranged rectangle or the unchanged foreground color.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange pixels of one foreground color into a corner rectangle based on edge contact rules.
    
    elements:
      - element: grid
        properties:
          - background_color: 7 (orange)
          - foreground_colors: [2 (red), 9 (maroon)]
          - height: 8
          - width: 8
      - element: pixel_group
        properties:
          - color: one of the foreground_colors
          - location: various coordinates in the input grid
          - count: number of pixels N
          - edge_contacts: counts of pixels touching [Top, Bottom, Left, Right] edges
    
    actions:
      - action: select_color
        criteria: Choose the foreground color whose pixels touch the most unique grid edges in the input. (If tied, potentially choose the one with more pixels).
        variable: target_color
      - action: count_pixels
        input: target_color pixels in input grid
        output: count N
      - action: determine_rectangle_shape
        input: N
        computation: Find factors (R, C) of N minimizing abs(R-C). Tie-break: choose smaller R.
        output: Height R, Width C
      - action: determine_target_corner
        input: edge_contact counts for target_color
        computation: Find the two edges with the highest contact counts. Tie-break for second edge: T > B > L > R.
        output: target_corner (TL, TR, BL, BR)
      - action: transform_grid
        steps:
          - Copy input grid to output grid.
          - Change all original target_color pixels in output grid to background_color (7).
          - Draw a solid rectangle of target_color with shape (Height R, Width C) in the target_corner.
    
    relationships:
      - The choice of target_color depends on maximizing unique edge contacts in the input.
      - The shape (R, C) of the output rectangle depends on the pixel count N and minimizing abs(R-C).
      - The position (target_corner) of the output rectangle depends on the two most frequent edge contacts in the input.
      - The non-target foreground color pixels are unaffected by the transformation.
    ```


*   **Natural Language Program:**
    1.  Identify the two foreground colors (non-orange) present in the input grid.
    2.  For each foreground color, count how many unique grid edges (Top, Bottom, Left, Right) its pixels are adjacent to.
    3.  Select the foreground color that touches the most unique grid edges as the `target_color`. (If there's a tie in unique edges touched, select the color with the greater total number of pixels).
    4.  Count the total number of pixels (`N`) of the `target_color` in the input grid.
    5.  Find all pairs of integer factors (R, C) such that `R * C = N`. Select the pair (R, C) that minimizes the absolute difference `abs(R - C)`. If there is a tie (e.g., for N=12, both (3,4) and (4,3) give a difference of 1), choose the pair with the smaller value for R. Let the chosen dimensions be `Height = R` and `Width = C`.
    6.  Count how many pixels of the `target_color` touch each of the four grid edges (Top, Bottom, Left, Right) in the input grid.
    7.  Identify the two edges with the highest contact counts. If there is a tie for the second highest count, use the priority order Top > Bottom > Left > Right to break the tie.
    8.  Determine the `target_corner` based on the two selected edges (e.g., Top and Right edges imply the Top-Right corner).
    9.  Create a new grid, initially identical to the input grid.
    10. Change all pixels that originally had the `target_color` to the background color (orange/7).
    11. Draw a solid rectangle of `target_color` with dimensions `Height` x `Width` in the `target_corner` of the grid. The placement rules are:
        *   Top-Left: Rows 0 to `Height-1`, Columns 0 to `Width-1`.
        *   Top-Right: Rows 0 to `Height-1`, Columns `GridWidth-Width` to `GridWidth-1`.
        *   Bottom-Left: Rows `GridHeight-Height` to `GridHeight-1`, Columns 0 to `Width-1`.
        *   Bottom-Right: Rows `GridHeight-Height` to `GridHeight-1`, Columns `GridWidth-Width` to `GridWidth-1`.
    12. The final grid is the result of these modifications.
```python
import math
import numpy as np
from collections import Counter

"""
1. Identify the two foreground colors (non-orange/7) present in the input grid.
2. For each foreground color:
    a. Find all pixel locations.
    b. Count how many unique grid edges (Top, Bottom, Left, Right) its pixels are adjacent to.
3. Select the foreground color ('target_color') that touches the most unique grid edges. If there's a tie, select the color with the greater total number of pixels.
4. Count the total number of pixels ('N') of the 'target_color'.
5. Find the pair of integer factors (R, C) of N such that R * C = N and the absolute difference abs(R - C) is minimized. If there's a tie (e.g., (3,4) vs (4,3)), choose the pair with the smaller R. Let the chosen dimensions be 'Height = R' and 'Width = C'.
6. For the 'target_color', count how many of its pixels touch each of the four grid edges (Top, Bottom, Left, Right).
7. Identify the two edges with the highest contact counts. If there's a tie for the second highest count, use the priority order Top > Bottom > Left > Right to break the tie.
8. Determine the 'target_corner' based on the two selected edges (e.g., Top and Right edges imply Top-Right corner).
9. Create an output grid, initially a copy of the input grid.
10. In the output grid, change all pixels that originally had the 'target_color' to the background color (orange/7).
11. Draw a solid rectangle of 'target_color' with dimensions Height x Width in the 'target_corner' of the output grid.
"""

def get_pixel_locations(grid, color):
    """Finds all locations (row, col) of a given color in the grid."""
    locations = []
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                locations.append((r, c))
    return locations

def get_unique_edge_contacts(grid_height, grid_width, locations):
    """Counts unique edges contacted by pixels at given locations."""
    edges = set()
    for r, c in locations:
        if r == 0:
            edges.add('T')
        if r == grid_height - 1:
            edges.add('B')
        if c == 0:
            edges.add('L')
        if c == grid_width - 1:
            edges.add('R')
    return len(edges)

def get_edge_contact_counts(grid_height, grid_width, locations):
    """Counts how many pixels contact each specific edge."""
    counts = {'T': 0, 'B': 0, 'L': 0, 'R': 0}
    for r, c in locations:
        if r == 0:
            counts['T'] += 1
        if r == grid_height - 1:
            counts['B'] += 1
        if c == 0:
            counts['L'] += 1
        if c == grid_width - 1:
            counts['R'] += 1
    return counts

def find_best_rectangle_shape(n):
    """Finds factors (R, C) of n minimizing abs(R-C), tie-breaking with smaller R."""
    best_shape = (0, 0)
    min_diff = float('inf')

    for r in range(1, int(math.sqrt(n)) + 1):
        if n % r == 0:
            c = n // r
            diff = abs(r - c)
            # Check factor pair (r, c)
            if diff < min_diff:
                min_diff = diff
                best_shape = (r, c)
            elif diff == min_diff:
                # Tie-break: choose smaller R
                if r < best_shape[0]:
                    best_shape = (r, c)
            
            # Check factor pair (c, r) if r*r != n
            if r * r != n:
                diff_rc = abs(c - r) # same diff
                if diff_rc < min_diff: # Should not happen if we proceed iteratively
                     min_diff = diff_rc
                     best_shape = (c, r)
                elif diff_rc == min_diff:
                    # Tie-break: choose smaller R (which is 'c' here)
                     if c < best_shape[0]:
                        best_shape = (c, r)

    # Ensure best_shape is found (handles n=1 case)
    if n==1: return (1,1)
    if best_shape == (0,0) and n > 0 : # fallback for prime or other edge cases, though factors logic should cover it
        factors = []
        for i in range(1, n + 1):
            if n % i == 0:
                 factors.append((i, n//i))
        min_diff_fallback = float('inf')
        for r_f, c_f in factors:
            diff_f = abs(r_f - c_f)
            if diff_f < min_diff_fallback:
                 min_diff_fallback = diff_f
                 best_shape = (r_f, c_f)
            elif diff_f == min_diff_fallback:
                 if r_f < best_shape[0]:
                      best_shape = (r_f, c_f)
                      
    return best_shape


def determine_target_corner(edge_counts):
    """Determines the target corner based on the two highest edge contact counts."""
    # Sort edges by count descending, then by priority T > B > L > R for ties
    edge_priority = {'T': 0, 'B': 1, 'L': 2, 'R': 3}
    sorted_edges = sorted(edge_counts.keys(), key=lambda edge: (-edge_counts[edge], edge_priority[edge]))

    edge1 = sorted_edges[0]
    edge2 = sorted_edges[1]

    # Determine corner based on the top two edges
    if ('T' in [edge1, edge2] and 'L' in [edge1, edge2]): return 'TL'
    if ('T' in [edge1, edge2] and 'R' in [edge1, edge2]): return 'TR'
    if ('B' in [edge1, edge2] and 'L' in [edge1, edge2]): return 'BL'
    if ('B' in [edge1, edge2] and 'R' in [edge1, edge2]): return 'BR'
    
    # Fallback/error case if logic somehow fails (shouldn't happen with 4 edges)
    print(f"Warning: Could not determine corner from edges: {edge1}, {edge2}")
    # Default based on highest edge? E.g. if only one edge has count > 0
    if edge1 == 'T': return 'TL'
    if edge1 == 'B': return 'BL'
    if edge1 == 'L': return 'TL'
    if edge1 == 'R': return 'TR'
    return 'TL' # Default default


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by rearranging pixels of one foreground color 
    (chosen based on edge contact) into a rectangle in a corner (determined 
    by edge contact frequency).
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    background_color = 7

    # 1. Identify foreground colors
    unique_colors = np.unique(input_np)
    foreground_colors = [c for c in unique_colors if c != background_color]

    # Ensure there are exactly two foreground colors as per problem description (or handle otherwise)
    if len(foreground_colors) != 2:
         # Handle error or unexpected input. For now, assume 2.
         # If only one FG color, maybe it's automatically the target?
         # If more than two, how to choose?
         # Let's proceed assuming 2 for now based on examples.
         if len(foreground_colors) == 0: return input_grid # No change if no FG
         if len(foreground_colors) == 1: 
             target_color = foreground_colors[0]
             other_color = -1 # Sentinel
         else: # > 2, maybe pick first two? Arbitrary. Task likely implies 2.
             foreground_colors = foreground_colors[:2]


    # 2 & 3. Find target color based on unique edge contacts, tie-breaking with pixel count
    color_data = {}
    for color in foreground_colors:
        locations = get_pixel_locations(input_np, color)
        unique_edges = get_unique_edge_contacts(height, width, locations)
        pixel_count = len(locations)
        color_data[color] = {'locations': locations, 'unique_edges': unique_edges, 'count': pixel_count}

    # Sort colors: primary key = unique_edges (desc), secondary key = count (desc)
    sorted_colors = sorted(foreground_colors, key=lambda c: (color_data[c]['unique_edges'], color_data[c]['count']), reverse=True)
    target_color = sorted_colors[0]
    # Find the other color (the one not chosen)
    other_color = next((c for c in foreground_colors if c != target_color), None)


    # 4. Count pixels N of target_color
    target_locations = color_data[target_color]['locations']
    n = color_data[target_color]['count']
    if n == 0: # If target color somehow has 0 pixels, return original grid
        return input_grid

    # 5. Determine rectangle shape (Height R, Width C)
    rect_height, rect_width = find_best_rectangle_shape(n)

    # 6. Calculate edge contact counts for target_color
    edge_counts = get_edge_contact_counts(height, width, target_locations)

    # 7 & 8. Determine target corner
    target_corner = determine_target_corner(edge_counts)

    # 9. Output grid is already initialized as a copy

    # 10. Change original target_color pixels to background color
    for r, c in target_locations:
        output_np[r, c] = background_color

    # 11. Draw the rectangle in the target corner
    start_row, start_col = 0, 0
    if target_corner == 'TL':
        start_row, start_col = 0, 0
    elif target_corner == 'TR':
        start_row, start_col = 0, width - rect_width
    elif target_corner == 'BL':
        start_row, start_col = height - rect_height, 0
    elif target_corner == 'BR':
        start_row, start_col = height - rect_height, width - rect_width

    for r in range(start_row, start_row + rect_height):
        for c in range(start_col, start_col + rect_width):
             # Check bounds just in case, although calculation should be correct
            if 0 <= r < height and 0 <= c < width:
                output_np[r, c] = target_color

    # Convert back to list of lists and return
    return output_np.tolist()
```
