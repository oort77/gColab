from setuptools import setup
setup(
    name='gdrive',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'gdrive=gdrive:main'
        ]
    }
)