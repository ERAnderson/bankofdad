from setuptools import setup, find_packages

setup(
    name="bankofdad",
    version="0.1",
    author="Tim Diller",
    author_email="timdiller@gmail.com",
    description=("Diller Family Bank of Dad Allowance system"),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['BOD = bankofdad.app.__main__:main'],
    },
)
