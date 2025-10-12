import {useEffect,useState} from 'react'
export default function Trade(){ const [acc,setAcc]=useState(null); useEffect(()=>{ fetch('/api/proxy/api/trader/account?user=demo&mode=paper').then(r=>r.json()).then(j=>setAcc(j.account)) },[]); return (<div style={{padding:20}}><h1>IQSIGNALS Trade</h1><pre>{JSON.stringify(acc,null,2)}</pre></div>) }
