cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

find_path(MUMPS_INCLUDE_DIR dmumps_c.h REQUIRED)
find_library(DMUMPS_LIB NAMES coinmumps dmumps)

add_custom_command(
  OUTPUT _dmumps.c
  COMMAND Python::Interpreter -m cython
          "${CMAKE_CURRENT_SOURCE_DIR}/mumps/_dmumps.pyx" --output-file _dmumps.c
  DEPENDS mumps/_dmumps.pyx
  VERBATIM)

python_add_library(_dmumps MODULE _dmumps.c WITH_SOABI)
target_include_directories(_dmumps PRIVATE ${MUMPS_INCLUDE_DIR})
target_link_libraries(_dmumps PRIVATE ${DMUMPS_LIB})

install(TARGETS _dmumps DESTINATION mumps)
