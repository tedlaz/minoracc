import os


def getfiles(root_dir, exe, product_name, product_version, publisher, web, license, installer):
    top = ';Script generated by makensis.py\n'
    top += '!define PRODUCT_NAME "%s"\n' % product_name
    top += '!define PRODUCT_VERSION "%s"\n' % product_version
    top += '!define PRODUCT_PUBLISHER "%s"\n' % publisher
    top += '!define PRODUCT_WEB_SITE "%s"\n' % web
    top += '!define PRODUCT_DIR_REGKEY "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\%s"\n' % exe
    top += '!define PRODUCT_UNINST_KEY "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${PRODUCT_NAME}"\n'
    top += '!define PRODUCT_UNINST_ROOT_KEY "HKLM"\n'
    top += '\nSetCompressor /SOLID lzma\n\n'
    top += '!include "MUI.nsh"\n'
    top += '!define MUI_ABORTWARNING\n'
    top += '!define MUI_ICON "${NSISDIR}\\Contrib\\Graphics\\Icons\\orange-install.ico"\n'
    top += '!define MUI_UNICON "${NSISDIR}\\Contrib\\Graphics\\Icons\\orange-uninstall.ico"\n'
    top += '!insertmacro MUI_PAGE_WELCOME\n'
    top += '!insertmacro MUI_PAGE_LICENSE %s\n' % license
    top += '!insertmacro MUI_PAGE_DIRECTORY\n'
    top += '!insertmacro MUI_PAGE_INSTFILES\n'
    top += '!define MUI_FINISHPAGE_RUN "$INSTDIR\\%s"\n' % exe
    top += '!insertmacro MUI_PAGE_FINISH\n'
    top += '!insertmacro MUI_UNPAGE_INSTFILES\n'
    top += '!insertmacro MUI_LANGUAGE "English"\n'
    top += 'Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"\n'
    top += 'OutFile "%s"\n' % installer
    top += 'InstallDir "$PROGRAMFILES\\%s"\n' % product_name
    top += 'InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""\n'
    top += 'ShowInstDetails show\n'
    top += 'ShowUnInstDetails show\n'
    instal = 'Section "MainSection" SEC01\n  SetOverwrite try\n'
    delete = 'Section Uninstall\n  Delete "$INSTDIR\\uninst.exe"\n'
    directories = []
    for dirname, _, filelist in os.walk(root_dir):
        directories.append(dirname.replace(root_dir, '$INSTDIR'))
        if len(filelist) > 0:
            instal += '  SetOutPath "%s"\n' % dirname.replace(root_dir, '$INSTDIR')
            for fname in filelist:
                fullpath = os.path.join(dirname, fname)
                instal += '  File "%s"\n' % fullpath
                delete += '  Delete "%s"\n' % fullpath.replace(root_dir, '$INSTDIR')
    instal += '  CreateDirectory "$SMPROGRAMS\\%s"\n' % product_name
    instal += '  CreateShortCut "$SMPROGRAMS\\%s\%s.lnk" "$INSTDIR\\%s"\n' % (product_name, product_name, exe)
    instal += '  CreateShortCut "$DESKTOP\%s.lnk" "$INSTDIR\%s"\n' % (product_name, exe)
    delete += '\n'
    delete += '  Delete "$SMPROGRAMS\\%s\\Uninstall.lnk"\n' % product_name
    delete += '  Delete "$DESKTOP\\%s.lnk"\n' % product_name
    delete += '  Delete "$SMPROGRAMS\\%s\\%s.lnk"\n' % (product_name, product_name)
    delete += '\n'
    delete += '  ;Remove directories\n'

    delete += '  RMDir "$SMPROGRAMS\\%s"\n' % product_name
    for adir in directories[::-1]:
        delete += '  RMDir "%s"\n' % adir
    delete += '\n'
    delete += '  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"\n'
    delete += '  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"\n'
    delete += '  SetAutoClose true\n'
    instal += 'SectionEnd'
    delete += 'SectionEnd'
    mid = 'Section -AdditionalIcons\n'
    mid += '  CreateShortCut "$SMPROGRAMS\\%s\\Uninstall.lnk" "$INSTDIR\\uninst.exe"\n' % product_name
    mid += 'SectionEnd\n\n'
    mid += 'Section -Post\n'
    mid += '  WriteUninstaller "$INSTDIR\\uninst.exe"\n'
    mid += '  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\\%s"\n' % exe
    mid += '  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"\n'
    mid += '  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\\uninst.exe"\n'
    mid += '  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\\%s"\n' % exe
    mid += '  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"\n'
    mid += '  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"\n'
    mid += '  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"\n'
    mid += 'SectionEnd\n\n'
    mid += 'Function un.onUninstSuccess\n'
    mid += '  HideWindow\n'
    mid += '  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."\n'
    mid += 'FunctionEnd\n\n'
    mid += 'Function un.onInit\n'
    mid += '  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2\n'
    mid += '  Abort\n'
    mid += 'FunctionEnd\n'
    return '\n\n'.join([top, instal, mid, delete])


def create_nsi(filename, productname, version, publisher, website):
    MAIN_FILE = filename
    PRODUCT = productname
    VERSION = version
    PUBLISHER = publisher
    WEBSITE = website
    CURPATH = os.path.dirname(os.path.realpath(__file__))
    ROOT = '%s\\dist\\%s' % (CURPATH, MAIN_FILE)
    LICENSE = "%s\\LICENSE" % CURPATH
    EXE = "%s.exe" % MAIN_FILE
    INSTALLER = "%s.Installer.%s.exe" % (PRODUCT, VERSION)
    return getfiles(ROOT, EXE, PRODUCT, VERSION, PUBLISHER,
                    WEBSITE, LICENSE, INSTALLER)


if __name__ == "__main__":
    MAIN_FILE = "qminoracc"
    PRODUCT = "qminoracc"
    VERSION = "1.0.18"
    PUBLISHER = "Ted Lazaros 2020"
    WEBSITE = "https://tedlaz.github.io/weblinks"
    print(create_nsi(MAIN_FILE, PRODUCT, VERSION, PUBLISHER, WEBSITE))
