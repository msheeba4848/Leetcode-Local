from setuptools import setup, find_packages

setup(
    name="leetcode-local",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'leetcode-local=leetcode_local.cli.commands:main',
        ],
    },
    install_requires=[
        'toml>=0.10.2',
    ],
    python_requires='>=3.6',
    description="Local practice environment for LeetCode 75 problems",
    author="Your Name",
    author_email="your.email@example.com",
)