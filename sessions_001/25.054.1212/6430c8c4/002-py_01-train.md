
## example 1
*input:*
```
7 7 0 7
0 7 7 0
0 7 7 7
0 7 7 0
4 4 4 4
0 0 0 0
0 2 0 2
2 2 2 0
2 0 0 2
```
*expected output:*
```
0 0 3 0
3 0 0 0
0 0 0 0
0 0 0 0
```
*transformed output:*
```
3 3 0 3
0 3 3 0
0 3 3 3
0 3 3 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 2
*input:*
```
0 0 7 7
0 0 7 7
0 7 7 0
7 7 0 0
4 4 4 4
2 0 2 0
0 2 0 2
0 2 2 0
0 0 2 0
```
*expected output:*
```
0 3 0 0
3 0 0 0
3 0 0 3
0 0 0 3
```
*transformed output:*
```
0 0 3 3
0 0 3 3
0 3 3 0
3 3 0 0
```
size: True
palette: True
color count: False
pixels off: 13
**FAILED!**

## example 3
*input:*
```
0 0 0 7
0 7 7 7
0 7 0 0
0 7 7 7
4 4 4 4
0 0 2 0
0 2 2 2
2 2 0 0
0 2 0 2
```
*expected output:*
```
3 3 0 0
3 0 0 0
0 0 3 3
3 0 0 0
```
*transformed output:*
```
0 0 0 3
0 3 3 3
0 3 0 0
0 3 3 3
```
size: True
palette: True
color count: False
pixels off: 14
**FAILED!**

## example 4
*input:*
```
7 0 7 0
0 0 7 7
7 0 7 7
7 7 0 0
4 4 4 4
0 0 2 2
0 0 0 0
2 0 0 2
0 2 0 2
```
*expected output:*
```
0 3 0 0
3 3 0 0
0 3 0 0
0 0 3 0
```
*transformed output:*
```
3 0 3 0
0 0 3 3
3 0 3 3
3 3 0 0
```
size: True
palette: True
color count: False
pixels off: 14
**FAILED!**
