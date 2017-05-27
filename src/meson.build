cycript_sources = [
  'ConvertUTF.c',
  'Decode.cpp',
  'Driver.cpp',
  'Error.cpp',
  'Highlight.cpp',
  'Library.cpp',
  'Output.cpp',
  'Replace.cpp',
  'Syntax.cpp',
  'sig/parse.cpp',
  'sig/copy.cpp',
]

cycript_features = ['C', 'Java', 'Ruby', 'Python', 'ObjectiveC']
cycript_link_args = []

filter = find_program('filter.py')

cycript_scanner_grammar = custom_target('cycript-scanner-grammar',
  input: 'Scanner.lpp.in',
  output: 'Scanner.lpp',
  command: [
    filter,
    '@INPUT@'
  ] + cycript_features,
  capture: true,
)
cycript_scanner = custom_target('cycript-scanner',
  input: cycript_scanner_grammar,
  output: ['Scanner.hpp', 'Scanner.cpp'],
  command: [
    flex,
    '--full',
    '--ecs',
    '-o', '@OUTPUT1@',
    '@INPUT@',
  ],
)
cycript_sources += cycript_scanner

cycript_parser_grammar = custom_target('cycript-parser-grammar',
  input: 'Parser.ypp.in',
  output: 'Parser.ypp',
  command: [
    filter,
    '@INPUT@'
  ] + cycript_features,
  capture: true,
)
cycript_parser = custom_target('cycript-parser',
  input: cycript_parser_grammar,
  output: ['Parser.hpp', 'Parser.cpp'],
  command: [
    find_program('generate-parser.py'),
    bison,
    '@INPUT@',
    '@OUTPUT@',
  ],
)
cycript_sources += cycript_parser

if get_option('enable_console')
  cycript_sources += ['Complete.cpp']
endif

if get_option('enable_engine')
  frida_core = custom_target('frida-core',
    output: ['frida-core.h'],
    command: [
      find_program('fetch-frida-devkit.py'),
      '10.0.8',
      host_os,
      host_arch,
      '@OUTDIR@',
    ],
  )
  cycript_sources += [
    'Execute.cpp',
    frida_core,
  ]
  cycript_link_args += [
    '-L' + meson.current_build_dir(),
    '-lfrida-core',
  ]
  if host_os == 'macos'
    cycript_link_args += [
      '-lbsm',
      '-lresolv',
      '-Wl,-framework,Foundation,-framework,AppKit',
      '-Wl,-no_compact_unwind',
    ]
  endif
endif

analyze_sources = [
  'Analyze.cpp',
  'Error.cpp',
  'Output.cpp',
  'Replace.cpp',
  'Syntax.cpp',
]
analyze = executable('Analyze', analyze_sources,
  include_directories: include_directories('extra'),
  dependencies: clang_dep,
  link_args: clank_link_flags,
)

cycript_bridge_definitions = custom_target('cycript-bridge-definitions',
  input: [
    analyze,
    'Analysis.cpp',
    'Bridge.old',
  ],
  output: 'Bridge.def',
  command: [
    find_program('generate-bridge-definitions.py'),
    '@INPUT@',
    '@OUTPUT@',
  ],
)

cycript_database = custom_target('cycript-database',
  input: cycript_bridge_definitions,
  output: 'libcycript.db',
  command: [
    find_program('libcycript.py'),
    '@INPUT@',
    '@OUTPUT@',
  ],
)
install_data(cycript_database, install_dir: get_option('datadir'))

library('cycript', cycript_sources,
  cpp_args: ['-DYYDEBUG=1'],
  link_args: cycript_link_args + dep_libs,
  install: true,
)
