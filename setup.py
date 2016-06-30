from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='oommfodt',
    version='0.1',
    description='A Python package for reading and analysing OOMMF odt files',
    long_description=readme,
    author='Computational Modelling Group',
    author_email='fangohr@soton.ac.uk',
    url = 'https://github.com/joommf/oommfodt',
    download_url = 'https://github.com/joommf/oommfodt/tarball/0.1',
    packages=['oommfodt', 'oommfodt.tests'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
