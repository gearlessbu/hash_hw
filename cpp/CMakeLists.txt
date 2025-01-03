cmake_minimum_required(VERSION 3.16)

project(Hash)

# Project-wide setup.
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)

# Customized macro.
# if(HASH_CHECK)
#     add_definitions(-DHASH_CHECK)
# endif()

# Configure include and lib paths.
include_directories("${HASH_ROOT}/cpp/")
# include_directories("${HASH_ROOT}/external/eigen/")

# Compile each library.
# Dependency map:
# basic <- empty;
add_subdirectory("basic")
# dictionary <- basic;
add_subdirectory("dictionary")

# Compile the main program.
# add_executable(main "main.cpp")
# target_link_libraries(main hash_pde_solver)