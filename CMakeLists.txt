# Cmake needs this line
cmake_minimum_required(VERSION 2.8)

# Define project name
#project(Project)

# Find OpenCV, if you did not install opencv in the default path, you need to set OpenCV_DIR variable first
set(OpenCV_DIR /path/to/opencv-3.2/share/OpenCV) #s Set the OpenCV path where you installed
find_package(OpenCV)

# Print some message showing some of them
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")

# Add OpenCV headers location to your include paths
include_directories(${OpenCV_INCLUDE_DIRS})

# Declare the executable target built from your sources
add_executable(main main.cpp)

# Link your application with OpenCV libraries
target_link_libraries(main ${OpenCV_LIBS})


