from setuptools import setup

setup(
    name="github-stars-history",
    version="1.1.0",
    description="Track the star history of any GitHub repository — daily and weekly growth analytics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marcos66236",
    url="https://github.com/Marcos66236/github-stars-history",
    py_modules=["star_history"],
    python_requires=">=3.8",
    install_requires=["requests>=2.28.0"],
    entry_points={
        "console_scripts": [
            "star-history=star_history:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
