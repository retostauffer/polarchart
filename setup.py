
import setuptools

# Read the contents of the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stars",
    version="0.0.1",
    author="Reto Stauffer",
    author_email="Reto.Stauffer@uibk.ac.at",
    description="A Python package for creating Star Plots (Radar Charts).",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://git.uibk.ac.at/c4031021/python-stars",
    #packages=setuptools.find_packages(exclude=['tests', 'docs']),  # Automatically finds the 'pystars' directory
    install_requires=[
        "numpy>=2.3",
        "pandas>=2.3",
        "matplotlib>=3.10",
    ],
    classifiers=[
        # Classifiers help users find your package on PyPI
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GPL-2 | GPL-3",
        "Operating System :: OS Independent"
        #"Intended Audience :: Science/Research",
        #"Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.13',

    # Should package data be included? (MANIFEST)
    #include_package_data=True,
)
