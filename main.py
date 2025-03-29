import decompress_audio
import decompress_video
import folder_copier_and_renamer

folder_copier_and_renamer.copy_files(
    r"com.aniplex.magia.exedra.en/files/CYU6", "processed"
)
decompress_audio.convert("processed/media/assets/audio")
print(
    "Open VGMTOOLBOX.exe and drag your processed/media/assets/video folder into 'Misc. Tools > Stream Tools > Video Demultiplexer' with format USM"
)
input("Press any key when VGMTOOLBOX is done...")
decompress_video.convert("processed/media/assets/video")
