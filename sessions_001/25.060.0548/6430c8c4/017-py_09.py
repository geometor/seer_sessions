def report(grid):
    grid = np.array(grid)
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    num_unique_colors = len(unique_colors)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    print(f"Dimensions: {rows}x{cols}")
    print(f"Unique Colors: {unique_colors}")
    print(f"Number of Unique Colors: {num_unique_colors}")
    print(f"Color Counts: {color_counts}")
    #detect solid object
    objects = {}
    for color in unique_colors:
      first = np.argwhere(grid==color)
      if len(first) > 0:
        objects[color] = {
            'first': first[0].tolist(),
            'count': len(first)
        }
    print("objects:")
    print(objects)

examples = task["train"]
for i, example in enumerate(examples):
    print(f"--- Example {i+1} Input ---")
    report(example['input'])
    print(f"--- Example {i+1} Output ---")
    report(example['output'])
    print("\n")
