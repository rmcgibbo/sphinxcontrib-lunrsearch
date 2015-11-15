"""MDTraj: A modern, open library for the analysis of molecular dynamics trajectories

MDTraj is a python library that allows users to manipulate molecular dynamics
(MD) trajectories and perform a variety of analyses, including fast RMSD,
solvent accessible surface area, hydrogen bonding, etc. A highlight of MDTraj
is the wide variety of molecular dynamics trajectory file formats which are
supported, including RCSB pdb, GROMACS xtc and trr, CHARMM / NAMD dcd, AMBER
binpos, AMBER NetCDF, AMBER mdcrd, TINKER arc and MDTraj HDF5.
"""

import sys
from setuptools import setup, find_packages
DOCLINES = __doc__.split("\n")

setup(
    name='sphinxcontrib-lunrsearch',
    url='https://github.com/rmcgibbo/sphinxcontrib-lunrsearch',
    download_url='https://pypi.python.org/pypi/sphinxcontrib-lunrsearch',
    license="MIT",
    author="Robert T. McGibbon",
    author_email="rmcgibbo@gmail.com",
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=['sphinxcontrib'],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'Sphinx>=1.0',
        'six>=1.4.1',
    ]
)
