import os
import shutil
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import copy


class RabbitmqCConan(ConanFile):
    name = "rabbitmq-c"
    version = "0.14.0"
    license = "MIT"
    url = "https://github.com/alanxz/rabbitmq-c"
    description = "C library for RabbitMQ"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "cmake/*", "librabbitmq/*", "librabbitmq.pc.in", "tests/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)

        # Build shared library
        cmake.configure(variables={"BUILD_SHARED_LIBS": "ON"})
        cmake.build()
        cmake.install()

        # Clean up build directory
        cmake.configure(variables={"BUILD_SHARED_LIBS": "OFF"})
        cmake.build()
        cmake.install()

    def package(self):
        include_dir = os.path.join(self.package_folder, "include")
        lib_dir = os.path.join(self.package_folder, "lib")
        bin_dir = os.path.join(self.package_folder, "bin")

        # Copy include files
        shutil.copytree("include", include_dir, dirs_exist_ok=True)

        # Copy library files
        for root, _, files in os.walk(self.build_folder):
            for file in files:
                if file.endswith((".lib", ".dll", ".so", ".dylib", ".a")):
                    shutil.copy(os.path.join(root, file), lib_dir)

    def package_info(self):
        self.cpp_info.libs = ["rabbitmq"]


# from conan import ConanFile
# from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
# from conan.tools.files import copy


# class RabbitmqCConan(ConanFile):
#     name = "rabbitmq-c"
#     version = "0.14.0"
#     license = "MIT"
#     url = "https://github.com/alanxz/rabbitmq-c"
#     description = "C library for RabbitMQ"
#     settings = "os", "compiler", "build_type", "arch"
#     options = {"shared": [True, False], "fPIC": [True, False]}
#     default_options = {"shared": True, "fPIC": True}
#     exports_sources = "CMakeLists.txt", "src/*", "include/*", "cmake/*", "librabbitmq/*", "librabbitmq.pc.in", "tests/*"

#     def config_options(self):
#         if self.settings.os == "Windows":
#             del self.options.fPIC

#     def configure(self):
#         if self.options.shared:
#             del self.options.fPIC

#     def generate(self):
#         tc = CMakeToolchain(self)
#         tc.generate()
#         deps = CMakeDeps(self)
#         deps.generate()

#     def build(self):
#         cmake = CMake(self)
#         cmake.configure()
#         cmake.build()

#     def package(self):
#         cmake = CMake(self)
#         cmake.install()
#         self.copy("*.h", dst="include", src="include")
#         self.copy("*.lib", dst="lib", keep_path=False)
#         self.copy("*.dll", dst="bin", keep_path=False)
#         self.copy("*.so", dst="lib", keep_path=False)
#         self.copy("*.dylib", dst="lib", keep_path=False)
#         self.copy("*.a", dst="lib", keep_path=False)

#     def package_info(self):
#         self.cpp_info.libs = ["rabbitmq"]
