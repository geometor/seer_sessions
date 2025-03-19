import numpy as np
from typing import List, Tuple, Dict

def get_objects(grid: np.ndarray) -> List[Dict]:
    """Identifies distinct objects within a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                neighbors.append((nr, nc))
        return neighbors
    
    def bfs(start_row, start_col, color):
        queue = [(start_row, start_col)]
        visited[start_row, start_col] = True
        min_row, min_col = start_row, start_col
        max_row, max_col = start_row, start_col
        coords = []

        while queue:
            row, col = queue.pop(0)
            coords.append((row,col))
            min_row = min(min_row, row)
            min_col = min(min_col, col)
            max_row = max(max_row, row)
            max_col = max(max_col, col)

            for nr, nc in get_neighbors(row, col):
                if not visited[nr, nc] and grid[nr, nc] == color:
                    visited[nr, nc] = True
                    queue.append((nr, nc))
        return {
            "color": int(color),
            "min_row": int(min_row),
            "min_col": int(min_col),
            "max_row": int(max_row),
            "max_col": int(max_col),
            "coords": coords,
        }

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                objects.append(bfs(row, col, grid[row, col]))
    return objects

def analyze_example(input_grid: np.ndarray, output_grid: np.ndarray, predicted_grid: np.ndarray) -> Dict:
    """Analyzes a single input-output example pair."""
    input_objects = get_objects(input_grid)
    output_objects = get_objects(output_grid)
    
    
    # Find the dividing line.
    dividing_line = find_dividing_line(input_grid)
    #Find the object at the dividing line
    min_row, min_col, max_row, max_col, color = find_object_at_line(input_grid, dividing_line)

    
    return {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "input_objects": input_objects,
        "output_objects": output_objects,
        "dividing_line": dividing_line,
        "object_at_line": {
            "min_row": min_row, "min_col": min_col, "max_row": max_row, "max_col": max_col, "color": color
        } if color is not None else None,
        "match": np.array_equal(output_grid, predicted_grid)
    }

def transform(i): #wrap for error handling
    try:
        return globals()['transform'](i)
    except Exception as e:
        return np.full(i.shape, -1) # return -1s to indicate an error

example_data = []
for idx, (input_grid, output_grid) in enumerate(zip(task_train_input_grids, task_train_output_grids)):
    predicted_output = transform(input_grid)
    example_data.append(analyze_example(input_grid, output_grid, predicted_output))

from IPython.display import display, HTML
import json

def display_example_data(example_data):
    """Displays the analysis results in a human-readable format."""
    
    html = "<table>"
    for idx, data in enumerate(example_data):
        html += f"<tr><th colspan='2'>Example {idx}</th></tr>"
        
        html += f"<tr><td>Match</td><td>{data['match']}</td></tr>"
        
        html += f"<tr><td>Input Shape</td><td>{data['input_shape']}</td></tr>"
        html += f"<tr><td>Output Shape</td><td>{data['output_shape']}</td></tr>"
        html += f"<tr><td>Dividing Line</td><td>{data['dividing_line']}</td></tr>"
        html += f"<tr><td>Object at Line</td><td>{data['object_at_line']}</td></tr>"


        html += f"<tr><td>Input Objects</td><td><pre>{json.dumps(data['input_objects'], indent=2)}</pre></td></tr>"
        html += f"<tr><td>Output Objects</td><td><pre>{json.dumps(data['output_objects'], indent=2)}</pre></td></tr>"

    html += "</table>"
    display(HTML(html))

display_example_data(example_data)
