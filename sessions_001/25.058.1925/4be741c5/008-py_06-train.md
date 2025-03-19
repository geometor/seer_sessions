
## example 1
*input:*
```
4 4 4 4 4 4 4 2 2 2 2 2 2 2 8 8
4 4 4 4 4 4 4 4 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 4 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 2 2 2 2 2 2 2 8 8 8
4 4 4 4 4 4 2 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 4 2 2 2 2 2 2 8 8 8
4 4 4 4 4 2 2 2 2 2 2 2 2 2 8 8
4 4 4 4 4 2 2 2 2 2 2 2 2 2 8 8
4 4 4 4 2 2 2 2 2 2 2 2 2 8 8 8
4 4 4 4 2 2 2 2 2 2 2 2 8 8 8 8
4 4 4 4 4 2 2 2 2 2 2 2 8 8 8 8
4 4 4 4 4 4 2 2 2 2 2 2 2 8 8 8
```
*expected output:*
```
4 2 8
```
*transformed output:*
```
4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8 4 2 8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 8 8 8 2 2 8
8 8 8 8 8 8 8
8 8 8 8 8 8 8
8 8 8 5 5 8 8
5 8 5 5 5 5 5
5 5 5 5 5 5 5
```
*expected output:*
```
2
8
5
```
*transformed output:*
```
2 2 2 2 8 2 8 8 8 8 5 8 5 8 5 5
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
6 6 6 6 6 6 6 6 6
6 6 4 4 6 6 6 6 6
6 4 4 4 6 4 6 4 4
4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4
4 2 2 4 4 4 2 2 4
2 2 2 2 2 2 2 2 2
2 3 2 2 2 2 2 3 3
3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3
```
*expected output:*
```
6
4
2
3
```
*transformed output:*
```
6 6 4 6 6 4 6 4 6 4 4 4 4 4 2 4 2 4 2 2 3 2 3 3 3
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
