const fs=require('fs'),path=require('path'),pptxgen=require('pptxgenjs');
const root=path.resolve(__dirname,'..');
const plan=JSON.parse(fs.readFileSync(path.join(root,'content/slide_plan.json'),'utf8'));
const sourceList=JSON.parse(fs.readFileSync(path.join(root,'sources/verified_sources.json'),'utf8')).sources;
const sources=Object.fromEntries(sourceList.map(s=>[s.id,s]));
const W=13.333333,H=7.5,FONT='Noto Sans CJK SC';
const C={bg:'0C1424',panel:'152238',panel2:'192C43',text:'F0F5FC',muted:'AABAD1',line:'34506B',cyan:'65D9F4',green:'9DE2BC',gold:'F5C879',purple:'B6AEFF',red:'F3A7A0'};
const geom=[];
function tx(s,v,x,y,w,h,size=18,color=C.text,bold=false,opt={}){
 const o={x,y,w,h,fontFace:FONT,fontSize:size,color,bold,margin:0,breakLine:false,valign:'mid',...opt};
 s.addText(String(v),o);geom.push({slide:s._talkId,type:'text',text:String(v),x,y,w,h,fontSize:size});
}
function rect(s,x,y,w,h,fill=C.panel,line=fill){s.addShape('rect',{x,y,w,h,fill:{color:fill},line:{color:line,width:.8}});geom.push({slide:s._talkId,type:'shape',x,y,w,h});}
function ln(s,x1,y1,x2,y2,color=C.cyan,arrow=true,dash=false){
 s.addShape('line',{x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.abs(x2-x1),h:Math.abs(y2-y1),flipH:x2<x1,flipV:y2<y1,line:{color,width:1.5,beginArrowType:'none',endArrowType:arrow?'triangle':'none',...(dash?{dashType:'dash'}:{})}});
}
function box(s,title,sub,x,y,w,h,color=C.cyan){rect(s,x,y,w,h);rect(s,x,y,.045,h,color);tx(s,title,x+.2,y+.13,w-.4,.45,20,color,true);if(sub)tx(s,sub,x+.2,y+.63,w-.4,h-.70,h<1.4?13:16,C.muted,false,{valign:'top',paraSpaceAfterPt:6});}
function pill(s,title,x,y,w,color=C.cyan){rect(s,x,y,w,.43,C.panel2);tx(s,title,x+.13,y+.04,w-.26,.34,12,color,true);}
function strip(s,v){rect(s,.65,5.99,12.03,.56,C.panel2);tx(s,v,.85,6.08,11.62,.36,15,C.green);}
function base(p,o){let s=p.addSlide();s._talkId=o.id;s.background={color:C.bg};rect(s,.65,.40,.34,.045,C.cyan);tx(s,o.label,1.10,.29,10.7,.25,10,C.muted,true);tx(s,o.title,.65,.86,12.05,.68,29,C.text,true);tx(s,o.main,.67,1.67,12,.49,20,C.cyan,true);
 tx(s,o.detail,.68,6.66,11.8,.24,9,C.muted);
 const ss=o.sources;let x=.68,y=7.06;ss.forEach((id,i)=>{const src=sources[id];const label=id+' '+({'S10':'Codex loop','S11':'工具策略','S04':'DSH 架构','S16':'AgentLoop','S19':'会话投影','S21':'工具 guard','S13':'Checkpoint','S18':'Store','S12':'StateGraph','S17':'Conversation','S14':'Agent.step','S20':'DGM loop','S08':'DGM 论文','S15':'DGM README','S02':'Codex harness','S01':'Codex platform','S03':'DSH 官网','S05':'Persistence','S06':'上下文工程','S07':'SDK 架构','S09':'Skills','S22':'Agents 定义'}[id]||'来源');
 const width=Math.min(2.0,.18+label.length*.068);if(x+width>11.8){x=.68;y-=.26;}
 tx(s,label,x,y,width,.20,7.5,C.muted,false,{hyperlink:{url:src.url,tooltip:src.name}});x+=width+.13;
 });
 tx(s,String(o.id).padStart(2,'0')+' / '+plan.slides.length,12.05,7.01,.62,.24,9,C.muted,false,{align:'right'});
 const notes=[o.notes,'','过渡问题：'+o.transition,'','结论：'+o.main,'证据类型：'+o.label,'Claims：'+o.claims.join(', '),'','来源（2026-10-23 核查；源码只静态阅读）：',...ss.map(id=>`${id} ${sources[id].name}\n${sources[id].url}\n定位：${sources[id].locator}`)].join('\n');s.addNotes(notes);return s;}
