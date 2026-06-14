/* ============================================================================
   China–US climate scenario explorer
   Data is loaded from the four CSV files in data/. Replacing those files with
   updated sourced data requires no changes to this script.
   ========================================================================== */

/* ============ CSV parsing ============ */
function splitCSVLine(line){
  const out=[];let cur="";let q=false;
  for(let i=0;i<line.length;i++){const ch=line[i];
    if(q){ if(ch=='"'){ if(line[i+1]=='"'){cur+='"';i++;} else q=false; } else cur+=ch; }
    else{ if(ch=='"')q=true; else if(ch==',' ){out.push(cur);cur="";} else cur+=ch; }
  }
  out.push(cur);return out;
}
function parseCSV(text){
  const lines=text.trim().split(/\r?\n/);
  const headers=splitCSVLine(lines[0]).map(h=>h.trim());
  return lines.slice(1).filter(l=>l.length).map(l=>{
    const c=splitCSVLine(l);const o={};headers.forEach((h,i)=>o[h]=(c[i]!==undefined?c[i]:""));return o;
  });
}

/* ============ constants ============ */
const COL={China:"#B23A2E","United States":"#2A4D69"};
const SYM={China:"circle","United States":"diamond"};
const GRID="#D8D4CC",INK="#1A1A1A",SUB="#555555",MUTED="#B0ABA2",BG="#F7F6F2";
const FONT='Inter, "Source Sans 3", system-ui, Arial, sans-serif';
const SCEN={
  low:{phys:"SSP1-2.6",trans:"Net Zero 2050",label:"Low",gw:1.8},
  intermediate:{phys:"SSP2-4.5",trans:"Delayed Transition",label:"Intermediate",gw:2.7},
  high:{phys:"SSP5-8.5",trans:"Current Policies",label:"High",gw:4.4}
};
// gw = best-estimate global mean warming by 2081-2100 vs 1850-1900 (IPCC AR6 SPM)
const INDIC={
  temp_anomaly:{title:"Mean temperature anomaly",ytitle:"Temperature anomaly (°C)",unit:"°C",
    desc:"Annual mean temperature relative to the 1981–2010 baseline.",
    fmt:v=>v.toFixed(2)+" °C",
    finding:"Both countries warm under every pathway; the magnitude depends strongly on the scenario."},
  precip_change:{title:"Annual precipitation change",ytitle:"Precipitation change (% vs baseline)",unit:"%",
    desc:"Annual precipitation relative to the 1981–2010 baseline.",
    fmt:v=>(v>0?"+":"")+v.toFixed(1)+" %",
    finding:"Precipitation responses are smaller, more mixed and more uncertain than temperature changes."},
  hot_days:{title:"Extremely hot days (> 35 °C)",ytitle:"Days above 35 °C per year",unit:"days",
    desc:"Annual count of days with maximum temperature above 35 °C (national average).",
    fmt:v=>Math.round(v)+" days",
    finding:"Extreme-heat exposure rises sharply under higher-emissions pathways."}
};
const HISTLAST=2020;

/* ============ state ============ */
const DEFAULTS={countries:{China:true,"United States":true},indicator:"temp_anomaly",
  scenario:"intermediate",view:"climate",from:1990,to:2100};
let state=JSON.parse(JSON.stringify(DEFAULTS));
let abateSel=new Set();

/* ============ data stores ============ */
let PHYS,TRANS,ABATE,TIP;

async function fetchCSV(path){
  const r=await fetch(path);
  if(!r.ok) throw new Error("Could not load "+path+" ("+r.status+")");
  return await r.text();
}
async function loadData(){
  const [p,t,a,k]=await Promise.all([
    fetchCSV("data/physical_climate.csv"),
    fetchCSV("data/transition_pathways.csv"),
    fetchCSV("data/abatement_options.csv"),
    fetchCSV("data/tipping_points.csv")
  ]);
  PHYS=parseCSV(p);TRANS=parseCSV(t);ABATE=parseCSV(a);TIP=parseCSV(k);
}

