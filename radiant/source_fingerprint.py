"""Deterministic fingerprint of files that can change Radiant execution/results."""
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT_FILES = ('Dockerfile','.dockerignore','requirements.txt')
ROOT_DIRS = ('radiant','data','db','ontology','scripts','examples','tests','.github')
SKIP_PARTS = {'__pycache__','.pytest_cache'}
SKIP_SUFFIXES = {'.pyc','.pyo'}

def iter_inputs(root: str|Path='.'):
    root=Path(root)
    paths=[]
    for name in ROOT_FILES:
        p=root/name
        if p.is_file(): paths.append(p)
    for name in ROOT_DIRS:
        base=root/name
        if not base.exists(): continue
        for p in base.rglob('*'):
            if not p.is_file() or any(part in SKIP_PARTS for part in p.parts) or p.suffix in SKIP_SUFFIXES:
                continue
            paths.append(p)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())

def fingerprint(root: str|Path='.') -> str:
    root=Path(root)
    h=hashlib.sha256()
    for p in iter_inputs(root):
        rel=p.relative_to(root).as_posix().encode()
        blob=p.read_bytes()
        h.update(len(rel).to_bytes(4,'big')); h.update(rel)
        h.update(len(blob).to_bytes(8,'big')); h.update(blob)
    return h.hexdigest()
