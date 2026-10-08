"""Hook de MkDocs: convierte los enlaces [[id]] de la base en enlaces reales al archivo correspondiente."""
import re
import pathlib

_index = None


def _build_index(config):
    global _index
    docs = pathlib.Path(config["docs_dir"])
    _index = {}
    for p in docs.rglob("*.md"):
        if p.name.startswith("_") or p.name in ("PLANTILLA.md", "PENDIENTES.md"):
            continue
        _index[p.stem] = p.relative_to(docs).as_posix()
    # ids con caracteres especiales (series de mercado) -> archivo
    _index.update({"^GSPC": "indicadores/GSPC.md", "^VIX": "indicadores/VIX.md", "DX-Y.NYB": "indicadores/DXY.md",
                   "CL=F": "indicadores/CL.md", "HG=F": "indicadores/HG.md", "GC=F": "indicadores/GC.md",
                   "EURUSD=X": "indicadores/EURUSD.md", "JPY=X": "indicadores/USDJPY.md", "NEWORDER": "indicadores/DGORDER.md"})


def on_page_markdown(markdown, page, config, files):
    if _index is None:
        _build_index(config)
    src = pathlib.Path(page.file.src_path)

    def repl(m):
        key = m.group(1)
        target = _index.get(key)
        if not target:
            return f"`{key}`"
        rel = pathlib.PurePosixPath(target)
        # ruta relativa desde la página actual
        up = "../" * (len(src.parts) - 1)
        return f"[{key}]({up}{rel.as_posix()})"

    return re.sub(r"\[\[([^\]]+)\]\]", repl, markdown)
