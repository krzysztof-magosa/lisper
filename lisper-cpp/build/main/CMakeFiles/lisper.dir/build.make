# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


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
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.7.2_1/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.7.2_1/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/km/projects/lisper-cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/km/projects/lisper-cpp/build

# Include any dependencies generated for this target.
include main/CMakeFiles/lisper.dir/depend.make

# Include the progress variables for this target.
include main/CMakeFiles/lisper.dir/progress.make

# Include the compile flags for this target's objects.
include main/CMakeFiles/lisper.dir/flags.make

main/CMakeFiles/lisper.dir/lisper.cc.o: main/CMakeFiles/lisper.dir/flags.make
main/CMakeFiles/lisper.dir/lisper.cc.o: ../main/lisper.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/km/projects/lisper-cpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object main/CMakeFiles/lisper.dir/lisper.cc.o"
	cd /Users/km/projects/lisper-cpp/build/main && /Library/Developer/CommandLineTools/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/lisper.dir/lisper.cc.o -c /Users/km/projects/lisper-cpp/main/lisper.cc

main/CMakeFiles/lisper.dir/lisper.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/lisper.dir/lisper.cc.i"
	cd /Users/km/projects/lisper-cpp/build/main && /Library/Developer/CommandLineTools/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/km/projects/lisper-cpp/main/lisper.cc > CMakeFiles/lisper.dir/lisper.cc.i

main/CMakeFiles/lisper.dir/lisper.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/lisper.dir/lisper.cc.s"
	cd /Users/km/projects/lisper-cpp/build/main && /Library/Developer/CommandLineTools/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/km/projects/lisper-cpp/main/lisper.cc -o CMakeFiles/lisper.dir/lisper.cc.s

main/CMakeFiles/lisper.dir/lisper.cc.o.requires:

.PHONY : main/CMakeFiles/lisper.dir/lisper.cc.o.requires

main/CMakeFiles/lisper.dir/lisper.cc.o.provides: main/CMakeFiles/lisper.dir/lisper.cc.o.requires
	$(MAKE) -f main/CMakeFiles/lisper.dir/build.make main/CMakeFiles/lisper.dir/lisper.cc.o.provides.build
.PHONY : main/CMakeFiles/lisper.dir/lisper.cc.o.provides

main/CMakeFiles/lisper.dir/lisper.cc.o.provides.build: main/CMakeFiles/lisper.dir/lisper.cc.o


# Object files for target lisper
lisper_OBJECTS = \
"CMakeFiles/lisper.dir/lisper.cc.o"

# External object files for target lisper
lisper_EXTERNAL_OBJECTS =

main/lisper: main/CMakeFiles/lisper.dir/lisper.cc.o
main/lisper: main/CMakeFiles/lisper.dir/build.make
main/lisper: src/liblisper_lib.a
main/lisper: main/CMakeFiles/lisper.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/km/projects/lisper-cpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable lisper"
	cd /Users/km/projects/lisper-cpp/build/main && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/lisper.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
main/CMakeFiles/lisper.dir/build: main/lisper

.PHONY : main/CMakeFiles/lisper.dir/build

main/CMakeFiles/lisper.dir/requires: main/CMakeFiles/lisper.dir/lisper.cc.o.requires

.PHONY : main/CMakeFiles/lisper.dir/requires

main/CMakeFiles/lisper.dir/clean:
	cd /Users/km/projects/lisper-cpp/build/main && $(CMAKE_COMMAND) -P CMakeFiles/lisper.dir/cmake_clean.cmake
.PHONY : main/CMakeFiles/lisper.dir/clean

main/CMakeFiles/lisper.dir/depend:
	cd /Users/km/projects/lisper-cpp/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/km/projects/lisper-cpp /Users/km/projects/lisper-cpp/main /Users/km/projects/lisper-cpp/build /Users/km/projects/lisper-cpp/build/main /Users/km/projects/lisper-cpp/build/main/CMakeFiles/lisper.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : main/CMakeFiles/lisper.dir/depend
