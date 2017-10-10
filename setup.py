import io
import os
import re

from setuptools import setup


def read(*parts):
    with open(os.path.join(*parts), 'rt') as f:
        return f.read().strip()

setup(
    name='aiciscospark',
    version='0.1',
    author='Zaheer Abbas Merali',
    author_email='zmerali@cisco.com',
    url='https://github.com/zmerali/aiociscospark',
    description='asyncio sdk for Cisco Spark',
    long_description=read('README.rst'),
    install_requires=[
        'aiohttp>=1.3.0',
    ],
    packages=['aiociscospark'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['spark', 'cisco', 'asyncio', 'aiohttp'],
)
