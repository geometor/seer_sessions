
## example 1
*input:*
```
0 0 0 2 2
0 0 2 0 2
2 0 0 2 2
2 2 0 0 2
0 0 0 0 2
0 2 0 0 0
4 4 4 4 4
2 0 0 0 0
2 2 0 0 0
2 0 2 0 0
0 0 2 0 0
0 0 0 2 2
2 0 0 2 0
```
*expected output:*
```
3 0 0 3 3
3 3 3 0 3
0 0 3 3 3
3 3 3 0 3
0 0 0 3 0
3 3 0 3 0
```
*transformed output:*
```
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 2
*input:*
```
0 2 2 2 2
0 0 0 0 2
2 0 2 2 2
0 0 2 2 0
2 2 2 2 0
2 2 0 0 2
4 4 4 4 4
0 0 0 0 0
0 0 2 0 0
2 0 0 0 2
0 0 0 2 0
0 2 0 2 0
0 2 2 2 0
```
*expected output:*
```
0 3 3 3 3
0 0 3 0 3
0 0 3 3 0
0 0 3 0 0
3 0 3 0 0
3 0 3 3 3
```
*transformed output:*
```
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 15
**FAILED!**

## example 3
*input:*
```
2 2 0 2 2
2 0 2 2 2
2 0 0 0 0
0 2 0 2 0
2 2 2 0 2
2 0 2 0 0
4 4 4 4 4
2 0 0 2 2
0 0 2 0 2
2 2 0 0 0
0 0 2 0 2
0 2 0 2 2
0 2 2 0 2
```
*expected output:*
```
0 3 0 0 0
3 0 0 3 0
0 3 0 0 0
0 3 3 3 3
3 0 3 3 0
3 3 0 0 3
```
*transformed output:*
```
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 16
**FAILED!**

## example 4
*input:*
```
0 2 0 2 0
2 2 0 2 2
0 2 2 2 0
0 2 2 0 0
0 2 2 2 2
2 0 2 0 2
4 4 4 4 4
2 0 2 2 2
0 2 2 0 0
2 0 2 0 2
2 0 0 0 2
2 2 0 2 0
2 0 2 2 0
```
*expected output:*
```
3 3 3 0 3
3 0 3 3 3
3 3 0 3 3
3 3 3 0 3
3 0 3 0 3
0 0 0 3 3
```
*transformed output:*
```
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 9
**FAILED!**
