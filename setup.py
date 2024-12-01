from setuptools import setup, find_packages

setup(
    name="virgin-atlantic",
    version="0.1.0",
    description="A Python package for fetching Virgin Atlantic flight prices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Alex Choi",
    author_email="alexchoidev@gmail.com",
    url="https://github.com/alexechoi/virgin-atlantic-py",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)