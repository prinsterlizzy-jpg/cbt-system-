import React, {useEffect, useState} from 'react';
import {getResults} from '../api';
export default function Dashboard({username, startExamCallback}){
  const [results, setResults] = useState([]);
  useEffect(()=>{ async function load(){ const r = await getResults(username); if(r.ok) setResults(r.results); } load(); }, [username]);
  return (
    <div>
      <h3>Welcome, {username}</h3>
      <button className='btn btn-primary mb-3' onClick={()=> startExamCallback()}>Start Exam</button>
      <h5>Your Past Results</h5>
      <table className='table'>
        <thead><tr><th>ID</th><th>Score</th><th>Total</th><th>Timestamp</th></tr></thead>
        <tbody>{results.map(r=> (<tr key={r.id}><td>{r.id}</td><td>{r.score}</td><td>{r.total}</td><td>{r.timestamp}</td></tr>))}</tbody>
      </table>
    </div>
  )
}
