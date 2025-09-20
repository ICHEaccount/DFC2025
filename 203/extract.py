import os
import struct
import zlib

def extract_from_entry(entry_file, out_dir="jpeg_out"):
    with open(entry_file, "rb") as f:
        data = f.read()

    sig = data[0:4]
    if sig != b"PK\x03\x04":
        print(f"[-] {entry_file}: Not a valid Local File Header")
        return None

    # Local File Header 구조 해석
    (
        version_needed,
        flags,
        compression,
        mod_time,
        mod_date,
        crc32,
        comp_size,
        uncomp_size,
        fname_len,
        extra_len
    ) = struct.unpack("<HHHHHIIIHH", data[4:30])

    filename = data[30:30+fname_len].decode(errors="ignore")
    offset = 30 + fname_len + extra_len
    comp_data = data[offset:offset+comp_size]

    # 압축 방식 처리
    if compression == 8:  # deflate
        try:
            jpg_data = zlib.decompress(comp_data, -15)  # raw deflate
        except Exception as e:
            print(f"[-] {entry_file}: Decompression failed ({e})")
            return None
    elif compression == 0:  # stored
        jpg_data = comp_data
    else:
        print(f"[-] {entry_file}: Unsupported compression method {compression}")
        return None

    # 출력 디렉토리 생성
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    with open(out_path, "wb") as out:
        out.write(jpg_data)

    print(f"[+] {entry_file} -> {out_path} ({len(jpg_data)} bytes)")
    return out_path


def batch_extract(entry_dir="output", out_dir="jpeg_out"):
    extracted = []
    for fname in sorted(os.listdir(entry_dir)):
        if fname.startswith("entry_") and fname.endswith(".bin"):
            fpath = os.path.join(entry_dir, fname)
            res = extract_from_entry(fpath, out_dir=out_dir)
            if res:
                extracted.append(res)

    print(f"[+] Done. Extracted {len(extracted)} JPEGs into {out_dir}")
    return extracted


if __name__ == "__main__":
    # 분리된 entry_x.bin 파일들이 들어있는 디렉토리 지정
    batch_extract(entry_dir="output", out_dir="jpeg_out")
