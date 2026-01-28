from setuptools import setup, find_packages

setup(
    name="pybrowser",
    version="0.1.0",
    description="A Python-based web browser for businesses",
    author="PyBrowser Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "PyQt6>=6.6.1",
        "PyQt6-WebEngine>=6.6.0",
        "requests>=2.31.0",
        "requests-oauthlib>=1.3.1",
        "keyring>=24.3.0",
        "pydantic>=2.5.3",
    ],
    entry_points={
        "console_scripts": [
            "pybrowser=pybrowser.main:main",
        ],
    },
)
