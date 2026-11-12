import io, sys, json, contextlib, traceback, os
def setup_cell(mods):
    src = {m: open(f'/home/claude/pkg/uzmst285_tahlil/{m}.py', encoding='utf8').read() for m in mods}
    return ('code', "# 0-hujayra. Dastur modullarini yuklash (daftar mustaqil ishlaydi).\n"
            "# Agar modullar shu papkada bo'lsa, ular ishlatiladi; bo'lmasa quyidagi matndan xotirada yaratiladi.\n"
            "import sys, types, importlib.util\n_MODULLAR = {\n" + ''.join(f"    {m!r}: {s!r},\n" for m, s in src.items()) + "}\n"
            "for _nom, _matn in _MODULLAR.items():\n"
            "    if importlib.util.find_spec(_nom) is not None and _nom not in sys.modules:\n"
            "        print(f\"{_nom}.py — papkadagi fayldan olinadi\"); continue\n"
            "    _m = types.ModuleType(_nom); _m.__file__ = f\"<{_nom}>\"\n"
            "    sys.modules[_nom] = _m; exec(compile(_matn, f\"<{_nom}>\", \"exec\"), _m.__dict__)\n"
            "    print(f\"{_nom} — daftar ichidan yuklandi\")\n")
def build(cells, out_nb, workdir):
    cwd = os.getcwd(); os.makedirs(workdir, exist_ok=True); os.chdir(workdir)
    sys.modules_backup = dict(sys.modules)
    ns = {'__name__': '__main__'}; nbc = []; cnt = 0
    for kind, src in cells:
        if kind == 'markdown': nbc.append({"cell_type": "markdown", "metadata": {}, "source": src.splitlines(True)}); continue
        cnt += 1; buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try: exec(compile(src, f'<cell{cnt}>', 'exec'), ns)
            except Exception: os.chdir(cwd); traceback.print_exc(); raise
        out = buf.getvalue(); sys.stderr.write(f"hujayra {cnt} tayyor\n")
        nbc.append({"cell_type": "code", "execution_count": cnt, "metadata": {}, "source": src.splitlines(True),
                    "outputs": [{"name": "stdout", "output_type": "stream", "text": out.splitlines(True)}] if out else []})
    nb = {"cells": nbc, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
          "language_info": {"name": "python", "version": "3"}}, "nbformat": 4, "nbformat_minor": 4}
    os.chdir(cwd); json.dump(nb, open(out_nb, 'w'), ensure_ascii=False, indent=1)
    return ns
