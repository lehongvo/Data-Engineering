# Linux Command Line Guide

## 1. Basic Navigation Commands

### pwd (Print Working Directory)
```bash
pwd                     # Print Working Directory - shows current path
```
- Shows the current directory path
- Example: /home/user/documents

### ls (List)
```bash
ls                      # List - show files and directories
ls -l                   # Long listing format - detailed view
ls -a                   # All - show hidden files
ls -h                   # Human readable - show sizes in KB, MB
ls -R                   # Recursive - show subdirectories content
```

### cd (Change Directory)
```bash
cd path                 # Change Directory - move to specified path
cd ..                   # Move to parent directory
cd ~                    # Move to home directory
cd -                    # Move to previous directory
```

## 2. File and Directory Operations

### mkdir (Make Directory)
```bash
mkdir directory_name    # Make Directory - create new directory
mkdir -p a/b/c         # Create nested directories with parents
```

### touch
```bash
touch filename.txt      # Create new file or update timestamp
```

### cp (Copy)
```bash
cp file1.txt file2.txt # Copy - duplicate a file
cp -r dir1 dir2        # Recursive copy - copy directory and contents
```

### mv (Move)
```bash
mv old.txt new.txt     # Move/Rename - change file name or location
mv file.txt /path/     # Move file to different directory
```

### rm (Remove)
```bash
rm file.txt            # Remove - delete file
rm -r directory        # Recursive remove - delete directory and contents
rm -f file.txt         # Force remove - delete without confirmation
```

## 3. File Content Viewing

### cat (Concatenate)
```bash
cat file.txt           # Concatenate - display entire file content
```

### less
```bash
less file.txt          # View file content page by page
```

### head
```bash
head file.txt          # Show first 10 lines
head -n 5 file.txt     # Show first 5 lines
```

### tail
```bash
tail file.txt          # Show last 10 lines
tail -f file.txt       # Follow - monitor file changes in real-time
```

## 4. File Permissions

### chmod (Change Mode)
```bash
chmod 755 file.txt     # Change Mode - set read-write-execute permissions
chmod +x file.txt      # Add execute permission
chmod -w file.txt      # Remove write permission
```

Permission numbers explained:
- 7 = 4(read) + 2(write) + 1(execute)
- 6 = 4(read) + 2(write)
- 5 = 4(read) + 1(execute)
- 4 = 4(read)

### chown (Change Owner)
```bash
chown user:group file.txt  # Change Owner - modify file ownership
```

## 5. Search Operations

### find
```bash
find . -name "*.txt"    # Find files by name pattern
find . -type d          # Find directories
find . -size +100M      # Find files larger than 100MB
```

### grep (Global Regular Expression Print)
```bash
grep "pattern" file.txt # Search for pattern in file
grep -r "pattern" .     # Recursive search in all files
```

## 6. Process Management

### ps (Process Status)
```bash
ps                      # Process Status - show current user processes
ps aux                  # Show all system processes
```