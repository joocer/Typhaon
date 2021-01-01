from setuptools import setup, find_packages  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='typhaon',
   version='1.0.3',
   description='Python Data Validator',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Joocer',
   author_email='justin.joyce@joocer.com',
   packages=find_packages(),
   url="https://github.com/joocer/Typhaon",
   install_requires=[]
)
