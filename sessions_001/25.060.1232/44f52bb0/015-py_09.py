def get_object_details(grid):
    """
    simple object detection - improved from describe_objects to return coords
    """
    # Convert grid to set of (color, (x,y)) tuples.
    pixels = {(color, (x, y)) for y, row in enumerate(grid) for x, color in enumerate(row)}
    objects = {}
    
    # Group contiguous pixels of same color by flood-fill procedure
    while pixels:
      color, (x,y) = pixels.pop()
      if color not in objects:
        objects[color] = []
      
      stack = [(x,y)]
      
      while stack:
        x,y = stack.pop()
        
        objects[color].append((x,y))

        # check the 4 adjacent neighbors
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nx, ny in neighbors:
            if (color, (nx, ny)) in pixels:
                pixels.remove((color, (nx, ny)))
                stack.append((nx, ny))

    details = {}
    for color, coords in objects.items():
        min_x = min(x for x, _ in coords)
        max_x = max(x for x, _ in coords)
        min_y = min(y for _, y in coords)
        max_y = max(y for _, y in coords)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        details[color] = {
            'coordinates': coords,
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'width': width,
            'height': height
        }
    return details

# Example Usage (replace with actual input grids from the task)
for idx, example in enumerate(task["train"]):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        print(f"Example {idx+1}:")
        print("Input Object Details:")
        print(get_object_details(input_grid))
        print("Output Object Details:")
        print(get_object_details(output_grid))
        print("Output Grid Shape:", output_grid.shape)
        print("---")