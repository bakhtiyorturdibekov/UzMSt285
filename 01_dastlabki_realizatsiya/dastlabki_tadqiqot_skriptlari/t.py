import re
docx_tab = """05 0d 06 0b 01 0a 0f 08 00 04 07 09 02 0c 03 0e
08 07 02 0e 0f 03 0b 06 01 0c 0d 0a 05 04 09 00
0e 02 0d 04 0c 07 01 0b 06 09 00 05 03 0a 08 0f
00 0e 09 0c 03 0d 07 04 0f 06 05 01 0b 02 0a 08
03 0a 07 02 04 0c 09 01 0e 0d 0f 08 00 05 0b 06
02 03 01 08 00 0e 05 09 0c 0b 06 07 0a 0f 0d 04
0a 04 0e 0f 09 05 08 02 0b 00 01 03 0c 06 07 0d
0b 09 0a 01 06 04 0d 0f 03 05 0e 00 08 07 02 0c
01 00 03 07 0d 0b 0a 0c 09 0e 04 06 0f 08 05 02
04 08 0b 09 0e 06 02 05 0a 03 0c 0f 07 0d 00 01
09 0c 0f 00 02 01 0e 0a 05 08 0b 0d 04 03 06 07
06 0b 08 0d 07 09 00 03 04 0f 0a 02 0e 01 0c 05
0f 01 00 05 0a 08 03 07 0d 02 09 0c 06 0e 04 0b
0c 05 04 0a 0b 02 06 0d 08 07 03 0e 01 00 0f 09
07 0f 0c 06 05 00 04 0e 02 0a 08 0b 0d 09 01 03
0d 06 05 03 08 0f 0c 00 07 01 02 04 09 0b 0e 0a"""
pdf_tab = """05 0d 06 0b 01 0a 0f 08 00 04 07 09 02 0c 03 14
08 07 02 0e 0f 03 0b 06 01 0c 0d 0a 05 04 09 00
14 02 0d 04 0c 07 01 0b 06 09 00 05 03 0a 08 15
00 0e 09 0c 03 0d 07 04 0f 06 05 01 0b 02 0a 08
03 0a 07 02 04 0c 09 01 0e 0d 0f 08 00 05 0b 06
02 03 01 08 00 0e 05 09 0c 0b 06 07 0a 0f 0d 04
0a 04 0e 0f 09 05 08 02 0b 00 01 03 0c 06 07 13
0b 09 0a 01 06 04 0d 0f 03 05 0e 00 08 07 02 12
01 00 03 07 0d 0b 0a 0c 09 0e 04 06 0f 08 05 02
04 08 0b 09 0e 06 02 05 0a 03 0c 0f 07 0d 00 01
09 0c 0f 00 02 01 0e 0a 05 08 0b 0d 04 03 06 07
06 0b 08 0d 07 09 00 03 04 0f 0a 02 0e 01 0c 05
0f 01 00 05 0a 08 03 07 0d 02 09 0c 06 0e 04 11
0c 05 04 0a 0b 02 06 0d 08 07 03 0e 01 00 0f 09
07 0f 0c 06 05 00 04 0e 02 0a 08 0b 0d 09 01 03
0d 06 05 03 08 0f 0c 00 07 01 02 04 09 0b 0e 10"""
D=[int(x,16) for x in docx_tab.split()]
P=pdf_tab.split()
for i,(d,p) in enumerate(zip(D,P)):
    if int(p,16)!=d: print(f"farq: indeks {i} (0x{i:02x}) PDF='{p}' (o'nlik bo'lsa {int(p)}={int(p):#04x}) DOCX={d:02x}")
for r in range(16):
    row=D[16*r:16*r+16]
    if sorted(row)!=list(range(16)): print("qator",r,"permutatsiya emas")
print("Har bir qator 0..f permutatsiyasimi:", all(sorted(D[16*r:16*r+16])==list(range(16)) for r in range(16)))
# columns?
print("Har bir ustun permutatsiyami:", all(sorted(D[c::16])==list(range(16)) for c in range(16)))
import collections; print(collections.Counter(D))
