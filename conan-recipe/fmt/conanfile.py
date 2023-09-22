from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, get
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.microsoft import is_msvc

import os

class fmtRecipe(ConanFile):
    name = "fmt"
    version = "10.0.0"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    implements = ["auto_shared_fpic"]

    def source(self):

        url = "https://github.com/jcar87/fmt/archive/9c8c64f66df3e6c9e4f46714b1b2294eae743b46.zip"
        checksum = "39eef94cc801e8d2abdf0ec3bd196c0de031981f1f74a36743592bae215c7b80"
        get(self, url=url, sha256=checksum, strip_root=True)

    def layout(self):
        cmake_layout(self)

    def validate(self):
        check_min_cppstd(self, "20")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["FMT_TEST"] = "OFF"
        tc.cache_variables["FMT_INSTALL"] = "ON"
        tc.cache_variables["FMT_FUZZ"] = "OFF"
        tc.cache_variables["CMAKE_VISIBILITY_INLINES_HIDDEN"] = "OFF"
        tc.cache_variables["CMAKE_CXX_VISIBILITY_PRESET"] = "default"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        #msvc
        copy(self, "fmt*.ifc", src=os.path.join(self.build_folder, "fmt.dir", "Release"), dst=os.path.join(self.package_folder, "bmi"))
        #clang
        copy(self, "fmt.pcm", src=os.path.join(self.build_folder, "CMakeFiles", "fmt.dir"), dst=os.path.join(self.package_folder, "bmi"))
        #gcc
        copy(self, "fmt.gcm", src=os.path.join(self.build_folder, "CMakeFiles", "fmt.dir"), dst=os.path.join(self.package_folder, "bmi"))

    def package_info(self):
        self.cpp_info.libs = ["fmt"]
        self.cpp_info.includedirs = []
        self.cpp_info.set_property("experimental_modules", ["fmt"])
        if is_msvc(self):
            bmi_dir = os.path.join(self.package_folder, "bmi").replace('\\','/')
            self.cpp_info.cxxflags = ["/reference fmt=fmt.cc.ifc", f"/ifcSearchDir{bmi_dir}"]
        elif self.settings.compiler == "clang":
            self.cpp_info.cxxflags = [f"-fmodule-file=fmt={self.package_folder}/bmi/fmt.pcm"]

        # self.cpp_info.set_property("cmake_find_mode", "none")
        # self.cpp_info.builddirs = ["."]

    

    

