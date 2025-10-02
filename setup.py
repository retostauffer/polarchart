
import setuptools

# Read the contents of the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name         = "radarchart",
    version      = "0.0.1",
    author       = "Reto Stauffer",
    author_email = "Reto.Stauffer@uibk.ac.at",
    description  = "A Python package for creating Star Plots (Radar Charts).",
    url          = "https://git.uibk.ac.at/c4031021/radarchart",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #packages=setuptools.find_packages(exclude=['tests', 'docs']),
    install_requires=[
        "numpy>=2.3",
        "pandas>=2.3",
        "matplotlib>=3.10",
    ],
    classifiers=[
        # Classifiers help users find your package on PyPI
        "Programming Language :: Python :: 3.13",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
        #"Intended Audience :: Science/Research",
        #"Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.13',

    # Should package data be included? (MANIFEST)
    #include_package_data=True,
)
