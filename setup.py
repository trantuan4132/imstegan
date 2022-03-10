from setuptools import setup, find_packages

setup(
   name='imstegan',
   version='0.0.2',
   description='An awesome image steganography library',
   author='Duc To, Tuan Tran and Viet Nguyen',
   author_email='',
   url='',
   packages=find_packages(),
   install_requires=['Pillow', 'numpy', 'numba'],
)