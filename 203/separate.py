import os

def split_and_extract_jpegs(input_file, 
                            signature=b"\x50\x4B\x03\x04", 
                            out_dir="output"):
    with open(input_file, "rb") as f:
        data = f.read()

    # ZIP File Entry 시그니처 위치 찾기
    indexes = []
    start = 0
    while True:
        idx = data.find(signature, start)
        if idx == -1:
            break
        indexes.append(idx)
        start = idx + 1

    print(f"[+] Found {len(indexes)} file entries.")

    os.makedirs(out_dir, exist_ok=True)

    jpeg_count = 0

    for i in range(len(indexes)):
        start = indexes[i]
        end = indexes[i+1] if i+1 < len(indexes) else len(data)
        chunk = data[start:end]

        entry_path = os.path.join(out_dir, f"entry_{i}.bin")
        with open(entry_path, "wb") as out:
            out.write(chunk)
        print(f"[+] Saved entry_{i}.bin ({len(chunk)} bytes)")

        # JPEG 시그니처 탐색
        pos = 0
        while True:
            start_jpg = chunk.find(b"\xFF\xD8", pos)  # JPEG 시작
            if start_jpg == -1:
                break
            end_jpg = chunk.find(b"\xFF\xD9", start_jpg)  # JPEG 끝
            if end_jpg == -1:
                break
            jpeg_data = chunk[start_jpg:end_jpg+2]  # 푸터 포함

            jpeg_path = os.path.join(out_dir, f"entry_{i}_img_{jpeg_count}.jpg")
            with open(jpeg_path, "wb") as jpg_out:
                jpg_out.write(jpeg_data)
            print(f"    -> Extracted JPEG: {jpeg_path} ({len(jpeg_data)} bytes)")
            jpeg_count += 1

            pos = end_jpg + 2  # 다음 검색으로 이동

    print(f"[+] Done. Extracted {jpeg_count} JPEGs in total.")


if __name__ == "__main__":
    split_and_extract_jpegs("PD12M_dataset.zip.enc")
