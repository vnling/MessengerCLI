from setuptools import setup
setup(
    name = 'messenger',
    version = '0.1.0',
    packages = ['messenger'],
    entry_points = {
        'console_scripts': [
            'messenger = messenger.__main__:cli'
        ]
    }
)