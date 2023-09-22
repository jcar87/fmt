cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)
if(NOT DEFINED CMAKE_EXPERIMENTAL_CXX_MODULE_CMAKE_API)
  #CMake 3.27
  set(CMAKE_EXPERIMENTAL_CXX_MODULE_CMAKE_API "aa1f7df0-828a-4fcd-9afc-2dc80491aca7")
endif()

set(CMAKE_EXPERIMENTAL_CXX_MODULE_DYNDEP 1)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
  # From: https://github.com/Kitware/CMake/blob/master/.gitlab/ci/cxx_modules_rules_gcc.cmake
  string(CONCAT CMAKE_EXPERIMENTAL_CXX_SCANDEP_SOURCE
    "<CMAKE_CXX_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -E -x c++ <SOURCE>"
    " -MT <DYNDEP_FILE> -MD -MF <DEP_FILE>"
    " -fmodules-ts -fdeps-file=<DYNDEP_FILE> -fdeps-target=<OBJECT> -fdeps-format=p1689r5"
    " -o <PREPROCESSED_SOURCE>")
  set(CMAKE_EXPERIMENTAL_CXX_MODULE_MAP_FORMAT "gcc")
  string(CONCAT CMAKE_EXPERIMENTAL_CXX_MODULE_MAP_FLAG
    # Turn on modules.
    "-fmodules-ts"
    # Read the module mapper file.
    " -fmodule-mapper=<MODULE_MAP_FILE>"
    # Make sure dependency tracking is enabled (missing from `try_*`).
    " -MD"
    # Suppress `CXX_MODULES +=` from generated depfile snippets.
    " -fdeps-format=p1689r5"
    # Force C++ as a language.
    " -x c++")
  set(CMAKE_EXPERIMENTAL_CXX_MODULE_BMI_ONLY_FLAG "-fmodule-only")
endif()

find_package(fmt CONFIG REQUIRED)

add_executable(example src/example.cpp)
target_link_libraries(example fmt::fmt)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
target_compile_options(example PRIVATE "-fmodule-mapper=${CMAKE_SOURCE_DIR}/modules.map")
endif()
