from setuptools import setup, find_packages

setup(
    name='cv_utils',
    version='0.0.1',
    author='huxiaoyang',
    author_email='huxiaoyang@holomatic.com',

    install_requires=['numpy', 'opencv-python', 'loguru'],

    packages=find_packages()
)
