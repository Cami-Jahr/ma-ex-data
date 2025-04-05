import decompress_audio
import decompress_video
from manifests import get_all_manifests
import madoka_decrypt

cwd = "com.aniplex.magia.exedra.en/files/CYU6"

print("DOWNLOADING NEW MANIFESTS")
get_all_manifests.run(False)

print("RENAMING FILES AND DECRYPTING UNITY FILES")
madoka_decrypt.copy_files("processed", cwd)

print("CONVERTING AUDIO")
decompress_audio.convert("processed/gallery/kfOi/Sound", "full/gallery/kfOi/Sound")
decompress_audio.minimize("full/gallery/kfOi/Sound", "mini/gallery/kfOi/Sound")

print(
    "\n\nOpen VGMTOOLBOX.exe and drag your processed/gallery/kfOi/CriMovie folder into 'Misc. Tools > Stream Tools > Video Demultiplexer' with format USM"
)
input("Press any key when VGMTOOLBOX is done...")
print("CONVERTING VIDEO")
decompress_video.convert(
    "processed/gallery/kfOi/CriMovie",
    "mini/gallery/kfOi/CriMovie",
    "full/gallery/kfOi/CriMovie",
)
print("DONE")
