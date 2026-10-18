cmake_minimum_required(VERSION 3.25)

project(p4danrecomp
    VERSION 0.1.0
    DESCRIPTION "Native port of Persona 4: Dancing All Night (PS Vita) via static recompilation"
    LANGUAGES C CXX)

# The toolkit (psvrecore): recompiler, runtime, tools and their tests.
add_subdirectory(psvrecore)

if(PSVRECORE_BUILD_TESTS)
    enable_testing()  # here too, so ctest from the build root runs psvrecore's tests (and the game's, once it has any)
endif()
