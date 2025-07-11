cmake_minimum_required(VERSION 3.16)
project(GrafoDinamico_Qt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

add_executable(GrafoDinamico_Qt
  main.cpp
  mainwindow.cpp
  mainwindow.h
  grafowidget.cpp
  grafowidget.h
)

target_link_libraries(GrafoDinamico_Qt PRIVATE Qt6::Widgets)