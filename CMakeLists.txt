cmake_minimum_required(VERSION 3.0)
project(gtsam_gnss CXX C)

# Enforce c++17 standards
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define user options
option(GTSAM_GNSS_BUILD_PYTHON "Build Python bindings." OFF)
option(GTSAM_GNSS_BUILD_MATLAB "Build Matlab bindings." ON)

set(WRAP_PYTHON_VERSION
    "Default"
    CACHE STRING "The Python version to use for wrapping")

set(WRAP_TOOLBOX_INSTALL_PATH
    "${CMAKE_INSTALL_PREFIX}/gtsam_toolbox"
    CACHE
      PATH
      "Matlab toolbox destination")

# Configure Microsoft-specific build options
if(MSVC)
  add_compile_options(-DBOOST_ALL_NO_LIB)
  set(GTSAMCMakeTools_DIR "C:/Program Files (x86)/GTSAM/CMake/GTSAMCMakeTools")
  set(gtwrap_DIR "C:/Program Files (x86)/GTSAM/CMake/gtwrap")
  set(CMAKE_INSTALL_PREFIX "C:/Program Files (x86)/GTSAM")
endif(MSVC)

# Find GTSAM components
find_package(GTSAM REQUIRED)
if(GTSAM_NOT_FOUND)
  message(FATAL_ERROR "This program requires the GTSAM library.")
endif(GTSAM_NOT_FOUND)

# Include GTSAM CMake tools
find_package(GTSAMCMakeTools)

# Import gtwrap package
find_package(gtwrap)
gtwrap_get_python_version(${WRAP_PYTHON_VERSION})

if (GTSAM_GNSS_BUILD_MATLAB)
  # Include the Matlab related code
  include(MatlabWrap)
endif()

# Include project headers
include_directories("${PROJECT_SOURCE_DIR}/src")

# Add sorce code directory
add_subdirectory(src)

# Install library
install(
  TARGETS ${PROJECT_NAME}
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin)

# ##############################################################################

# Build Python wrapper
if (GTSAM_GNSS_BUILD_PYTHON)
  add_subdirectory(python)
endif()

# Build MATLAB wrapper
if (GTSAM_GNSS_BUILD_MATLAB)
  matlab_wrap("${PROJECT_SOURCE_DIR}/gtsam_gnss.i" "${PROJECT_NAME}" "" "" "${mexFlags}" "${FilesToIgnore}" OFF)
endif()

message("========== Configuration Options ==========")
message(STATUS "Project:                  ${PROJECT_NAME}")
if (GTSAM_GNSS_BUILD_PYTHON)
  message(STATUS "Python:                   ${Python_EXECUTABLE}")
  message(STATUS "Python version:           ${WRAP_PYTHON_VERSION}")
endif()
if (GTSAM_GNSS_BUILD_MATLAB)
  message(STATUS "MATLAB Root:              ${MATLAB_ROOT}")
  message(STATUS "Mex Compiler:             ${Matlab_MEX_COMPILER}")
endif()
message("===========================================")
