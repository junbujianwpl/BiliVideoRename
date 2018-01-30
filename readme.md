
# Rename video within bili download directory

## goals
### 1. save primary info
    * for recovery when these scripts do something wrong
    * log when counter empty dir(without *.blv file)

### 2. rename video files
    * change suffix blv to mp4
    * use prefix from entry.json which followed by index as the file name

### 3. create directory
    * get title from entry.json and make the dir
    * mv all renamed video to the dir

### 4. save progress info and avoid repeat jobs
    * record jobs had done and never do repeat jobs
