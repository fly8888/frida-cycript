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
  'ObjectiveC/Output.cpp',
  'ObjectiveC/Replace.cpp',
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
      host_os,
      host_arch,
      '@INPUT@',
      '@OUTPUT@',
      '-DCY_JAVA=' + enable_java.to_string('1', '0'),
      '-DCY_PYTHON=' + enable_python.to_string('1', '0'),
      '-DCY_OBJECTIVEC=' + enable_objc.to_string('1', '0'),
    ] + dep_includes,
  )

  cycript_database = custom_target('cycript-database',
    input: cycript_bridge_definitions,
    output: 'libcycript.db',
    command: [
      find_program('generate-database.py'),
      host_os_id,
      '@OUTPUT@',
      '@INPUT@',
      join_paths(meson.source_root(), 'ext', 'node'),
    ],
    install: true,
    install_dir: get_option('datadir'),
  )

  node_modules = custom_target('node-modules',
    input: 'package.json',
    output: 'node_modules',
    command: [
      find_program('fetch-node-modules.py'),
      find_program('npm'),
      '@INPUT@',
      '@OUTDIR@',
    ],
  )

  custom_target('cycript-runtime',
    input: [
      'Agent/index.js',
      node_modules,
    ],
    output: 'libcycript.js',
    command: [
      find_program('generate-runtime.py'),
      '@INPUT@',
      '@OUTPUT@',
    ],
    install: true,
    install_dir: get_option('datadir'),
  )
endif

library('cycript', cycript_sources,
  cpp_args: ['-DYYDEBUG=1'],
  link_args: cycript_link_args + dep_libs,
  install: true,
)
