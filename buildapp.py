from jute import config

import py2app
assert py2app

# TODO: Should any of this be joined to base path? Don't have a Mac to test...

setup_args = dict(
    app=["app.py"],
    options=dict(
        py2app=dict(
            argv_emulation=True,
            iconfile="appicons/app.icns",
            resources=["icons", "targets", "appicons/doc.icns"],
            plist=dict(
                CFBundleName=config.APP_NAME,
                CFBundleGetInfoString=config.APP_DESCRIPTION,
                CFBundleShortVersionString=config.APP_VERSION_STRING,
                CFBundleSignature="twee",
                CFBundleIconFile="app.icns",
                CFBundleDocumentTypes=[
                    dict(
                        CFBundleTypeExtensions=["tws"],
                        CFBundleTypeIconFile="doc.icns",
                        CFBundleTypeName="Twine story",
                        CFBundleTypeRole="Editor",
                    )
                ],
                NSHumanReadableCopyright=config.APP_LICENSE,
            ),
        )
    ),
)
