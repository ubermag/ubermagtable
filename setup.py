import setuptools

with open("README.rst") as f:
    readme = f.read()

setuptools.setup(
    name="oommfodt",
    version="0.7.7",
    description="A Python package for reading and analysing OOMMF odt files",
    long_description=readme,
    url='https://joommf.github.io',
    author='Marijan Beg, Ryan A. Pepper, and Hans Fangohr',
    author_email='jupyteroommf@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=["pandas",
                      "openpyxl",
                      "xlrd",
                      "xlwt"],
    package_data={'oommfodt.tests': ["test_odt_files/*.odt"]},
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 3 :: Only']
)
