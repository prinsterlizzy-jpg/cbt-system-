import React, {useState} from 'react';
import Login from './components/Login';
import Exam from './components/Exam';
import Dashboard from './components/Dashboard';
import 'bootstrap/dist/css/bootstrap.min.css';

function App(){
  const [user, setUser] = useState(null);
  const [taking, setTaking] = useState(false);
  const [result, setResult] = useState(null);

  const onLogin = (username) => setUser(username);
  const startExam = () => { setTaking(true); setResult(null); }
  const finishExam = (score, total) => { setTaking(false); setResult({score,total}); }

  if(!user) return (
    <div className='container py-5'><Login onLogin={onLogin} /></div>
  );

  if(taking) return <div className='container py-3'><Exam username={user} onFinish={finishExam} /></div>;

  return (
    <div className='container py-3'>
      <Dashboard username={user} startExamCallback={startExam} />
      {result && <div className='alert alert-success mt-3'>You scored {result.score} / {result.total}</div>}
    </div>
  )
}

export default App;
