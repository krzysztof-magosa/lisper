# @TODO this looks like hack for me, maybe there is better way.
include_directories("${CMAKE_CURRENT_BINARY_DIR}/../src")

find_package(Threads REQUIRED)

add_executable(
  lisper
  lisper.cc
)
target_link_libraries(lisper lisper_lib)
target_link_libraries(lisper ${CMAKE_THREAD_LIBS_INIT})
install(TARGETS lisper
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
