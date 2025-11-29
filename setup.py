
import setuptools

# Read the contents of the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name             = "polarchart",
    version          = "0.0.2",
    author           = "Reto Stauffer",
    author_email     = "Reto.Stauffer@uibk.ac.at",
    maintainer_email = "Reto.Stauffer@uibk.ac.at",
    license          = "GPL-2 | GPL-3",
    description      = "Utility Package for the Data Analytics Course",
    long_description              = long_description,
    long_description_content_type = "text/markdown",

    keywords         = "polar charts, radar chart, radar plot, star plot, star chart, spider plot, spider chart",
    url          = "https://github.com/retostauffer/polarchart",
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization"
    ],

    install_requires = ["numpy>=2.3", "pandas>=2.3", "matplotlib>=3.10", "colorspace>=1.0", "statsmodels>=0.14.5"],
    python_requires = ">=3.10",

    # Exclude on build
    packages = setuptools.find_packages(exclude = ["tests", "docs"]),

    # Should package data be included? (MANIFEST)
    include_package_data = True
)
