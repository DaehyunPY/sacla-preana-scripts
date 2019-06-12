:begin
"C:\Program Files (x86)\WinSCP\WinSCP.com" /init=nul /script="sync.txt"
".\rclone.exe" sync -P xhpcfep:"/work/uedalab/2019A8045Fukuzawa/hdf_files" daehyun:"/SACLA 2019A8045 Fukuzawa/hdf_files"
TIMEOUT 60
goto begin
