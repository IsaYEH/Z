async function postChart(){
  const date=document.getElementById('date').value;
  const time=document.getElementById('time').value;
  const place=document.getElementById('place').value;

  const res=await fetch('/api/charts',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({date,time,place})
  });
  const j=await res.json();

  const grid=document.getElementById('zwGrid');
  grid.innerHTML="";
  const palaces=["命宮","兄弟宮","夫妻宮","子女宮","財帛宮","疾厄宮","遷移宮","交友宮","官祿宮","田宅宮","福德宮","父母宮"];
  palaces.forEach(p=>{
    const cell=document.createElement('div');
    cell.className="palace";
    const stars=j.natal.stars[p]||[];
    cell.innerHTML=`<strong>${p}</strong><br>`+stars.map(s=>s.name).join("、");
    grid.appendChild(cell);
  });
}
document.getElementById('formRoot').addEventListener('submit',e=>{e.preventDefault();postChart();});
