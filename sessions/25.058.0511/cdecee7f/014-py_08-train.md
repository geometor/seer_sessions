
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
3 1 8
9 7 6
0 0 0
```
*transformed output:*
```
8 9 7
3 1 6
0 0 0
```
size: True
palette: True
color count: True
pixels off: 5
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 2
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
9 3 4
5 8 6
2 0 0
```
*transformed output:*
```
3 5 9
6 8 4
2 0 0
```
size: True
palette: True
color count: True
pixels off: 5
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 3
0 0 5 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
2 4 5
1 9 3
5 1 3
```
*transformed output:*
```
2 1 3
5 4 1
5 9 3
```
size: True
palette: True
color count: True
pixels off: 6
**FAILED!**
