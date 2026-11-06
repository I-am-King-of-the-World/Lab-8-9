# 8-семинар: Хэмминг кодын құру, қатені синдром арқылы табу және түзету. 9-семинар: біркелкі код үшін 2^k >= N шарты бойынша бит санын табу, Фано шартын тексеру және префикстік кодпен хабарды декодтау.


class Hamming:
    def __init__(self, info):
        self.info = info
        self.nk = 0
        while 2 ** self.nk < len(info) + self.nk + 1:
            self.nk += 1
        self.n = len(info) + self.nk
        self.code = []

    def covers(self, position, control):
        b = bin(position)[2:].zfill(self.nk)
        number = bin(control)[2:].zfill(self.nk)
        index = number.index("1")
        return b[index] == "1"

    def encode(self):
        self.code = []
        rest = list(self.info)
        for pos in range(1, self.n + 1):
            if pos in self.controls():
                self.code.append("_")
            else:
                self.code.append(rest.pop(0))
        print("Maket: C =", " ".join(self.code))

        for c in self.controls():
            s = 0
            for pos in range(1, self.n + 1):
                if pos != c and self.covers(pos, c):
                    s += int(self.code[pos - 1])
            self.code[c - 1] = str(s % 2)
        return "".join(self.code)

    def controls(self):
        return [2 ** i for i in range(self.nk)]

    def syndrome(self, received):
        result = ""
        for c in self.controls():
            s = 0
            for pos in range(1, self.n + 1):
                if self.covers(pos, c):
                    s += int(received[pos - 1])
            result = str(s % 2) + result
        return result


class PrefixCode:
    def __init__(self, table):
        self.table = table

    def fano(self):
        words = list(self.table.values())
        for w1 in words:
            for w2 in words:
                if w1 != w2 and w2.startswith(w1):
                    return False
        return True

    def decode(self, message):
        reverse = {}
        for letter in self.table:
            reverse[self.table[letter]] = letter
        out = ""
        current = ""
        for bit in message:
            current += bit
            if current in reverse:
                out += reverse[current]
                current = ""
        return out, current


def uniform_bits(n):
    k = 1
    while 2 ** k < n:
        k += 1
    return k


print("--- 8-seminar ---")
h = Hamming(input("Aqparattyq soz: "))
print("ni =", len(h.info), "nk =", h.nk, "n =", h.n, "baqylau pozitsiyalary:", h.controls())
c = h.encode()
print("Dairyn kod C =", c)

bad = int(input("Burmalangan razriad: "))
c_star = list(c)
c_star[bad - 1] = "1" if c_star[bad - 1] == "0" else "0"
c_star = "".join(c_star)
print("C* =", c_star)

s = h.syndrome(c_star)
pos = int(s, 2)
print("S =", s, "->", pos)
if pos != 0:
    fixed = list(c_star)
    fixed[pos - 1] = "1" if fixed[pos - 1] == "0" else "0"
    print("Tuzetilgen:", "".join(fixed))

print("\n--- 9-seminar ---")
n = int(input("N = "))
print("k =", uniform_bits(n), "bit")

code = PrefixCode({"A": "0", "B": "10", "C": "110", "D": "111"})
if code.fano():
    print("Fano sharty oryndalady.")
else:
    print("Fano sharty oryndalmaidy!")
text, left = code.decode(input("Habar: "))
print("Dekodtau natijesi:", text)
if left:
    print("Songynda tolyq emes bolik qaldy:", left)
