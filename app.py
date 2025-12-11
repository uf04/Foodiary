from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 데이터 구조 변경: ID와 조리 순서(steps) 추가
MOCK_RECIPES = [
    {
        "id": 1,
        "title": "김치찌개",
        "ingredients": ["김치", "돼지고기", "두부", "대파"],
        "desc": "한국인의 소울푸드, 얼큰한 김치찌개입니다.",
        "steps": [
            "돼지고기를 냄비에 넣고 볶아 기름을 냅니다.",
            "김치를 넣고 함께 볶습니다.",
            "물을 붓고 끓어오르면 두부와 대파를 넣습니다.",
            "간을 맞추고 한소끔 더 끓여 완성합니다."
        ]
    },
    {
        "id": 2,
        "title": "된장찌개",
        "ingredients": ["된장", "두부", "호박", "양파"],
        "desc": "구수한 국물이 일품인 된장찌개.",
        "steps": [
            "뚝배기에 물을 붓고 멸치 육수를 냅니다.",
            "된장을 풀고 호박, 양파를 넣어 끓입니다.",
            "야채가 익으면 두부를 넣습니다.",
            "마지막에 고춧가루를 살짝 뿌려 냅니다."
        ]
    },
    {
        "id": 3,
        "title": "제육볶음",
        "ingredients": ["돼지고기", "고추장", "양파", "당근"],
        "desc": "매콤달콤 밥도둑 제육볶음.",
        "steps": [
            "돼지고기를 먹기 좋은 크기로 썹니다.",
            "고추장, 간장, 설탕으로 양념장을 만듭니다.",
            "고기에 양념을 버무려 재워둡니다.",
            "팬에 기름을 두르고 야채와 함께 볶아냅니다."
        ]
    },
     {
        "id": 4,
        "title": "계란말이",
        "ingredients": ["계란", "파", "당근", "소금"],
        "desc": "부드럽고 폭신한 국민 반찬.",
        "steps": [
            "계란을 풀고 다진 야채를 섞습니다.",
            "팬에 기름을 두르고 계란물을 얇게 붓습니다.",
            "끝에서부터 돌돌 말아줍니다.",
            "반복하여 두툼하게 만든 뒤 썰어냅니다."
        ]
    },
    {
        "id": 5,
        "title": "두부김치",
        "ingredients": ["김치", "두부", "참기름", "깨"],
        "desc": "술안주로 최고인 두부김치.",
        "steps": [
            "두부를 끓는 물에 살짝 데칩니다.",
            "김치는 참기름에 달달 볶습니다.",
            "접시에 두부와 볶음김치를 예쁘게 담습니다.",
            "깨를 뿌려 마무리합니다."
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# [NEW] 상세 페이지 라우트
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    # ID에 해당하는 레시피 찾기
    recipe = next((r for r in MOCK_RECIPES if r['id'] == recipe_id), None)
    
    if recipe:
        return render_template('detail.html', recipe=recipe)
    else:
        return "레시피를 찾을 수 없습니다.", 404

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('ingredient', '').strip()
    
    if not query:
        return jsonify({'status': 'error', 'message': '재료를 입력해주세요.'})

    results = [
        r for r in MOCK_RECIPES 
        if any(query in ing for ing in r['ingredients'])
    ]

    return jsonify({'status': 'success', 'results': results})

if __name__ == '__main__':
    app.run(debug=True)