
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, List

DEFAULT_EXCLUDE = {".git", "__pycache__", ".venv", "output"}

ALGOS = ["sha224", "sha256", "sha512"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Gerar hash único ou manifesto de hashes do repositório.")
    p.add_argument("--root", default=".", help="Diretório raiz")
    p.add_argument("--output", default="manifest_hashes.json", help="Arquivo de saída JSON (modo --full)")
    p.add_argument("--algo", choices=ALGOS, default="sha256", help="Algoritmo para hash único")
    p.add_argument("--full", action="store_true", help="Gerar manifesto completo")
    p.add_argument("--include-hidden", action="store_true", help="Incluir arquivos ocultos")
    return p.parse_args()


def file_hashes(path: Path) -> Dict[str, str]:
    data = path.read_bytes()
    return {algo: getattr(hashlib, algo)(data).hexdigest() for algo in ALGOS}


def should_skip(path: Path) -> bool:
    name = path.name
    if any(part in DEFAULT_EXCLUDE for part in path.parts):
        return True
    if name.endswith(".enc"):
        return True
    return False


def aggregate_hash(all_hashes: List[str], algo: str) -> str:
    h = getattr(hashlib, algo)()
    for value in all_hashes:
        h.update(value.encode("utf-8"))
    return h.hexdigest()


def main():
    args = parse_args()
    root = Path(args.root).resolve()
    file_list = []
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if should_skip(path):
            continue
        if not args.include_hidden and path.name.startswith('.'):
            continue
        file_list.append(path)

    if not args.full:
        h = getattr(hashlib, args.algo)()
        for p in file_list:
            rel = p.relative_to(root).as_posix().encode("utf-8")
            h.update(rel + b"\0")
            h.update(p.read_bytes())
        digest = h.hexdigest()
        print(f"HASH_UNICO_{args.algo.upper()}: {digest}")
        print(f"Total de arquivos considerados: {len(file_list)}")
        return

    manifest = {"root": str(root), "files": [], "aggregate": {}}
    per_algo_values = {algo: [] for algo in ALGOS}
    for p in file_list:
        fh = file_hashes(p)
        manifest["files"].append({"path": str(p.relative_to(root)), "hashes": fh})
        for algo in ALGOS:
            per_algo_values[algo].append(fh[algo])
    for algo in ALGOS:
        manifest["aggregate"][algo] = aggregate_hash(per_algo_values[algo], algo)
    out = Path(args.output)
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Manifesto gerado:", out)
    for algo in ALGOS:
        print(f"AGREGADO_{algo.upper()}: {manifest['aggregate'][algo]}")
    print(f"Total de arquivos: {len(file_list)}")


if __name__ == "__main__":
    main()
