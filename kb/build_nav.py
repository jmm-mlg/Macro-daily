"""Genera mkdocs.yml con la navegación a partir de las carpetas de kb/. Se ejecuta antes de mkdocs build."""
import pathlib
import re
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
SECTIONS = [("indicadores", "Indicadores"), ("sectores", "Sectores"), ("mecanismos", "Mecanismos"),
            ("casuisticas", "Casuísticas"), ("conceptos", "Conceptos"), ("episodios", "Episodios")]
BLOCK_ORDER = ["Tipos", "Inflación", "Empleo", "Actividad", "Vivienda", "Crédito", "Mercado"]


def title_of(p: pathlib.Path) -> str:
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^nombre:\s*(.+)$", t, re.M)
    if m:
        return m.group(1).strip().strip('"')
    m = re.search(r"^# (.+)$", t, re.M)
    return m.group(1).strip() if m else p.stem


def block_of(p: pathlib.Path) -> str:
    m = re.search(r"^bloque:\s*(.+)$", p.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else "Otros"


nav = [{"Inicio": "README.md"}]
for folder, label in SECTIONS:
    d = KB / folder
    if not d.exists():
        continue
    files = sorted(p for p in d.glob("*.md") if not p.name.startswith("_"))
    if not files:
        continue
    if folder == "indicadores":
        groups = {}
        for p in files:
            groups.setdefault(block_of(p), []).append({title_of(p): f"{folder}/{p.name}"})
        ordered = [{b: groups[b]} for b in BLOCK_ORDER if b in groups] + [{b: groups[b]} for b in groups if b not in BLOCK_ORDER]
        nav.append({label: ordered})
    else:
        nav.append({label: [{title_of(p): f"{folder}/{p.name}"} for p in files]})
nav.append({"Biblioteca": "BIBLIOTECA.md"})
nav.append({"Plantilla": "PLANTILLA.md"})
nav.append({"Verificación": "_verificacion.md"} if (KB / "_verificacion.md").exists() else {"Pendientes": "PENDIENTES.md"})

cfg = {
    "site_name": "Macro Monitor · Base de conocimiento",
    "site_url": "https://jmm-mlg.github.io/Macro-daily/kb/",
    "docs_dir": "kb",
    "site_dir": "docs/kb",
    "use_directory_urls": True,
    "exclude_docs": "verificar.py\nverificacion.yaml\nbuild_nav.py\n_hooks.py\n",
    "theme": {"name": "material", "language": "es",
              "palette": [{"scheme": "default", "primary": "blue grey", "accent": "amber", "toggle": {"icon": "material/brightness-7", "name": "Modo oscuro"}},
                          {"scheme": "slate", "primary": "blue grey", "accent": "amber", "toggle": {"icon": "material/brightness-4", "name": "Modo claro"}}],
              "features": ["navigation.sections", "navigation.indexes", "navigation.top", "search.suggest", "search.highlight", "content.tabs.link", "toc.integrate"]},
    "markdown_extensions": ["tables", "admonition", "toc", "attr_list", "md_in_html", {"pymdownx.superfences": {}}],
    "plugins": [{"search": {"lang": "es"}}],
    "hooks": ["kb/_hooks.py"],
    "nav": nav,
}
(ROOT / "mkdocs.yml").write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(f"mkdocs.yml generado: {sum(len(list(v.values())[0]) if isinstance(list(v.values())[0], list) else 1 for v in nav)} entradas de navegación")