/* ============ helpers ============ */
function selectedCountries(){return ["China","United States"].filter(c=>state.countries[c]);}
function physSeries(country,indicator,scenKey){
  const ssp=SCEN[scenKey].phys;
  const map=r=>({year:+r.year,v:+r.value,lo:+r.lower_bound,hi:+r.upper_bound,unit:r.unit,base:r.baseline_period});
  const hist=PHYS.filter(r=>r.country===country&&r.indicator===indicator&&r.scenario==="historical").map(map).sort((a,b)=>a.year-b.year);
  let proj=PHYS.filter(r=>r.country===country&&r.indicator===indicator&&r.scenario===ssp).map(map).sort((a,b)=>a.year-b.year);
  if(hist.length){proj=[hist[hist.length-1]].concat(proj);} // bridge gap
  return {hist,proj};
}

/* ============ climate chart ============ */
function updateClimateChart(){
  const ind=INDIC[state.indicator];const traces=[];const ann=[];
  selectedCountries().forEach(country=>{
    const {hist,proj}=physSeries(country,state.indicator,state.scenario);
    const col=COL[country];
    // uncertainty ribbon (projected)
    const xs=proj.map(d=>d.year);
    traces.push({x:xs,y:proj.map(d=>d.hi),mode:"lines",line:{width:0},
      hoverinfo:"skip",showlegend:false,name:country+" upper"});
    traces.push({x:xs,y:proj.map(d=>d.lo),mode:"lines",line:{width:0},fill:"tonexty",
      fillcolor:hexA(col,0.13),hoverinfo:"skip",showlegend:false,name:country+" lower"});
    // historical solid
    traces.push({x:hist.map(d=>d.year),y:hist.map(d=>d.v),mode:"lines+markers",
      line:{color:col,width:2.4},marker:{symbol:SYM[country],size:5,color:col},
      name:country+" (observed)",legendgroup:country,
      customdata:hist.map(d=>[country,"Observed",ind.fmt(d.v),ind.fmt(d.lo)+" – "+ind.fmt(d.hi),d.base]),
      hovertemplate:"<b>%{customdata[0]}</b> · %{x}<br>%{customdata[1]}<br>"+ind.title+": %{customdata[2]}<br>Baseline: %{customdata[4]}<extra></extra>"});
    // projected dashed
    traces.push({x:xs,y:proj.map(d=>d.v),mode:"lines",
      line:{color:col,width:2.4,dash:"dash"},name:country+" ("+SCEN[state.scenario].phys+")",legendgroup:country,
      customdata:proj.map(d=>[country,"Projected · "+SCEN[state.scenario].phys,ind.fmt(d.v),ind.fmt(d.lo)+" – "+ind.fmt(d.hi),d.base]),
      hovertemplate:"<b>%{customdata[0]}</b> · %{x}<br>%{customdata[1]}<br>"+ind.title+": %{customdata[2]}<br>Range: %{customdata[3]}<br>Baseline: %{customdata[4]}<extra></extra>"});
    // direct end label
    const last=proj[proj.length-1];
    if(last&&last.year<=state.to){ann.push({x:last.year,y:last.v,xanchor:"left",yanchor:"middle",
      text:" "+country.replace("United States","U.S."),showarrow:false,font:{color:col,size:12,family:FONT}});}
  });
  const layout=baseLayout();
  layout.yaxis.title={text:ind.ytitle,font:{size:12.5,family:FONT,color:SUB}};
  layout.xaxis.range=[state.from,state.to];
  layout.xaxis.title={text:"Year",font:{size:12,family:FONT,color:SUB}};
  layout.annotations=[{x:HISTLAST,y:1,yref:"paper",yanchor:"bottom",text:"Climate-model projections begin",
    showarrow:false,font:{size:10.5,color:"#999",family:FONT},xanchor:"left"}].concat(ann);
  layout.shapes=[{type:"line",x0:HISTLAST,x1:HISTLAST,y0:0,y1:1,yref:"paper",
    line:{color:"#bbb",width:1,dash:"dot"}}];
  layout.title={text:"<b>"+ind.title+"</b><br><span style='font-size:12px;color:#555'>"+ind.desc+"  China (red) vs United States (blue)</span>",
    font:{family:'Source Serif 4, Georgia, serif',size:17,color:INK},x:0.01,xanchor:"left",y:0.97};
  layout.margin.t=64;
  Plotly.react("climate-chart",traces,layout,{displayModeBar:false,responsive:true});
  // side panel
  document.getElementById("ind-title").textContent=ind.title;
  document.getElementById("ind-desc").textContent=ind.desc;
  document.getElementById("ind-finding").textContent=ind.finding;
  document.getElementById("p-scen").textContent=SCEN[state.scenario].phys+" ("+SCEN[state.scenario].label+")";
  updateClimateKeyNumbers();
}

