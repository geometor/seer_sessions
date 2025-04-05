
## train_1

**input:**
```
0 5 5 0 0
5 0 5 0 5
0 0 0 5 0
0 0 5 0 0
0 5 0 5 0
```


**output:**
```
0 2 2 0 0
5 0 2 0 5
0 0 0 5 0
0 0 5 0 0
0 5 0 5 0
```


## train_2

**input:**
```
0 5 5 5 0
5 0 0 0 5
0 5 0 5 0
5 0 5 0 0
0 0 5 0 5
```


**output:**
```
0 2 2 2 0
5 0 0 0 5
0 5 0 5 0
5 0 2 0 0
0 0 2 0 5
```


## train_3

**input:**
```
5 0 5 0 5
0 5 0 5 0
0 0 5 0 5
5 0 5 5 0
0 5 0 0 5
```


**output:**
```
5 0 5 0 5
0 5 0 5 0
0 0 2 0 5
5 0 2 2 0
0 5 0 0 5
```

*   **Perception:** The task involves transforming a 5x5 grid containing integers 0 and 5 into a new 5x5 grid. The output grid contains integers 0, 2, and 5. The transformation seems to selectively change some of the 5s in the input grid to 2s in the output grid, while leaving 0s and other 5s unchanged. The change appears to depend on the local arrangement and connectivity of the cells containing 5. Specifically, it seems related to whether a 5 is part of a sufficiently "dense" cluster of connected 5s.

*   **YAML Facts:**
    
