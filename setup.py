import io
from os.path import abspath, dirname, join
import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup, find_packages

HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
    name='micropython-netpie',
    py_modules=['netpie','simple'],
    version='1.0.0',
    install_requires=[],
    description='MicroPython Library for Interfacing with the NETPIE IoT Platform',
    long_description=DESCRIPTION,
    keywords= ['NETPIE', 'esp32', 'esp8266' ,'micropython'],
    url='https://github.com/PerfecXX/MicroPython-NETPIE',
    author='Teeraphat Kullanankanjana',
    author_email='ku.teeraphat@hotmail.com',
    maintainer='Teeraphat Kullanankanjana',
    maintainer_email='ku.teeraphat@hotmail.com',
    license='MIT',
    classifiers = [
        'Development Status :: 3 - Alpha', 
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ],
)

