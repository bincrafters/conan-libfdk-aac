#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class FDKAACConan(ConanFile):
    name = "libfdk-aac"
    version = "0.1.5"
    url = "https://github.com/bincrafters/conan-libfdk-aac"
    description = "A standalone library of the Fraunhofer FDK AAC code from Android"
    license = "https://github.com/mstorsjo/fdk-aac/blob/master/NOTICE"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        source_url = "https://github.com/mstorsjo/fdk-aac/archive/v%s.tar.gz" % self.version
        tools.get(source_url)
        extracted_dir = "fdk-aac-" + self.version
        os.rename(extracted_dir, "sources")

    def build_vs(self):
        raise Exception("TODO")

    def build_configure(self):
        with tools.chdir('sources'):
            args = ['--prefix=%s' % self.package_folder]
            if self.options.shared:
                args.extend(['--disable-static', '--enable-shared'])
            else:
                args.extend(['--disable-shared', '--enable-static'])
            env_build = AutoToolsBuildEnvironment(self)
            self.run('autoreconf -fiv')
            env_build.configure(args=args)
            env_build.make()
            env_build.make(args=['install'])

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            self.build_vs()
        else:
            self.build_configure()

    def package(self):
        self.copy(pattern="NOTICE", src='sources')

    def package_info(self):
        self.cpp_info.libs = ['fdk-aac']
