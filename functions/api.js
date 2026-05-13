const fs = require('fs');

const DATA_FILE = '/tmp/survey_data.json';

function readData() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    }
  } catch (e) {}
  return [];
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

function getStats(data) {
  const stats = {
    total: data.length, recent_7_days: 0,
    by_subject: {}, by_experience: {}, by_grade: {},
    big_screen_interactive: {}, big_screen_ai: {}, big_screen_assessment: {}, big_screen_record: {},
    big_screen_complexity: {},
    ai_prep: {}, ai_classroom: {}, ai_evaluation: {}, ai_personalized: {},
    ipad_need: {}, ipad_interactive: {}, ipad_create: {}, ipad_ar: {}, ipad_ai: {}, ipad_manage: {},
    ipad_worry: {}, support: {}, willingness: {}
  };

  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

  data.forEach(function(item) {
    if (item.timestamp && new Date(item.timestamp) >= sevenDaysAgo) stats.recent_7_days++;

    const fieldMap = {
      q1: 'by_subject', q3: 'by_grade',
      q7a: 'big_screen_interactive', q7b: 'big_screen_ai',
      q7c: 'big_screen_assessment', q7d: 'big_screen_record',
      q11a: 'ipad_interactive', q11b: 'ipad_create', q11c: 'ipad_ar',
      q11d: 'ipad_ai', q11e: 'ipad_manage', q12: 'ipad_worry', q14: 'support'
    };

    Object.keys(fieldMap).forEach(function(k) {
      if (Array.isArray(item[k])) {
        item[k].forEach(function(v) { stats[fieldMap[k]][v] = (stats[fieldMap[k]][v] || 0) + 1; });
      }
    });

    if (item.q2 && item.q2.length > 0) stats.by_experience[item.q2[0]] = (stats.by_experience[item.q2[0]] || 0) + 1;
    if (item.q8) stats.big_screen_complexity[item.q8] = (stats.big_screen_complexity[item.q8] || 0) + 1;
    if (item.q10 && item.q10.length > 0) stats.ipad_need[item.q10[0]] = (stats.ipad_need[item.q10[0]] || 0) + 1;
    if (item.q15) stats.willingness[item.q15] = (stats.willingness[item.q15] || 0) + 1;

    if (Array.isArray(item.q9)) {
      item.q9.forEach(function(v) {
        if (/教案|课件|素材|出题|作业/.test(v)) stats.ai_prep[v] = (stats.ai_prep[v] || 0) + 1;
        else if (/互动|角色|游戏|沉浸|跨学科/.test(v)) stats.ai_classroom[v] = (stats.ai_classroom[v] || 0) + 1;
        else if (/学情|答题|作品|口语|报告/.test(v)) stats.ai_evaluation[v] = (stats.ai_evaluation[v] || 0) + 1;
        else if (/个性化|自适应|知识图谱/.test(v)) stats.ai_personalized[v] = (stats.ai_personalized[v] || 0) + 1;
      });
    }
  });

  return stats;
}

function getWordcloud(data) {
  const wc = { big_screen: {}, ai_features: {}, ipad_features: {}, concerns: {} };

  data.forEach(function(item) {
    ['q7a','q7b','q7c','q7d'].forEach(function(k) {
      if (Array.isArray(item[k])) item[k].forEach(function(v) { wc.big_screen[v] = (wc.big_screen[v] || 0) + 1; });
    });
    if (Array.isArray(item.q9)) item.q9.forEach(function(v) { wc.ai_features[v] = (wc.ai_features[v] || 0) + 1; });
    ['q11a','q11b','q11c','q11d','q11e'].forEach(function(k) {
      if (Array.isArray(item[k])) item[k].forEach(function(v) { wc.ipad_features[v] = (wc.ipad_features[v] || 0) + 1; });
    });
    if (Array.isArray(item.q12)) item.q12.forEach(function(v) { wc.concerns[v] = (wc.concerns[v] || 0) + 1; });
  });

  function toList(obj) { return Object.keys(obj).map(function(k) { return { name: k, value: obj[k] }; }); }

  return {
    big_screen: toList(wc.big_screen), ai_features: toList(wc.ai_features),
    ipad_features: toList(wc.ipad_features), concerns: toList(wc.concerns)
  };
}

exports.handler = async function(event) {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };

  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers, body: '' };

  const p = event.path || '';
  const method = event.httpMethod;

  try {
    if (p.includes('/submit') && method === 'POST') {
      const body = JSON.parse(event.body || '{}');
      body.timestamp = body.timestamp || new Date().toISOString();
      const all = readData();
      body.id = all.length + 1;
      all.push(body);
      saveData(all);
      return { statusCode: 200, headers, body: JSON.stringify({ success: true, message: '提交成功' }) };
    }
    if (p.includes('/data') && method === 'GET') {
      return { statusCode: 200, headers, body: JSON.stringify(readData()) };
    }
    if (p.includes('/stats') && method === 'GET') {
      return { statusCode: 200, headers, body: JSON.stringify(getStats(readData())) };
    }
    if (p.includes('/wordcloud') && method === 'GET') {
      return { statusCode: 200, headers, body: JSON.stringify(getWordcloud(readData())) };
    }
    return { statusCode: 404, headers, body: JSON.stringify({ error: 'Not found' }) };
  } catch (e) {
    return { statusCode: 500, headers, body: JSON.stringify({ success: false, message: e.message }) };
  }
};