/* live per-country end-of-century readout (details on demand) */
function updateClimateKeyNumbers(){
  const ind=INDIC[state.indicator];const host=document.getElementById("keynums");host.innerHTML="";
  const ssp=SCEN[state.scenario].phys;
  host.innerHTML='<div class="kn-head">End-of-century projection &middot; '+ssp+'</div>';
  selectedCountries().forEach(country=>{
    const {proj}=physSeries(country,state.indicator,state.scenario);
    const last=proj[proj.length-1];if(!last)return;
    const row=document.createElement("div");row.className="knrow";
    row.innerHTML='<span class="kndot" style="background:'+COL[country]+'"></span>'+
      '<div class="kncol">'+
        '<div class="knlab">'+country.replace("United States","U.S.")+' in '+last.year+'</div>'+
        '<div class="knval">'+ind.fmt(last.v)+'</div>'+
        '<div class="knrange">likely range '+ind.fmt(last.lo)+' to '+ind.fmt(last.hi)+'</div>'+
      '</div>';
    host.appendChild(row);
  });
}

/* ============ interactive tipping-point explainer ============ */
let tipIndex=0;
function buildTipSelect(){
  const sel=document.getElementById("tip-select");sel.innerHTML="";
  TIP.forEach((r,i)=>{const o=document.createElement("option");o.value=i;o.textContent=r.tipping_element;sel.appendChild(o);});
  sel.value=tipIndex;
}
function tipRisk(w,lo,ce,hi){
  if(w<lo)  return {pct:0,  color:"#2A4D69",status:"Below estimated threshold range",lead:"If this threshold is crossed:"};
  if(w>=hi) return {pct:100,color:"#B23A2E",status:"Above estimated range — crossing likely",lead:"Likely impact:"};
  const pct=Math.round((w-lo)/(hi-lo)*100);
  if(w<ce)  return {pct,color:"#E69F00",status:"Entering threshold range — risk rising",lead:"Potential impact:"};
  return {pct,color:"#C0552E",status:"Within likely threshold range",lead:"Potential impact:"};
}
function setTipWarming(v){
  document.getElementById("tip-warming").value=v;
  document.getElementById("tip-warming-val").textContent=(+v).toFixed(1)+" °C";
  updateTipDetail();
}
function updateTipScenNote(){
  const sc=SCEN[state.scenario];
  document.getElementById("tip-scennote").innerHTML=
    "The selected scenario ("+sc.phys+") reaches about <b>"+sc.gw.toFixed(1)+" °C</b> of global mean warming by 2100 (IPCC AR6). Drag to explore other levels.";
}
function updateTipDetail(){
  const r=TIP[tipIndex];if(!r)return;
  const lo=+r.lower_warming_level,ce=+r.central_warming_level,hi=+r.upper_warming_level;
  const w=+document.getElementById("tip-warming").value;
  const rk=tipRisk(w,lo,ce,hi);
  const st=document.getElementById("tip-status");
  st.textContent=rk.status+" · "+rk.pct+"%";st.style.background=rk.color;
  const mf=document.getElementById("tip-meter-fill");mf.style.width=rk.pct+"%";mf.style.background=rk.color;
  document.getElementById("tip-consequence").innerHTML="<b>"+rk.lead+"</b> "+r.consequence+
    " (central estimate "+ce.toFixed(1)+" °C; estimated range "+lo.toFixed(1)+"–"+hi.toFixed(1)+" °C).";
  document.getElementById("tip-source").textContent=r.source+" · confidence: "+r.confidence;
  const rel=document.getElementById("tip-relevance-text");if(rel)rel.textContent=r.relevance||"";
  renderTipRuler(r,lo,ce,hi,w,rk.color);
}
function renderTipRuler(r,lo,ce,hi,w,color){
  const band={y:["x"],x:[hi-lo],base:[lo],orientation:"h",type:"bar",width:[0.5],
    marker:{color:hexA(MUTED,0.5),line:{color:MUTED,width:1}},
    hovertemplate:"Estimated threshold range: "+lo.toFixed(1)+"–"+hi.toFixed(1)+" °C<extra></extra>",showlegend:false};
  const central={y:["x"],x:[ce],type:"scatter",mode:"markers",
    marker:{symbol:"line-ns-open",size:28,color:INK,line:{width:2}},
    hovertemplate:"Central estimate: "+ce.toFixed(1)+" °C<extra></extra>",showlegend:false};
  const marker={y:["x"],x:[w],type:"scatter",mode:"markers+text",
    marker:{symbol:"diamond",size:15,color:color,line:{color:"#fff",width:1.5}},
    text:["  "+w.toFixed(1)+" °C"],textposition:"top center",textfont:{family:FONT,size:12,color:color},
    hovertemplate:"Selected warming: "+w.toFixed(1)+" °C<extra></extra>",showlegend:false};
  const layout=baseLayout();
  layout.height=150;layout.margin={l:14,r:18,t:28,b:36};layout.showlegend=false;
  layout.title={text:"<b>"+r.tipping_element+"</b>",font:{family:'Source Serif 4, Georgia, serif',size:14,color:INK},x:0,xanchor:"left",y:0.98};
  layout.xaxis={range:[1,4.5],tickvals:[1,1.5,2,3,4],ticktext:["1°","1.5°","2°","3°","4°"],
    gridcolor:"rgba(0,0,0,0)",zeroline:false,showline:true,linecolor:GRID,ticks:"outside",tickcolor:GRID,
    title:{text:"Global warming above pre-industrial (°C)",font:{size:11,family:FONT,color:SUB}},
    tickfont:{family:FONT,size:11,color:INK}};
  layout.yaxis={visible:false,range:[-0.6,0.7]};
  layout.shapes=[1.5,2,3,4].map(v=>({type:"line",x0:v,x1:v,y0:0,y1:1,yref:"paper",line:{color:"#ddd",width:1,dash:"dot"}}));
  Plotly.react("tip-ruler",[band,central,marker],layout,{displayModeBar:false,responsive:true});
}

