Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import collections

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (list[list[int]]): The input grid.
        background_color (int): The background color.

    Returns:
        list[dict]: A list of dictionaries, each representing an object.
                    Each dictionary contains 'color', 'pixels' (a set of (r, c) tuples),
                    and 'rows' (a set of row indices).
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            if (r, c) not in visited and grid[r][c] != background_color:
                color = grid[r][c]
                obj_pixels = set()
                obj_rows = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    obj_rows.add(row)
                    
                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           (nr, nc) not in visited and grid[nr][nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'rows': obj_rows
                })
    return objects

def find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = collections.Counter(pixel for row in grid for pixel in row)
    # Return the most common color, default to 0 if grid is empty or uniform
    if not counts:
        return 0
    return counts.most_common(1)[0][0]

def transform(input_grid):
    """
    Transforms the input grid based on object row span.
    
    Rule:
    1. Identify the background color (most frequent).
    2. Find all contiguous non-background objects, noting their color, pixels, and row span.
    3. Identify objects spanning multiple rows ("multi-row objects").
    4. Create a "pattern template" row:
       - Start with the background color.
       - For each column containing pixels from any multi-row object, set the template's
         pixel in that column to the multi-row object's color. (Assumes one color per column
         among multi-row objects).
    5. Create the output grid (same size as input, initialized to background color).
    6. Process each row of the input grid:
       a. Find all objects confined strictly to the current row ("single-row objects").
       b. If NO single-row objects exist in this row:
          - Copy the "pattern template" row to the corresponding output row.
       c. If one or more single-row objects exist in this row:
          i.  If all these single-row objects have the SAME color:
              - Fill the entire corresponding output row with that color.
          ii. If these single-row objects have DIFFERENT colors:
              - Find the rightmost pixel belonging to any of these single-row objects.
              - Fill the entire corresponding output row with the color of that rightmost pixel's object.
    7. Return the output grid.
    """
    
    height = len(input_grid)
    width = len(input_grid[0])

    # 1. Identify Background Color
    background_color = find_background_color(input_grid)

    # Initialize output grid with background color
    output_grid = [[background_color for _ in range(width)] for _ in range(height)]

    # 2. Find Objects
    objects = find_objects(input_grid, background_color)
    
    # 3. Identify Multi-Row Objects and their pixels
    multi_row_pixels = {} # Map column -> color
    for obj in objects:
        if len(obj['rows']) > 1:
            for r, c in obj['pixels']:
                # Assuming consistency: last seen color for a column prevails if conflict
                multi_row_pixels[c] = obj['color']

    # 4. Create Pattern Template Row
    pattern_template = [background_color] * width
    for c, color in multi_row_pixels.items():
        pattern_template[c] = color

    # Create a lookup for faster access: row -> list of objects intersecting that row
    objects_by_row = collections.defaultdict(list)
    for i, obj in enumerate(objects):
        obj['id'] = i # Assign a unique id for easy reference
        for r in obj['rows']:
            objects_by_row[r].append(obj)

    # 6. Process Rows
    for r in range(height):
        intersecting_objects = objects_by_row[r]

---
