import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="oommfodt",
    version="0.8.1",
    description="Python package for reading and analysis of OOMMF .odt files.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://joommf.github.io',
    author='Marijan Beg, Ryan A. Pepper, Thomas Kluyver, and Hans Fangohr',
    author_email='jupyteroommf@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=["pandas",
                      "openpyxl",
                      "xlrd",
                      "xlwt"],
    package_data={'oommfodt.tests': ["test_odt_files/*.odt"]},
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3 :: Only',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English']
)
