'''
from setuptools import setup, find_packages

setup(
    name = "CDO", 
    version="0.1.0",
    packages = ['CDO'],
    description = "CDO",
    author = "Hisin Wang",
    author_email = "wangyao1052@163.com",
    platforms = "Independant"
)
'''
from setuptools import setup
setup(
    name='CDO',
    version='0.1',
    description='Coroutine-based networking library',
    author='Linden Lab',
    author_email='sldev@lists.secondlife.com',
    url='http://wiki.secondlife.com/wiki/Eventlet',
    packages=['CDO'],
      long_description="""\
      eventlet is a coroutines-based network library for python ...
      """,
      classifiers=[
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Topic :: Internet",
      ],
      keywords='networking eventlet nonblocking internet',
      license='GPL',
      install_requires=[
        'setuptools',
        'greenlet',
      ],
)