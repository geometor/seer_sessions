import numpy as np

def analyze_grid(grid):
    """
    Analyzes a grid to find blue and red regions, their bounding boxes, and the top-left pixel of the blue region.
    """

    def find_contiguous_region(grid, color):
        pixels = np.argwhere(grid == color)
        if len(pixels) == 0:
            return []

        seed = tuple(pixels[0])
        region = set()
        region.add(seed)
        queue = [seed]

        while queue:
            x, y = queue.pop(0)
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for nx, ny in neighbors:
                if (0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and
                    grid[nx, ny] == color and (nx, ny) not in region):
                    region.add((nx, ny))
                    queue.append((nx, ny))

        return list(region)

    def find_top_left(region):
        if not region:
          return None

        min_row = min(pixel[0] for pixel in region)
        min_col_candidates = [pixel for pixel in region if pixel[0] == min_row]
        min_col = min(pixel[1] for pixel in min_col_candidates)
        return (min_row,min_col)
    
    def get_bounding_box(region):
        if not region:
            return None
        min_row = min(r for r, c in region)
        max_row = max(r for r, c in region)
        min_col = min(c for r, c in region)
        max_col = max(c for r, c in region)
        return (min_row, min_col, max_row, max_col)

    blue_region = find_contiguous_region(grid, 1)
    red_region = find_contiguous_region(grid, 2)
    blue_top_left = find_top_left(blue_region)
    blue_bbox = get_bounding_box(blue_region)
    red_bbox = get_bounding_box(red_region)

    return {
        "blue_region": blue_region,
        "red_region": red_region,
        "blue_top_left": blue_top_left,
        "blue_bbox": blue_bbox,
        "red_bbox": red_bbox,
    }

def calculate_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        transformed_grid = transform(input_grid)  # Apply the provided transform function

        input_analysis = analyze_grid(input_grid)
        output_analysis = analyze_grid(output_grid)
        transformed_analysis = analyze_grid(transformed_grid)
        results.append({
          'input':input_analysis,
          'output': output_analysis,
          'transform': transformed_analysis
        })
    return results