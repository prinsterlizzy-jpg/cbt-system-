import React, {useEffect, useState} from 'react';
import {getQuestion} from '../api';
export default function QuestionPage({examId, idx, onAnswer, selectedAnswer}){
  const [question, setQuestion] = useState(null);
  useEffect(()=>{ let mounted=true; async function load(){ const r = await getQuestion(examId, idx); if(r.ok && mounted) setQuestion(r.question);} load(); return ()=> mounted=false; }, [examId, idx]);

  if(!question) return <div>Loading question...</div>;
  const qid = question.id;
  const sel = selectedAnswer && selectedAnswer[qid];

  return (
    <div className='card p-3'>
      <h5>{question.text}</h5>
      <div className='list-group'>
        {question.options.map((opt,i)=>
          <label className={'list-group-item ' + (sel===opt ? 'active' : '')} key={i}>
            <input type='radio' name={'opt'+qid} checked={sel===opt} onChange={()=>onAnswer(qid,opt)} /> {' '}
            {opt}
          </label>
        )}
      </div>
    </div>
  )
}
