from lab1 import *

class System:
    def __init__(self, m, k, e, 
                    conf_file = 'config.csv', 
                    mp_mode = 'random', 
                    message_p = [],
                    kp_mode = 'random',
                    key_p = []
                    ):
        self.m = m
        self.k = k
        self.e = e
        self.conf = read_config(conf_file)
        self.init_f() # f(m,k)
        self.init_message_p(mp_mode, message_p) # Pm
        self.init_key_p(kp_mode, key_p)         # Pk

    def init_f(self):
        self.f = make_matrix1(self.m, self.k, self.e)
        apply_config(self.f, self.conf)
 
    def init_message_p(self, mode = 'random', mp = []):
        if mode == 'random':
            self.message_p = prior_probs(self.m)
        elif mode == 'even':
            self.message_p = prior_probs(self.m, False)
        elif mode == 'exact':
            if mp and len(mp) == self.m: 
                self.message_p = mp
            else: 
                print('Invalid message probabilities provided. Using random mode.')
                self.message_p = prior_probs(self.m)
        else: 
            print('Unsupported message probabilities mode provided. Using random mode.')
            self.message_p = prior_probs(self.m)

    def init_key_p(self, mode = 'random', kp = []):
        if mode == 'random':
            self.key_p = prior_probs(self.k)
        elif mode == 'even':
            self.key_p = prior_probs(self.k, False)
        elif mode == 'zeros':
            p = 1.0 / sum(1 for x in kp if x != 0)
            self.key_p = [p if x != 0 else 0 for x in kp]
        elif mode == 'exact':
            if mp and len(mp) == self.m: 
                self.key_p = kp
            else: 
                print('Invalid keys probabilities provided. Using random mode.')
                self.key_p = prior_probs(self.k)
        else: 
            print('Unsupported keys probabilities mode provided. Using random mode.')
            self.key_p = prior_probs(self.k)

    def fi(self, m, k, e):
        if self.f[k - 1][m - 1] == e: return 1
        else: return 0

    # Pm(e)
    def p_m_e(self, m, e):
        return sum(self.key_p[k - 1] * self.fi(m, k, e) for k in range(1, 1 + self.k))

    def p_m(self, m):
        return self.message_p[m - 1]

    def p_k(self, k):
        return self.key_p[k - 1]

    def p_e(self, e):
        s = 0
        for k in range(1, self.k + 1):
            for m in range(1, self.m + 1):
                s += self.fi(m, k, e) * self.p_m(m) * self.p_k(k)
        return s

    def p_k_e(self, k, e):
        return sum(self.p_m(m) * self.fi(m, k, e) for m in range(1, self.m + 1))

    def p_e_k(self, e, k):
        return self.p_k(k) * self.p_k_e(k, e) / self.p_e(e)

    def compute_posteriori_message_p(self):
        self.pem = []
        for e in range(1, self.e + 1):
            self.pem.append([])
            for m in range(1, self.m + 1):
                self.pem[e - 1].append(self.p_m_e(m, e) * self.p_m(m) / self.p_e(e))

    def compute_pem_diffs(self):
        self.pem_d = []
        for e in range(self.e):
            self.pem_d.append([])
            for m in range(self.m):
                self.pem_d[e].append(self.pem[e][m] - self.message_p[m])

    def get_m(self, k, e):
        if e in self.f[k - 1]:
            return self.f[k - 1].index(e) + 1
        else: return 0

    # Pe(k) / P(m)
    def compute_ratio(self):
        self.ratio = []
        for k in range(1, self.k + 1):
            self.ratio.append([])
            for e in range(1, self.e + 1):
                m = self.get_m(k, e)
                if m != 0:
                    self.ratio[k-1].append(self.p_e_k(e, k) / self.p_m(m))
                else: self.ratio[k-1].append(0)

    def recompute(self):
        self.compute_posteriori_message_p()
        self.compute_pem_diffs()
        self.compute_ratio()

    def full_dump(self, file_name):
        f_out = open(file_name, 'w', encoding = 'utf8')
        writer = csv.writer(f_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL, lineterminator = '\n')
        # f(m,k) 
        writer.writerow(['f(m,k)'] + ['M' + str(i + 1) for i in range(self.m)])
        row_names = ['K' + str(i + 1) for i in range(self.k)]
        for i in range(self.k):
            line = [row_names[i]] + self.f[i]
            writer.writerow(line)

        # P(m)
        writer.writerow([])
        writer.writerow(['P(m)'] + ['M' + str(i + 1) for i in range(self.m)])
        writer.writerow(['P'] + [str(round(p, 3)) for p in self.message_p])

        # P(k)
        writer.writerow([])
        writer.writerow(['P(k)'] + ['K' + str(i + 1) for i in range(self.k)])
        writer.writerow(['P'] + [str(round(p, 3)) for p in self.key_p])

        # Pe(m)
        writer.writerow([])
        writer.writerow(['Pe(m)'] + ['M' + str(i + 1) for i in range(self.m)])
        row_names = ['E' + str(i + 1) for i in range(self.e)]
        for i in range(self.e):
            line = [row_names[i]] + [str(round(p, 3)) for p in self.pem[i]]
            writer.writerow(line)

        # Pe(m) - P(m)
        writer.writerow([])
        writer.writerow(['Pe(m)-P(m)'] + ['M' + str(i + 1) for i in range(self.m)])
        row_names = ['E' + str(i + 1) for i in range(self.e)]
        for i in range(self.e):
            line = [row_names[i]] + [str(round(p, 3)) for p in self.pem_d[i]]
            writer.writerow(line)

        # Pe(k) / P(m)
        writer.writerow([])
        writer.writerow(['Pe(k)/P(m)'] + ['E' + str(i + 1) for i in range(self.e)])
        row_names = ['K' + str(i + 1) for i in range(self.k)]
        for i in range(self.k):
            line = [row_names[i]] + [str(round(p, 3)) for p in self.ratio[i]]
            writer.writerow(line)

        f_out.close()

    def load(self, file_name):
        with open(file_name, 'r', encoding = 'utf8') as csvfile:    
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL, lineterminator='\n')
            # f(m,k)
            header = next(reader)
            self.f = []
            for row in reader:
                #print(row)
                if not row or not row[0] or not row[0][0] == 'K': break
                self.f.append([int(x) for x in row[1:]])
            self.m = len(self.f[0])
            self.k = len(self.f)
            # P(m)
            header = next(reader)
            pm = next(reader)
            print(pm)
            self.message_p = [float(x) for x in pm[1:]]
            # P(k)
            header = next(reader)
            header = next(reader)
            pk = next(reader)
            print(pk)
            self.key_p = [float(x) for x in pk[1:]]
            if 0 in self.key_p:
                self.init_key_p(mode = 'zeros', kp = self.key_p)

            e = 0
            for row in reader:
                if row and row[0] and row[0][0] == 'E':
                    e_ = int(row[0][1:])
                    if e < e_: e = e_
            self.e = e

            self.recompute()






