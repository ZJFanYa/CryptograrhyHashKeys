all:
	swig -c++ -python bigNumDLL.i
	g++ -fPIC -c bigNumDLL.cpp
	g++ -fPIC -c bigNumDLL_wrap.cxx -I/usr/include/python2.7
	g++ -shared bigNumDLL.o bigNumDLL_wrap.o -o _bigNumDLL.so
	rm *.o *.cxx

windows32:
	"C:\Program Files\swigwin-3.0.0\swig" -c++ -python bigNumDLL.i
	g++ -fPIC -c bigNumDLL.cpp
	g++ -c bigNumDLL_wrap.cxx -IC:\Python27\include
	g++ bigNumDLL.o bigNumDLL_wrap.o -Ic:\python27\include -Lc:\python27\libs -lpython27 -shared -o _bigNumDLL.pyd
	
windows64:
	"C:\Program Files\swigwin-3.0.0\swig" -c++ -python bigNumDLL.i
	C:\TDM-GCC-64\bin\g++ -c bigNumDLL.cpp
	C:\TDM-GCC-64\bin\g++ -c bigNumDLL_wrap.cxx -IC:\Python27\include
	C:\TDM-GCC-64\bin\g++ bigNumDLL.o bigNumDLL_wrap.o -Ic:\python27\include -Lc:\python27\libs -lpython27 -shared -o _bigNumDLL.pyd
	del *.o *.cxx