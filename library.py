"""Read the three explicitly bundled workflow reference files without executing them."""
import hashlib
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / '_assets' / 'workflows'
WORKFLOWS = {'ES': 'Energy scheduling', 'CR': 'Complaint routing', 'DC': 'Data cleaning'}


def export_workflow(workflow: str) -> tuple[str, bytes]:
    if workflow not in WORKFLOWS:
        raise ValueError('Choose workflow ES, CR, or DC.')
    name = f'TomJ-{workflow}.yml'
    return name, (ASSETS / name).read_bytes()


def _parts(blob: bytes) -> list[str]:
    remaining = blob.decode('utf-8')
    chunks = []
    while remaining:
        piece = remaining.encode('utf-8')[:4500].decode('utf-8', errors='ignore')
        boundary = piece.rfind('\n') + 1
        if boundary > len(piece) // 2:
            piece = piece[:boundary]
        chunks.append(piece)
        remaining = remaining[len(piece):]
    return chunks


def catalog() -> list[dict]:
    result = []
    for key, title in WORKFLOWS.items():
        name, blob = export_workflow(key)
        result.append({'id': key, 'name': f'TomJ-{key}', 'description': title,
                       'filename': name, 'bytes': len(blob),
                       'parts': len(_parts(blob)), 'sha256': hashlib.sha256(blob).hexdigest()})
    return result


def read_part(workflow: str, part: object = 1) -> str:
    name, blob = export_workflow(workflow)
    try:
        number = int(part)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError('Part must be a positive integer.') from exc
    if isinstance(part, bool) or isinstance(part, float) and part != number:
        raise ValueError('Part must be a positive integer.')
    chunks = _parts(blob)
    if number < 1 or number > len(chunks):
        raise ValueError(f'Part must be between 1 and {len(chunks)}.')
    return (f'{name} part {number}/{len(chunks)}\n'
            f'BEGIN_ORIGINAL\n{chunks[number - 1]}\nEND_ORIGINAL\n'
            f'PART_END=TOMJ-{workflow}-{number:03d}-END')
