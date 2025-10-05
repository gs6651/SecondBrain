`lsblk`   # To check the partitions
`sudo umount /dev/sdX1`   # un-mount pendrive
`sudo dd if=/path/to/ubuntu.iso of=/dev/sdX bs=4M status=progress`
- if: specifies the input file (your ISO image).
- of: specifies the output file (your USB drive).
- bs=4M: sets the block size to 4 megabytes for faster writing.
- status=progress: shows the progress of the writing process (available in newer versions of dd).
`sync`    # to ensure all data in sync

