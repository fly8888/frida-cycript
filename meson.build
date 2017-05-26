project('frida-cycript', 'c', 'cpp',
  version: '1.0.0',
  default_options: ['cpp_std=c++11'],
)

host_os_family = host_machine.system()
host_os = host_os_family
host_arch = host_machine.cpu_family()

languages = ['c', 'cpp']
if host_os_family == 'darwin'
  languages += ['objc', 'objcpp']
  add_languages('objc', 'objcpp')
endif

cc = meson.get_compiler('c')

target_conditionals_prefix = '#include <TargetConditionals.h>'

is_macos_src = target_conditionals_prefix + '''
#if !TARGET_OS_OSX
# error Not macOS
#endif
'''
if cc.compiles(is_macos_src, name: 'compiling for macOS')
  host_os = 'macos'
endif

is_ios_src = target_conditionals_prefix + '''
#if !TARGET_OS_IOS
# error Not iOS
#endif
'''
if cc.compiles(is_ios_src, name: 'compiling for iOS')
  host_os = 'ios'
endif

if cc.has_header('android/api-level.h')
  host_os = 'android'
endif

flex = find_program('flex')
bison = find_program(files('ext/toolchain/usr/bin/bison.py'))

cdata = configuration_data()

cdata.set_quoted('CY_SYSTEM', '1')

if get_option('enable_engine')
  cdata.set('CY_EXECUTE', 1)
endif

dep_libs = []

if not cc.has_header('sqlite3.h')
  error('sqlite3 is required')
endif
dep_libs += ['-lsqlite3']

if build_machine.system() == 'darwin'
  result = run_command(find_program('scripts/detect-xcode-clang-libdir'))
  clang_libdir = result.stdout().strip()
  clang_dep = cc.find_library('clang', dirs: clang_libdir)
  clank_link_flags = ['-rpath', clang_libdir]
else
  clang_dep = cc.find_library('clang')
  clank_link_flags = []
endif

configure_file(input: 'config.h.in',
  output: 'config.h',
  configuration: cdata)

add_project_arguments('-include', 'config.h', language: languages)

if cc.get_id() == 'gcc' or cc.get_id() == 'clang'
  candidate_flags = [
    '-Werror',
    '-Wno-non-virtual-dtor',
    ## XXX: this one is used to support GNU Objective-C struct objc_method
    '-Wno-deprecated-declarations',
    '-Wno-dangling-else',
    '-Wno-empty-body',
    '-Wno-overloaded-virtual',
    '-Wno-parentheses',
    '-Wno-tautological-undefined-compare',
    '-Wno-unneeded-internal-declaration',
    '-Wno-inconsistent-missing-override',
  ]
else
  candidate_flags = []
endif

extra_args = []
foreach flag : candidate_flags
  if cc.has_argument(flag)
    extra_args += [flag]
  endif
endforeach
add_project_arguments(extra_args, language: languages)

if host_os == 'macos'
  add_project_arguments(
    '-mmacosx-version-min=10.9',
    language: languages)
  add_project_link_arguments(
    '-Wl,-macosx_version_min,10.9',
    '-Wl,-dead_strip',
    language: languages)
endif

subdir('src')
