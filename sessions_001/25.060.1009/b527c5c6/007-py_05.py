import numpy as np

def get_objects(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.array(np.where(grid == color)).T

def object_metrics(grid):
  """
  calculate the metrics of the current grid
  - number of colors
  - for each color:
    - count
    - bounding box
  """
  unique_colors = np.unique(grid)
  metrics = {
      "num_colors":len(unique_colors)
  }
  
  for color in unique_colors:
    coords = get_objects(grid,color)
    count = len(coords)
    if count > 0:
      min_row, min_col = np.min(coords, axis=0)
      max_row, max_col = np.max(coords, axis=0)
      bounding_box = {
          'top': int(min_row),
          'left': int(min_col),
          'bottom': int(max_row),
          'right': int(max_col),
          'height': int(max_row - min_row + 1),
          'width': int(max_col - min_col + 1)
          }
    else:
      bounding_box = None
    metrics[int(color)] = {
        'count':count,
        'bounding_box': bounding_box
    }
  return metrics
def show_metrics(metrics, title=None):
    if title:
        print(title)
    for k,v in metrics.items():
        print(f"  {k}:{v}")

def compare_grids(grid1,grid2):
  """
  compare two grids and returnt he differece metrics
  """
  metrics1 = object_metrics(grid1)
  metrics2 = object_metrics(grid2)
  
  show_metrics(metrics1,"GRID 1")
  show_metrics(metrics2, "GRID 2")
  
  diff = {
      "num_colors": metrics2["num_colors"] - metrics1["num_colors"]
  }
  
  for color in metrics1:
    if color in metrics2 and color != "num_colors":
      diff[color] = {}
      diff[color]["count"] = metrics2[color]["count"] - metrics1[color]["count"]
      if metrics1[color]["bounding_box"] is not None and metrics2[color]["bounding_box"] is not None:
        for k in metrics1[color]["bounding_box"]:
          diff[color][k] = metrics2[color]["bounding_box"][k] = metrics1[color]["bounding_box"][k]
  show_metrics(diff,"DIFF")
  return diff