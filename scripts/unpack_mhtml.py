#!/usr/bin/env python3
"""Unpack a browser MHTML archive for inspection, without network access."""

import argparse
from email import policy
from email.parser import BytesParser
import hashlib
import json
from pathlib import Path
import tempfile

EXTENSIONS = {
    'text/html': '.html', 'text/css': '.css', 'text/plain': '.txt',
    'text/javascript': '.js', 'application/javascript': '.js',
    'application/json': '.json', 'image/svg+xml': '.svg',
    'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp',
    'image/gif': '.gif', 'image/avif': '.avif', 'image/x-icon': '.ico',
    'font/woff': '.woff', 'font/woff2': '.woff2', 'font/ttf': '.ttf',
    'application/font-woff': '.woff', 'application/octet-stream': '.bin',
}


def unpack(source: Path, output: Path) -> dict:
    source = source.resolve()
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise FileExistsError(f'Output already exists: {output}; choose a new directory')
    message = BytesParser(policy=policy.default).parsebytes(source.read_bytes())
    if not message.is_multipart():
        raise ValueError('Expected a multipart MHTML archive, not plain HTML')
    parts = [part for part in message.walk() if not part.is_multipart()]
    html_indices = [i for i, part in enumerate(parts) if part.get_content_type() == 'text/html']
    if not html_indices:
        raise ValueError('Archive contains no HTML document')
    snapshot_url = str(message.get('Snapshot-Content-Location', ''))
    main_index = next((i for i in html_indices if snapshot_url and
                       str(parts[i].get('Content-Location', '')) == snapshot_url), html_indices[0])
    inventory = {
        'archive': source.name,
        'snapshot_url': snapshot_url,
        'main_document': 'index.html',
        'main_resource_index': main_index,
        'html_export': 'MHTML main document; resource URLs are not rewritten',
        'resources': [],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.mhtml-', dir=output.parent) as temp:
        staging = Path(temp) / 'unpacked'
        resources = staging / 'resources'
        resources.mkdir(parents=True)
        for index, part in enumerate(parts):
            data = part.get_payload(decode=True) or b''
            mime = part.get_content_type()
            digest = hashlib.sha256(data).hexdigest()
            filename = f'{index:04d}-{digest[:12]}{EXTENSIONS.get(mime, ".bin")}'
            (resources / filename).write_bytes(data)
            inventory['resources'].append({
                'path': f'resources/{filename}',
                'mime': mime,
                'bytes': len(data),
                'sha256': digest,
                'location': str(part.get('Content-Location', '')),
                'content_id': str(part.get('Content-ID', '')),
                'charset': part.get_content_charset(),
            })
            if index == main_index:
                charset = part.get_content_charset() or 'utf-8'
                try:
                    html = data.decode(charset, errors='replace')
                except LookupError:
                    html = data.decode('utf-8', errors='replace')
                (staging / 'index.html').write_text(html, encoding='utf-8')
        (staging / 'inventory.json').write_text(
            json.dumps(inventory, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        # Publish only complete output; never derive filenames from captured URLs.
        if output.exists() or output.is_symlink():
            raise FileExistsError(f'Output appeared while extracting: {output}')
        staging.rename(output)
    return inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--out', required=True, type=Path, help='New output directory')
    args = parser.parse_args()
    try:
        result = unpack(args.archive, args.out)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')
    counts = {}
    for item in result['resources']:
        counts[item['mime']] = counts.get(item['mime'], 0) + 1
    print(json.dumps({'output': str(args.out.absolute()), 'resources': counts}, indent=2))


if __name__ == '__main__':
    main()
