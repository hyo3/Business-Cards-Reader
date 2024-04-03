import re
def extract_file_id(url):
    # Google Drive URL のパターンを正規表現で定義
    pattern = r'https://drive\.google\.com/file/d/([^/]+)'
    
    # 正規表現とURLを照合して、IDを取得
    match = re.search(pattern, url)
    
    if match:
        file_id = match.group(1)
        return file_id
    else:
        return None