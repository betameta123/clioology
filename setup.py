from setuptools import setup

setup(
    name='clioology',
    version='0.1',
    py_modules=['clioology'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        clioology=clioology:cli
    ''',
    
)
