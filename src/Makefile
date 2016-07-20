libs  = -L/usr/local/lib
libs += -L/usr/local/cuda-7.5/lib64
libs += -lopencv_calib3d
libs += -lopencv_contrib
libs += -lopencv_core
libs += -lopencv_features2d
libs += -lopencv_flann
libs += -lopencv_gpu
libs += -lopencv_highgui
libs += -lopencv_imgproc
libs += -lopencv_legacy
libs += -lopencv_ml
libs += -lopencv_objdetect
libs += -lopencv_photo
libs += -lopencv_stitching
libs += -lopencv_superres
libs += -lopencv_ts
libs += -lopencv_video
libs += -lopencv_videostab
libs += -lcufft
libs += -lnpps
libs += -lnppi
libs += -lnppc
libs += -lcudart
libs += -lrt
libs += -lpthread
libs += -lm
libs += -ldl  

inc += -I/usr/local/include
inc += -I/usr/local/include/opencv
inc += -I/usr/local/caffe/include
inc += -I/usr/local/cuda-7.5/include

CFLAGS=-g
UTILS = bright cropper example snapshots extract_fg

all: $(UTILS)
clean:
	rm -f $(UTILS) *.o
example: example.o
	g++ $(CFLAGS) -o example example.o $(libs)
example.o: example.cpp
	g++ $(CFLAGS) $(inc) -c example.cpp
bright.o: bright.cpp
	g++ $(CFLAGS) $(inc) -c bright.cpp
bright: bright.o
	g++ $(CFLAGS) -o bright bright.o $(libs)
snapshots.o: snapshots.cpp
	g++ $(CFLAGS) $(inc) -c snapshots.cpp
snapshots: snapshots.o
	g++ $(CFLAGS) -o snapshots snapshots.o $(libs)
cropper.o: cropper.cpp
	g++ $(CFLAGS) $(inc) -c cropper.cpp
cropper: cropper.o
	g++ $(CFLAGS) -o cropper cropper.o $(libs)
extract_fg.o: extract_fg.cpp
	g++ $(CFLAGS) $(inc) -c extract_fg.cpp
extract_fg: extract_fg.o
	g++ $(CFLAGS) -o extract_fg extract_fg.o $(libs)
