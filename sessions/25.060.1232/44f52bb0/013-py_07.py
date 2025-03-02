def describe_grid(grid):
    """
    convert grid to string representation
    """
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def describe_objects(grid):
    """
    simple object detection
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

    object_descriptions = []
    for color, coords in objects.items():
        min_x = min(x for x, _ in coords)
        max_x = max(x for x, _ in coords)
        min_y = min(y for _, y in coords)
        max_y = max(y for _, y in coords)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        object_descriptions.append(
            f"Color {color}: Size {width}x{height} at position ({min_x}, {min_y})"
        )
    return object_descriptions
    

task_data = {
    "train": [
        {
            "input": [
                [8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8]
            ],
            "output": [[1]]
        },
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8]
            ],
            "output": [
                [1, 1],
                [1, 1]
            ]
        },
        {
            "input": [
                [8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8]
            ],
            "output": [
                [1, 1, 1],
                [1, 1, 1]
            ]
        },
        {
            "input":[
                [8, 8, 8, 8],
                [8, 8, 8, 8],
                [8, 8, 8, 8]
            ],
            "output": [[1, 1, 1, 1]]
        }
    ],
    "test": [
        {
            "input": [
                [8, 8, 8],
                [8, 8, 8]
            ]
        }
    ]
}

for i, example in enumerate(task_data["train"]):
    input_grid = example["input"]
    output_grid = example["output"]
    input_objects = describe_objects(input_grid)
    output_objects = describe_objects(output_grid)

    print(f"Example {i+1}:")
    print(f"Input shape: {np.array(input_grid).shape}")
    print(f"Output shape: {np.array(output_grid).shape}")
    print(f"Input Objects: {input_objects}")
    print(f"Output Objects: {output_objects}")
    print("-" * 20)