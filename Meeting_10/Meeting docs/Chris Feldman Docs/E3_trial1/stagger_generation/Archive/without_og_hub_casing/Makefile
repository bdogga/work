
#
LIBDIR = lib

DEFINE = -DUNDERSCORE -DBO_DEC
FCOMP  = ifort
#FOPTS  = -O -fno-second-underscore -fPIC -g
FOPTS = -fPIC -g

OBJS =   geomturbo_creator.o

XLIBS  = -L/usr/X11R6/lib64 -lX11 -lpthread
GLIBS  = -L/usr/X11R6/lib64 -lGLU -lGL -lX11 -lXext -lpthread

#default:	3dbgb

geomturbo:	$(OBJS)
	$(FCOMP)  -g $(OBJS) -o geomturbo 

geomturbo_creator.o:geomturbo_creator.f90
	$(FCOMP) $(FOPTS) -c geomturbo_creator.f90

clean:
	-rm -f geomturbo geomturbo_creator.o

