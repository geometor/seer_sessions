def object_report(grid):
    """
    Finds objects in a grid and returns a report.
    An object is a contiguous set of pixels with the same color.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, obj_id):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        objects[obj_id].append((row, col))
        dfs(row + 1, col, color, obj_id)
        dfs(row - 1, col, color, obj_id)
        dfs(row, col + 1, color, obj_id)
        dfs(row, col - 1, color, obj_id)

    obj_id = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                objects[obj_id] = []
                dfs(row, col, color, obj_id)
                obj_id += 1

    report = []
    for obj_id, pixels in objects.items():
        rows = [p[0] for p in pixels]
        cols = [p[1] for p in pixels]
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        color = grid[pixels[0]] # all pixels in object have same color
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        report.append({
            "object_id": obj_id,
            "color": color,
            "min_row": min_row,
            "max_row": max_row,
            "min_col": min_col,
            "max_col": max_col,
            "height": height,
            "width": width,
            "pixels": sorted(pixels) # consistent order for comparison
        })

    return report

import json
def test_all(transform, task_json):

    with open(task_json, 'r') as f:
      data = json.load(f)

    print("TASK: ", task_json)
    train_examples = data['train']
    test_examples = data['test']

    for i, example in enumerate(train_examples):
      print("example: ", i)
      input_grid = np.array(example['input'])
      output_grid = np.array(example['output'])

      input_report = object_report(input_grid)
      output_report = object_report(output_grid)
      print("INPUT REPORT")
      print(input_report)
      print("OUTPUT REPORT")
      print(output_report)

      predicted = transform(input_grid)

      if np.array_equal(predicted,output_grid):
        print("RESULT: PASS")
      else:
        print("RESULT: FAIL")
        print("PREDICTED")
        print(predicted)
        print("EXPECTED")
        print(output_grid)

test_all(transform, "6d0aefbc.json")