/* ============ transition chart ============ */
function transSeries(country,scenName){
  return TRANS.filter(r=>r.country===country&&r.scenario===scenName)
    .map(r=>({year:+r.year,e:+r.emissions_mtco2e,inv:+r.investment_usd_billion,cp:+r.carbon_price_usd}))
    .sort((a,b)=>a.year-b.year);
}
function updateTransitionChart(){
  const traces=[];const selName=SCEN[state.scenario].trans;
  const others=["Current Policies","Delayed Transition","Net Zero 2050"].filter(s=>s!==selName);
  selectedCountries().forEach(country=>{
    const col=COL[country];
    others.forEach(s=>{const d=transSeries(country,s);
      traces.push({x:d.map(p=>p.year),y:d.map(p=>p.e),mode:"lines",
        line:{color:hexA(col,0.28),width:1.3},name:country+" · "+s,showlegend:false,
        hovertemplate:"<b>%{x}</b> "+country+" · "+s+"<br>%{y:,} MtCO₂e<extra></extra>"});});
    const d=transSeries(country,selName);
    traces.push({x:d.map(p=>p.year),y:d.map(p=>p.e),mode:"lines+markers",
      line:{color:col,width:2.6},marker:{symbol:SYM[country],size:5,color:col},
      name:country+" · "+selName,
      customdata:d.map(p=>[country,selName,p.inv,p.cp]),
      hovertemplate:"<b>%{customdata[0]}</b> · %{x}<br>%{customdata[1]}<br>Emissions: %{y:,} MtCO₂e<br>Investment: $%{customdata[2]}bn/yr<br>Carbon price: $%{customdata[3]}/t<extra></extra>"});
    const last=d[d.length-1];
    if(last){traces.push({x:[last.year],y:[last.e],mode:"text",text:[" "+country.replace("United States","U.S.")],
      textposition:"middle right",textfont:{color:col,size:12,family:FONT},showlegend:false,hoverinfo:"skip"});}
  });
  const layout=baseLayout();
  layout.xaxis.range=[2020,2052];layout.xaxis.title={text:"Year",font:{size:12,family:FONT,color:SUB}};
  layout.yaxis.title={text:"Annual emissions (MtCO₂e)",font:{size:12.5,family:FONT,color:SUB}};
  layout.yaxis.rangemode="tozero";
  layout.title={text:"<b>Emissions pathways — "+selName+"</b><br><span style='font-size:12px;color:#555'>Bold line = selected scenario; faint lines = other scenarios. China (red) vs United States (blue)</span>",
    font:{family:'Source Serif 4, Georgia, serif',size:17,color:INK},x:0.01,xanchor:"left",y:0.97};
  layout.margin.t=64;
  Plotly.react("transition-chart",traces,layout,{displayModeBar:false,responsive:true});
}

