
## example 1
*input:*
```
0 3 0 0
2 2 2 2
0 3 0 0
0 3 0 0
```
*expected output:*
```
4 4 4 0
4 2 4 2
4 4 4 0
0 3 0 0
```
*transformed output:*
```
4 3 4 0
2 2 2 2
4 3 4 0
0 3 0 4
```
size: True
palette: True
color count: False
pixels off: 5
**FAILED!**

## example 2
*input:*
```
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
8 8 8 8 6 8 8 8
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
```
*expected output:*
```
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 4 4 4 0 0
8 8 8 4 6 4 8 8
0 0 0 4 4 4 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
```
*transformed output:*
```
4 0 4 0 6 4 0 4
0 4 0 4 6 0 4 0
4 0 4 0 6 4 0 4
0 4 0 4 6 0 4 0
8 8 8 8 6 8 8 8
4 0 4 0 6 4 0 4
0 4 0 4 6 0 4 0
4 0 4 0 6 4 0 4
```
size: True
palette: True
color count: False
pixels off: 29
**FAILED!**

## example 3
*input:*
```
0 0 1 0 0 0
0 0 1 0 0 0
9 9 1 9 9 9
0 0 1 0 0 0
0 0 1 0 0 0
0 0 1 0 0 0
```
*expected output:*
```
0 0 1 0 0 0
0 4 4 4 0 0
9 4 1 4 9 9
0 4 4 4 0 0
0 0 1 0 0 0
0 0 1 0 0 0
```
*transformed output:*
```
4 0 1 4 0 4
0 4 1 0 4 0
9 9 1 9 9 9
4 0 1 4 0 4
0 4 1 0 4 0
4 0 1 4 0 4
```
size: True
palette: True
color count: False
pixels off: 17
**FAILED!**
