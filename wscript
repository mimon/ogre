APPNAME = 'Ogre'
VERSION = '2.1'
from waflib.Errors import ConfigurationError

def options(opt):
  opt.load('compiler_cxx compiler_c')
  opt.add_option('--dependencies', action='store', dest='OGRE_DEPENDENCIES', default='')

def configure(conf):
  conf.load('c_config compiler_cxx compiler_c')
  dependencies = [
    ('zziplib', 'OGRE_NO_ZIP_ARCHIVE')
  ]
  lib_is_present = 0
  lib_is_not_present = 1
  for libname, config_name in dependencies:
    try:
      conf.check_cfg(package=libname, uselib_store=libname, args=['--cflags', '--libs'])
      conf.define(config_name, lib_is_present)
    except ConfigurationError as k:
      conf.define(config_name, lib_is_not_present)

  conf.env.FRAMEWORK_VERSION = '2.1'
  conf.env.ARCHS = 'x86_64'
  conf.env.MACOSX_DEPLOYMENT_TARGET = '10.9'
  conf.env.SDKROOT = 'macosx10.9'
  conf.env.PRODUCT_NAME = '$(TARGET_NAME)'
  conf.env.append_value('INCLUDES', conf.bldnode.abspath())
  conf.env.append_value('CXXFLAGS', ['-std=c++11', '-stdlib=libc++'])

  # conf.define('OGRE_STATIC_LIB', 1)
  # conf.define('OGRE_BUILD_RENDERSYSTEM_D3D11', 1)
  conf.define('OGRE_NO_FREEIMAGE', 1)
  conf.define('OGRE_NO_JSON', 1)
  # conf.define('OGRE_BUILD_RENDERSYSTEM_GLES', 1)
  # conf.define('OGRE_BUILD_RENDERSYSTEM_GLES2', 1)
  conf.define('OGRE_BUILD_PLUGIN_PFX', 1)
  # conf.define('OGRE_BUILD_PLUGIN_CG', 1)
  conf.define('OGRE_BUILD_COMPONENT_HLMS_PBS_MOBILE', 1)
  conf.define('OGRE_BUILD_COMPONENT_HLMS_UNLIT_MOBILE', 1)
  conf.define('OGRE_BUILD_COMPONENT_HLMS_PBS', 1)
  conf.define('OGRE_BUILD_COMPONENT_HLMS_UNLIT', 1)
  # conf.define('OGRE_BUILD_COMPONENT_PAGING', 1)
  conf.define('OGRE_BUILD_COMPONENT_MESHLODGENERATOR', 1)
  # conf.define('OGRE_BUILD_COMPONENT_TERRAIN', 1)
  # conf.define('OGRE_BUILD_COMPONENT_VOLUME', 1)
  # conf.define('OGRE_BUILD_COMPONENT_PROPERTY', 1)
  conf.define('OGRE_BUILD_COMPONENT_OVERLAY', 1)
  # conf.define('OGRE_BUILD_COMPONENT_RTSHADERSYSTEM', 1)
  conf.define('OGRE_CONFIG_LITTLE_ENDIAN', 1)
  # conf.define('OGRE_CONFIG_BIG_ENDIAN', 1)
  conf.define('OGRE_LEGACY_ANIMATIONS', 1)
  conf.define('OGRE_DOUBLE_PRECISION', 0)
  conf.define('OGRE_MEMORY_ALLOCATOR', 4)
  conf.define('OGRE_CONTAINERS_USE_CUSTOM_MEMORY_ALLOCATOR', 1)
  conf.define('OGRE_STRING_USE_CUSTOM_MEMORY_ALLOCATOR', 0)
  conf.define('OGRE_MEMORY_TRACKER_DEBUG_MODE', 0)
  conf.define('OGRE_MEMORY_TRACKER_RELEASE_MODE', 0)
  conf.define('OGRE_ASSERT_MODE', 0)
  conf.define('OGRE_THREAD_SUPPORT', 0)
  conf.define('OGRE_THREAD_PROVIDER', 0)
  conf.define('OGRE_NO_MESHLOD', 0)
  # conf.define('OGRE_NO_FREEIMAGE', 0)
  conf.define('OGRE_NO_DDS_CODEC', 0)
  conf.define('OGRE_NO_PVRTC_CODEC', 1)
  conf.define('OGRE_NO_ETC_CODEC', 0)
  conf.define('OGRE_NO_STBI_CODEC', 1)
  # conf.define('OGRE_NO_ZIP_ARCHIVE', 0)
  conf.define('OGRE_NO_VIEWPORT_ORIENTATIONMODE', 1)
  conf.define('OGRE_NO_GLES2_CG_SUPPORT', 1)
  conf.define('OGRE_NO_GLES2_GLSL_OPTIMISER', 1)
  conf.define('OGRE_NO_GLES2_VAO_SUPPORT', 1)
  conf.define('OGRE_NO_GL_STATE_CACHE_SUPPORT', 1)
  conf.define('OGRE_NO_GLES3_SUPPORT', 1)
  conf.define('OGRE_NO_TBB_SCHEDULER', 0)
  conf.define('OGRE_USE_BOOST', 0)
  conf.define('OGRE_PROFILING', 0)
  conf.define('OGRE_NO_QUAD_BUFFER_STEREO', 1)
  conf.define('OGRE_USE_SIMD', 1)
  conf.define('OGRE_RESTRICT_ALIASING', 1)
  conf.define('RTSHADER_SYSTEM_BUILD_CORE_SHADERS', 1)
  conf.define('RTSHADER_SYSTEM_BUILD_EXT_SHADERS', 1)

  # conf.check_cxx(header_name='Freeimage.h', define_name='OGRE_NO_FREEIMAGE')

  conf.write_config_header('OgreBuildSettings.h', top = True)

