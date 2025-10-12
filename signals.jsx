import {useEffect,useState} from 'react'
export default function Signals(){ const [s,setS]=useState([]); useEffect(()=>{ fetch('/api/proxy/api/ai/latest').then(r=>r.json()).then(j=>setS(j.latest||[])) },[]); return (<div style={{padding:20}}><h1>AI Signals</h1><pre>{JSON.stringify(s,null,2)}</pre></div>) }
