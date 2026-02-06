cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

find_library(DMUMPS_LIB dmumps)
find_library(MUMPS_COMMON_LIB mumps_common)

add_custom_command(
  OUTPUT _dmumps.c
  COMMAND Python::Interpreter -m cython
          "${CMAKE_CURRENT_SOURCE_DIR}/mumps/_dmumps.pyx" --output-file _dmumps.c
  DEPENDS mumps/_dmumps.pyx
  VERBATIM)

python_add_library(_dmumps MODULE _dmumps.c WITH_SOABI)
target_link_libraries(_dmumps PRIVATE ${DMUMPS_LIB} ${MUMPS_COMMON_LIB})

install(TARGETS _dmumps DESTINATION mumps)
