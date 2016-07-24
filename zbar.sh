wget https://pypi.python.org/packages/source/z/zbar/zbar-0.10.tar.bz2
wget https://github.com/npinchot/zbar/commit/d3c1611ad2411fbdc3e79eb96ca704a63d30ae69.diff
tar jxvf zbar-0.10.tar.bz2
cd zbar-0.10
patch -p1 < ../d3c1611ad2411fbdc3e79eb96ca704a63d30ae69.diff
python setup.py install