/* ============ abatement options + cards ============ */
function buildOpts(){
  const opts=[...new Set(ABATE.map(r=>r.option))];
  const host=document.getElementById("opts");host.innerHTML="";
  opts.forEach(opt=>{
    const row=ABATE.find(r=>r.option===opt);
    const div=document.createElement("div");div.className="opt-row";
    div.innerHTML='<label><input type="checkbox" data-opt="'+opt+'"><span><span class="o-name">'+opt+'</span>'+
      '<div class="o-meta">'+row.sector+' · confidence: '+row.confidence+'</div></span></label>';
    host.appendChild(div);
    const cb=div.querySelector("input");
    cb.addEventListener("change",()=>{ if(cb.checked)abateSel.add(opt);else abateSel.delete(opt);
      div.classList.toggle("sel",cb.checked);updateCards();});
  });
  updateCards();
}
function updateCards(){
  const cs=selectedCountries();
  let inv=0,ann=0,cum=0;
  ABATE.forEach(r=>{if(abateSel.has(r.option)&&cs.includes(r.country)){
    inv+=+r.estimated_investment_usd_billion;ann+=+r.estimated_annual_abatement_mtco2e;
    cum+=+r.cumulative_abatement_2050_mtco2e;}});
  const selName=SCEN[state.scenario].trans;
  let base2050=0;cs.forEach(c=>{const d=transSeries(c,selName);const last=d.find(p=>p.year===2050)||d[d.length-1];if(last)base2050+=last.e;});
  const rem=Math.max(0,base2050-ann);
  const f=n=>n.toLocaleString(undefined,{maximumFractionDigits:0});
  document.getElementById("card-inv").textContent="$"+f(inv);
  document.getElementById("card-ann").textContent=f(ann);
  document.getElementById("card-cum").textContent=f(cum);
  document.getElementById("card-rem").textContent=f(rem);
  updateTransDetail();
}

/* live per-country 2050 emissions & carbon price under the selected scenario */
function updateTransDetail(){
  const host=document.getElementById("trans-detail");if(!host)return;host.innerHTML="";
  const selName=SCEN[state.scenario].trans;
  host.innerHTML='<div class="kn-head">Projected 2050 outcome &middot; '+selName+'</div>';
  selectedCountries().forEach(country=>{
    const d=transSeries(country,selName);const last=d.find(p=>p.year===2050)||d[d.length-1];if(!last)return;
    const row=document.createElement("div");row.className="knrow";
    row.innerHTML='<span class="kndot" style="background:'+COL[country]+'"></span>'+
      '<div class="kncol">'+
        '<div class="knlab">'+country.replace("United States","U.S.")+' in 2050</div>'+
        '<div><span class="knval">'+last.e.toLocaleString()+'</span> <span class="knunit">MtCO&#8322;e per year (emissions)</span></div>'+
        '<div class="knrange">carbon price $'+last.cp+' per tonne CO&#8322;</div>'+
      '</div>';
    host.appendChild(row);
  });
}

/* ============ shared layout / color ============ */
function baseLayout(){
  return {paper_bgcolor:BG,plot_bgcolor:"#fff",font:{family:FONT,color:INK,size:12},
    margin:{l:62,r:24,t:30,b:44},hovermode:"closest",hoverlabel:{bgcolor:"#fff",bordercolor:GRID,font:{family:FONT,size:12}},
    legend:{orientation:"h",y:-0.18,x:0,font:{size:11,family:FONT}},showlegend:true,
    xaxis:{gridcolor:"rgba(0,0,0,0)",zeroline:false,tickfont:{family:FONT,size:11,color:INK},showline:true,linecolor:GRID,ticks:"outside",tickcolor:GRID},
    yaxis:{gridcolor:GRID,zeroline:false,tickfont:{family:FONT,size:11,color:INK}}};
}
function hexA(hex,a){const n=parseInt(hex.slice(1),16);return"rgba("+((n>>16)&255)+","+((n>>8)&255)+","+(n&255)+","+a+")";}

