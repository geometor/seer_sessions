"""
1. Identify Rectangles: Find all rectangles in the input grid. A rectangle is defined as a contiguous block of pixels of the same color.
2. Filter by Size: Consider only rectangles with a height and width of 3 or greater.
3. Find Largest: Among the rectangles of the same color, identify the largest rectangle, if multiple exists.
4. Locate Subgrid: Within the largest rectangle of a given color, locate the 3x3 subgrid at the top-left corner of that rectangle.
5. Extract Subgrid: Extract this 3x3 subgrid as the output. If multiple largest rectangles of different color exist, select the one iterated first (implicit iteration order by color value).
"""

import numpy as np

def find_rectangles(grid):
    """Finds all rectangles in the grid."""
    rectangles = []
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_rectangle):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        current_rectangle.append((r, c))
        dfs(r + 1, c, color, current_rectangle)
        dfs(r - 1, c, color, current_rectangle)
        dfs(r, c + 1, color, current_rectangle)
        dfs(r, c - 1, color, current_rectangle)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_rectangle = []
                dfs(r, c, grid[r][c], current_rectangle)
                if current_rectangle:
                    # calculate rectangle parameters
                    min_row = min(coord[0] for coord in current_rectangle)
                    max_row = max(coord[0] for coord in current_rectangle)
                    min_col = min(coord[1] for coord in current_rectangle)
                    max_col = max(coord[1] for coord in current_rectangle)
                    height = max_row - min_row + 1
                    width = max_col - min_col + 1
                    rectangles.append(
                        {
                            "color": grid[r][c],
                            "top_left": (min_row, min_col),
                            "height": height,
                            "width": width,
                        }
                    )
    return rectangles

def find_largest_rectangle(rectangles):
    """Finds the largest rectangle of each color."""
    largest_rectangles = {}
    for rect in rectangles:
        color = rect['color']
        if color not in largest_rectangles or (rect['height'] * rect['width'] > largest_rectangles[color]['height'] * largest_rectangles[color]['width']):
            largest_rectangles[color] = rect
    return largest_rectangles

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)

    # Find all rectangles
    rectangles = find_rectangles(grid)

    # Filter rectangles by size (height and width >= 3)
    filtered_rectangles = [
        rect for rect in rectangles if rect["height"] >= 3 and rect["width"] >= 3
    ]

    # Find the largest rectangle of each color
    largest_rectangles = find_largest_rectangle(filtered_rectangles)
    
    # Initialize output (default 3x3 zeros)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the largest rectangles and extract 3x3 subgrid
    for color, rect in largest_rectangles.items():
        top_left_row, top_left_col = rect["top_left"]
        # Extract 3x3 subgrid
        output_grid = grid[top_left_row : top_left_row + 3, top_left_col : top_left_col + 3]
        break # select the first one

    return output_grid.tolist()