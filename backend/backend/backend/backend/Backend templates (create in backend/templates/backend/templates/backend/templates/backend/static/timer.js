// Example timer for server-rendered exam pages (non-React)
function startTimer(elemId, duration, onEnd){
  let t = duration;
  const el = document.getElementById(elemId);
  const iv = setInterval(()=>{
    const mm = Math.floor(t/60);
    const ss = t%60;
    if(el) el.textContent = mm.toString().padStart(2,'0') + ':' + ss.toString().padStart(2,'0');
    if(t<=0){
      clearInterval(iv);
      if(onEnd) onEnd();
    }
    t--;
  },1000);
  return iv;
}
