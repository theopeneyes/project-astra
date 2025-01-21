import pypdf

def check_pdf_for_drm(file_obj) -> bool:
    """
    Checks if the provided PDF is encrypted, which may indicate DRM protection.
    Returns True if DRM protection (encryption) is found, otherwise False.
    """
    try:
        reader = pypdf.PdfFileReader(file_obj)
        if reader.isEncrypted:
            try:
                reader.decrypt("")
                return True  # The PDF is encrypted, so it might be DRM-protected
            except Exception as e:
                # Decryption failed, indicating that it might be password-protected or DRM-protected
                return True
        
    except Exception as e:
        # If there is any error opening or reading the PDF, assume DRM or unsupported PDF format
        return False
    
    # return False
