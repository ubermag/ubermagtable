import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='ubermagtable',
    version='0.1.11',
    description=('Python package for manipulating '
                 'OOMMF and mumax3 tabular data.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://ubermag.github.io',
    author=('Marijan Beg, Vanessa Nehruji, Sergii Mamedov, '
            'Ryan A. Pepper, Thomas Kluyver, and Hans Fangohr'),
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['ubermagutil==0.2.6',
                      'matplotlib>=3.2',
                      'pandas>=1.0',
                      'jupyterlab>=2.1',
                      'ipywidgets>=7.5'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Education',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: English',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Topic :: Scientific/Engineering :: Visualization']
)
