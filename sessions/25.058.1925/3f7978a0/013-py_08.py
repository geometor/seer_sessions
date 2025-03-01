def get_objects_and_diagonal(grid):
    grid = np.array(grid)
    objects = find_objects(grid)
    primary_diagonal = find_primary_diagonal(grid, objects)
    return objects, primary_diagonal

def check_object_in_subgrid(obj, diagonal):
  if not diagonal: return False
  rows = sorted(list(set([r for r, c in diagonal])))
  cols = sorted(list(set([c for r, c in diagonal])))
  for r,c in obj:
      if r in rows or c in cols:
          return True
  return False

def get_transformation_summary(example):
    input_grid = example['input']
    output_grid = example['output']
    objects, diagonal = get_objects_and_diagonal(input_grid)
    
    input_grid_np = np.array(input_grid)
    output_grid_np = np.array(output_grid)

    objects_in_output = []
    for obj in objects:
      all_present = True
      for r,c in obj:
        if not (0 <= r < output_grid_np.shape[0] and 0 <= c < output_grid_np.shape[1] and output_grid_np[r,c] == input_grid_np[r,c]):
            all_present = False
            break
      if all_present:
        objects_in_output.append(obj)
            
    
    print(f"  Objects: {objects}")
    print(f"  Primary Diagonal: {diagonal}")
    print(f"  Objects in Output: {objects_in_output}")
    
    subgrid_objects = []
    for obj in objects:
        if check_object_in_subgrid(obj, diagonal):
            subgrid_objects.append(obj)
    print(f" Objects intersecting diagonal: {subgrid_objects}")

    in_shape = input_grid_np.shape
    out_shape = output_grid_np.shape
    print(f" In shape: {in_shape}, Out shape: {out_shape}")

    output_matches = np.array_equal(np.array(transform(input_grid)), output_grid_np)
    print(f"  Output Matches Expected: {output_matches}")
    print("---")


task = task_data[0]
for i, example in enumerate(task['train']):
    print(f"Example {i+1}:")
    get_transformation_summary(example)
