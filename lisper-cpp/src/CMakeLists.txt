find_package(BISON 3.0.0)
find_package(FLEX)

bison_target(parser lisper/parser.y ${CMAKE_CURRENT_BINARY_DIR}/parser.cc)
flex_target(lexer lisper/lexer.l ${CMAKE_CURRENT_BINARY_DIR}/lexer.cc)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
file(GLOB_RECURSE lisper_sources lisper/*.cc)

add_library(
  lisper_lib
  ${BISON_parser_OUTPUTS}
  ${FLEX_lexer_OUTPUTS}
  ${lisper_sources}
)

target_link_libraries(lisper_lib)

install(TARGETS lisper_lib
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
