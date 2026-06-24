from pathlib import Path
import struct

def png_size(path):
    with open(path, 'rb') as f:
        header = f.read(24)
        if header[:8] != b'\x89PNG\r\n\x1a\n':
            return None
        return struct.unpack('>II', header[16:24])

def jpeg_size(path):
    with open(path, 'rb') as f:
        if f.read(2) != b'\xff\xd8':
            return None
        while True:
            marker = f.read(1)
            code = f.read(1)
            if not marker or marker != b'\xff':
                return None
            while code == b'\xff':
                code = f.read(1)
            if code in [b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc5', b'\xc6', b'\xc7', b'\xc9', b'\xca', b'\xcb', b'\xcd', b'\xce', b'\xcf']:
                length = struct.unpack('>H', f.read(2))[0]
                data = f.read(length - 2)
                return struct.unpack('>HH', data[1:5])[::-1]
            else:
                length = struct.unpack('>H', f.read(2))[0]
                f.seek(length - 2, 1)

for name in [r'c:\xampp\htdocs\Habana_5\img\Logo.png', r'c:\xampp\htdocs\Habana_5\img\Habana_6.png']:
    p = Path(name)
    if not p.exists():
        print(name, 'MISSING')
        continue
    with open(p, 'rb') as f:
        sig = f.read(8)
    if sig.startswith(b'\x89PNG'):
        size = png_size(p)
        fmt = 'PNG'
    elif sig[:2] == b'\xff\xd8':
        size = jpeg_size(p)
        fmt = 'JPEG'
    else:
        size = None
        fmt = 'UNKNOWN'
    print(name, fmt, 'size=', size, 'bytes=', p.stat().st_size)
