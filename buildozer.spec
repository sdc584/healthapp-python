[app]

# (str) Title of your application
title = 健康追踪应用

# (str) Package name
package.name = healthapp

# (str) Package domain (needed for android/ios packaging)
package.domain = com.healthapp.python

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Extra pip arguments
pip.extra_args = --break-system-packages

[android]

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
# android.service = myapp:PyService

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android API to use
android.api = 28

# (str) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
#android.ndk = 25c

# (int) Android NDK API to use. This is the minimum API your app will support
android.ndk_api = 21

# (str) Android private storage
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path = /Users/sdc/AppData/Local/Android/Sdk

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules =

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the manifestPlaceholders property.
# This property takes a map of key-value pairs. (via a string)
# Usage example : android.manifest_placeholders = [myCustomUrl:myCustomUrl]
# android.manifest_placeholders = [:]

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

[buildozer:global]

# Here you can change the buildozer working directory
# buildozer.workdir = /tmp

# Here you can change the build directory
# buildozer.build_dir = .buildozer

# 使用中国镜像加速下载
# 设置Git使用中国镜像
# 设置pip使用中国镜像

[app:permissions]

# (list) List of permissions which your app will request:
android.permissions = ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION,CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,VIBRATE

[app:meta_data]

# (str) Android application metadata to set (key=value format)
#android.meta_data =

[app:gradle_dependencies]

# (list) Gradle dependencies which your app will use
android.gradle_dependencies = 

[app:gradle_repositories]

# (list) Gradle repositories which your app will use
android.gradle_repositories = 

[app:java_options]

# (str) java options for javac
#android.java_options = -Xms512m -Xmx2048m

[app:gradle_options]

# (str) gradle options
#android.gradle_options = -PandroidX=true
