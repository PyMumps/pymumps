from pathlib import Path

BASE_DIR = Path(__file__).parent / 'mumps'

with open(BASE_DIR / '_mumps.tpl', 'rt') as f:
    template = f.read()

for x in {'s', 'd', 'c', 'z'}:
    with open(BASE_DIR / f'_{x}mumps.pyx', 'wt') as f:
        f.write(template.format(x=x, X=x.upper()))
