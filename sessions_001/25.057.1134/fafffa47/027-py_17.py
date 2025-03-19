def analyze_example(input_grid, output_grid):
    objects = find_objects(input_grid)
    maroon_object = None
    for obj in objects:
        if obj['color'] == 9:
            maroon_object = obj
            break

    output_red_pixels = []
    if output_grid is not None:
      for r in range(output_grid.shape[0]):
          for c in range(output_grid.shape[1]):
              if output_grid[r, c] == 2:
                  output_red_pixels.append((r, c))

    analysis = {
        'maroon_object_exists': maroon_object is not None,
        'maroon_object_pixels': maroon_object['pixels'] if maroon_object else [],
        'output_red_pixels': output_red_pixels,
    }
    return analysis

def show_grid(grid, title):
  if grid is None:
    return title + ': None'
  return title + ':\n' + str(grid)

examples = [
    # example 1
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 9, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 9, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])
    ),
    # example 2
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([
            [2, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])
    ),
    # example 3
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([
            [0, 2, 0],
            [0, 0, 0],
            [0, 0, 0]])
    )
]

results = []
for i, (input_grid, output_grid) in enumerate(examples):
    print(show_grid(input_grid, f'Example {i+1} Input'))
    print(show_grid(output_grid, f'Example {i+1} Expected Output'))
    predicted_output = transform(input_grid)
    print(show_grid(predicted_output, f'Example {i + 1} Predicted Output'))

    analysis = analyze_example(input_grid, output_grid)
    print(f"Analysis of Example {i+1}:")
    print(f"  Maroon Object Exists: {analysis['maroon_object_exists']}")
    print(f"  Maroon Object Pixels: {analysis['maroon_object_pixels']}")
    print(f"  Expected Output Red Pixels: {analysis['output_red_pixels']}")
    print("-" * 30)
    results.append(analysis)
