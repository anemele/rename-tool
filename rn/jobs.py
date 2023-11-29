from pathlib import Path

from .pp import preprocess


@preprocess
def rename_extension(filename: str):
    import filetype

    path = Path(filename)
    content = path.read_bytes()
    ext = filetype.guess_extension(content)
    if ext is None:
        print(f'[INFO] Cannot guess extension: {path.name}')
        return

    new_name = path.with_suffix(f'.{ext}')
    if new_name == filename:
        print(f'[INFO] Exists: {new_name}')
    else:
        path.rename(new_name)
        print(f'[INFO] Done: {filename} --> {new_name}')


@preprocess
def rename_md5(filename: str):
    from hashlib import md5

    path = Path(filename)
    content = path.read_bytes()
    md5 = md5(content)

    new_path = path.parent / (md5.hexdigest() + path.suffix)

    if new_path == filename or new_path.exists():
        print(f'[INFO] Exists: {filename} --> {new_path}')
    else:
        path.rename(new_path)
        print(f'[INFO] Done: {filename} --> {new_path}')


@preprocess
def rename_lower(filename: str):
    path = Path(filename)
    path.rename(path.with_name(path.name.lower()))
    print(f'[INFO] Done: {path}')


@preprocess
def rename_upper(filename: str):
    path = Path(filename)
    path.rename(path.with_name(path.name.upper()))
    print(f'[INFO] Done: {path}')


@preprocess
def rename_random(filename: str):
    """Rename using random generator"""
    import random
    import string

    CHAR_SET = string.ascii_lowercase + string.digits
    NAME_LENGTH = 6
    path = Path(filename)
    suffix = path.suffix

    while True:
        char_list = random.choices(CHAR_SET, k=NAME_LENGTH)
        name = ''.join(char_list)
        new_name = Path(f'{name}{suffix}')
        if new_name.exists():
            continue
        path.rename(new_name)
        print(f'[INFO] Done: {filename} --> {new_name}')
        break
