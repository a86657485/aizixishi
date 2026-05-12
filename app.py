from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = 'survey_data.json'

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def read_data():
    init_data_file()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('ai_classroom_survey.html')

@app.route('/api/submit', methods=['POST'])
def submit_survey():
    try:
        data = request.get_json()
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['id'] = len(read_data()) + 1
        
        all_data = read_data()
        all_data.append(data)
        save_data(all_data)
        
        return jsonify({'success': True, 'message': '提交成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/data')
def get_all_data():
    data = read_data()
    return jsonify(data)

@app.route('/api/stats')
def get_stats():
    data = read_data()
    stats = {
        'total': len(data),
        'recent_7_days': 0,
        'by_subject': {},
        'by_experience': {},
        'by_grade': {},
        'big_screen_interactive': {},
        'big_screen_ai': {},
        'big_screen_assessment': {},
        'big_screen_record': {},
        'big_screen_complexity': {},
        'ai_prep': {},
        'ai_classroom': {},
        'ai_evaluation': {},
        'ai_personalized': {},
        'ipad_need': {},
        'ipad_interactive': {},
        'ipad_create': {},
        'ipad_ar': {},
        'ipad_ai': {},
        'ipad_manage': {},
        'ipad_worry': {},
        'support': {},
        'willingness': {}
    }
    
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    for item in data:
        try:
            ts = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
            if ts >= seven_days_ago:
                stats['recent_7_days'] += 1
        except:
            pass
        
        if 'q1' in item:
            for subject in item['q1']:
                stats['by_subject'][subject] = stats['by_subject'].get(subject, 0) + 1
        
        if 'q2' in item and len(item['q2']) > 0:
            exp = item['q2'][0]
            stats['by_experience'][exp] = stats['by_experience'].get(exp, 0) + 1
        
        if 'q3' in item:
            for grade in item['q3']:
                stats['by_grade'][grade] = stats['by_grade'].get(grade, 0) + 1
        
        if 'q7a' in item:
            for feature in item['q7a']:
                stats['big_screen_interactive'][feature] = stats['big_screen_interactive'].get(feature, 0) + 1
        
        if 'q7b' in item:
            for feature in item['q7b']:
                stats['big_screen_ai'][feature] = stats['big_screen_ai'].get(feature, 0) + 1
        
        if 'q7c' in item:
            for feature in item['q7c']:
                stats['big_screen_assessment'][feature] = stats['big_screen_assessment'].get(feature, 0) + 1
        
        if 'q7d' in item:
            for feature in item['q7d']:
                stats['big_screen_record'][feature] = stats['big_screen_record'].get(feature, 0) + 1
        
        if 'q8' in item and item['q8']:
            stats['big_screen_complexity'][item['q8']] = stats['big_screen_complexity'].get(item['q8'], 0) + 1
        
        if 'q9' in item:
            for feature in item['q9']:
                if '教案' in feature or '课件' in feature or '素材' in feature or '出题' in feature or '作业' in feature:
                    stats['ai_prep'][feature] = stats['ai_prep'].get(feature, 0) + 1
                elif '互动' in feature or '角色' in feature or '游戏' in feature or '沉浸' in feature or '跨学科' in feature:
                    stats['ai_classroom'][feature] = stats['ai_classroom'].get(feature, 0) + 1
                elif '学情' in feature or '答题' in feature or '作品' in feature or '口语' in feature or '报告' in feature:
                    stats['ai_evaluation'][feature] = stats['ai_evaluation'].get(feature, 0) + 1
                elif '个性化' in feature or '自适应' in feature or '知识图谱' in feature:
                    stats['ai_personalized'][feature] = stats['ai_personalized'].get(feature, 0) + 1
        
        if 'q10' in item and len(item['q10']) > 0:
            need = item['q10'][0]
            stats['ipad_need'][need] = stats['ipad_need'].get(need, 0) + 1
        
        if 'q11a' in item:
            for feature in item['q11a']:
                stats['ipad_interactive'][feature] = stats['ipad_interactive'].get(feature, 0) + 1
        
        if 'q11b' in item:
            for feature in item['q11b']:
                stats['ipad_create'][feature] = stats['ipad_create'].get(feature, 0) + 1
        
        if 'q11c' in item:
            for feature in item['q11c']:
                stats['ipad_ar'][feature] = stats['ipad_ar'].get(feature, 0) + 1
        
        if 'q11d' in item:
            for feature in item['q11d']:
                stats['ipad_ai'][feature] = stats['ipad_ai'].get(feature, 0) + 1
        
        if 'q11e' in item:
            for feature in item['q11e']:
                stats['ipad_manage'][feature] = stats['ipad_manage'].get(feature, 0) + 1
        
        if 'q12' in item:
            for worry in item['q12']:
                stats['ipad_worry'][worry] = stats['ipad_worry'].get(worry, 0) + 1
        
        if 'q14' in item:
            for support in item['q14']:
                stats['support'][support] = stats['support'].get(support, 0) + 1
        
        if 'q15' in item and item['q15']:
            stats['willingness'][item['q15']] = stats['willingness'].get(item['q15'], 0) + 1
    
    return jsonify(stats)

@app.route('/api/wordcloud')
def get_wordcloud():
    data = read_data()
    wordcloud_data = {
        'big_screen': {},
        'ai_features': {},
        'ipad_features': {},
        'concerns': {}
    }
    
    for item in data:
        if 'q7a' in item:
            for feature in item['q7a']:
                wordcloud_data['big_screen'][feature] = wordcloud_data['big_screen'].get(feature, 0) + 1
        if 'q7b' in item:
            for feature in item['q7b']:
                wordcloud_data['big_screen'][feature] = wordcloud_data['big_screen'].get(feature, 0) + 1
        if 'q7c' in item:
            for feature in item['q7c']:
                wordcloud_data['big_screen'][feature] = wordcloud_data['big_screen'].get(feature, 0) + 1
        if 'q7d' in item:
            for feature in item['q7d']:
                wordcloud_data['big_screen'][feature] = wordcloud_data['big_screen'].get(feature, 0) + 1
        
        if 'q9' in item:
            for feature in item['q9']:
                wordcloud_data['ai_features'][feature] = wordcloud_data['ai_features'].get(feature, 0) + 1
        
        if 'q11a' in item:
            for feature in item['q11a']:
                wordcloud_data['ipad_features'][feature] = wordcloud_data['ipad_features'].get(feature, 0) + 1
        if 'q11b' in item:
            for feature in item['q11b']:
                wordcloud_data['ipad_features'][feature] = wordcloud_data['ipad_features'].get(feature, 0) + 1
        if 'q11c' in item:
            for feature in item['q11c']:
                wordcloud_data['ipad_features'][feature] = wordcloud_data['ipad_features'].get(feature, 0) + 1
        if 'q11d' in item:
            for feature in item['q11d']:
                wordcloud_data['ipad_features'][feature] = wordcloud_data['ipad_features'].get(feature, 0) + 1
        if 'q11e' in item:
            for feature in item['q11e']:
                wordcloud_data['ipad_features'][feature] = wordcloud_data['ipad_features'].get(feature, 0) + 1
        
        if 'q12' in item:
            for worry in item['q12']:
                wordcloud_data['concerns'][worry] = wordcloud_data['concerns'].get(worry, 0) + 1
    
    def convert_to_list(word_dict):
        return [{'name': k, 'value': v} for k, v in word_dict.items()]
    
    return jsonify({
        'big_screen': convert_to_list(wordcloud_data['big_screen']),
        'ai_features': convert_to_list(wordcloud_data['ai_features']),
        'ipad_features': convert_to_list(wordcloud_data['ipad_features']),
        'concerns': convert_to_list(wordcloud_data['concerns'])
    })

@app.route('/api/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    data = read_data()
    new_data = [item for item in data if item.get('id') != data_id]
    if len(new_data) < len(data):
        for i, item in enumerate(new_data):
            item['id'] = i + 1
        save_data(new_data)
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    init_data_file()
    app.run(debug=True, host='0.0.0.0', port=5000)
