cmake_minimum_required(VERSION 3.25)

project(p4danrecomp
    VERSION 0.1.0
    DESCRIPTION "Native port of Persona 4: Dancing All Night (PS Vita) via static recompilation"
    LANGUAGES C CXX)

# The toolkit (psvrecore): recompiler, runtime, tools and their tests.
add_subdirectory(psvrecore)

# The game: psvrecore's frontend running the recompiled game (a shared library loaded by the Java activity on
# Android, where SDL's activity calls its main).
if(ANDROID)
    add_library(p4danrecomp SHARED src/main.cpp)
    set_target_properties(p4danrecomp PROPERTIES OUTPUT_NAME main)
else()
    add_executable(p4danrecomp src/main.cpp)
endif()
target_link_libraries(p4danrecomp PRIVATE psvrecore::frontend)
psvrecore_target_defaults(p4danrecomp)

if(PSVRECORE_BUILD_TESTS)
    enable_testing()  # here too, so ctest from the build root runs psvrecore's tests (and the game's, once it has any)
endif()
