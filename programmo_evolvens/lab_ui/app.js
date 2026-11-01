const $ = id => document.getElementById(id);
let lang = localStorage.getItem('pe-lab-language') || 'ru', paused = false, state = null, selected = null;
const words = {
ru:{laboratory:'ЛАБОРАТОРИЯ',connecting:'Подключение',eyebrow:'НАБЛЮДЕНИЕ / WSL2',title:'Жизнь начинается со среды.',subtitle:'Реальные запуски, ресурсы и границы программного мира.',pause:'Приостановить просмотр',resume:'Продолжить просмотр',world:'СОСТОЯНИЕ МИРА',cpuCap:'Лимит: 100% одного ядра',memory:'ПАМЯТЬ / WORKER',memoryCap:'Лимит: 256 MiB · swap 0',tasks:'ПРОЦЕССЫ И ПОТОКИ',tasksCap:'Лимит: 64 · запуск последовательно',resources:'Ресурсы мира',resourceSubtitle:'Внешние измерения cgroup v2 · обновление каждые 2 секунды',live:'В реальном времени',memoryMib:'Память MiB',chartScale:'Шкалы: 100% / 256 MiB',chartStart:'Последние 3 минуты наблюдения',chartEnd:'Сейчас',development:'Путь к организму',environment:'Ограниченный мир',genome:'Геном → структура',genomeState:'Следующий этап · ещё не реализован',function:'Структура → функция',functionState:'После проверяемого развития',honesty:'Клетки и поколения появятся здесь вместе с их реальными событиями.',boundary:'Приёмка границ W0',journal:'Журнал запусков',journalSubtitle:'Выберите строку, чтобы увидеть исходное событие и хеши.',probe:'Проба',result:'Результат',duration:'Время',peak:'Пик памяти',started:'Начало',empty:'Запусков пока нет.',raw:'Исходное событие',footer:'Локальная лаборатория · ограниченные опыты в W0',connected:'Источник подключён',offline:'Источник недоступен',idle:'Простаивает',running:'Идёт проба',accepted:'Проверено · текущий профиль',notAccepted:'Требуется приёмка текущего профиля',noJob:'Нет активного запуска',expected:'Ожидаемая остановка',passed:'Успешно',interrupted:'Прерван',paused:'Просмотр приостановлен',search:'Поиск по ID или пробе…',updated:'Обновлено',noData:'Ожидание измерений',noEvidence:'На этом ПК ещё нет применимого отчёта',fail:'Ошибка пробы'},
en:{laboratory:'LABORATORY',connecting:'Connecting',eyebrow:'OBSERVATION / WSL2',title:'Life begins with an environment.',subtitle:'Actual runs, resources and boundaries of a software world.',pause:'Pause observation',resume:'Resume observation',world:'WORLD STATE',cpuCap:'Limit: 100% of one CPU core',memory:'MEMORY / WORKER',memoryCap:'Limit: 256 MiB · no swap',tasks:'PROCESSES & THREADS',tasksCap:'Limit: 64 · serial execution',resources:'World resources',resourceSubtitle:'External cgroup v2 measurements · refresh every 2 seconds',live:'Live telemetry',memoryMib:'Memory MiB',chartScale:'Scales: 100% / 256 MiB',chartStart:'Last 3 minutes of observation',chartEnd:'Now',development:'Toward an organism',environment:'Bounded world',genome:'Genome → structure',genomeState:'Next stage · not implemented yet',function:'Structure → function',functionState:'After verifiable development',honesty:'Cells and generations will appear alongside their actual events.',boundary:'W0 boundary acceptance',journal:'Run journal',journalSubtitle:'Select a row to inspect the source event and hashes.',probe:'Probe',result:'Outcome',duration:'Elapsed',peak:'Peak memory',started:'Started',empty:'No runs yet.',raw:'Source event',footer:'Local laboratory · bounded W0 experiments',connected:'Source connected',offline:'Source unavailable',idle:'Idle',running:'Probe running',accepted:'Verified · current profile',notAccepted:'Current profile needs acceptance',noJob:'No active run',expected:'Expected stop',passed:'Passed',interrupted:'Interrupted',paused:'Observation paused',search:'Search ID or probe…',updated:'Updated',noData:'Waiting for measurements',noEvidence:'No applicable report on this computer yet',fail:'Probe failed'}
};
const names = {memory:['Память','Memory'], output:['Вывод','Output'],line:['Длинная строка','Long line'],protocol:['Протокол','Protocol'],hang:['Зависание','Hang'],'closed-pipes':['Закрытые каналы','Closed channels'],permissions:['Полномочия','Permissions'],inspect:['Видимость','Visibility'],cpu:['CPU','CPU'],deadline:['Таймер','Deadline'],pids:['Лимит задач','Task limit'],'controller-death-and-concurrency':['Смерть контроллера / параллельность','Controller death / concurrency'],recovery:['Восстановление','Recovery'],smoke:['Пробный запуск','Smoke']};
Object.assign(words.ru,{structuralTitle:'Развитие из генома',structuralSubtitle:'Фактическая структура и происхождение изменений последнего эксперимента',noDevelopment:'Эксперимент развития ещё не запускался.',developmentEvents:'События развития · выбрать для просмотра происхождения',prescribed:'Предписанное развитие подтверждено',experimentPending:'Эксперимент выполняется',cellsLabel:'Клетки',linksLabel:'Связи',rulesLabel:'Сработавшие правила',outputLabel:'Результат',memoryLabel:'Локальная память',stepsLabel:'Шаги',limitedFunction:'Проверен ограниченный пример: текст и память',developmentNote:'Предписанная структура проверена. Поиск, усвоение и эволюция ещё впереди.',developmentProbe:'Развитие из генома'});
Object.assign(words.en,{structuralTitle:'Genome-driven development',structuralSubtitle:'Actual structure and change provenance from the latest experiment',noDevelopment:'No development experiment has run yet.',developmentEvents:'Development events · select to inspect provenance',prescribed:'Prescribed development verified',experimentPending:'Experiment running',cellsLabel:'Cells',linksLabel:'Connections',rulesLabel:'Rules fired',outputLabel:'Output',memoryLabel:'Local memory',stepsLabel:'Steps',limitedFunction:'Limited example verified: text and memory',developmentNote:'Prescribed structure verified. Search, assimilation and evolution remain pending.',developmentProbe:'Genome-driven development'});
names.development=['Развитие из генома','Genome-driven development'];
Object.assign(words.ru,{replayFirst:'В начало',replayPrev:'Назад',replayPlay:'▶ Показать развитие',replayPause:'Ⅱ Пауза',replayNext:'Далее',replayLast:'В конец',replayRecord:'Запись выполнения · просмотр не запускает организм',eventLabel:'Событие',checksLabel:'Проверки',durationLabel:'Время опыта',structuralSubtitle:'Посмотрите по шагам, как из исходной клетки появилась работающая структура.'});
Object.assign(words.en,{replayFirst:'Start',replayPrev:'Previous',replayPlay:'▶ Show development',replayPause:'Ⅱ Pause',replayNext:'Next',replayLast:'End',replayRecord:'Recorded execution · viewing does not run the organism',eventLabel:'Event',checksLabel:'Checks',durationLabel:'Experiment time',structuralSubtitle:'Step through how the initial cell became a working structure.'});
Object.assign(words.ru,{organismTitle:'Итоговый экземпляр',organismSubtitle:'Состояние, геном и код именно выполненного экземпляра',organismNote:'Это сохранённый результат опыта. Процесс исполнения завершён.',organismState:'Посмотреть организм',organismGenome:'Геном JSON',organismEngine:'Код исполнителя',organismPrimitives:'Код примитивов',organismDownload:'↓ Скачать паспорт JSON',organismSaved:'Сохранённый экземпляр',inputLabel:'Вход',mechanismsLabel:'Механизмы',sourceMissing:'Исходный пакет этого экземпляра недоступен'});
Object.assign(words.en,{organismTitle:'Resulting instance',organismSubtitle:'State, genome and source of the actual executed instance',organismNote:'Saved experiment result. Its execution process has finished.',organismState:'Inspect organism',organismGenome:'Genome JSON',organismEngine:'Executor source',organismPrimitives:'Primitive source',organismDownload:'↓ Download specimen JSON',organismSaved:'Saved instance',inputLabel:'Input',mechanismsLabel:'Mechanisms',sourceMissing:'Source bundle for this instance is unavailable'});
Object.assign(words.ru,{customLabel:'Проверить другой текст тем же геномом',customSubmit:'Проверить 2 раза',customHelp:'Один заданный геном · два свежих экземпляра · пробелы обрезаются, регистр понижается',customBusy:'Проверка в W0…',customWaiting:'Требуется свободный мир с действующей приёмкой W0.',customExpected:'Эталон',customRepeat:'Два свежих экземпляра совпали',yes:'да',no:'нет'});
Object.assign(words.en,{customLabel:'Test different text with the same genome',customSubmit:'Check twice',customHelp:'One authored genome · two fresh instances · trim whitespace and lowercase',customBusy:'Checking inside W0…',customWaiting:'Requires an idle world with applicable W0 acceptance.',customExpected:'Reference',customRepeat:'Two fresh instances agree',yes:'yes',no:'no'});
let customSubmitting=false,customError='',specimenViewRun=null;
let replayRun=null,replayCursor=0,replayTimer=null,uiVersion=null;
const t = key => words[lang][key] || key;
const name = key => names[key]?.[lang === 'ru' ? 0 : 1] || key || '—';
const bytes = value => (Number(value) / 1048576).toFixed(1) + ' MiB';
function translate(){ document.documentElement.lang=lang;document.querySelectorAll('[data-i]').forEach(el=>el.textContent=t(el.dataset.i));$('language').textContent=lang==='ru'?'EN':'RU';$('search').placeholder=t('search');$('pause').textContent=t(paused?'resume':'pause'); if(state) render(); }
function cell(row,text){ const el=document.createElement('td');el.textContent=text;row.append(el);return el; }
function show(run){ selected=run.id;$('raw').textContent=JSON.stringify(run,null,2);$('source').textContent=run.source;$('details').open=true;renderRuns(); }
function renderRuns(){
 const query=$('search').value.toLowerCase(), rows=(state?.runs||[]).filter(r=>(r.id+' '+r.probe+' '+name(r.probe)+' '+r.outcome).toLowerCase().includes(query));
 $('runs').replaceChildren();$('empty').hidden=rows.length>0;
 for(const run of rows){const row=document.createElement('tr');row.tabIndex=0;row.classList.toggle('selected',run.id===selected);row.addEventListener('click',()=>show(run));row.addEventListener('keydown',e=>{if(e.key==='Enter')show(run)});cell(row,run.id.slice(0,10));cell(row,name(run.probe));const badge=document.createElement('span');let text=run.outcome||'interrupted',style='';if(text==='running'){text=t('running')}else if(text==='passed'){text=t('passed');style='pass'}else if(run.expected_test_pass){text=t('expected');style='pass'}else if(text==='interrupted'){text=t('interrupted')}else {text=t('fail')+' · '+text;style='fail'}badge.textContent=text;badge.className='badge '+style;cell(row,'').append(badge);cell(row,run.elapsed_seconds!=null?run.elapsed_seconds.toFixed(3)+' s':'—');cell(row,run.worker_stats?.['memory.peak']?bytes(run.worker_stats['memory.peak']):'—');cell(row,run.started_unix?new Date(run.started_unix*1000).toLocaleString(lang==='ru'?'ru-RU':'en-GB',{month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'}):'—');$('runs').append(row);}
}
function render(){
 const ok=state.available;$('connection').className='connection '+(ok?'ok':'bad');$('connection').textContent='● '+t(paused?'paused':ok?'connected':'offline');$('error').hidden=ok;$('error').textContent=state.error||'';$('updated').textContent=t('updated')+' '+new Date((state.sample_unix||Date.now()/1000)*1000).toLocaleTimeString();
 $('world').textContent=ok?t(state.active?'running':'idle'):'—';$('run-label').textContent=ok?(state.active_run_id?.slice(0,16)||t('noJob')):'—';$('cpu').textContent=ok&&state.cpu_percent!=null?state.cpu_percent.toFixed(1)+'%':'—';$('memory').textContent=ok?bytes(state.memory_bytes):'—';$('tasks').textContent=ok?state.tasks+' / 64':'—';
 const accepted=ok&&state.acceptance.accepted;$('acceptance-label').textContent=t(accepted?'accepted':'notAccepted');$('w0-step').classList.toggle('done',accepted);const cases=state.acceptance?.cases||[];$('check-count').textContent=accepted?cases.length+' / '+cases.length:'—';$('acceptance-source').textContent=state.acceptance?.source||t('noEvidence');$('checks').replaceChildren();for(const key of Object.keys(names).filter(k=>k!=='smoke'&&k!=='development')){const el=document.createElement('span');const pass=accepted&&cases.includes(key);el.className='check'+(pass?' pass':'');el.textContent=(pass?'✓ ':'○ ')+name(key);$('checks').append(el)}$('kernel').textContent=state.kernel||'WSL2';renderRuns();renderOrganism();renderCustom();renderDevelopment();draw();
}
function renderCustom(){
 const size=new TextEncoder().encode($('custom-text').value).length,job=state?.experiment_job;
 $('custom-size').textContent=size+' / 256 UTF-8 bytes';
 $('custom-submit').disabled=customSubmitting||size>256||!state?.available||!state.acceptance?.accepted||state.active||job?.status==='running';
 if(customError){$('custom-status').textContent=customError;return}
 if(job?.status==='running'||customSubmitting){$('custom-status').textContent=t('customBusy');return}
 if(job?.status==='error'){$('custom-status').textContent=job.error;return}
 if(job?.status==='completed'){const result=job.report.result;$('custom-status').textContent=t('inputLabel')+': '+JSON.stringify(result.input)+' → '+t('outputLabel')+': '+JSON.stringify(result.development.value)+' · '+t('customExpected')+': '+JSON.stringify(result.expected)+' · '+t('customRepeat')+': '+t(result.reproducible?'yes':'no');return}
 $('custom-status').textContent=state?.acceptance?.accepted?'':t('customWaiting');
}
const customDraft=sessionStorage.getItem('pe-custom-draft');if(customDraft!==null)$('custom-text').value=customDraft;
$('custom-text').addEventListener('input',()=>{sessionStorage.setItem('pe-custom-draft',$('custom-text').value);customError='';renderCustom()});
$('custom-form').addEventListener('submit',async event=>{
 event.preventDefault();if($('custom-submit').disabled)return;
 customSubmitting=true;customError='';renderCustom();
 try{const response=await fetch('/api/development',{method:'POST',headers:{'Content-Type':'application/json','X-Lab-Token':state.job_token},body:JSON.stringify({text:$('custom-text').value})});if(response.status!==202)throw Error('HTTP '+response.status);await poll()}catch(error){customError=String(error)}finally{customSubmitting=false;renderCustom()}
});
function renderOrganism(){
 const dev=state?.development,result=dev?.result?.development;
 $('organism-empty').hidden=!!result;$('organism-view').hidden=!result;
 $('organism-id').textContent=result?.genome_id||'';$('organism-status').textContent=result?t('organismSaved'):'—';
 if(!result)return;
 if(specimenViewRun&&specimenViewRun!==dev.run_id){$('organism-code').hidden=true;$('organism-code').textContent='';specimenViewRun=null}
 const input=dev.events.find(event=>event.event==='mechanism_executed')?.nodes?.find(node=>node.pp==='SENSE')?.value;
 const facts=[t('inputLabel')+': '+JSON.stringify(input),t('outputLabel')+': '+JSON.stringify(result.value),t('cellsLabel')+': '+result.cells.length,t('mechanismsLabel')+': '+result.cells.reduce((count,cell)=>count+cell.mechanisms.length,0),t('linksLabel')+': '+result.links.length,'DNA: '+result.genome_sha256.slice(0,16)];
 $('organism-summary').replaceChildren();for(const text of facts){const item=document.createElement('span');item.textContent=text;$('organism-summary').append(item)}
}
async function inspectOrganism(kind){
 const target=$('organism-code');target.hidden=false;
 try{const response=await fetch('/api/organism',{cache:'no-store'});if(!response.ok)throw Error('HTTP '+response.status);const specimen=await response.json();if(!specimen.available)throw Error(specimen.error);specimenViewRun=specimen.run_id;const value=kind==='state'?specimen.organism:kind==='genome'?specimen.genome:specimen.source_code?.[kind]?.text;target.textContent=value==null?t('sourceMissing'):typeof value==='string'?value:JSON.stringify(value,null,2)}catch(error){target.textContent=String(error)}
}
$('organism-state').addEventListener('click',()=>inspectOrganism('state'));
$('organism-genome').addEventListener('click',()=>inspectOrganism('genome'));
$('organism-engine').addEventListener('click',()=>inspectOrganism('development.py'));
$('organism-primitives').addEventListener('click',()=>inspectOrganism('runtime.py'));
function stopReplay(){ if(replayTimer){clearInterval(replayTimer);replayTimer=null} }
function jumpReplay(index){stopReplay();replayCursor=index;renderDevelopment()}
function describeEvent(event){
 if(!event)return '—';
 const ru=lang==='ru',cell=typeof event.cell==='string'?event.cell:event.cell?.id;
 if(event.event==='initial')return ru?'Исходная клетка: механизмов и связей ещё нет.':'Initial cell: no mechanisms or connections yet.';
 if(event.event==='mechanism_expressed')return (ru?'Выражен механизм ':'Mechanism expressed: ')+event.mechanism.id+' · '+event.origin.gene+' / '+event.origin.rule;
 if(event.event==='cell_created')return (ru?'Создана дочерняя клетка ':'Child cell created: ')+cell+' ← '+event.cell.parent+' · '+event.origin.rule;
 if(event.event==='link_created')return (ru?'Создана связь ':'Connection created: ')+event.link.from+'.out → '+event.link.to+'.in · '+event.origin.rule;
 if(event.event==='cell_received')return (ru?'Клетка получила сообщение: ':'Cell received a message: ')+cell+' ← '+event.source;
 if(event.event==='mechanism_executed')return event.mechanism+' · '+event.nodes.map(node=>node.pp).join(' → ')+' · '+(ru?'выход: ':'output: ')+JSON.stringify(event.output);
 if(event.event==='function_checked'){
  const labels={source_unexpressed:['Функция недоступна: у исходной клетки нет механизма.','Function unavailable: the source cell has no mechanism.'],endpoint_missing:['Источник работает, но целевая клетка ещё не создана.','Source operates, but the destination cell does not exist yet.'],endpoint_unexpressed:['Целевая клетка создана, но её механизм ещё не выражен.','Destination cell exists, but its mechanism is not expressed yet.'],disconnected:['Обе клетки существуют. Передачи между ними ещё нет.','Both cells exist. There is no delivery between them yet.'],delivered:['Результат доставлен: ','Result delivered: ']};
  return (labels[event.feedback]?.[ru?0:1]||event.feedback)+(event.delivered?JSON.stringify(event.value):'');
 }
 return event.event+' · '+(event.reason||cell||'');
}
function renderDevelopment(){
 const dev=state?.development,outcome=dev?.result,result=outcome?.development,events=dev?.events||[];
 $('dev-empty').hidden=!!dev;$('dev-view').hidden=!dev;
 $('dev-status').textContent=outcome?.passed?t('prescribed'):dev?(dev.completed?t('fail'):t('experimentPending')):'—';
 if(!dev)return;
 if(replayRun!==dev.run_id){stopReplay();replayRun=dev.run_id;replayCursor=Math.max(0,events.length-1)}
 replayCursor=Math.max(0,Math.min(events.length-1,replayCursor));
 const valid=outcome?.passed&&result?.delivered;
 $('development-step').classList.toggle('done',!!valid);$('function-step').classList.toggle('done',!!valid);
 document.querySelector('[data-i="genomeState"]').textContent=t(valid?'prescribed':'genomeState');
 document.querySelector('[data-i="functionState"]').textContent=t(valid?'limitedFunction':'functionState');
 document.querySelector('[data-i="honesty"]').textContent=t(valid?'developmentNote':'honesty');
 const view=PEDevelopment.frame(events,replayCursor),cells=view.cells,links=view.links,visible=events.slice(0,replayCursor+1);
 $('replay-range').max=Math.max(0,events.length-1);$('replay-range').value=replayCursor;
 $('replay-position').textContent=t('eventLabel')+' '+(events.length?replayCursor+1:0)+' / '+events.length;
 $('replay-play').textContent=t(replayTimer?'replayPause':'replayPlay');
 $('replay-first').disabled=$('replay-prev').disabled=replayCursor<=0;
 $('replay-last').disabled=$('replay-next').disabled=replayCursor>=events.length-1;
 $('replay-caption').textContent=describeEvent(view.event);
 $('dev-facts').replaceChildren();const run=state.runs?.find(run=>run.id===dev.run_id);
 const facts=[t('cellsLabel')+': '+cells.length,t('linksLabel')+': '+links.length,t('rulesLabel')+': '+view.firedRules.length,t('outputLabel')+': '+(view.value??'—')];
 if(outcome?.cases)facts.push(t('checksLabel')+': '+outcome.cases.filter(test=>test.passed).length+' / '+outcome.cases.length);
 if(run?.elapsed_seconds!=null)facts.push(t('durationLabel')+': '+run.elapsed_seconds.toFixed(3)+' s');
 for(const text of facts){const el=document.createElement('span');el.textContent=text;$('dev-facts').append(el)}
 $('cell-graph').replaceChildren();for(const cell of cells){
  const box=document.createElement('article');box.className='cell-card';const title=document.createElement('h3');title.textContent=cell.id;box.append(title);
  const status=document.createElement('span');status.className='mono';status.textContent=(cell.state||'idle')+' / '+(cell.health||'ok');box.append(status);
  for(const mech of cell.mechanisms||[]){const line=document.createElement('p');line.textContent=mech.id;const execution=visible.findLast(event=>event.event==='mechanism_executed'&&event.mechanism===mech.id);const ops=document.createElement('small');ops.textContent=execution?.nodes?.map(node=>node.pp).join(' → ')||mech.gene;line.append(ops);box.append(line)}
  const memory=document.createElement('div');memory.className='cell-memory';memory.textContent=t('memoryLabel')+': '+JSON.stringify(cell.memory||{});box.append(memory);
  const budget=document.createElement('div');budget.className='mono';budget.textContent=t('stepsLabel')+': '+(cell.used_steps??0)+' / '+cell.budget;box.append(budget);$('cell-graph').append(box);
 }
 $('cell-links').replaceChildren();for(const link of links){const el=document.createElement('div');el.textContent=link.from+'.'+link.from_port+' → '+link.to+'.'+link.to_port+'  · '+link.origin.rule;$('cell-links').append(el)}
 $('dev-events').replaceChildren();for(const event of events){const button=document.createElement('button');button.classList.toggle('current',event.seq===view.event?.seq);button.textContent=event.tick+' · '+event.event+(typeof event.cell==='string'?' · '+event.cell:'');button.addEventListener('click',()=>{jumpReplay(events.indexOf(event));$('raw').textContent=JSON.stringify(event,null,2);$('source').textContent=dev.source+' #'+event.seq;$('details').open=true});$('dev-events').append(button)}
}
$('replay-first').addEventListener('click',()=>jumpReplay(0));
$('replay-prev').addEventListener('click',()=>jumpReplay(replayCursor-1));
$('replay-next').addEventListener('click',()=>jumpReplay(replayCursor+1));
$('replay-last').addEventListener('click',()=>jumpReplay((state?.development?.events.length||1)-1));
$('replay-range').addEventListener('input',event=>jumpReplay(Number(event.target.value)));
$('replay-play').addEventListener('click',()=>{
 if(replayTimer){stopReplay();renderDevelopment();return}
 const events=state?.development?.events||[];if(!events.length)return;
 if(replayCursor>=events.length-1)replayCursor=0;
 replayTimer=setInterval(()=>{replayCursor++;if(replayCursor>=events.length-1)stopReplay();renderDevelopment()},1200);
 renderDevelopment();
});
function draw(){ const canvas=$('chart'),rect=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;canvas.width=rect.width*dpr;canvas.height=180*dpr;const ctx=canvas.getContext('2d');ctx.scale(dpr,dpr);const w=rect.width,h=180;ctx.lineWidth=1;ctx.font='10px Consolas,monospace';for(let i=0;i<=4;i++){const y=10+i*38;ctx.strokeStyle='#2b383f';ctx.beginPath();ctx.moveTo(30,y);ctx.lineTo(w,y);ctx.stroke();ctx.fillStyle='#91a1aa';ctx.fillText(String(100-i*25),0,y+3)}const data=state?.history||[];if(data.length<2){ctx.fillStyle='#91a1aa';ctx.fillText(t('noData'),45,90);return}const latest=data.at(-1).time;for(const [key,max,color]of[['cpu',100,'#7bdbe6'],['memory',268435456,'#c8e88d']]){ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=2;let drawing=false;data.forEach((point,i)=>{if(point[key]==null){drawing=false;return}const x=30+(w-30)*(1-(latest-point.time)/180),y=162-Math.min(1,point[key]/max)*152;if(!drawing){ctx.moveTo(x,y);drawing=true}else ctx.lineTo(x,y)});ctx.stroke()}}
async function poll(){if(!paused){try{const response=await fetch('/api/state',{cache:'no-store'});if(!response.ok)throw Error('HTTP '+response.status);const incoming=await response.json();if(uiVersion&&incoming.ui_version&&uiVersion!==incoming.ui_version){location.reload();return}uiVersion=incoming.ui_version;state=incoming;render()}catch(error){state={available:false,error:String(error),history:state?.history||[]};render()}}}
$('language').addEventListener('click',()=>{lang=lang==='ru'?'en':'ru';localStorage.setItem('pe-lab-language',lang);translate()});$('pause').addEventListener('click',()=>{paused=!paused;translate();if(!paused)poll()});$('search').addEventListener('input',renderRuns);new ResizeObserver(()=>{if(state)draw()}).observe($('chart'));translate();poll();setInterval(poll,2000);
