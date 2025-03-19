import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects within a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                if color != 0:  # Ignore background
                    obj_coords = []
                    dfs(row, col, color, obj_coords)
                    if obj_coords:
                        objects.append({
                            'color': color,
                            'coords': obj_coords,
                            'size': len(obj_coords)
                        })
    return objects

def transform(input_grid):
   
    #get objects
    objects = get_objects(input_grid)
    
    #find largest object
    largest_object = None
    max_size = 0
    
    for obj in objects:
        if obj['size'] > max_size:
            largest_object = obj
            max_size = obj['size']
    
    #if no objects, return input grid
    if largest_object is None:
        return input_grid.copy()
        
    output_grid = np.zeros_like(input_grid)
    
    #get coords of the largest object
    coords = largest_object.get('coords')
    if coords:
      #find the lowest y
      min_y = min(y for x, y in coords)
      #filter for the lowest y
      filtered_coords = [(x,y) for x,y in coords if y == min_y]
    
      for x,y in filtered_coords:
          output_grid[x,y] = largest_object['color']

    return output_grid