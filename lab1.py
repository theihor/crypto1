import random
import csv
from os import urandom

class Table:
    def __init__(self, name = '', n = 0, m = 0):
        self.name = name
        self.content = [[0] * m] * n
        self.row_names = ['row'] * n
        self.col_names = ['col'] * m
        self.n = n
        self.m = m

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
    print('r =', r)
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

def gen_random_table(n, m, name = 'f(m,k)'):
    t = Table(name, n, m)
    c = t.content
    for i in range(n):
        available = list(range(m))
        random.shuffle(available)
        c[i] = [0] * m
        for j in range(m):
            print(t.content)
            c[i][j] = random_pop(available)
    t.content = c
    return t

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
def latin_square(n, filter):
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



