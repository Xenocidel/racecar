# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ubuntu/catkin_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ubuntu/catkin_ws/build

# Include any dependencies generated for this target.
include race/CMakeFiles/ZedFuncs.dir/depend.make

# Include the progress variables for this target.
include race/CMakeFiles/ZedFuncs.dir/progress.make

# Include the compile flags for this target's objects.
include race/CMakeFiles/ZedFuncs.dir/flags.make

race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o: race/CMakeFiles/ZedFuncs.dir/flags.make
race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o: /home/ubuntu/catkin_ws/src/race/src/zedMagic.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/ubuntu/catkin_ws/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o"
	cd /home/ubuntu/catkin_ws/build/race && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o -c /home/ubuntu/catkin_ws/src/race/src/zedMagic.cpp

race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.i"
	cd /home/ubuntu/catkin_ws/build/race && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/ubuntu/catkin_ws/src/race/src/zedMagic.cpp > CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.i

race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.s"
	cd /home/ubuntu/catkin_ws/build/race && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/ubuntu/catkin_ws/src/race/src/zedMagic.cpp -o CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.s

race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.requires:
.PHONY : race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.requires

race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.provides: race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.requires
	$(MAKE) -f race/CMakeFiles/ZedFuncs.dir/build.make race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.provides.build
.PHONY : race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.provides

race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.provides.build: race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o

# Object files for target ZedFuncs
ZedFuncs_OBJECTS = \
"CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o"

# External object files for target ZedFuncs
ZedFuncs_EXTERNAL_OBJECTS =

/home/ubuntu/catkin_ws/devel/lib/libZedFuncs.so: race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o
/home/ubuntu/catkin_ws/devel/lib/libZedFuncs.so: race/CMakeFiles/ZedFuncs.dir/build.make
/home/ubuntu/catkin_ws/devel/lib/libZedFuncs.so: race/CMakeFiles/ZedFuncs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library /home/ubuntu/catkin_ws/devel/lib/libZedFuncs.so"
	cd /home/ubuntu/catkin_ws/build/race && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ZedFuncs.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
race/CMakeFiles/ZedFuncs.dir/build: /home/ubuntu/catkin_ws/devel/lib/libZedFuncs.so
.PHONY : race/CMakeFiles/ZedFuncs.dir/build

race/CMakeFiles/ZedFuncs.dir/requires: race/CMakeFiles/ZedFuncs.dir/src/zedMagic.cpp.o.requires
.PHONY : race/CMakeFiles/ZedFuncs.dir/requires

race/CMakeFiles/ZedFuncs.dir/clean:
	cd /home/ubuntu/catkin_ws/build/race && $(CMAKE_COMMAND) -P CMakeFiles/ZedFuncs.dir/cmake_clean.cmake
.PHONY : race/CMakeFiles/ZedFuncs.dir/clean

race/CMakeFiles/ZedFuncs.dir/depend:
	cd /home/ubuntu/catkin_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ubuntu/catkin_ws/src /home/ubuntu/catkin_ws/src/race /home/ubuntu/catkin_ws/build /home/ubuntu/catkin_ws/build/race /home/ubuntu/catkin_ws/build/race/CMakeFiles/ZedFuncs.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : race/CMakeFiles/ZedFuncs.dir/depend

