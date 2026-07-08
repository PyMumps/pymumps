import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent / 'mumps'
OUTPUT_DIR = BASE_DIR

def select_template(version, src_dir=BASE_DIR):
    """Select the appropriate template based on MUMPS version string."""
    # Parse major.minor from version string (e.g. "5.7.3" -> 5, 7)
    parts = version.split('.')
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else 0

    if major < 5:
        raise ValueError(f'Version {version} not supported, version should be >= 5.0.x')

    if major > 5 or minor >= 9:
        tpl_version = '5.9'
    elif minor >= 7:
        tpl_version = '5.7'
    elif minor >= 3:
        tpl_version = '5.3'
    elif minor >= 1:
        tpl_version = '5.1'
    else:
        tpl_version = '5.0'

    tpl_file = src_dir / f'_mumps_{tpl_version}.x.tpl'
    if not tpl_file.exists():
        raise FileNotFoundError(f'Template file {tpl_file} not found')

    print(f'Using template for MUMPS {tpl_version}.x (detected version: {version})')
    return tpl_file


def generate_wrappers(version="5.7.0", src_dir=BASE_DIR, output_dir=OUTPUT_DIR):
    """Generate Cython wrapper .pyx files for all MUMPS arithmetic types."""
    tpl_file = select_template(version, src_dir)

    with open(tpl_file, 'rt') as f:
        template = f.read()

    for x in ('s', 'd', 'c', 'z'):
        out_path = output_dir / f'_{x}mumps.pyx'
        with open(out_path, 'wt') as f:
            f.write(template.format(x=x, X=x.upper()))
        print(f'  Generated {out_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate MUMPS Cython wrappers')
    parser.add_argument('--version', default='5.7.0',
                        help='MUMPS version string (e.g. 5.7.3)')
    args = parser.parse_args()
    generate_wrappers(version=args.version)

