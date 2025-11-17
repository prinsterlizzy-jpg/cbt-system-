import React, {useState, useEffect, useRef} from 'react';
import {startExam, getQuestion, submitExam} from '../api';
import QuestionPage from './QuestionPage';
export default function Exam({username, onFinish}){
  const [examId, setExamId] = useState(null);
  const [total, setTotal] = useState(0);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const timerRef = useRef(null);

  useEffect(()=>{ async function start(){ const r = await startExam(username, 300); if(r.ok){ setExamId(r.exam_id); setTotal(r.question_order.length); setTimeLeft(r.duration);} else { alert('Could not start exam'); } } start(); }, [username]);

  useEffect(()=>{ if(timeLeft <= 0 && examId){ handleSubmit(); } timerRef.current = setTimeout(()=> setTimeLeft(t => t-1), 1000); return ()=> clearTimeout(timerRef.current); }, [timeLeft, examId]);

  const handleAnswer = (qid, selected) => setAnswers(prev => ({...prev, [qid]: selected}));
  const next = () => setCurrentIdx(i => Math.min(i+1, total-1));
  const prev = () => setCurrentIdx(i => Math.max(i-1, 0));
  const handleSubmit = async () => {
    const res = await submitExam({exam_id: examId, username, answers});
    if(res.ok){ onFinish(res.score, res.total); } else { alert('Submit error'); }
  }

  if(!examId) return <div>Starting exam...</div>;

  return (
    <div>
      <div className='d-flex justify-content-between mb-2'><div>Question {currentIdx+1} / {total}</div><div>Time left: {Math.floor(timeLeft/60)}:{String(timeLeft%60).padStart(2,'0')}</div></div>
      <QuestionPage examId={examId} idx={currentIdx} onAnswer={handleAnswer} selectedAnswer={answers} />
      <div className='mt-3'>
        <button className='btn btn-secondary me-2' onClick={prev} disabled={currentIdx===0}>Previous</button>
        <button className='btn btn-secondary me-2' onClick={next} disabled={currentIdx===total-1}>Next</button>
        <button className='btn btn-danger' onClick={handleSubmit}>Submit Exam</button>
      </div>
    </div>
  )
}