def build(bld):
  threading_files = [
    'OgreMain/src/Threading/OgreBarrierPThreads.cpp',
    'OgreMain/src/Threading/OgreLightweightMutexPThreads.cpp',
    'OgreMain/src/Threading/OgreThreadsPThreads.cpp',
    'OgreMain/src/Threading/OgreDefaultWorkQueueStandard.cpp'
  ]
  math_files = [
    'OgreMain/src/Math/*.cpp',
    'OgreMain/src/Math/Array/*.cpp',
    'OgreMain/src/Math/Array/SSE2/Single/*.cpp',
    'OgreMain/src/Math/Simple/C/*.cpp',
  ]
  print bld.env.DEST_OS
  platform_specific_files = []
  if bld.env.DEST_OS == 'linux':
    platform_specific_files.append('OgreMain/src/GLX/*.cpp')
  elif bld.env.DEST_OS == 'darwin':
    platform_specific_files.append('OgreMain/src/OSX/*.cpp')

  ogremain_includes = bld.path.ant_glob(
    incl = [
      'OgreMain/include',
      'OgreMain/src/nedmalloc',
      'OgreMain/include/**'],
      src = False,
      dir = True
  )

  tg = bld.stlib(
    source = bld.path.ant_glob(
      incl = [
        'OgreMain/src/*.cpp', 
        'OgreMain/src/CommandBuffer/*.cpp',
        'OgreMain/src/Hash/*.cpp',
        'OgreMain/src/Vao/*.cpp',
        'OgreMain/src/Compositor/**/*.cpp',
        'OgreMain/src/Animation/*.cpp'
      ] + threading_files + math_files + platform_specific_files,
      excl = [
        'OgreMain/src/OgreFreeImageCodec.cpp'
      ]),
    includes = ogremain_includes,
    export_includes = ogremain_includes,
    group_files = {'Include':bld.path.ant_glob('OgreMain/include/*.h')},
    target = 'OgreMainStatic',
    uselib = 'zziplib',
    framework = 'Cocoa'
  )

  rendersystem_null_includes = tg.includes + [
    'RenderSystems/NULL/include',
    'RenderSystems/NULL/include/Vao'
  ]
  bld.stlib(
    source = bld.path.ant_glob(incl = [
      'RenderSystems/NULL/src/**/*.cpp'
    ]),
    includes = rendersystem_null_includes,
    export_includes = rendersystem_null_includes,
    target='RenderSystem_NULL',
    use='OgreMainStatic'
  )

  hlms_common_includes = tg.includes + [
    'Components/Hlms/Common/include'
  ]
  bld.stlib(
    source = bld.path.ant_glob(incl = [
      'Components/Hlms/Common/src/**.cpp'
    ]),
    includes = hlms_common_includes,
    export_includes = hlms_common_includes,
    target = 'OgreHlmsCommonStatic',
    use = 'OgreMainStatic'
  )

  hlms_includes = tg.includes + [
    'Components/Hlms/Unlit/include',
    'Components/Hlms/Common/include'
  ]
  bld.stlib(
    source = bld.path.ant_glob(incl = [
      'Components/Hlms/Unlit/src/**.cpp'
    ]),
    includes = hlms_includes,
    export_includes = hlms_includes,
    target = 'OgreHlmsUnlitStatic',
    use = 'OgreMainStatic OgreHlmsCommonStatic'
  )
  
  # GL_files = [
  #   'RenderSystems/NULL/src/**.cpp'
  # ]

  # bld.stlib(
  #   source=bld.srcnode.ant_glob(incl=GL_files),
  #   includes= tg.includes + ['RenderSystems/GL3Plus/include', 'RenderSystems/GL3Plus/include/GLSL', 'RenderSystems/GL3Plus/include/windowing/OSX'],
  #   target='RenderSystem_GL3Plus',
  #   framework='Cocoa OpenGL',
  #   use='Ogre'
  # )