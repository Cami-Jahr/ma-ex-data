# Tools
Lots of mess. I'll figure something out eventually.
If you want something in particular just @ me. I understand if u don't want to download everything

Requirements: 
* [ffmpeg](https://ffmpeg.org/download.html) - must be available in PATH, accessed by ``ffmpeg``
* [vgmstream](https://github.com/vgmstream/vgmstream) - Just put it in same folder as main.py, accessed by ``vgmstream/vgmstream-cli.exe``
* [VGMToolbox](https://sourceforge.net/projects/vgmtoolbox/) - GUI tool to extract video files
* [AssetStudioMod](https://github.com/aelurum/AssetStudio) - GUI tool to extract Unity files

## How to get data
Data can be extracted by using [adb](https://medium.com/@yadav-ajay/a-step-by-step-guide-to-setting-up-adb-path-on-windows-0b833faebf18) connected to [Mumu](https://www.mumuplayer.com/)

Open Mumu, install Exedra and run through the download steps, enable root in settings, run this do download into wherever you run this from. run main.py from the same folder, or change paths in main.py
```powershell
> adb connect 127.0.0.1:7555
> adb root
> adb -s 127.0.0.1:7555 pull /data/data/com.aniplex.magia.exedra.en
```

main.py will create:
* /manifests/resen will be updated with new files 
* /processed - Where the original files reside
* /full - Where decompiled wav and mp3 files reside
* /mini - Where minimized ogg and webm files reside. Can also be found here

Unity data can be found in ``processed/gallery/library``. Throw the entire folder into AssetStudioMod, and extract from there. 

## Uploading to wiki
wiki pages can be created by running the main.py file in ``/wiki``
To bulk upload or do other edits you have to Rename *user-password-TEMPLATE.py* to *user-password.py* and input your wiki credentials.
Then run ``uploader.py`` to upload pages, or write custom scripts following that pattern.
