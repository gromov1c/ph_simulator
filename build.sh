#!/bin/bash

# PyInstller Command (on Igor's machine):
# pyinstaller --onefile --windowed --icon="C:\Users\igrom\Documents\GitHub\ph_s25\src\graphics\icon.ico" --add-data "C:\Users\igrom\Documents\GitHub\ph_s25\src\graphics;graphics" C:\Users\igrom\Documents\GitHub\ph_s25\src\main.py


#pyinstaller --clean --noconsole --onefile --icon="/Users/nicholasdill/PycharmProjects/ph_s25/src/graphics/icon.icns" --add-data="/Users/nicholasdill/PycharmProjects/ph_s25/src/graphics:graphics" /Users/nicholasdill/PycharmProjects/ph_s25/src/main.py

# Exit on error
set -e

echo "=== pH Calculator Build Script ==="
echo "Installing required packages if needed..."

# Check if PySide6 is installed, install if not
pip install -q PySide6 nuitka ordered-set

echo "Starting Nuitka build process..."



# Base Nuitka command2
NUITKA_CMD="python -m nuitka \
    --onefile \
    --follow-imports \
    --plugin-enable=pyside6 \
    --include-package=PySide6.QtWidgets \
    --include-package=PySide6.QtCore \
    --include-package=PySide6.QtGui \
    --nofollow-import-to=PySide6.QtQml \
    --nofollow-import-to=PySide6.QtQuick \
    --nofollow-import-to=PySide6.QtQuick3D \
    --nofollow-import-to=PySide6.QtWebEngine \
    --nofollow-import-to=PySide6.Qt3D \
    --nofollow-import-to=PySide6.QtDataVisualization \
    --nofollow-import-to=PySide6.QtCharts \
    --nofollow-import-to=PySide6.QtNetwork \
    --nofollow-import-to=PySide6.QtSql \
    --nofollow-import-to=PySide6.QtTest \
    --nofollow-import-to=PySide6.QtMultimedia \
    --disable-console \
    --output-dir=dist"

# Add platform-specific options
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Building for macOS..."
    NUITKA_CMD+=" --macos-create-app-bundle"

    # Add icon if it exists
    if [ -f "icon.png" ]; then
        NUITKA_CMD+=" --macos-app-icon=icon.png"
    else
        echo "Note: No icon.png found. Using default application icon."
    fi
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin"* ]]; then
    echo "Building for Windows..."

    # Add Windows-specific options for standalone exe
    NUITKA_CMD+=" --onefile"
    NUITKA_CMD+=" --windows-disable-console"
    NUITKA_CMD+=" --windows-product-name=\"pH Calculator\""
    NUITKA_CMD+=" --windows-file-version=1.0.0"
    NUITKA_CMD+=" --windows-product-version=1.0.0"

    # Add icon if it exists
    if [ -f "icon.ico" ]; then
        NUITKA_CMD+=" --windows-icon-from-ico=icon.ico"
    else
        echo "Note: No icon.ico found. Using default application icon."
    fi
fi

# Add Qt plugin options to reduce size
NUITKA_CMD+=" --include-qt-plugins=platforms,styles"
NUITKA_CMD+=" --noinclude-qt-plugins=qml,qmltooling,multimedia,webengine,webview,designer,3dinput,3drender,geoservices,texttospeech,virtualkeyboard,quick,quick3d,sensors"

# Exclude unused image format plugins (application only uses PNG which is built-in)
NUITKA_CMD+=" --noinclude-qt-plugins=imageformats/qgif,imageformats/qicns,imageformats/qico,imageformats/qjpeg"
NUITKA_CMD+=" --noinclude-qt-plugins=imageformats/qsvg,imageformats/qtga,imageformats/qtiff"
NUITKA_CMD+=" --noinclude-qt-plugins=imageformats/qwbmp,imageformats/qwebp,imageformats/qpdf"

# Exclude test directories and unittest modules
NUITKA_CMD+=" --nofollow-import-to=test,tests,testing"
NUITKA_CMD+=" --nofollow-import-to=unittest"

# Add the target file
NUITKA_CMD+=" src/main.py"

# Add the graphics directory to the build
NUITKA_CMD+=" --include-data-dir=src/graphics=graphics"

# Execute the command
eval $NUITKA_CMD

echo "Build completed successfully!"
echo "The executable can be found in the dist directory."

# Provide platform-specific instructions
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "On macOS, you can find the application bundle at: dist/gui.app"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin"* ]]; then
    echo "On Windows, you can find the executable at: dist/gui.exe"
else
    echo "On Linux, you can find the executable at: dist/gui.bin"
fi

echo "=== Build Complete ==="
