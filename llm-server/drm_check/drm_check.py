import pdfreader
def check_pdf_for_drm(file) -> bool:
    try:
        reader = pdfreader(file)
        return reader.is_encrypted
    except Exception:
        return True 