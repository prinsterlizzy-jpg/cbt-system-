const API_BASE = "http://127.0.0.1:5000";
export async function login(username, password){
  const res = await fetch(API_BASE + "/api/login", {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username, password})
  });
  return res.json();
}
export async function register(username, password){
  const res = await fetch(API_BASE + "/api/register", {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username, password})
  });
  return res.json();
}
export async function startExam(username, duration=300){
  const res = await fetch(API_BASE + "/api/start_exam", {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username, duration})
  });
  return res.json();
}
export async function getQuestion(exam_id, idx){
  const res = await fetch(`${API_BASE}/api/exam/${exam_id}/question/${idx}`);
  return res.json();
}
export async function submitExam(payload){
  const res = await fetch(API_BASE + "/api/submit_exam", {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  return res.json();
}
export async function getResults(username){
  const res = await fetch(`${API_BASE}/api/results/${username}`);
  return res.json();
}
