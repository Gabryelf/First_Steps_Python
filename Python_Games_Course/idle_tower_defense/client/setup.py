from setuptools import setup, find_packages

setup(
    name="idle_tower_defense_client",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        'client.src': ['*.py'],
    },
    install_requires=[
        "pygame>=2.5.0",
    ],
    python_requires=">=3.8",
)