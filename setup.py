import io
from setuptools import setup, find_packages


def readfile(filename):
    with io.open(filename, encoding="utf-8") as stream:
        return stream.read().splitlines()

setup(
    name='sphinxcontrib-lunrsearch',
    url='https://github.com/rmcgibbo/sphinxcontrib-lunrsearch',
    download_url='https://pypi.python.org/pypi/sphinxcontrib-lunrsearch',
    license="MIT",
    author="Robert T. McGibbon",
    author_email="rmcgibbo@gmail.com",
    description="Instant search for Sphinx",
    long_description='\n'.join(readfile("README.rst")[3:]),
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
