from setuptools import find_packages, setup

setup(
    name='test_server',
    version='3.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)