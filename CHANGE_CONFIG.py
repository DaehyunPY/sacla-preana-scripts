# %% import
from os import makedirs
from os.path import join
from subprocess import call
from glob import iglob as glob
from textwrap import dedent
from yaml import load as load_config
from cytoolz import curry
from cytoolz.curried import reduce

# %% read config
config_asstr = dedent(
    """\
    exe_path: C:\\home\\programs\\lma2root_SACLA\\Binaries\\lma2root.exe
    txt_template_file: C:\\Users\\uedalab\\Desktop\\RESORT_SCRIPT\\template.txt
    lma_files: Z:\\2017B8050\\lma_files\\{aq}__*.lma
    output_dir: D:\\2017B8050\\hit_files\\{aq}
    output_basename: {aq}
    """.format(aq="Aq002"))
config = load_config(config_asstr)

# %% read txt template
with open(config['txt_template_file'], 'r') as f:
    txt_asstr = f.read()

# %% write txt and bat file
dir = config['output_dir']
makedirs(dir, exist_ok=True)
in_dir = curry(join, dir)

filelist = reduce(lambda s1, s2: '{}\n{}'.format(s1, s2))
globbed = glob(config['lma_files'])

with open(in_dir('resort.txt'), 'w') as f:
    f.write(txt_asstr.format(
        basename=config['output_basename'],
        lma_filelist=filelist(globbed)))

with open(in_dir('resort.bat'), 'w') as f:
    f.write(dedent(
        """\
        pushd {dir}
        {exe} < resort.txt
        """).format(dir=in_dir(''), exe=config['exe_path']))

# %% call
call(in_dir('resort.bat'))
