def clean_text(text):
    import  re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove \n, \r, and other whitespace characters
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Strip leading/trailing spaces
    text = text.strip()
    return text