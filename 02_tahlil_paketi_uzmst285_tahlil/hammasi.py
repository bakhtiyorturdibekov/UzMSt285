"""Barcha tahlillarni ketma-ket bajaradi.  Ishlatish:  python hammasi.py [--tez]"""
import subprocess, sys, time
extra = ['--tez'] if '--tez' in sys.argv else []
steps = [['algoritm.py'], ['chiziqli.py'] + extra, ['differensial.py'] + extra, ['algebraik.py'] + extra, ['integral.py'] + extra, ['grafiklar.py']]
for st in steps:
    t = time.time(); print(f"\n=== {st[0]} ===", flush=True)
    r = subprocess.run([sys.executable] + st)
    if r.returncode != 0: sys.exit(f"{st[0]} xato bilan tugadi")
    print(f"({time.time() - t:.0f} s)")
