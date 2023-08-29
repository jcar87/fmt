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

        url = "https://github.com/jcar87/fmt/archive/1e5d99ff3f1f4eb9879d7669bca9c5f30214f7ee.zip"
        checksum = "66ccc6796b33af3aed2671c91ec08e6ea2a46621a506847a3a9273a1aaf3008d"
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
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "fmt*.ifc", src=os.path.join(self.build_folder, "fmt.dir", "Release"), dst=os.path.join(self.package_folder, "bmi"))

    def package_info(self):
        self.cpp_info.libs = ["fmt"]
        if is_msvc(self):
            bmi_dir = os.path.join(self.package_folder, "bmi").replace('\\','/')
            self.cpp_info.cxxflags = ["/reference fmt=fmt.cc.ifc", f"/ifcSearchDir{bmi_dir}"]

        # self.cpp_info.set_property("cmake_find_mode", "none")
        # self.cpp_info.builddirs = ["."]

    

    

