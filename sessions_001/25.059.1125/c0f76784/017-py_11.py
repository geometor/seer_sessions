import numpy as np

def analyze_example(input_grid, output_grid):
    def find_objects(grid, color):
        objects = []
        visited = np.zeros_like(grid, dtype=bool)

        def is_valid(x, y):
            return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

        def dfs(x, y, current_object):
            if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
                return
            visited[x, y] = True
            current_object.append((x, y))
            dfs(x + 1, y, current_object)
            dfs(x - 1, y, current_object)
            dfs(x, y + 1, current_object)
            dfs(x, y - 1, current_object)

        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if grid[x, y] == color and not visited[x, y]:
                    current_object = []
                    dfs(x, y, current_object)
                    objects.append(current_object)
        return objects
    
    def get_outline(obj):
      outline = set()
      for x, y in obj:
          is_outline = False
          for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
              nx, ny = x + dx, y + dy
              if not (0 <= nx < 30 and 0 <= ny < 30 and (nx, ny) in obj): # Simplified border check
                  is_outline = True
                  break
          if is_outline:
              outline.add((x,y))
      return outline

    input_grey_objects = find_objects(input_grid, 5)
    output_grey_objects = find_objects(output_grid, 5)
    output_azure_objects = find_objects(output_grid, 8)
    output_orange_objects = find_objects(output_grid, 7)
    
    analysis = {
      'input_grey_objects': [],
      'output_grey_objects': [],
      'output_azure_objects': [],
      'output_orange_objects': []
    }

    for obj in input_grey_objects:
      coords = [{'x': p[0], 'y': p[1]} for p in obj]
      analysis['input_grey_objects'].append({'coordinates': coords, 'outline': [{'x':p[0],'y':p[1]} for p in get_outline(obj)]})
    
    for obj in output_grey_objects:
      coords = [{'x': p[0], 'y': p[1]} for p in obj]
      analysis['output_grey_objects'].append({'coordinates': coords, 'outline': [{'x':p[0],'y':p[1]} for p in get_outline(obj)]})
    
    for obj in output_azure_objects:
      coords = [{'x': p[0], 'y': p[1]} for p in obj]
      analysis['output_azure_objects'].append({'coordinates': coords, 'outline': [{'x':p[0],'y':p[1]} for p in get_outline(obj)]})

    for obj in output_orange_objects:
      coords = [{'x': p[0], 'y': p[1]} for p in obj]
      analysis['output_orange_objects'].append({'coordinates': coords, 'outline': [{'x':p[0],'y':p[1]} for p in get_outline(obj)]})
    
    return analysis