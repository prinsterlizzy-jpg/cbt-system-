import React, {useState} from 'react';
import {login, register} from '../api';
export default function Login({onLogin}){
  const [username,setUsername]=useState('');
  const [password,setPassword]=useState('');
  const [registering,setRegistering]=useState(false);
  const submit = async (e) => {
    e.preventDefault();
    if(registering){
      const r = await register(username,password);
      if(r.ok) alert('Registered! Now login.');
      else alert(r.error || 'Register failed');
      setRegistering(false);
      return;
    }
    const res = await login(username, password);
    if(res.ok){
      onLogin(res.username);
    } else {
      alert(res.error || 'Login failed');
    }
  }
  return (
    <div className='card p-4'>
      <h3>{registering ? 'Register' : 'Login'}</h3>
      <form onSubmit={submit}>
        <div className='mb-2'><input value={username} onChange={e=>setUsername(e.target.value)} className='form-control' placeholder='username' required /></div>
        <div className='mb-2'><input value={password} onChange={e=>setPassword(e.target.value)} type='password' className='form-control' placeholder='password' required /></div>
        <button className='btn btn-primary me-2' type='submit'>{registering ? 'Register' : 'Login'}</button>
        <button type='button' className='btn btn-link' onClick={()=>setRegistering(s=>!s)}>{registering ? 'Already have account? Login' : 'Create account'}</button>
      </form>
    </div>
  )
}
