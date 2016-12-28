#coding=utf-8
import sys,os,shutil,ConfigParser


from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = cythonize("**/Arch*.py", exclude="ArchDataStruct.py")

# Only compile the following if numpy is installed.
try:
    from numpy.distutils.misc_util import get_numpy_include_dirs
    numpy_demo = [Extension("*",
                            ["ArchDocumentObject.py"],
                            include_dirs=get_numpy_include_dirs())]
    ext_modules.extend(cythonize(numpy_demo))
except ImportError:
    pass

setup(
  name = 'ArchDocumentObject',
  ext_modules = ext_modules,
)


try:
    from numpy.distutils.misc_util import get_numpy_include_dirs
    numpy_demo = [Extension("*",
                            ["ArchDefine.py"],
                            include_dirs=get_numpy_include_dirs())]
    ext_modules.extend(cythonize(numpy_demo))
except ImportError:
    pass

setup(
  name = 'ArchDefine',
  ext_modules = ext_modules,
)

cf = ConfigParser.ConfigParser()


path=os.getcwd()
sourcefile=os.path.join(path,unicode('ArchData/ArchDocumentObject.so','utf8'))
shutil.copyfile(sourcefile,'%s/%s'%(path,'ArchDocumentObject.so'))
sourcefile=os.path.join(path,unicode('ArchData/ArchDefine.so','utf8'))
shutil.copyfile(sourcefile,'%s/%s'%(path,'ArchDefine.so'))