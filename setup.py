from setuptools import find_packages, setup


def read(path):
    with open(path, 'r') as f:
        return f.read()


long_description = read('README.md')

setup(
    name='ngsutils',
    version='0.0.0',
    url='https://github.com/Lioscro/ngsutils',
    author='Kyung Hoi (Joseph) Min',
    author_email='phoenixter96@gmail.com',
    description='',  # noqa
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='',
    python_requires='>=3.7',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    zip_safe=False,
    include_package_data=True,
    install_requires=read('requirements.txt').strip().split('\n'),
    entry_points={},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Utilities',
    ],
)