import setuptools


def get_version() -> str:
    with open("flake8_function_order/__init__.py") as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("__version__"):
            return line.split("=")[-1].strip().strip("'").strip("-")
    return ""


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="flake8-function-order",
    description="flake8 extension that checks function order within a class",
    classifiers=[
        "Environment :: Console",
        "Framework :: Flake8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_degscription=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    keywords="flake8",
    version=get_version(),
    author="Tyler Yep",
    author_email="tyep@cs.stanford.edu",
    install_requires=["flake8", "setuptools"],
    entry_points={
        "flake8.extension": [
            "CCE = flake8_function_order.checker:ClassFunctionOrderChecker",
        ],
    },
    url="https://github.com/TylerYep/flake8-function-order",
    license="MIT",
    py_modules=["flake8_function_order"],
    zip_safe=False,
)
