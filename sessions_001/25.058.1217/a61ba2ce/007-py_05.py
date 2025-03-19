import numpy as np

def _find_objects(grid):
    """Finds contiguous blocks of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def _dfs(row, col, color, obj_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            _dfs(row + dr, col + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_coords = []
                _dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:
                  min_r = min(coord[0] for coord in obj_coords)
                  min_c = min(coord[1] for coord in obj_coords)
                  max_r = max(coord[0] for coord in obj_coords)
                  max_c = max(coord[1] for coord in obj_coords)

                  objects.append({
                      'color': grid[r, c],
                      'coords': obj_coords,
                      'top_left':(min_r,min_c),
                      'rows': max_r-min_r+1,
                      'cols': max_c-min_c+1
                  })
    return objects
def analyze_example(input_grid, output_grid):
    input_objects = _find_objects(np.array(input_grid))
    output_objects = _find_objects(np.array(output_grid))

    input_height, input_width = np.array(input_grid).shape
    output_height, output_width = np.array(output_grid).shape

    print(f"  Input: {input_width}x{input_height}")
    for i, obj in enumerate(input_objects):
        print(f"    Object {i+1}:")
        print(f"      Color: {obj['color']}")
        print(f"      rows: {obj['rows']}")
        print(f"      cols: {obj['cols']}")
        print(f"      Size: {len(obj['coords'])}")
        print(f"      Top Left: {obj['top_left']}")

    print(f"  Output: {output_width}x{output_height}")
    for i, obj in enumerate(output_objects):
        print(f"    Object {i+1}:")
        print(f"      Color: {obj['color']}")
        print(f"      rows: {obj['rows']}")
        print(f"      cols: {obj['cols']}")
        print(f"      Size: {len(obj['coords'])}")
        print(f"      Top Left: {obj['top_left']}")

# Example data (replace with your actual data)
train = [
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 7, 7, 0, 0],
        [0, 0, 0, 0, 7, 7, 7, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], [
        [7, 7, 7, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ],
     [
        [6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 9, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 9, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ],
     [
        [9, 9, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ]),
    ([
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ],
     [
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ])
]

for i, (input_grid, output_grid) in enumerate(train):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("-" * 20)
