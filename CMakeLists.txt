cmake_minimum_required(VERSION 3.10)

project(FieldCalibrator)

find_package(OpenCV CONFIG REQUIRED)
find_package(apriltag CONFIG REQUIRED)
find_package(ceres CONFIG REQUIRED)
find_package(CLI11 CONFIG REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(FieldCalibrator src/main.cpp)

set_property(TARGET FieldCalibrator PROPERTY CXX_STANDARD 20)
target_link_options(FieldCalibrator PRIVATE -fsanitize=address -O3)
add_definitions(-DEIGEN_MAX_ALIGN_BYTES=0)

target_include_directories(FieldCalibrator PRIVATE ${CLI11_INCLUDE_DIR})
target_link_libraries(FieldCalibrator PRIVATE opencv_core opencv_imgproc opencv_highgui opencv_video opencv_videoio apriltag::apriltag Ceres::ceres CLI11::CLI11 Eigen3::Eigen nlohmann_json::nlohmann_json)
