from setuptools import find_packages, setup

name = 'requests_builder'
release = '0.1.3'

production_dependencies = [
    'openai == 0.27.6',
]

setup(
    name=name,
    author='Maria',
    version=release,
    python_requires='>= 3.11, < 4',
    packages=find_packages(),
    install_requires=production_dependencies,
    entry_points={
        'console_scripts': [
            'build-requests=requests_builder.main:main',
        ],
    },
)
