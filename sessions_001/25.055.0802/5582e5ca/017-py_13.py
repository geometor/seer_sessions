import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in a grid.  An object is a contiguous region
    of the same color.  Uses a simple flood-fill algorithm.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def flood_fill(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        flood_fill(row + 1, col, color, object_pixels)
        flood_fill(row - 1, col, color, object_pixels)
        flood_fill(row, col + 1, color, object_pixels)
        flood_fill(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                flood_fill(row, col, color, object_pixels)
                if object_pixels:
                    objects.append({
                        'color': color,
                        'pixels': object_pixels,
                        'bounding_box': (min(p[0] for p in object_pixels), min(p[1] for p in object_pixels),
                                         max(p[0] for p in object_pixels), max(p[1] for p in object_pixels)),
                        'area': len(object_pixels)
                    })
    return objects

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair and returns a report.
    """
    input_objects = get_objects(input_grid)
    output_objects = get_objects(output_grid)

    report = {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'input_object_count': len(input_objects),
        'output_object_count': len(output_objects),
        'input_colors': list(np.unique(input_grid)),
        'output_colors': list(np.unique(output_grid)),
        'input_objects': [{'color': obj['color'], 'area': obj['area'], 'bounding_box': obj['bounding_box']} for obj in input_objects],
        'output_objects': [{'color': obj['color'], 'area': obj['area'], 'bounding_box': obj['bounding_box']} for obj in output_objects],
    }
    return report

#This will be called for each example
# analyze_example(input_grid, output_grid)