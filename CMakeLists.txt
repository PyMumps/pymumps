cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

set(MUMPS_ROOT "" CACHE PATH "MUMPS root directory")

find_path(MUMPS_INCLUDE_DIR 
    dmumps_c.h 
    HINTS ${MUMPS_ROOT}
    PATH_SUFFIXES include include/coin-or/mumps
    REQUIRED)

find_library(SMUMPS_LIB 
    NAMES smumps
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

find_library(CMUMPS_LIB 
    NAMES cmumps
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

find_library(DMUMPS_LIB 
    NAMES coinmumps dmumps
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

find_library(ZMUMPS_LIB 
    NAMES zmumps
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

add_custom_command(
  OUTPUT mumps/_smumps.pyx mumps/_dmumps.pyx mumps/_cmumps.pyx mumps/_zmumps.pyx
  COMMAND Python::Interpreter
          "${CMAKE_CURRENT_SOURCE_DIR}/generate_wrappers.py"
  VERBATIM)

if(SMUMPS_LIB)
    add_custom_command(
      OUTPUT _smumps.c
      COMMAND Python::Interpreter -m cython
              "${CMAKE_CURRENT_SOURCE_DIR}/mumps/_smumps.pyx" --output-file _smumps.c
      DEPENDS mumps/_smumps.pyx
      VERBATIM)

    python_add_library(_smumps MODULE _smumps.c WITH_SOABI)
    target_include_directories(_smumps PRIVATE ${MUMPS_INCLUDE_DIR})
    target_link_libraries(_smumps PRIVATE ${SMUMPS_LIB})
    install(TARGETS _smumps DESTINATION mumps)
endif()

if(CMUMPS_LIB)
    add_custom_command(
      OUTPUT _cmumps.c
      COMMAND Python::Interpreter -m cython
              "${CMAKE_CURRENT_SOURCE_DIR}/mumps/_cmumps.pyx" --output-file _cmumps.c
      DEPENDS mumps/_cmumps.pyx
      VERBATIM)

    python_add_library(_cmumps MODULE _cmumps.c WITH_SOABI)
    target_include_directories(_cmumps PRIVATE ${MUMPS_INCLUDE_DIR})
    target_link_libraries(_cmumps PRIVATE ${CMUMPS_LIB})
    install(TARGETS _cmumps DESTINATION mumps)
endif()

if(DMUMPS_LIB)
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
endif()

if(ZMUMPS_LIB)
    add_custom_command(
      OUTPUT _zmumps.c
      COMMAND Python::Interpreter -m cython
              "${CMAKE_CURRENT_SOURCE_DIR}/mumps/_zmumps.pyx" --output-file _zmumps.c
      DEPENDS mumps/_dmumps.pyx
      VERBATIM)

    python_add_library(_zmumps MODULE _zmumps.c WITH_SOABI)
    target_include_directories(_zmumps PRIVATE ${MUMPS_INCLUDE_DIR})
    target_link_libraries(_zmumps PRIVATE ${ZMUMPS_LIB})
    install(TARGETS _zmumps DESTINATION mumps)
endif()
