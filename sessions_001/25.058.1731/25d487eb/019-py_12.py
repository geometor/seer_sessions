import numpy as np

def analyze_grids(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        # Find red pixels
        red_pixels = np.argwhere(input_grid == 2).tolist()

        # Find green regions
        green_regions = []
        visited = np.zeros_like(input_grid, dtype=bool)
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r, c] == 3 and not visited[r, c]:
                    region = []
                    stack = [(r, c)]
                    visited[r, c] = True
                    while stack:
                        row, col = stack.pop()
                        region.append((row, col))
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < input_grid.shape[0] and 0 <= nc < input_grid.shape[1] and input_grid[nr, nc] == 3 and not visited[nr, nc]:
                                stack.append((nr, nc))
                                visited[nr, nc] = True
                    green_regions.append(region)

        # Check if red pixels are within green regions
        red_in_green = []
        for red_pixel in red_pixels:
            for region in green_regions:
                if red_pixel in region:
                    red_in_green.append(red_pixel)
                    break

        results.append({
            'red_pixels': red_pixels,
            'green_regions': [[{'row': r, 'col': c} for r, c in region] for region in green_regions],
            'red_in_green': red_in_green
        })

    return results

# the function 'get_task_data' is not defined here, because the context is unknown.
#task_data = get_task_data()
#analysis_results = analyze_grids(task_data)
#print(analysis_results)

# the following lines simulate a response in the notebook
task_data = {
 'train': [
  {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0], [0, 0, 0, 3, 2, 3, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
  'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0], [0, 0, 0, 3, 2, 3, 0, 0], [0, 0, 0, 3, 2, 3, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0]]},
  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 2, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 2, 3, 0, 0, 0], [0, 0, 0, 3, 2, 3, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0]]},
  {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 2, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0]],
   'output': [[0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 3, 0], [0, 3, 3, 3, 2, 3, 0], [0, 3, 3, 3, 2, 3, 0], [0, 3, 3, 3, 2, 3, 0], [0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0]]},
  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0]]}
 ]
}
analysis_results = analyze_grids(task_data)
print(analysis_results)