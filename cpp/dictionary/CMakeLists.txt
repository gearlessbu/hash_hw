file(GLOB_RECURSE dictionary_cpp_files "./src/*.cpp")

add_library(hash_dictionary SHARED ${dictionary_cpp_files})
target_link_libraries(hash_dictionary hash_basic)

# Add a test project.
add_executable(test_probing "./test_probing.cpp")
target_link_libraries(test_probing hash_dictionary hash_basic)