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

# The game's code, recompiled by scripts/generate_code.py into generated/code (never committed): the executable and
# the modules it imports from (libc, libfios2). Without it the program builds with no code and refuses to start.
set(P4D_GENERATED_DIR "${CMAKE_CURRENT_SOURCE_DIR}/generated/code")
if(EXISTS "${P4D_GENERATED_DIR}/p4d_eboot")
    foreach(_module p4d_eboot p4d_libc p4d_libfios2)
        file(GLOB _sources CONFIGURE_DEPENDS "${P4D_GENERATED_DIR}/${_module}/*.c")
        add_library(${_module}_code STATIC ${_sources})
        target_include_directories(${_module}_code PRIVATE "${P4D_GENERATED_DIR}/${_module}")
        target_link_libraries(${_module}_code PUBLIC psvrecore::recomp_support)
        psvrecore_generated_code(${_module}_code)
        target_link_libraries(p4danrecomp PRIVATE ${_module}_code)
    endforeach()
    target_compile_definitions(p4danrecomp PRIVATE P4D_HAVE_CODE=1)
    message(STATUS "p4danrecomp: the game's generated code from ${P4D_GENERATED_DIR}")
else()
    message(STATUS "p4danrecomp: no generated code (scripts/generate_code.py): the program will refuse to start")
endif()

if(PSVRECORE_BUILD_TESTS)
    enable_testing()  # here too, so ctest from the build root runs psvrecore's tests (and the game's, once it has any)
endif()
