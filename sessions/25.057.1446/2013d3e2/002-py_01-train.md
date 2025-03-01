
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 6 8 8 6 0 0 0
0 0 7 8 4 4 8 7 0 0
0 0 7 8 4 4 8 7 0 0
0 0 0 6 8 8 6 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 7
0 6 8
7 8 4
```
*transformed output:*
```
0 0 7 7 0 0
0 6 8 8 6 0
7 8 4 4 8 7
7 8 4 4 8 7
0 6 8 8 6 0
0 0 7 7 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0
0 0 3 6 5 3 0 0 0 0
0 0 5 2 2 6 0 0 0 0
0 0 6 2 2 5 0 0 0 0
0 0 3 5 6 3 0 0 0 0
0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
1 0 0
0 3 6
0 5 2
```
*transformed output:*
```
1 0 0 0 0 1
0 3 6 5 3 0
0 5 2 2 6 0
0 6 2 2 5 0
0 3 5 6 3 0
1 0 0 0 0 1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