function cards(s,o){const arr=o.cards,gap=.22,w=(12.03-gap*(arr.length-1))/arr.length;arr.forEach((a,i)=>{let x=.65+i*(w+gap);rect(s,x,2.70,w,2.68);tx(s,String(i+1).padStart(2,'0'),x+.22,2.91,.6,.39,14,C.muted);tx(s,a[0],x+.22,3.52,w-.44,.58,arr.length===4?20:22,[C.cyan,C.green,C.gold,C.purple][i],true);tx(s,a[1],x+.22,4.25,w-.44,.45,17,C.text);if(a[2])tx(s,a[2],x+.22,4.82,w-.44,.33,13,C.muted);});}
function steps(s,o,loop=false){let arr=o.steps,n=arr.length,g=.24,w=(12.03-g*(n-1))/n;arr.forEach((a,i)=>{const x=.65+i*(w+g);rect(s,x,3.02,w,1.46);tx(s,String(i+1).padStart(2,'0'),x+.15,3.16,w-.3,.26,10,C.muted);tx(s,a,x+.12,3.56,w-.24,.65,n>4?17:20,[C.cyan,C.green,C.gold,C.purple,C.cyan,C.green][i],true,{align:'center'});if(i<n-1)ln(s,x+w+.035,3.77,x+w+g-.035,3.77);});if(loop){ln(s,11.2,4.55,11.2,5.12,C.muted,false);ln(s,11.2,5.12,2.05,5.12,C.muted,false);ln(s,2.05,5.12,2.05,4.55,C.muted,true);tx(s,'反馈进入后续请求；完成、受阻或预算到达时停止',3.0,5.23,7.5,.29,13,C.muted,false,{align:'center'});}}
function rows(s,o){const reading=o.kind==='reading',arr=o.rows;const widths=reading?[2.05,9.98]:[2.15,4.5,5.38];let y=2.61;arr.forEach((a,i)=>{rect(s,.65,y,12.03,.66,i%2?C.panel:C.panel2);let x=.65;a.forEach((v,j)=>{tx(s,v,x+.18,y+.1,widths[j]-.36,.45,j===0?17:16,j===0?C.cyan:C.text,j===0);x+=widths[j];});y+=.77;});}
function render(p,o){const s=base(p,o);
 if(o.kind==='cover'){
  rect(s,.65,2.54,8.0,2.81,C.panel);tx(s,'从一份 PPT 开始',.94,2.87,7.3,.6,30,C.text,true);tx(s,o.tagline,.96,3.74,7.2,.75,19,C.cyan,true);tx(s,'官方资料与源码 · 一个贯穿案例 · 三个开放问题',.96,4.64,7.2,.32,14,C.muted);
  rect(s,9.03,2.54,3.65,2.81,C.panel2);tx(s,'23',9.28,2.81,2.95,1.12,60,C.green,true);tx(s,'页交流素材',9.31,4.05,2.95,.4,19,C.text);tx(s,'约 43 分钟 + 20 分钟讨论',9.31,4.69,3,.31,12,C.muted);
  tx(s,'先看一次完整交付，再讨论系统为什么能持续做事。',.75,5.98,11.8,.5,20,C.muted);
 }else if(['cards','failures','triad','memoryfix','validation','levels','discussion'].includes(o.kind)){cards(s,o);}
 else if(['pipeline','context','dgm'].includes(o.kind)){steps(s,o);if(o.kind==='dgm'){tx(s,'多分支探索，不是每一代只保留一个冠军',2.3,5.02,8.8,.38,16,C.muted,false,{align:'center'});}}
 else if(o.kind==='loop')steps(s,o,true);
 else if(['comparison','reading','eval'].includes(o.kind))rows(s,o);
 else if(o.kind==='harness'){
  rect(s,.65,2.53,9.12,3.05,C.panel2);pill(s,'HARNESS · 运行边界',.85,2.70,3.05);
  box(s,'Agent Loop','模型决策 ↔ 工具反馈',.87,3.41,3.85,1.0);box(s,'工具 / 权限','执行政策 · 沙箱 · 错误返回',5.04,3.41,4.49,1.0,C.green);ln(s,4.75,3.92,4.99,3.92);
  tx(s,'会话与日志     上下文管理     任务状态',1.05,4.86,8.12,.37,19,C.muted,false,{align:'center'});
  box(s,'应用验收','来源核查\n结构校验\n渲染目检',10.06,2.53,2.62,3.05,C.gold);
  ln(s,9.80,4.1,10.02,4.1,C.gold);
 }else if(o.kind==='codex'){
  pill(s,'客户端 / App Server · 线程、轮次、事件',.65,2.50,8.77);
  box(s,'run_turn','组装请求 / 判断是否继续',.65,3.23,3.58,1.41);box(s,'工具执行编排','审批 / 沙箱 / 错误重试',4.76,3.23,3.78,1.41,C.green);box(s,'执行环境','文件 / Shell / 外部能力',9.07,3.23,3.61,1.41,C.gold);
  ln(s,4.28,3.92,4.70,3.92);ln(s,8.59,3.92,9.01,3.92);
  ln(s,10.9,4.7,10.9,5.26,C.muted,false);ln(s,10.9,5.26,2.3,5.26,C.muted,false);ln(s,2.3,5.26,2.3,4.7,C.muted);
  tx(s,'工具输出 / 错误 → 会话记录 → 后续模型请求',3.0,5.34,7.3,.29,13,C.muted,false,{align:'center'});
 }else if(o.kind==='dsh'){
  rect(s,.65,2.55,12.03,.62,C.panel2);tx(s,'Profile = 有顺序的 bundles + patches',.9,2.69,11.5,.34,19,C.cyan,true,{align:'center'});
  const ns=[['Agent Loop','驱动决策与行动'],['LLM adapter','模型消息与流'],['Tools','注册与执行策略'],['Session','事件日志与投影']];ns.forEach((a,i)=>box(s,a[0],a[1],.65+i*3.08,3.67,2.79,1.18,[C.cyan,C.green,C.gold,C.purple][i]));
  rect(s,.65,5.15,12.03,.44,C.panel2);tx(s,'CORDIS   ·   services  /  events  /  reversible effects',.89,5.22,11.5,.28,14,C.muted,false,{align:'center'});
  ns.forEach((a,i)=>ln(s,2.04+i*3.08,4.88,2.04+i*3.08,5.10,C.muted,false));
 }else if(o.kind==='checkpoint'){
  const xs=[.65,3.86,7.07];[['研究','来源与候选结论'],['核查','已核 / 待核 / 不确定'],['生成','文件路径与待办']].forEach((a,i)=>box(s,a[0],a[1],xs[i],2.69,2.63,1.15,[C.cyan,C.green,C.gold][i]));ln(s,3.32,3.25,3.80,3.25);ln(s,6.53,3.25,7.01,3.25);
  box(s,'恢复','沿 thread_id\n找回保存状态',10.27,2.69,2.41,2.83,C.purple);
  rect(s,.65,4.30,9.05,1.22,C.panel2);tx(s,'Checkpointer · 当前 thread',.87,4.45,8.6,.38,19,C.green,true);tx(s,'保存状态与进度；需要持久后端才能跨进程保留',.87,5.02,8.5,.28,14,C.muted);
  [1.96,5.17,8.38].forEach(x=>ln(s,x,3.88,x,4.24,C.muted));ln(s,9.75,4.92,10.22,4.92,C.green);
 }else if(o.kind==='openhands'){
  box(s,'Agent + Conversation','决策 / 事件 / 会话状态',.65,2.66,4.13,1.24);ln(s,4.82,3.29,5.24,3.29);
  box(s,'LocalWorkspace','本地进程\n工具在本地环境运行',5.3,2.48,7.38,1.37,C.cyan);
  box(s,'RemoteWorkspace','远程 Conversation → Agent Server\nAgent 与工具在远程环境运行',5.3,4.20,7.38,1.37,C.green);
  ln(s,4.91,3.3,4.91,4.89,C.muted,false);ln(s,4.91,4.89,5.24,4.89,C.green);
  tx(s,'工厂按 workspace 类型\n选择实现',.91,4.55,3.57,.73,18,C.muted);
 }else if(o.kind==='memory'){
  box(s,'State → Checkpoint','当前任务：已核结论 / 待办 / 文件位置',.65,2.55,12.03,.95,C.cyan);
  const ns=[['候选','知识 / 经历 / 方法'],['写入筛选','来源 / 范围 / 版本'],['Memory Store','按 namespace 保存'],['检索到 Context','与本轮任务相关']];ns.forEach((a,i)=>{box(s,a[0],a[1],.65+i*3.09,3.94,2.76,1.25,[C.cyan,C.green,C.gold,C.purple][i]);if(i<3)ln(s,3.46+i*3.09,4.57,3.68+i*3.09,4.57);});
  tx(s,'纠错 / 失效 / 复核：更新持久记录，再让后续检索生效',1.0,5.46,11.3,.30,15,C.muted,false,{align:'center'});
 }else if(o.kind==='system'){
  box(s,'Context 组装','目标 + 相关片段 + 当前进度',.65,2.52,3.34,1.15,C.purple);box(s,'Agent Loop','决策 ↔ 行动 ↔ 反馈',4.48,2.52,4.12,1.15,C.cyan);box(s,'工具 / 环境','文件 · 执行 · 观察',9.11,2.52,3.57,1.15,C.green);ln(s,4.03,3.1,4.43,3.1);ln(s,8.64,3.1,9.06,3.1);
  rect(s,4.48,3.91,8.20,.51,C.panel2);tx(s,'Harness：运行政策 / 会话日志 / 生命周期',4.69,4.01,7.78,.29,15,C.muted);
  box(s,'State / Memory','保存进度与可复用信息',.65,4.62,3.34,1.12,C.gold);box(s,'Eval → 改动验收','事实 / 产物 / 成本；未见任务',4.48,4.62,4.12,1.12,C.green);box(s,'RSI 研究问题','是否提升后续自改进能力？',9.11,4.62,3.57,1.12,C.purple);
  ln(s,2.31,4.56,2.31,3.72,C.gold);ln(s,6.54,4.47,6.54,4.57,C.green);ln(s,8.64,5.18,9.06,5.18,C.purple);
 }
 if(o.takeaway)strip(s,o.takeaway);
 return s;
}
function setup(title){const p=new pptxgen();p.layout='LAYOUT_WIDE';p.author='Codex';p.subject='Agent、Harness、上下文、记忆、评测及 RSI 的关系';p.title=title;p.lang='zh-CN';p.theme={headFontFace:FONT,bodyFontFace:FONT,lang:'zh-CN'};p.company='';return p;}
async function main(){fs.mkdirSync(path.join(root,'output'),{recursive:true});const p=setup('从一份 PPT 看 Agent 与 Harness');plan.slides.forEach(o=>render(p,o));await p.writeFile({fileName:path.join(root,'output/ai-agent-harness-talk.pptx')});const q=setup('可编辑架构图');const selected=[4,6,7,9,10,11,15,21];plan.slides.filter(o=>selected.includes(o.id)).forEach(o=>render(q,o));await q.writeFile({fileName:path.join(root,'output/architecture-diagrams.pptx')});fs.writeFileSync(path.join(root,'output/layout-geometry.json'),JSON.stringify({width:W,height:H,font:FONT,elements:geom},null,2));console.log(`Built ${plan.slides.length} slides and ${selected.length} editable architecture diagrams.`);}
main().catch(e=>{console.error(e);process.exit(1)});
