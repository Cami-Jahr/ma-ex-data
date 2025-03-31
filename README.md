# Tools
Lots of mess. I'll figure something out eventually.
If you want something in particular just @ me. I understand if u don't want to download everything

Requirements: 
* [ffmpeg](https://ffmpeg.org/download.html) - available in PATH, accessed by ``ffmpeg``
* [vgmstream](https://github.com/vgmstream/vgmstream) - Just put it in same folder as main.py, accessed by ``vgmstream/vgmstream-cli.exe``
* [VGMToolbox](https://sourceforge.net/projects/vgmtoolbox/) - GUI tool

Recommended:
* Data can be extracted by using [adb](https://medium.com/@yadav-ajay/a-step-by-step-guide-to-setting-up-adb-path-on-windows-0b833faebf18) connected to [Mumu](https://www.mumuplayer.com/)

Open Mumu, install Exedra and run through the download steps, enable root in settings, run this do download into wherever you run this from. run main.py from the same folder, or change paths in main.py
```powershell
> adb connect 127.0.0.1:7555
> adb root
> adb -s 127.0.0.1:7555 pull /data/data/com.aniplex.magia.exedra.en
```
