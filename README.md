# BackupBuffer (Memory Saver)

A Python utility that automatically manages backup files by keeping only a specified number of the most recent files in a folder, deleting older ones to save disk space.

## Features

- **Automatic File Management**: Automatically removes the oldest files from a specified directory
- **Configurable**: Easy configuration via `cfg.txt` file
- **Safe Operation**: Only deletes files when the count exceeds the configured limit
- **Logging**: Built-in logging system for tracking operations
- **Standalone Executable**: Can be built as a Windows executable using PyInstaller

## Requirements

- Python 3.6 or higher (for running as script)
- Windows OS (for executable version with console features)

## Installation

### Running as Python Script

1. Clone the repository:
```bash
git clone https://github.com/L-JANUSZ/BackupBuffer.git
cd BackupBuffer
```

2. Run the script:
```bash
python app.py
```

### Building as Executable

To build a standalone Windows executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller Memory_saver.spec
```

The executable will be created in the `dist` folder.

## Configuration

Create or edit the `cfg.txt` file in the same directory as the script/executable:

```
Number of files = "4"
Path: "C:\Users\YourName\Documents\BackupFolder"
```

**Configuration Parameters:**

- `Number of files`: The number of most recent files to keep in the folder
- `Path`: Full path to the folder containing the backup files to manage

## Usage

### As Python Script
```bash
python app.py
```

### As Executable
Simply double-click `Memory_saver.exe` or run it from the command line:
```bash
Memory_saver.exe
```

The program will:
1. Read the configuration from `cfg.txt`
2. List all files in the specified folder
3. Sort files by modification time
4. Delete the oldest files, keeping only the specified number of recent files
5. Display results and log operations to `Memory_saver.log`

## Example

If your backup folder contains 10 files and `cfg.txt` is configured to keep 4 files:

```
Number of files = "4"
Path: "C:\Backups\MyData"
```

The program will:
- Identify the 10 files in the folder
- Sort them by modification time
- Delete the 6 oldest files
- Keep the 4 most recent files

## Logging

All operations are logged to `Memory_saver.log` in the same directory as the program. The log includes:
- Program start/stop times
- Configuration details
- Files deleted
- Any errors encountered

## Notes

- The program only processes files in the specified folder (not subfolders)
- Files are sorted by modification time (`st_mtime`)
- If the number of files is less than or equal to the configured limit, no files are deleted
- Make sure to test with a non-critical folder first to ensure the configuration is correct

## License

No license specified. Please contact the author for usage rights and permissions.

## Author

L-JANUSZ
