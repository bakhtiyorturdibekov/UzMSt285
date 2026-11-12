import io, sys, json, contextlib, traceback, time
from cells import CELLS
ns={'__name__':'__main__'}; nb_cells=[]; cnt=0
for kind,src in CELLS:
    if kind=='markdown':
        nb_cells.append({"cell_type":"markdown","metadata":{},"source":src.splitlines(True)}); continue
    cnt+=1; buf=io.StringIO(); t=time.time()
    with contextlib.redirect_stdout(buf):
        try: exec(compile(src,f'<cell{cnt}>','exec'),ns)
        except Exception: traceback.print_exc(file=sys.stderr); print("XATO", file=sys.stderr); sys.exit(1)
    out=buf.getvalue(); sys.stderr.write(f"cell {cnt}: {time.time()-t:.1f}s\n")
    nb_cells.append({"cell_type":"code","execution_count":cnt,"metadata":{},"source":src.splitlines(True),
                     "outputs":[{"name":"stdout","output_type":"stream","text":out.splitlines(True)}] if out else []})
nb={"cells":nb_cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
    "language_info":{"name":"python","version":"3"}},"nbformat":4,"nbformat_minor":4}
json.dump(nb,open('xulosalar_misollar.ipynb','w'),ensure_ascii=False,indent=1)
print("ok")
