
## example 1
*input:*
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 9 3 0 0
0 0 7 8 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
8 8 0 0 7 7
8 8 0 0 7 7
0 0 9 3 0 0
0 0 7 8 0 0
3 3 0 0 9 9
3 3 0 0 9 9
```
*transformed output:*
```
8 7 0 0 8 7
3 9 0 0 3 9
0 0 9 3 0 0
0 0 7 8 0 0
8 7 0 0 8 7
3 9 0 0 3 9
```
size: True
palette: True
color count: True
pixels off: 12
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0
0 4 6 0 0 0
0 2 1 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
1 0 0 2 2 0
0 4 6 0 0 0
0 2 1 0 0 0
6 0 0 4 4 0
6 0 0 4 4 0
0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0
0 1 0 0 0 1
0 0 1 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 1 0 0 0 1
```
size: True
palette: True
color count: False
pixels off: 15
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 3 6 0 0
0 0 5 2 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
2 2 0 0 5 5
2 2 0 0 5 5
0 0 3 6 0 0
0 0 5 2 0 0
6 6 0 0 3 3
6 6 0 0 3 3
```
*transformed output:*
```
2 5 0 0 2 5
6 3 0 0 6 3
0 0 3 6 0 0
0 0 5 2 0 0
2 5 0 0 2 5
6 3 0 0 6 3
```
size: True
palette: True
color count: True
pixels off: 12
**FAILED!**
