from flask import Flask, render_template, request, jsonify
import requests
import re # 정규표현식 (HTML 태그 제거용)

app = Flask(__name__)

# ==========================================
# [중요] 발급받은 네이버 API 키를 여기에 입력하세요
# ==========================================
CLIENT_ID = "w2ysouqzNQzzrT_Y_h9L"
CLIENT_SECRET = "ZeNkdw_bOm"

def clean_html(text):
    """네이버 API 결과에 포함된 <b>, &quot; 같은 태그를 제거하는 함수"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)
    return cleantext

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('ingredient', '').strip()
    
    if not keyword:
        return jsonify({'status': 'error', 'message': '재료를 입력해주세요.'})

    # 네이버 블로그 검색 API 호출
    # 검색어 뒤에 ' 레시피'를 자동으로 붙여서 검색 정확도를 높임
    encText = keyword + " 레시피"
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display=10&sort=sim"
    
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            # 프론트엔드에 보낼 데이터 정리
            results = []
            for item in items:
                results.append({
                    "title": clean_html(item['title']),
                    "desc": clean_html(item['description']),
                    "link": item['link'], # 블로그 원문 링크
                    "blogger": item['bloggername'],
                    "postdate": item['postdate']
                })
            
            return jsonify({'status': 'success', 'results': results})
        else:
            return jsonify({'status': 'error', 'message': '네이버 API 호출 실패'})
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': '서버 에러 발생'})

if __name__ == '__main__':
    app.run(debug=True)