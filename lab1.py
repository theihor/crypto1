import random
import csv
from os import urandom
from math import ceil

class Table:
    def __init__(self, matrix, name = ''):
        self.name = name
        self.content = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.row_names = ['K' + str(i + 1) for i in range(self.n)]
        self.col_names = ['M' + str(i + 1) for i in range(self.m)]

    def fill_none(self):
        for i in range(self.n):
            row = self.content[i]
            for j in range(self.m):
                row[j] = None

    def dump_csv(self, file_name):
        f_out = open(file_name, 'w', encoding = 'utf8')
        writer = csv.writer(f_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL, lineterminator = '\n')
        writer.writerow([self.name] + self.col_names)
        for i in range(self.n):
            line = [self.row_names[i]]
            row = self.content[i]
            for j in range(self.m):
                line.append(str(row[j]))
            writer.writerow(line)
        f_out.close()

    def show(self):
        print([self.name] + self.col_names)
        for i in range(self.n):
            line = [self.row_names[i]]
            row = self.content[i]
            for j in range(self.m):
                line.append(str(row[j]))
            print(line)

def rand(a = 0, b = 100):
    r = int.from_bytes(urandom(1), byteorder='little')
    #print('r =', r)
    return a + round(r * (b - a) / 256.0)

def random_pop(lst):
    if len(lst) == 1:
        x = lst[0]
        lst.clear()
        return x
    i = rand(0, len(lst) - 1)
    print(i)
    x = lst[i]
    lst.remove(x)
    return x

def all_permutations(lst):
    if len(lst) == 1: return [lst]
    elif len(lst) == 2: return [lst, [lst[1], lst[0]]]
    res = []
    for i in lst:
        l = list(lst)
        l.remove(i)
        res += [[i] + p for p in all_permutations(l)]
    return res

def collide(lst, row):
    for r in lst:
        for i in range(len(r)):
            if r[i] == row[i]: return True
    return False

# WARNING: BRUTE FORCE IS USED
def latin_square(n, filter = lambda x: True):
    r = [x + 1 for x in range(n)]
    all_p = all_permutations(r)
    res = []
    for i in r:
        row = random.choice(all_p)
        res += [row]
        all_p = [p for p in all_p if not collide(res, p) and filter(p)]
    return res

# N is number of squares in rectangle
def latin_rectangle(m, N):
    res = []
    for i in range(N):
        res += latin_square(m, lambda x: not x in res)
    return res

def read_config(config_file_name):
    with open(config_file_name, 'r', encoding = 'utf8') as csvfile:    
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL, lineterminator='\n')
        header = next(reader)
        print(header)
        res = []
        for row in reader:
            res.append({'m' : int(row[0]), 'k' : int(row[1]), 'e' : int(row[2])})
        return res

# matrix and config
def apply_config(matrix, conf):
    for c in conf:
        m = c['m'] - 1; k = c['k'] - 1; e = c['e']
        row = next(x for x in matrix if x[m] == e)
        i = matrix.index(row)
        matrix[i] = matrix[k]
        matrix[k] = row
    return matrix

def make_matrix1(m,k,e):
    if m == k and m == e: 
        return latin_square(m)
    elif m < k and m == e:
        res = latin_rectangle(m, ceil(k / m))
        res = res[:k]
    elif m < k and m < e:
        res = latin_rectangle(e, ceil(k / e))
        res = res[:k]
        for row in res:
            row = row[:m]
    else:
        print('Invalid m, k, e parameters')
    return res
   
def prior_probs(n, r = True):
    a = [1] * n
    p = [1.0 / n] * n
    if r:
        s = 0
        for i in range(n): 
            a[i] = rand(1,256)
            s += a[i]
        for i in range(n): 
            p[i] = a[i] / s
    return (a, p)
        

