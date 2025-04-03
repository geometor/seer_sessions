
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 0 0
0 2 4 2 0 3 1 3 0 0 0
0 2 2 2 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 7 7 7
0 0 0 6 4 6 0 0 7 8 7
0 0 0 6 6 6 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 0
0 3 3 3 3 0 0 0 0 4 5 5 4 0
0 3 2 2 3 0 0 0 0 4 5 5 4 0
0 3 2 2 3 0 0 0 0 4 4 4 4 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 7 7 8 0 0 0
0 0 0 0 0 0 0 8 7 7 8 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0
0 0 9 4 4 9 0 0 1 1 1 1 0 0
0 0 9 4 4 9 0 0 1 2 2 1 0 0
0 0 9 9 9 9 0 0 1 2 2 1 0 0
0 0 0 0 0 0 0 0 1 1 1 1 0 0
```


**output:**
```
2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 7 3 0 0 5 5 5 0
0 3 7 3 0 0 5 7 5 0
0 3 3 3 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 4 4 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
```


**output:**
```
7
```

*   **perception**: The input is a 2D grid containing multiple distinct "objects". These objects are contiguous blocks of the same non-zero digit, potentially surrounding a different non-zero digit. The background is represented by the digit 0. The output is a single digit. The task appears to involve identifying specific properties of these objects and selecting one particular digit based on these properties. Specifically, it seems to focus on objects that contain another digit within them.

*   **facts**:
    
```yaml
    task_elements:
      - element: grid
        properties:
          - type: 2D array of integers
          - contains: background (0), objects (non-zero digits)
      - element: object
        properties:
          - type: connected component of non-zero integers
          - composition: typically consists of a primary digit ('main_number')
          - feature: may contain one or more cells of a different non-zero digit ('internal_number') located strictly inside the object's boundary
          - relationship: multiple objects can exist in a grid, separated by background (0)
      - element: internal_number
        properties:
          - type: integer
          - location: inside an object, surrounded by the object's main_number
          - relationship: associated with a specific object and its main_number
      - element: output
        properties:
          - type: single integer
          - derivation: determined by examining properties of objects with internal_numbers
    transformation:
      - action: identify_objects
        input: grid
        output: list of objects with their main_number and internal_number (if present)
      - action: filter_objects
        input: list of objects
        criteria: must contain an internal_number
        output: filtered list of objects
      - action: find_min_main_number
        input: filtered list of objects
        output: minimum main_number among the filtered objects
      - action: select_relevant_objects
        input: filtered list of objects, minimum main_number
        criteria: object's main_number equals the minimum main_number
        output: list of relevant objects
      - action: extract_internal_numbers
        input: list of relevant objects
        output: list of internal_numbers from the relevant objects
      - action: find_max_internal_number
        input: list of internal_numbers
        output: the final single integer output
    relationships:
      - an object is defined by its connected main_number
      - an internal_number is defined by being different from the main_number and fully enclosed within it
      - the final output depends on the internal_number associated with the object(s) having the smallest main_number among those containing an internal_number
    ```


*   **natural language program**:
    1.  Scan the input grid to identify all distinct connected components (objects) formed by non-zero numbers.
    2.  For each identified object, determine its primary constituent number (the 'main number').
    3.  Check if the object encloses one or more cells containing a single, different non-zero number (the 'internal number'). Only consider objects that have such an internal number.
    4.  From the set of objects identified in step 3, find the minimum 'main number'.
    5.  Identify all objects from step 3 whose 'main number' is equal to this minimum value.
    6.  Collect the 'internal number'(s) from these specific objects found in step 5.
    7.  The final output is the maximum value among the collected 'internal number'(s).
