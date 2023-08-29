from conan import ConanFile
from conan.tools.files import get
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class fmtRecipe(ConanFile):
    name = "fmt"
    version = "10.1.0"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    implements = ["auto_shared_fpic"]

    def source(self):

        url = "https://github.com/jcar87/fmt/archive/7f56699bfbef8bb07829c0aee73ef01844424289.zip"
        checksum = "c0b827ebc63ea5d61bce363e5a5c79e6e769d6ea551d2fb25c691f6b9ad16f82"
        get(self, url=url, sha256=checksum, strip_root=True)

    def layout(self):
        cmake_layout(self)

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

    def package_info(self):
        self.cpp_info.libs = ["fmt"]
        # self.cpp_info.set_property("cmake_find_mode", "none")
        # self.cpp_info.builddirs = ["."]

    

    

