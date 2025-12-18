# YModTerm

A modern serial terminal application with YMODEM, YMODEM-G, XMODEM, and ZMODEM protocol support.

**Based on [o-murphy/ymodem](https://github.com/o-murphy/ymodem) fork of [alexwoo1900/ymodem](https://github.com/alexwoo1900/ymodem) library**
**GUI inpired by [CuteCom](https://gitlab.com/cutecom/cutecom/) - graphical serial terminal**

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Multiple Protocol Support**: YMODEM, YMODEM-G, XMODEM, and ZMODEM file transfer protocols
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Modern GUI**: Built with Qt (via qtpy) for a responsive interface
- **Flexible Configuration**: Customizable serial port settings (baudrate, parity, stop bits, etc.)
- **Input History**: Keep track of previously sent commands
- **Multiple Output Modes**: ASCII, Hex, and control character display
- **File Logging**: Optional logging to file with append mode
- **Auto-Reconnect**: Automatic port reconnection option
- **Settings Persistence**: All settings are saved between sessions

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/yourusername/ymodterm.git
cd ymodterm
pip install -r requirements.txt
```

### Dependencies

- `qtpy` - Qt abstraction layer
- `PyQt5` or `PySide2` or `PyQt6` or `PySide6` - Qt bindings
- `pyserial` - Serial port communication
- `ymodem` - YMODEM protocol implementation (based on [alexwoo1900/ymodem](https://github.com/alexwoo1900/ymodem))

## Usage

### Basic Usage

```bash
python ymodterm_gui.py
```

### Command Line Arguments

```bash
python ymodterm_gui.py [options]

Options:
  -h, --help            Show help message and exit
  -p PORT, --port PORT  COM port
  -b BAUDRATE, --baudrate BAUDRATE
                        Baudrate (default: 9600)
  -pr {N,E,O,S,M}, --parity {N,E,O,S,M}
                        Parity: N(one), E(ven), O(dd), S(pace), M(ark)
  -db {5,6,7,8}, --databits {5,6,7,8}
                        Data bits (default: 8)
  -sb {1,2,1.5}, --stopbits {1,2,1.5}
                        Stop bits (default: 1)
  -m {X,Y,YG,Z}, --modem {X,Y,YG,Z}
                        Modem protocol: X(Modem), Y(Modem), YG(Modem-G), Z(Modem)
  -d, --debug           Enable debug logging
  -V, --version         Show version and exit
```

### Example

```bash
# Connect to COM3 at 115200 baud with YMODEM protocol
python ymodterm_gui.py -p COM3 -b 115200 -m Y

# Linux example with debug output
python ymodterm_gui.py -p /dev/ttyUSB0 -b 9600 -d
```

## GUI Features

### Connection Panel
- **Device Selection**: Dropdown list of available serial ports with auto-refresh
- **Connect/Disconnect**: Toggle connection button
- **RTS/DTR Control**: Hardware flow control signals
- **Auto Reconnect**: Automatic reconnection on port disconnect
- **Settings Panel**: Expandable panel for advanced serial configuration

### Settings Panel
- **Baudrate**: Configurable from 1200 to 10000000 (editable combo box)
- **Data Bits**: 5, 6, 7, or 8 bits
- **Flow Control**: None, Hardware, or Software
- **Parity**: None, Even, Odd, Space, Mark
- **Stop Bits**: 1, 1.5, or 2
- **Open Mode**: Read Only, Write Only, or Read/Write
- **Display Options**: Control character display, timestamps
- **Logfile**: Configure output logging with append mode

### Terminal Output
- **Hex Output Mode**: Display data in hexadecimal format
- **Control Character Display**: Show control characters as `<0x00>` format
- **UTF-8 Support**: Proper handling of multi-byte UTF-8 sequences
- **Auto-scroll**: Automatic scrolling to latest output
- **Clear Function**: Clear terminal output
- **File Logging**: Optional logging to file

### Input Panel
- **Command Input**: Text field with Enter-to-send
- **Line Ending Options**: LF, CR, CR/LF, None, or Hex input
- **Auto Return**: Automatically send on text change
- **File Transfer**: Send files using selected modem protocol
- **Protocol Selection**: YMODEM, YMODEM-G, XMODEM, or ZMODEM

### Input History
- **Command History**: List of previously sent commands
- **Click to Resend**: Click any history item to populate input field
- **Context Menu**: Remove individual items or clear all history

## File Transfer

YModTerm supports multiple file transfer protocols:

1. **YMODEM**: Reliable batch file transfer with CRC checking
2. **YMODEM-G**: Streaming variant of YMODEM (faster, no error recovery)
3. **XMODEM**: Classic single-file transfer protocol
4. **ZMODEM**: Advanced protocol with crash recovery

### Sending Files

1. Ensure serial port is connected
2. Select desired protocol from dropdown
3. Click "Send File..." button
4. Select file to transfer
5. Monitor progress in dialog
6. Cancel anytime if needed

### Receiving Files

File reception feature is implemented in the modem manager but requires additional UI work for directory selection.

## Technical Details

### Architecture

- **SerialManagerWidget**: Handles serial port connection and configuration
- **ModemTransferManager**: Manages file transfers with queue-based data handling
- **QSerialPortModemAdapter**: Adapter between Qt serial port and ymodem library
- **AppState**: Centralized state management with persistent settings
- **StatefullProp**: Reactive property system for UI binding

### Data Flow

```
Serial Port → QSerialPort → readyRead signal
                                ↓
                    data_received signal
                                ↓
        ┌───────────────────────┴────────────────────┐
        ↓                                            ↓
OutputViewWidget                        ModemTransferManager
(display to user)                       (transfer queue)
```

### Control Character Handling

The application properly handles control characters in multiple ways:
- Visual display: `<0x00>`, `<0x0D>`, etc.
- Named representation: `^@`, `^A`, `\n`, `\t`
- Hex mode: All bytes as hex pairs

### UTF-8 Support

Smart UTF-8 decoding with fallback:
1. Attempts to decode valid UTF-8 sequences
2. Falls back to hex representation for invalid bytes
3. Preserves multi-byte character integrity

## Configuration

Settings are automatically saved to:
- **Windows**: `%APPDATA%/o-murphy/ymodterm.ini`
- **Linux/macOS**: `~/.config/o-murphy/ymodterm.conf`

## Development

### Project Structure

```
ymodterm/
├── ymodterm_gui.py          # Main application file
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── ymodem/                 # YMODEM library
    ├── Protocol.py
    └── Socket.py
```

### Adding Features

The codebase uses Qt's signal/slot mechanism extensively. To add new features:

1. Create a `StatefullProp` for state management
2. Bind UI widgets to properties using `.bind()` method
3. Connect signals for reactive updates
4. Add persistence in `AppState.save_settings()`

## Troubleshooting

### Port Access Issues (Linux)

Add your user to the dialout group:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

### Permission Denied (macOS)

Grant Terminal.app full disk access in System Preferences → Security & Privacy.

### Transfer Failures

- Ensure both devices use the same protocol
- Check baud rate matches on both ends
- Verify flow control settings
- Enable debug mode: `python ymodterm_gui.py -d`

### Qt Backend Issues

YModTerm uses qtpy for Qt abstraction. If you encounter import errors:
```bash
# Try different Qt backends
pip install PyQt5  # or
pip install PySide2  # or
pip install PyQt6  # or
pip install PySide6
```

## Credits

- Based on [alexwoo1900/ymodem](https://github.com/alexwoo1900/ymodem) library
- Built with Qt and Python
- Serial communication via pyserial

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
