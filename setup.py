import subprocess
import os

from setuptools import setup
from setuptools.command.bdist_wheel import get_platform
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):

    def run(self) -> None:

        cmake_args = [
            'cmake',
            os.path.abspath('.'), # Path to your CMakeLists.txt
        ]
        subprocess.check_call(cmake_args, cwd='.')

        # Build with CMake
        build_args = ['cmake', '--build', '.', '--config', 'Release']
        subprocess.check_call(build_args, cwd='.')

        import shutil
        base_dir = os.getcwd()
        try:
            shutil.move(os.path.join(base_dir, "pybc7.so"), "src/pybc7/pybc7.so")
        except FileNotFoundError:
            shutil.move(os.path.join(base_dir, "Release", "pybc7.dll"), "src/pybc7/pybc7.dll")

        super().run()

    def finalize_options(self):
        self.root_is_pure = False
        self.plat_name = get_platform(None)
        _bdist_wheel.finalize_options(self)

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        # We don't contain any python source
        python, abi = 'py3', 'none'
        return python, abi, plat


setup(cmdclass={'bdist_wheel': bdist_wheel})
