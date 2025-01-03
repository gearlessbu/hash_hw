file(GLOB_RECURSE basic_cpp_files "./src/*.cpp")

add_library(hash_basic SHARED ${basic_cpp_files})