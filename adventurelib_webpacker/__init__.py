import sys
import re
import pkgutil
import argparse
import json
import base64
from pathlib import Path
import adventurelib
import time


def package_text(name):
    return pkgutil.get_data(__name__, name).decode('utf8')


def render_template(name, scripts):
    template = package_text('data/template.html')
    template = re.sub(
        r'^NAME = \.\.\.',
        'NAME = {!r}'.format(name),
        template,
        flags=re.M
    )
    def script_replacement(mo):
        name = mo.group(1)

        if '/' in name:
            return mo.group(0)

        script_src = pkgutil.get_data(__name__, 'data/' + name)
        url = (
            'data:application/javascript;base64,' +
            base64.b64encode(script_src).decode('ascii')
        )
        return '<script src="{}"></script>'.format(url)

    template = re.sub(
        r'<script src="([^"]+)"></script>',
        script_replacement,
        template
    )

    extras = []
    for k, v in scripts.items():
        extras.append(
            '__BRYTHON__.VFS[{}] = {};'.format(
                json.dumps(k),
                json.dumps(v)
            )
        )

    template = template.replace(
        r'<script id="extra_modules"></script>',
        '<script>\n{}\n</script>\n'.format('\n'.join(extras))
    )
    template = re.sub(r'\$NOW\b', str(int(time.time() * 1000)), template)

    return template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="The name of the game to pack.")

    args = parser.parse_args()

    name = args.name
    if name.endswith('.py'):
        name = name[:-3]

    if not Path(name + '.py').exists() \
            and not Path(name, '__init__.py').exists():
        parser.error("Module {} does not exist.".format(name))

    root = Path.cwd()
    mods = {
        'adventurelib': [
            '.py',
            Path(adventurelib.__file__).read_text(),
            're sys inspect readline textwrap random copy shutil'.split(),
        ],
    }

    for pyfile in root.glob('**/*.py'):
        pymod = pyfile.relative_to(root)
        parts = list(pymod.parent.parts)
        if pymod.name != '__init__.py':
            parts.append(pymod.stem)
            is_pkg = False
        else:
            is_pkg = True

        modname = '.'.join(parts)
        try:
            v = mods[modname] = ['.py', pymod.read_text(), []]
        except UnicodeDecodeError as e:
            raise Exception(
                "Failed to decode {}.".format(pymod)
            ) from e
        if is_pkg:
            v.append(1)

    out = Path(name + '.html')
    out.write_text(render_template(name, mods))
    print("Wrote", out)
