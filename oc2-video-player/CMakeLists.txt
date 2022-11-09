cmake_minimum_required(VERSION 3.5)

set(CMAKE_C_FLAGS "-O2 -s")

project(oc2-video-player C)

include(ExternalProject)

add_executable(main main.c)
