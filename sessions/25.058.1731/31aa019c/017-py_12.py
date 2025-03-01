def find_objects(grid):
    """
    Identifies distinct objects in a grid.  An object is a set of connected pixels of the same color.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, object_id):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        objects[object_id]['pixels'].append((r, c))
        dfs(r + 1, c, color, object_id)
        dfs(r - 1, c, color, object_id)
        dfs(r, c + 1, color, object_id)
        dfs(r, c - 1, color, object_id)

    object_id = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                objects[object_id] = {'color': grid[r, c], 'pixels': []}
                dfs(r, c, grid[r, c], object_id)
                object_id += 1

    return objects

def detect_l_shape(grid, objects):
    """Detects L-shaped objects within the grid."""
    l_shapes = []
    rows, cols = grid.shape

    for obj_id, obj_data in objects.items():
        pixels = obj_data['pixels']
        color = obj_data['color']
        
        # Check for 2x2 blocks
        for r in range(rows - 1):
            for c in range(cols - 1):
                if (grid[r,c] == color and grid[r+1,c] == color and
                    grid[r,c+1] == color and grid[r+1,c+1] == color):
                    #check for a fifth pixel
                    corners = [(r-1,c),(r-1,c+1),(r-1,c+2),(r,c+2),(r+1,c+2),(r+2,c+2),
                               (r+2,c+1),(r+2,c),(r+1,c-1),(r,c-1)]
                    for cr,cc in corners:
                        if 0 <= cr < rows and 0 <= cc < cols and grid[cr,cc] == color:
                            l_shapes.append({'color': color, 'corner':(r,c)}) #corner of 2x2
                            break #found l shape
    return l_shapes

train_pairs = task['train']
input_grid = train_pairs[0]['input']
output_grid = train_pairs[0]['output']

input_objects = find_objects(input_grid)
l_shapes = detect_l_shape(np.array(input_grid), input_objects)

print(l_shapes)
