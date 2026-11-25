# Codice di Emanuele Parmegiani
# Uso: python strumenti/prepara_cestino.py images.jpg cestino.png
# Riporta images.jpg alla sua griglia di pixel, toglie sfondo, manico e coperchio,
# aggiunge la bocca aperta e salva cestino.png (1 pixel = 1 pixel del disegno).
import sys
from collections import Counter
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); W, H = im.size; px = im.load()
g = (424 - 33) / 40; ox = 33 % g; oy = 130 % g          # 1 pixel del disegno = 9,775 px dell'immagine
cols, rows = int((W - ox) // g), int((H - oy) // g)

def cella(i, j):  # media del centro della cella, per togliere il rumore del jpg
    cx, cy = ox + (i + 0.5) * g, oy + (j + 0.5) * g
    pts = [px[int(cx + dx), int(cy + dy)] for dx in (-2, 0, 2) for dy in (-2, 0, 2)]
    return tuple(sum(p[k] for p in pts) // len(pts) for k in range(3))

grid = [[cella(i, j) for i in range(cols)] for j in range(rows)]

# tavolozza: colori più frequenti, ogni cella va al più vicino (via le sfumature del jpg)
dist = lambda a, b: sum((a[k] - b[k]) ** 2 for k in range(3))
tav = []
for c, _ in Counter(c for r in grid for c in r).most_common():
    if all(dist(c, t) > 30 ** 2 for t in tav): tav.append(c)
grid = [[min(tav, key=lambda t: dist(c, t)) for c in r] for r in grid]

# sfondo: bianco collegato ai bordi -> trasparente
bianco = lambda c: sum(c) > 700
fuori = set(); pila = [(i, j) for i in range(cols) for j in (0, rows - 1)] + [(i, j) for j in range(rows) for i in (0, cols - 1)]
while pila:
    i, j = pila.pop()
    if (i, j) in fuori or not (0 <= i < cols and 0 <= j < rows) or not bianco(grid[j][i]): continue
    fuori.add((i, j)); pila += [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]

NERO = (0, 0, 0)
nero = min(tav, key=sum)
chiaro = grid[10][3]                                   # colore chiaro della fascia
BUIO, BUIO2 = (36, 57, 63), (47, 74, 81)

# bocca aperta (4 righe) sopra la fascia del coperchio (righe 9..fine)
L, R = 1, cols - 2                                     # la fascia va da colonna 1 a cols-2
bocca = [[None] * cols for _ in range(4)]
for i in range(L + 2, R - 1): bocca[0][i] = nero
bocca[1][L + 1] = bocca[1][R - 1] = nero
for i in range(L + 2, R - 1): bocca[1][i] = chiaro     # bordo lontano
for y, fondo in ((2, BUIO2), (3, BUIO)):
    bocca[y][L] = bocca[y][R] = nero
    bocca[y][L + 1] = bocca[y][R - 1] = chiaro
    for i in range(L + 2, R - 1): bocca[y][i] = fondo

corpo = [[None if (i, j) in fuori else grid[j][i] for i in range(cols)] for j in range(9, rows - 1)]
righe = bocca + corpo
out = Image.new('RGBA', (cols, len(righe)), (0, 0, 0, 0))
for j, r in enumerate(righe):
    for i, c in enumerate(r):
        if c: out.putpixel((i, j), c + (255,))
out.save(dst)
print('salvato', dst, out.size, 'colori:', len(tav))
