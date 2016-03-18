from setuptools import setup, find_packages

setup(
    name='shadecli',
    version='0.1',
    license='BSD',
    author='Karel Vervaeke',
    author_email='karel@vervaeke@info',
    url='https://github.com/karel1980/shadecli',
    long_description="README.txt",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shadecli = shadecli.cli:run_cli',
        ],
	},
    package_data={
    },
    data_files=[],
	description="shadecli: cli tool for openhab controlled shades"
)
