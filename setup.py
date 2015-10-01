from setuptools import setup, find_packages
import os

version = '0.6'

setup(
    name='cs.zestreleaser.changelog',
    version=version,
    description="Dump the last commit logs into the CHANGES file",
    long_description=open("README.rst").read() + "\n" +
                     open(os.path.join("docs", "HISTORY.txt")).read(),
        # Get more strings from
        # http://pypi.python.org/pypi?:action=list_classifiers
        classifiers=[
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities',
    ],
    keywords='',
    author='Mikel Larreategi',
    author_email='mlarreategi@codesyntax.com',
    url='https://github.com/codesyntax/cs.zestreleaser.changelog',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['cs', 'cs.zestreleaser'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zest.releaser',
    ],
    entry_points={
        'zest.releaser.prereleaser.before':
        ['fillchangelog=cs.zestreleaser.changelog:fillchangelog']
    },
)
