# ------- Preparation -------------------------
# Default command:
#
# ./run.sh CHECK=1
# export CHECK=1

# Parse arguments:
# for ARGUMENT in "$@"
# do
#    KEY=$(echo $ARGUMENT | cut -f1 -d=)

#    KEY_LENGTH=${#KEY}
#    VALUE="${ARGUMENT:$KEY_LENGTH+1}"

#    export "$KEY"="$VALUE"
# done
# echo "Compiling with the following arguments..."
# echo "CHECK: ${CHECK}"

# Specify some root directories.
export HASH_ROOT=$PWD
export HASH_BUILD_ROOT=$PWD/build
mkdir -p build

# -------- Compile our codebase ----------------
cd $HASH_BUILD_ROOT
mkdir -p Hash
cd Hash

# Configure the options for cmake.
CMAKE_OPTIONS="-DHASH_ROOT=${HASH_ROOT}"
# if [ $CHECK != 0 ]; then
#     CMAKE_OPTIONS="${CMAKE_OPTIONS} -DHASH_CHECK=ON"
# else
#     CMAKE_OPTIONS="${CMAKE_OPTIONS} -DHASH_CHECK=OFF"
# fi
cmake ${CMAKE_OPTIONS} ../../cpp/

RET=$?
if [ $RET != 0 ]; then
    echo "$(tput setaf 1)cmake in Hash failed. Please check the output."
    exit
fi

make -j$(nproc)
RET=$?
if [ $RET != 0 ]; then
    echo "$(tput setaf 1)make in Hash failed. Please check the output."
    exit
fi

# Uncomment the lines below if you want to execute the test programs.
# ./basic/test_basic
# ./linear_solver/test_linear_solver
# ./finite_element/test_finite_element
# ./integral/test_integral
# ./pde_solver/test_pde_solver
# ./main

# --------- Back to the root folder -------------
cd $HASH_ROOT



# # --------- Run python binding ------------------
# # "pip3 install ." is recommended but requires Internet connection.
# # "python setup.py install" can run without Internet, but I find it does not update the package
# # when I change binding/ functions. Maybe I will figure it out in the future.
# # python setup.py install
# pip3 install .
# RET=$?
# if [ $RET != 0 ]; then
#     echo "$(tput setaf 1)python binding failed to compile. Please check the output."
#     exit
# fi

# python3.10 -c "import pygrady as pg; pg.PrintInfo('Command line', 'Python binding is successful.')"
# RET=$?
# if [ $RET != 0 ]; then
#     echo "$(tput setaf 1)python binding failed. Please check the output."
#     exit
# fi

# # --------- Write $HASH_ROOT to a file ---------
# printf 'root = "%s"\n' "$HASH_ROOT" > python/grady_root.py