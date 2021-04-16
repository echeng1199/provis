# make the project installable (i.e. work anywhere even if flaskr package is not installed)
# this should actually be the first step in making an app

# describe project and the files that belong to it

from setuptools import find_packages, setup

setup(
    name='proteomicsdb',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
