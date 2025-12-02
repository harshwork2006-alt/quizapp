[app]
# (str) Title of your application
title = QuizApp

# (str) Package name
package.name = quizapp
package.domain = org.harshmishra

# (str) Source dir / main .py file
source.dir = .
source.include_exts = py,png,jpg,kv,json
source.main = main.py

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Add extra libs if used (comma separated), e.g. python3,kivy,requests,Pillow
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (str) Android architectures
android.arch = armeabi-v7a,arm64-v8a

# (int) Android API target (optional)
android.api = 33

# (str) Presplash/icon (optional)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
