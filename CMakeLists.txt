cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

set(MUMPS_ROOT "" CACHE PATH "MUMPS root directory")

message(STATUS "Looking for MUMPS in ${MUMPS_ROOT}...")

# Find MUMPS include directory
find_path(MUMPS_INCLUDE_DIR
    NAMES smumps_c.h dmumps_c.h cmumps_c.h zmumps_c.h
    HINTS ${MUMPS_ROOT}
    PATH_SUFFIXES include include/coin-or/mumps
    REQUIRED)

# Find MUMPS libraries (try coinmumps first, then individual libs, then seq variants)
find_library(SMUMPS_LIB
    NAMES coinmumps smumps smumps_seq
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

find_library(CMUMPS_LIB
    NAMES coinmumps cmumps cmumps_seq
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

find_library(DMUMPS_LIB
    NAMES coinmumps dmumps dmumps_seq
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

find_library(ZMUMPS_LIB
    NAMES zmumps zmumps_seq
    HINTS ${MUMPS_ROOT}/lib
    OPTIONAL
)

# Detect MUMPS version from header
set(_MUMPS_VERSION_LINE "")
set(_HEADER_list smumps_c.h dmumps_c.h cmumps_c.h zmumps_c.h)
foreach (_HEADER IN LISTS _HEADER_list)
    if(NOT _MUMPS_VERSION_LINE)
        file(STRINGS "${MUMPS_INCLUDE_DIR}/${_HEADER}" _MUMPS_VERSION_LINE
             REGEX "^#define MUMPS_VERSION[ \t]+\"[0-9]+\\.[0-9]+\\.[0-9]+\"")
    endif()
endforeach()
if(_MUMPS_VERSION_LINE)
    string(REGEX MATCH "\"([0-9]+\\.[0-9]+\\.[0-9]+)\"" _ "${_MUMPS_VERSION_LINE}")
    set(MUMPS_VERSION "${CMAKE_MATCH_1}")
    message(STATUS "Detected MUMPS version: ${MUMPS_VERSION}")
else()
    message(WARNING "Could not detect MUMPS version from header, defaulting to 5.7.x")
    set(MUMPS_VERSION "5.7.0")
endif()

# Generate Cython wrappers (passing detected version)
add_custom_command(
  OUTPUT mumps/_smumps.pyx mumps/_dmumps.pyx mumps/_cmumps.pyx mumps/_zmumps.pyx
  COMMAND Python::Interpreter
          "${CMAKE_CURRENT_SOURCE_DIR}/generate_wrappers.py"
          "--version" "${MUMPS_VERSION}"
  VERBATIM)

if(SMUMPS_LIB)
    message(STATUS "SMUMPS detected")
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
else()
    message(STATUS "SMUMPS not found, skipping _smumps wrapper")
endif()

if(CMUMPS_LIB)
    message(STATUS "CMUMPS detected")
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
else()
    message(STATUS "CMUMPS not found, skipping _cmumps wrapper")
endif()

if(DMUMPS_LIB)
    message(STATUS "DMUMPS detected")
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
else()
    message(STATUS "DMUMPS not found, skipping _dmumps wrapper")
endif()

if(ZMUMPS_LIB)
    message(STATUS "ZMUMPS detected")
    add_custom_command(
      OUTPUT _zmumps.c
      COMMAND Python::Interpreter -m cython
              "${CMAKE_CURRENT_SOURCE_DIR}/mumps/_zmumps.pyx" --output-file _zmumps.c
      DEPENDS mumps/_zmumps.pyx
      VERBATIM)

    python_add_library(_zmumps MODULE _zmumps.c WITH_SOABI)
    target_include_directories(_zmumps PRIVATE ${MUMPS_INCLUDE_DIR})
    target_link_libraries(_zmumps PRIVATE ${ZMUMPS_LIB})
    install(TARGETS _zmumps DESTINATION mumps)
else()
    message(STATUS "ZMUMPS not found, skipping _zmumps wrapper")
endif()