/* ============ view switching ============ */
function setView(v){
  state.view=v;
  document.getElementById("climate-view").classList.toggle("hidden",v!=="climate");
  document.getElementById("transition-view").classList.toggle("hidden",v!=="transition");
  document.getElementById("tab-climate").setAttribute("aria-selected",v==="climate");
  document.getElementById("tab-transition").setAttribute("aria-selected",v==="transition");
  // indicator + time controls only apply to climate view
  document.getElementById("indicator-group").style.opacity=(v==="climate")?"1":"0.4";
  document.getElementById("time-group").style.opacity=(v==="climate")?"1":"0.4";
  if(v==="climate"){updateClimateChart();updateTipDetail();}
  else{updateTransitionChart();updateCards();}
}

/* ============ wiring ============ */
function syncTimeReadout(){document.getElementById("time-readout").textContent="("+state.from+"–"+state.to+")";}
function wire(){
  document.getElementById("c-china").addEventListener("change",e=>onCountry("China",e.target));
  document.getElementById("c-us").addEventListener("change",e=>onCountry("United States",e.target));
  document.querySelectorAll('input[name="indicator"]').forEach(r=>r.addEventListener("change",e=>{
    state.indicator=e.target.value;updateClimateChart();}));
  document.querySelectorAll('input[name="scenario"]').forEach(r=>r.addEventListener("change",e=>{
    state.scenario=e.target.value;refreshAll();
    updateTipScenNote();setTipWarming(SCEN[state.scenario].gw);}));
  document.getElementById("tip-select").addEventListener("change",e=>{tipIndex=+e.target.value;updateTipDetail();});
  document.getElementById("tip-warming").addEventListener("input",e=>{
    document.getElementById("tip-warming-val").textContent=(+e.target.value).toFixed(1)+" °C";updateTipDetail();});
  document.getElementById("tab-climate").addEventListener("click",()=>setView("climate"));
  document.getElementById("tab-transition").addEventListener("click",()=>setView("transition"));
  document.getElementById("reset").addEventListener("click",resetView);
  const tf=document.getElementById("t-from"),tt=document.getElementById("t-to");
  tf.addEventListener("input",()=>{state.from=Math.min(+tf.value,+tt.value-5);tf.value=state.from;syncTimeReadout();updateClimateChart();});
  tt.addEventListener("input",()=>{state.to=Math.max(+tt.value,+tf.value+5);tt.value=state.to;syncTimeReadout();updateClimateChart();});
}
function onCountry(country,el){
  if(!el.checked && selectedCountries().length===1){el.checked=true;return;} // keep >=1
  state.countries[country]=el.checked;refreshAll();
}
function refreshAll(){
  if(state.view==="climate"){updateClimateChart();updateTipDetail();}
  else{updateTransitionChart();updateCards();}
}
function resetView(){
  state=JSON.parse(JSON.stringify(DEFAULTS));abateSel=new Set();
  document.getElementById("c-china").checked=true;document.getElementById("c-us").checked=true;
  document.querySelector('input[name="indicator"][value="temp_anomaly"]').checked=true;
  document.querySelector('input[name="scenario"][value="intermediate"]').checked=true;
  document.getElementById("t-from").value=1990;document.getElementById("t-to").value=2100;
  document.querySelectorAll('#opts input').forEach(cb=>{cb.checked=false;cb.closest(".opt-row").classList.remove("sel");});
  tipIndex=0;document.getElementById("tip-select").value=0;
  updateTipScenNote();setTipWarming(SCEN[state.scenario].gw);
  syncTimeReadout();setView("climate");
}

/* ============ init ============ */
(async function(){
  try{
    await loadData();
  }catch(e){
    document.querySelector(".wrap").insertAdjacentHTML("beforeend",
      '<p style="color:#B23A2E;font-size:14px;margin-top:18px">Could not load data files. '+
      'Open this page through a web server (e.g. GitHub Pages or <code>python -m http.server</code>), not as a local file. '+
      'Details: '+e.message+'</p>');
    return;
  }
  buildOpts();
  buildTipSelect();
  wire();
  resetView();   // force deterministic default state (ignore any browser-restored control values)
})();
