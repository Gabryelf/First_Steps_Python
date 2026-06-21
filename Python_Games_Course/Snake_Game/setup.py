from setuptools import setup, find_packages

setup(
    name="snake_game",
    version="1.0.0",
    description="Змейка на Python с применением ООП и SOLID принципов",
    author="RPO",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.1",
        "typing-extensions>=4.9.0"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'snake-game=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)