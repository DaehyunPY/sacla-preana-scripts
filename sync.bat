:begin
"C:\Program Files (x86)\WinSCP\WinSCP.com" /init=nul /script="sync.txt"
rclone copy -P L:\home\data\2019B8035Fukuzawa\ "google-2019b8035fukuzawa:/Experimental data/Online/"
TIMEOUT 60
goto begin
