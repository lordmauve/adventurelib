import sys
import re
import pkgutil
import argparse
import json
from pathlib import Path



def render_template(name, scripts):
    template = pkgutil.get_data('data/template.html').decode('utf8')
    template = re.sub(
        r'^NAME = \.\.\.',
        'NAME = {name!r}'.format(name),
        template
    )
    def script_replacement(mo):
        name = mo.group(1)

        script_src = pkgutil.get_data(name).decode('utf8')
        if '/' in name:
            return mo.group(0)

        return '<script>{}</script>'.format(script_src)

    template = re.sub(
        r'<script src="([^"])"></script>',
        script_replacement,
        template
    )
    template = re.sub(
        r'^EXTRA = \.\.\.',
        'EXTRA = {}'.format(json.dumps(scripts)),
        template
    )

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
    mods = {}
    for pyfile in root.glob('**/*.py'):
        pymod = pyfile.relative_to(root)
        modname = '.'.join(pymod.parent.parts)
        if pymod.name != '__init__.py':
            modname += '.' + pymod.stem

        mods[modname] = ['.py', pymod.read_text()]

    out = Path(name + '.html')
    out.write_text(render_template(name, mods))
    print("Wrote", out)
