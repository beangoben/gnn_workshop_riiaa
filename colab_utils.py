"""Collections of functions for running colab kernels."""
import glob
import os
import pathlib
import pkgutil
import shlex
import shutil
import subprocess
import sys
import urllib.request
from typing import List, Text, Tuple

import IPython.display
import matplotlib as mpl
import seaborn as sns
import yaml

# Assumes miniconda3 latests is 3.7, might have to update if it changes.
CONDA_DIR = '/usr/local/lib/python3.7/site-packages/'
IN_COLAB = 'google.colab' in sys.modules
CONDA_URL = 'https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh'

# Packages already present in colab.
DEFAULT_CONDA_EXCLUDE = ['cudatoolkit', 'cudnn',
                         'ipython', 'scikit-learn', 'tensorflow-gpu']


def add_conda_dir_to_python_path():
    """Add CONDA_DIR to sys.path."""
    sys.path.append(CONDA_DIR)


def is_running_colab() -> bool:
    """Check if running colab"""
    return 'google.colab' in sys.modules


def pip_install(package_list, force=False):
    extra = '--upgrade --force-reinstall' if force else ''
    [run_cmd(f'pip install {extra} {p}') for p in package_list]


def run_cmd(cmd: Text, split: bool = True, shell=False, verbose: bool = True):
    """Run a system command and print output."""
    print(f'CMD: {cmd}')
    cmd = shlex.split(cmd) if split else [cmd]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    while True:
        output = process.stdout.readline().decode('utf-8').strip()
        if output == '' and process.poll() is not None:
            break
        if output and verbose:
            print(output)
    return_code = process.poll()
    if return_code != 0:
        print(f'\tERROR ({return_code}) running command!')
    return return_code


def run_cmd_list(cmd_list: List[Text]):
    """Run several commands."""
    list(map(run_cmd, cmd_list))


def clone_repo(repo_url: Text) -> None:
    """Clone github repo and move to main dir."""
    repo_dir = repo_url.split('/')[-1].replace('.git', '')
    run_cmd(f'git clone --recursive {repo_url}', split=False, shell=True)
    for src in glob.glob(f'{repo_dir}/*'):
        dst = os.path.basename(src)
        if os.path.exists(dst):
            shutil.copy(src, dst)
        else:
            shutil.move(src, '.')
    shutil.rmtree(repo_dir)


def copy_ssh_key(id_rsa_url: Text) -> None:
    """Copy ssh keys for private repos."""
    key_dir = "/root/.ssh"
    key_path = os.path.join(key_dir, 'id_rsa')
    pathlib.Path(key_dir).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(id_rsa_url, key_path)
    os.chmod(key_path, 0o400)
    # Same as 'ssh-keyscan github.com >> {key_dir}/known_hosts'
    text = subprocess.check_output(['ssh-keyscan', 'github.com'])
    with open(os.path.join(key_dir, 'known_hosts'), 'wb') as afile:
        afile.write(text)

def make_ssh_key_from_file(src_filename: Text) -> None:
    """Write a ssh key for a private repo."""
    key_dir = "/root/.ssh"
    key_path = os.path.join(key_dir, 'id_rsa')
    pathlib.Path(key_dir).mkdir(parents=True, exist_ok=True)
    shutil.move(src_filename, key_path)
    os.chmod(key_path, 0o400)
    # Same as 'ssh-keyscan github.com >> {key_dir}/known_hosts'
    text = subprocess.check_output(['ssh-keyscan', 'github.com'])
    with open(os.path.join(key_dir, 'known_hosts'), 'wb') as afile:
        afile.write(text)

def parse_environment_yaml(filename: Text) -> Tuple[List[Text], List[Text], List[Text]]:
    """Parse yaml file and get channels, conda and pip modules."""
    pip_modules = []
    conda_modules = []
    with open(filename, 'r') as afile:
        config = yaml.load(afile)
        channels = config.get('channels') or []
        assert 'dependencies' in config, f'{filename} is not a valid conda yaml'
        for item in config['dependencies']:
            if isinstance(item, dict) and item['pip'] is not None:
                pip_modules = item['pip']
            if isinstance(item, str):
                conda_modules.append(item)
    return channels, conda_modules, pip_modules


def pip_install_from_yaml(filename: Text = 'environment.yml',
                          exclude: List[Text] = DEFAULT_CONDA_EXCLUDE,
                          filter_installed: bool = True,
                          force: bool = False):
    """Using a conda env yaml, install pip packages not found in colab."""
    _, _, pip_modules = parse_environment_yaml(filename)

    # Setup pip packages.
    if filter_installed:
        installed_modules = [p.name for p in pkgutil.iter_modules()]
        keep_modules = set(pip_modules).difference(installed_modules)
        keep_modules = keep_modules.difference(exclude)
        pip_modules = [c for c in pip_modules if c in keep_modules]

    print(f'pip installing {pip_modules}')
    if IN_COLAB:
        pip_install(pip_modules, force)


def conda_install_from_yaml(filename: Text = 'environment.yml',
                            exclude: List[Text] = DEFAULT_CONDA_EXCLUDE,
                            filter_installed: bool = True):
    """Using a conda env yaml, install packages not found in colab."""
    if os.path.exists(CONDA_DIR):
        print('Ignoring: conda install already exists in {CONDA_DIR}!')
        return

    channels, conda_modules, _ = parse_environment_yaml(filename)

    # Setup conda packages.
    if filter_installed:
        installed_modules = [p.name for p in pkgutil.iter_modules()]
        keep_modules = set(conda_modules).difference(installed_modules)
        keep_modules = keep_modules.difference(exclude)
        conda_modules = [c for c in conda_modules if c in keep_modules]
    print(f'Conda installing {conda_modules}')
    print(f' from channels {channels}')
    conda_prefix = f'conda install -q -y '
    chanel_str = ' '.join([f'-c {c}' for c in channels])
    conda_cmds = [f"{conda_prefix} {chanel_str} {pkg}" for pkg in conda_modules]

    conda_sh = CONDA_URL.split('/')[-1]
    cmd_list = [
                   f"wget -c {CONDA_URL}",
                   f"chmod +x {conda_sh}",
                   f"bash ./{conda_sh} -b -f -p /usr/local",
                   f"rm -rf {conda_sh}"] + conda_cmds

    if IN_COLAB and len(conda_cmds) > 0:
        run_cmd_list(cmd_list)
        print(f'Append "{CONDA_DIR}" to sys.path, or use "colab_utils.add_conda_dir_to_python_path()"!')


def print_module_versions(module_list):
    """Print module versions"""
    for module in module_list:
        print(f'{module.__name__:<10s}: {module.__version__}')


def matplotlib_settings():
    """"Change matplotlib settings."""
    sns.set_style("white")
    sns.set_style('ticks')
    sns.set_context("paper", font_scale=2.25)
    sns.set_palette(sns.color_palette('bright'))

    params = {'savefig.dpi': 100,
              'lines.linewidth': 3,
              'axes.linewidth': 2.5,
              'savefig.dpi': 300,
              'xtick.major.width': 2.5,
              'ytick.major.width': 2.5,
              'xtick.minor.width': 1,
              'ytick.minor.width': 1,
              'font.weight': 'medium',
              'figure.figsize': (12, 8)
              }

    mpl.rcParams.update(params)
    IPython.display.set_matplotlib_formats('retina')
