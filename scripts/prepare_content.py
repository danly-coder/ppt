"""研究记录与演讲内容的可复用数据源；修改后运行 python3 scripts/prepare_content.py。"""
import json, subprocess, hashlib
from pathlib import Path
R=Path(__file__).resolve().parent.parent
DATE='2026-10-23'
def save(p,v):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n' if not isinstance(v,str) else v,encoding='utf8')
repos={'codex':('openai/codex','main'),'dsh':('deepseek-ai/deepseek-harness','master'),'langgraph':('langchain-ai/langgraph','main'),'openhands':('OpenHands/software-agent-sdk','main'),'dgm':('jennyzzt/dgm','main')}
commits={k:subprocess.check_output(['git','-C',str(R/'work/sources'/k),'rev-parse','HEAD'],text=True).strip() for k in repos}
sources=[]
def doc(id,name,url,says,doesnot,example,loc,date=None):
 sources.append(dict(id=id,name=name,kind='official documentation / primary paper',url=url,checked_on=DATE,status='read_at_run_time',version=date or 'unversioned web page',locator=loc,says=says,does_not_claim=doesnot,example=example,confidence='high for cited scope; no runtime capability test'))
def code(id,name,repo,file,ranges,says,doesnot,example):
 p=R/'work/sources'/repo/file;txt=p.read_text();ls=txt.splitlines();sha=commits[repo]
 url=f'https://github.com/{repos[repo][0]}/blob/{sha}/{file}'
 evidence=[]
 for a,b in ranges:
  evidence.append({'start':a,'end':b,'text':'\n'.join(f'{i}: {ls[i-1]}' for i in range(a,min(b,len(ls))+1))})
 s=dict(id=id,name=name,kind='official source code' if repo!='dgm' else 'paper authors source code',url=url+f'#L{ranges[0][0]}',checked_on=DATE,status='read_at_run_time',version=sha,repository=repos[repo][0],path=file,locator=str(ranges),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),says=says,does_not_claim=doesnot,example=example,confidence='high: static code reading only')
 sources.append(s);save(Path('sources/evidence')/(id+'.json'),dict(**s,excerpts=evidence))
doc('S01','Codex as a platform','https://developers.openai.com/blog/codex-as-a-platform','开源 Harness 管理运行边界并可嵌入应用。','模型权重或托管服务随 Harness 开源。','应用用 app-server 承接进度与审批。','The reusable part is the agent loop', '2026-08-19')
doc('S02','Unlocking the Codex harness','https://openai.com/index/unlocking-the-codex-harness/','Codex core 包含循环；App Server 暴露双向 JSON-RPC 与线程生命周期。','所有客户端与当前版本部署细节完全一致。','审批请求可暂停 turn 等待客户端。','Inside the Codex harness; conversation primitives','2026-02-04')
doc('S03','DeepSeek Harness 官网','https://deepseek.com/harness/','页面标注预览版，链接官方仓库；强调插件组合。','营销演示证明任意任务可靠或性能领先。','官网的 PPT 任务仅作产品演示。','预览版; 一切皆插件')
code('S04','DSH architecture','dsh','docs/architecture.md',[(1,42),(74,145)],'Cordis 以服务、事件与可撤销 effects 组合插件；profile 叠加 bundle/patch。','每种插件组合均兼容或无需回归。','更换工具执行 provider 仍须检查日志与策略。')
doc('S05','LangGraph Persistence','https://docs.langchain.com/oss/python/langgraph/persistence','checkpointer 面向 thread，Store 面向跨 thread；内存 saver 重启会丢失。','默认 InMemorySaver 可断电恢复，或自动撤回外部动作。','PPT 任务恢复需配置持久后端。','Checkpointer vs. store; MemorySaver does not persist between restarts')
doc('S06','Effective context engineering','https://www.anthropic.com/research/effective-context-engineering-for-ai-agents','按任务维护有限上下文；压缩与外部笔记可支持长任务。','摘要无损或所有任务都应多 Agent。','保留未解决问题与证据路径。','Context engineering vs. prompt engineering; Long-horizon tasks','2025-09-29')
doc('S07','OpenHands SDK architecture','https://docs.openhands.dev/sdk/arch/overview','SDK、工具、workspace、agent-server 分包；支持本地与远程执行。','LocalWorkspace 默认隔离宿主机，或所有 tools 通过 workspace RPC 执行。','切换 workspace 部署形态要同时检查隔离策略。','Four-Package Architecture; Two Deployment Modes')
doc('S08','Darwin Gödel Machine paper','https://arxiv.org/abs/2505.22954v3','论文以编码基准经验验证自修改，并保留候选 Agent 档案。','证明所有修改有益，或通用无限 RSI 已实现。','只在已定义任务和评测范围解读改进。','Abstract; submission history','v3, 2026-03-12; v1 2025-05-29')
doc('S09','Build skills','https://learn.chatgpt.com/docs/build-skills','Skill 目录含 SKILL.md，可附脚本与资料，按需读取。','读取 Skill 即保证遵循或产物正确。','本项目 ai-tech-talk 规定研究与构建流程。','How ChatGPT and Codex use skills; Where Codex loads local skills')
code('S10','Codex run_turn','codex','codex-rs/core/src/session/turn.rs',[(158,195),(570,640),(730,750)],'run_turn 处理模型输出、工具反馈和是否继续，并考虑待处理输入。','只有一个无限 while 就涵盖完整 Codex；本次代码已运行。','工具报错后下一轮可读取结果再行动。')
code('S11','Codex ToolOrchestrator','codex','codex-rs/core/src/tools/orchestrator.rs',[(1,4),(130,180),(280,305)],'工具编排协调审批、沙箱选择及拒绝后重试。','沙箱保证内容正确，或所有动作都会弹窗。','文件可写权限与事实可信度是两种检查。')
code('S12','LangGraph StateGraph.compile','langgraph','libs/langgraph/langgraph/graph/state.py',[(131,157),(1177,1214),(1355,1365)],'图编译可独立接受 checkpointer 与 store。','LangGraph 本身等同具体编码 Agent 产品。','研究→核查节点共享 typed state。')
code('S13','LangGraph BaseCheckpointSaver','langgraph','libs/checkpoint/langgraph/checkpoint/base/__init__.py',[(93,130),(199,230)],'Checkpoint 保存通道值和版本；以 thread_id 检索线程状态。','checkpoint 是可执行进程内存快照，或恢复撤销外部副作用。','记录已确认 claims 与待完成节点。')
code('S14','OpenHands Agent.step','openhands','openhands-sdk/openhands/sdk/agent/agent.py',[(690,757)],'step 先处理待确认行动，再从会话视图组装消息并处理 condensation。','Agent 对象本身保存所有状态，或压缩等同长期记忆。','长任务先整理会话视图，再继续调用模型。')
code('S15','DGM authors README','dgm','README.md',[(20,32),(75,104)],'作者将系统描述为代码自修改加编码基准验证。','已在本次环境复现论文结果。','研究讨论保留设计而不复述成绩排名。')
code('S16','DSH AgentLoop service','dsh','packages/core/agent-loop/src/index.ts',[(338,365)],'AgentLoop 是 Cordis Service，注入 agents/sessions/llm/tools/systemPrompt 等依赖。','一切皆插件就等于安全热替换已验证。','组合不同工具或模型适配，不改业务 UI。')
code('S17','OpenHands Conversation factory','openhands','openhands-sdk/openhands/sdk/conversation/conversation.py',[(34,58),(153,165),(190,235)],'Conversation 按 workspace 类型返回本地或远程会话。','远程工具经本地 workspace 代理；本地自动沙箱。','在服务器容器内执行渲染工具。')
code('S18','LangGraph BaseStore','langgraph','libs/checkpoint/langgraph/store/base/__init__.py',[(1,12),(708,736)],'跨线程 key-value Store 使用 namespace；语义搜索与 TTL 依实现和配置。','Store 自动选择值得记住的信息、自动纠错或默认有向量搜索。','namespace=(alumni,style)，保留演讲偏好。')
code('S19','DSH ReactLoopAgent','dsh','packages/core/agent-loop/src/agent.ts',[(260,313),(675,703)],'预步骤扩展点与 session 日志投影参与循环。','日志有记录就证明推理或事实正确。','审查模型可见历史来自哪些事件。')
code('S20','DGM outer loop','dgm','DGM_outer.py',[(146,190),(270,300),(315,332)],'选择父 Agent、产生自修改尝试并更新档案；默认可 keep_all。','只保留本代分数最高者或每一步必须严格变好。','失败或中等候选也可能成为后续探索起点。')
code('S21','DSH guarded tools','dsh','packages/core/tools/src/index.ts',[(725,739),(1500,1537)],'扩展 pre-execute 流水线后还有执行 guard。','随便挂插件就应绕过权限边界。','新增网页检索工具同时测试政策和记录。')
doc('S22','Building effective agents','https://www.anthropic.com/research/building-effective-agents','以预定代码路径与模型动态决策区分 workflow/agent；术语存在差异。','这是所有项目统一采用的定义。','固定构建脚本嵌在 Agent 流程中。','What are agents?','2024-12-19; page notes tooling has evolved')
# 从 starter 的未经验证入口切换到核实后的来源清单；保留原入口供审计。
seed=R/'sources/seed_sources.json'
if not (R/'sources/starter_seed_sources.json').exists():save('sources/starter_seed_sources.json',json.loads(seed.read_text()))
srcdata=dict(checked_on=DATE,scope='官方文档阅读 + 固定 commit 源码静态检查；没有运行四项目或复现论文',repositories={k:dict(repository=v[0],commit=commits[k]) for k,v in repos.items()},sources=sources)
save('sources/seed_sources.json',srcdata)
save('sources/verified_sources.json',srcdata)
claims=[]
def claim(id,kind,text,ss,loc,confidence='high'):
 claims.append(dict(id=id,kind=kind,claim=text,source_ids=ss,locator=loc,confidence=confidence,checked_on=DATE))
claim('C01','fact','Codex 的 Harness 包含 Agent Loop、工具策略与线程持久化。',['S02','S10','S11'],'Inside the harness; run_turn; ToolOrchestrator')
claim('C02','fact','DSH 的循环、模型、工具和会话可作为 Cordis 插件组合。',['S04','S16'],'Cordis; AgentLoop.static inject')
claim('C03','fact','LangGraph checkpointer 按 thread 管状态，Store 可跨 thread 使用。',['S05','S12','S13','S18'],'Persistence; compile; BaseCheckpointSaver; BaseStore')
claim('C04','fact','OpenHands Conversation 根据 workspace 返回本地或远程实现。',['S07','S17'],'Conversation.__new__')
claim('C05','fact','OpenHands step 使用会话视图并可先产生压缩事件。',['S14'],'Agent._step 690–757')
claim('C06','fact','Skill 可封装说明、脚本与参考资料，并按需加载。',['S09'],'SKILL.md; progressive disclosure')
claim('C07','synthesis','Tool 是动作接口，MCP 是连接协议，Skill 是任务方法包；三者可组合。',['S02','S09','S21'],'跨项目工作定义；不是互斥分类')
claim('C08','synthesis','Agent 指反馈驱动的决策行为；Harness 指承载运行的系统；framework 提供构建抽象。',['S01','S02','S12','S22'],'讲解用边界，各项目命名不同')
claim('C09','fact','上下文工程处理当前模型输入的信息选择与维护。',['S06'],'Context engineering vs. prompt engineering')
claim('C10','synthesis','Context 是模型本轮输入；State 是程序保存的任务记录；Memory 是可复用保留信息，后两者可重叠。',['S13','S14','S18'],'教学视图；State 不保证语义真实')
claim('C11','fact','InMemorySaver 重启不保留；BaseStore 向量检索和 TTL 取决于实现/配置。',['S05','S18'],'Troubleshooting; BaseStore docstring')
claim('C12','synthesis','可信记忆需要来源、适用范围、版本、纠错和失效策略。',['S18','S06'],'本次设计建议，不是框架默认保证')
claim('C13','synthesis','构建通过、事实正确和演讲易懂需要分别验证。',['S11','S13'],'从执行/状态机制归纳；项目验收方案')
claim('C14','synthesis','评测改进需固定任务、独立验收并观察成本和人工介入。',['S20'],'将 DGM 的经验验证思路迁移到本案例')
claim('C15','fact','DGM 维护候选档案，在编码评测中经验验证代码自修改；不等于数学证明。',['S08','S15','S20'],'paper abstract; choose_selfimproves/update_archive')
claim('C16','synthesis','任务内修正、积累记忆和修改 Agent 自身属于不同层次的变化。',['S10','S18','S20'],'教学分层，不是统一 RSI 分类标准')
claim('C17','hypothesis','本案例的失败轨迹可用于提出 Harness 或 Skill 改动，再用未见任务检验迁移。',['S20'],'待设计实验，没有本次性能数据','medium')
claim('C18','hypothesis','校友团队可先用单 Agent 加独立验证，按瓶颈决定是否多 Agent。',['S22'],'场景建议，非性能结论','medium')
save('knowledge/claims.json',dict(checked_on=DATE,claims=claims))
slides=[]
def slide(kind,title,main,detail,ss,cs,notes,q,**kw):
 slides.append(dict(id=len(slides)+1,kind=kind,title=title,main=main,detail=detail,sources=ss,claims=cs,notes=notes,transition=q,**kw))
slide('cover','让 AI 交付成果，需要一整套系统','从这份 PPT，聊 Agent、Harness 与持续改进','2026.10.23 · 交流素材',[],[],
'今天不从名词考试开始。我们把准备这场交流会的过程摆到台面上：AI 要查官方资料、读源码、解释概念、制作幻灯片，最后还要证明自己确实检查过。大家可以带着一个问题听：如果把你工作中的一项任务交给它，你最不放心哪一步？我会把能从官方材料核实的机制，与个人的架构归纳和研究设想分开说。先用这份 PPT 本身做案例，再看四个项目各自提供了什么。','一份能看的回答，离一份能交付的 PPT 还有多远？',label='交流地图',tagline='Agent × Harness × Context × Memory × Eval × RSI')
slide('pipeline','交付一份 PPT，至少要走完六步','同一个目标，需要多次行动、落盘和核验','本场案例｜不是四套系统的同题实测',[],[],
'假设委托只有一句话：帮我准备校友 AI 交流会。如果模型只返回一篇大纲，回答已经结束，工作却刚开始。资料要能追溯，讲解要适合初学者，PPT 要能编辑，最后还要打开看看。我们把它拆成六段，后面每个概念都回到其中一个具体环节。特别留意“检查”这一步：文件存在、能打开、事实有证据，是不同条件。这个任务由当前 Codex 会话完成，其他项目用于官方架构对照。','哪些步骤适合固定下来，哪些步骤需要模型临场判断？',steps=['找官方资料','核事实出处','整理知识','设计讲法','生成 PPT','验证交付'],label='贯穿案例',takeaway='交付标准先写清：可追溯、可编辑、可检查。')
slide('cards','固定流程与动态决策可以一起用','LLM 生成内容；Workflow 固定路径；Agent 根据反馈选下一步','术语采用工作定义；不同项目用法并不完全相同',['S22','S10'],['C08'],
'把三者看成可组合的做法。单次模型调用可以解释 Harness；固定脚本可以把 JSON 生成 PPT；Agent 则在发现文档链接失效后决定换到官方仓库。这里的差异是“下一步由谁选择”，不是谁听起来更高级。现实系统常把开放的研究步骤交给 Agent，把构建和校验交给确定性程序。如果步骤已经清楚，固定流程往往更容易观察和复现。','当模型开始调用工具后，循环是怎样闭合的？',cards=[['单次 LLM','输入 → 回答','“解释一下 Harness”'],['Workflow','预定代码路径','“JSON → PPTX → PDF”'],['Agent','观察反馈再选行动','“链接失效 → 换官方来源”']],label='架构归纳')
slide('loop','Agent Loop 把工具结果带回下一轮','决策 → 行动 → 观察 → 再决策','示意架构｜闭环能适应反馈，但不会自动保证正确',['S10','S19'],['C01','C08'],
'我们请求查 DSH 的架构，模型提出读取文档，宿主执行读取，返回内容或报错。下一轮模型看到反馈，才决定是否继续读源码。这就是最小闭环。图里的“决策”是模型生成下一步建议；真正执行命令的是程序和工具，模型自己并没有文件系统权限。Codex 的 run_turn 明确处理工具反馈与继续条件；DSH 也有对应循环。停止条件同样重要：交付完成、预算耗尽或需要人工输入，都应该能退出。','既然能根据结果调整，为什么长任务仍会失败？',label='源码事实 + 示意架构',steps=['决策\n找什么证据','行动\n读取官方仓库','观察\n内容 / 报错','更新\n继续 / 停止'],takeaway='行动改变环境；观察改变下一次模型输入。')
slide('failures','能调用工具，还不足以可靠交付','失败可能出在信息、执行、连续性和验收四处','以下是故障注入情景，不是项目性能测量',[],['C13'],
'想象四个小故障：搜索命中了过期教程，渲染工具没有安装，会话中断忘了哪条结论还没核实，最后构建成功但中文挤出文本框。这些都不是多写一句“请认真”就能完全解决的。需要分别补来源管理、执行环境、持久状态和验收机制。模型能力当然重要，但我们也能通过工程设计让失败更容易被发现和修复。今天我们实际遇到过缺少项目 Skill 与网络连接问题，这些属于环境前提，而不是事实真假。','这些补丁能不能组成一个可复用的运行底座？',label='案例推演',cards=[['资料过期','有链接 ≠ 有证据'],['环境缺失','有工具名 ≠ 能执行'],['任务中断','聊天记录 ≠ 恢复点'],['验收遗漏','能构建 ≠ 能交付']],takeaway='先定位失败发生在哪一层，再决定修模型、流程还是环境。')
slide('harness','Harness 承载循环，也管理运行边界','模型提出行动；Harness 决定怎样执行和记录','示意架构｜Harness 与 Agent Loop 存在包含和重叠关系',['S02','S11','S04'],['C01','C08'],
'可以把 Harness 理解为让智能体做事的运行底座。里面有循环，也有工具调用、权限、日志、上下文管理与状态；应用还可以在外面加验收与业务规则。这个词不是一个跨项目统一接口。我们只用它帮助定位责任：是模型建议错了，还是工具没有执行，还是结果没保存？图上把“事实核查”和“构建检查”放到应用验收层，是我们的设计建议，不能误称 Codex 会替所有任务自动做完。','在 Codex 里，哪些部分能找到具体代码？',label='架构归纳',takeaway='Harness 提高可控性；内容可信度还需要应用自己的验收。')
slide('codex','Codex 把循环、工具策略和会话接在一起','从 run_turn 到 ToolOrchestrator，再把反馈写回会话','官方事实 + 简化调用关系｜省略内部模块，不是完整调用图',['S10','S11','S02'],['C01'],
'对应到本次任务，模型决定读取文件，run_turn 驱动一次次请求，工具编排层处理执行政策，再把返回值送回后续上下文。源码的 run_turn 在当前提交已经移到 session/turn.rs，直接照搬旧路径会找不到。ToolOrchestrator 的职责注释写着审批、沙箱选择和拒绝后的重试。App Server 让客户端围绕 thread、turn 和 item 呈现工作进度。这里的持久会话不是长期知识库，也不代表所有外部动作都可回滚。','Skill、MCP 和 Tool 分别放在哪里？',label='CODEX / 运行控制',takeaway='开源的是 Harness 与集成层；不要据此推断模型权重开放。')
slide('cards','Tool、MCP、Skill 各自补上不同的一环','Tool 提供动作；MCP 连接能力；Skill 组织做事方法','本次 ai-tech-talk：研究规范 + 讲解规则 + 构建脚本',['S09','S02','S21'],['C06','C07'],
'举三个具体例子：读取一个文件是 Tool；通过 MCP 暴露的仓库连接，让 Agent 能访问外部能力；ai-tech-talk Skill 则告诉它先核来源、再写知识资料、再生成和检查 PPT。Skill 可以附脚本，但文字指令并不是硬性执行器；因此仍需检查代码和产物。MCP 服务不一定只提供工具，也可能提供资源等能力。三者不是竞争关系，一项任务可以同时用到它们。我们这次确实读取了项目 Skill，并在它的基础上重写内容和生成器。','如果要让模型、循环甚至会话都能替换，会怎样组织？',label='架构归纳',cards=[['Tool · 动作','读取 / 搜索 / 渲染','具体输入和输出'],['MCP · 连接','对接外部工具与资源','协议与服务边界'],['Skill · 方法','怎样研究与验收','说明 + 脚本 + 参考资料']],takeaway='“装了 Skill”不是质量证书，执行与验收仍要有证据。')
slide('dsh','DSH 用 Cordis 把运行能力组合成插件树','模型适配、工具、会话与 Agent Loop 都有替换接缝','官方架构的简化图｜官网仍标注预览版',['S03','S04','S16','S19','S21'],['C02'],
'DeepSeek Harness 不是 DeepSeek 模型的另一种称呼。官方架构把 Cordis 作为插件基础，插件贡献服务、事件与可撤销的注册效果。AgentLoop 在代码里也是 Service，依赖 sessions、llm、tools 等服务。profile 通过有顺序的 bundle 与 patch 组成运行树。对于 PPT 案例，可以想象替换资料检索或渲染能力，而不是复制一套界面。可替换带来灵活性，也需要接口、生命周期和权限回归；这里没有测量组合后的性能。','替换能力之外，任务中断时怎样接着做？',label='DSH / 插件组合',takeaway='源码观察：AgentLoop extends Service；插件化不等于免测试。')
slide('checkpoint','LangGraph 把恢复建立在线程状态之上','Graph State → Checkpoint → 同一 thread 继续','示意架构｜必须选择持久后端；进程内 saver 重启会丢失',['S05','S12','S13','S18'],['C03','C11'],
'假设核查已经完成，PPT 还没渲染。我们把已核结论、文件位置、待办和下一个节点放在图状态中，由 checkpointer 保存。恢复时用同一 thread_id 找回对应进度。Store 是另一条线，保存跨任务复用的信息，例如这类交流会喜欢先讲案例。源码 compile 同时接受两者。注意恢复的是保存的状态和执行进度，不是冻结整个操作系统；外部发邮件、重复计费或覆盖文件，仍需应用处理幂等和边界。','有了图状态，执行工具的工作区又在哪里？',label='LANGGRAPH / 持久状态',takeaway='Checkpoint 解决“接着做到哪”；Store 解决“别的任务也能用什么”。')
slide('openhands','OpenHands 把 Agent 行为与执行部署分开','Conversation 选择本地或远程；工具在选定环境运行','官方 SDK 简化图｜LocalWorkspace 不自动隔离宿主机',['S07','S14','S17'],['C04','C05'],
'OpenHands Software Agent SDK 有 Agent、Conversation、Tool 和 Workspace 等组件。Conversation 工厂检查 workspace 类型，返回本地或远程实现；Agent.step 从会话视图组装输入，也处理压缩事件。用在 PPT 案例里，本地原型可以直接调用渲染工具，而远程部署可以让 Agent Server 在容器工作区内执行同一类工作。不能把“用了 workspace”就等同有沙箱，也不要把 UI 产品和 SDK 当成同一个仓库。我们读了源码，但没有部署这个 SDK。','四个项目放在一起，究竟该比较什么？',label='OPENHANDS / 执行部署',takeaway='本地模式与远程模式是部署选择；隔离效果取决于实际配置。')
slide('comparison','四个项目提供的是不同的设计抓手','先问自己缺什么，再选择要借用哪一层','架构归纳｜能力有重叠，可组合，不是四选一或性能榜单',['S10','S11','S04','S12','S13','S17'],['C01','C02','C03','C04'],
'如果已经在 Codex 里完成代码与文档任务，可以先利用它的工具执行和运行边界。如果在做可扩展产品，DSH 提供插件组合视角。如果任务的人工确认、分支和恢复很复杂，LangGraph 的状态模型值得研究。如果要把软件 Agent 放进远程工作区，OpenHands SDK 的部署分层很直观。这些都是观察重点，不是独占功能清单，更不是一个排序。也可以让 LangGraph 编排一个调用 Codex 的节点，前提是明确两边谁保存状态、谁处理失败。','选好底座以后，每次模型调用到底该看到什么？',label='设计取舍',rows=[['Codex','怎样可控地运行任务','循环、工具政策、线程'],['DSH','怎样替换和组合能力','Cordis 服务、事件、profile'],['LangGraph','怎样保存与恢复进度','Graph / Checkpointer / Store'],['OpenHands SDK','怎样部署软件 Agent','Conversation / Workspace / Server']],takeaway='比较维度：运行控制、扩展接缝、持久状态、执行环境。')
slide('context','上下文工程决定这一轮模型拿到哪些信息','把任务目标、相关证据和当前进度组装成有效输入','示意流程｜不是把所有历史都塞进窗口',['S06','S14','S19'],['C09','C05'],
'我们已经读了不少源码，但写某一页时不需要把五个仓库全部塞给模型。这一轮可能只需要一条结论、两段相关代码、来源路径以及还没解决的问题。上下文工程就是持续决定这些输入。压缩历史可以节省空间，但要保住约束、未核实项与可回查路径，不能把“没检查”压成“已确认”。OpenHands 的 step 与 DSH 的会话投影也说明，模型看到的是经过组装的视图，不是程序里所有数据。','这些原材料、进度和经验，是同一种“记忆”吗？',label='架构归纳',steps=['选相关证据','检索原文片段','组装当前输入','压缩冗余历史','保留回查路径'],takeaway='本例：写 checkpoint 页，只带恢复机制的证据与边界。')
slide('triad','Context、State、Memory 是三个观察视角','本轮输入｜任务记录｜可复用保留信息','教学区分｜可重叠；State 里的值也可能记录错',['S13','S18','S14'],['C10'],
'用同一份 PPT 看三个视角。模型正在读的源码片段属于 Context；程序保存“第十页待渲染、三条结论待复核”，属于 State；下次交流还适用的听众偏好，属于 Memory。State 可以包含记忆，取出的记忆也会进入 Context，所以它们不是三个互斥的桶。尤其不要把“State 是任务真相”理解成内容一定为真，它只是程序当前依赖的记录，仍然需要来源和校验。换一个窗口，也不等于把所有持久资料都清空。','记忆怎样写入和检索，才不会越用越错？',label='架构归纳',cards=[['Context · 现在看见','这一轮的模型输入','当前源码片段 + 指令'],['State · 当前记录','工作流保存的状态','页数 / 待核事实 / 文件路径'],['Memory · 留作复用','跨时间保留的信息','听众偏好 / 已验证经验']],takeaway='窗口容量、状态持久化、记忆质量，是三个不同问题。')
slide('memory','记忆要经过写入筛选，也要能失效纠错','候选信息 → 验证与定界 → 保存 → 检索 → 更新','示意设计｜不是 LangGraph Store 默认提供的完整记忆策略',['S18','S13'],['C10','C11','C12'],
'我们可以把短期进度放 checkpoint，把经核实的知识和偏好放应用自己的 Store。写入时至少问：来自哪里、适用谁、什么时候核实、何时复核？检索时也不只是相似度高就全拿来，要按当前任务和范围筛选。语义知识、情景经历、程序性经验是有用的分类，但不必为每一类建一个数据库。源码 BaseStore 提供存取接口和 namespace，是否启用向量搜索、TTL 及如何纠错，需要另外设计。','如果一条错误知识已经被保存，会造成什么？',label='设计建议',steps=['候选知识','来源 / 范围 / 版本','持久保存','按任务检索','纠错 / 失效'],takeaway='先把“可信地记住与忘记”做好，再决定是否引入向量库。')
slide('memoryfix','把错误写成长期事实，会放大后续失误','例：把“内存 saver”误记为“重启可恢复”','故障注入示例｜官方文档明确指出内存 saver 的限制',['S05','S18'],['C11','C12'],
'这里做一个小型故障演练。旧笔记写着“启用 checkpoint 后，断电也不丢”。下次做项目时照着用 InMemorySaver，就可能在重启后发现状态没了。正确的处理不只是改当前回答，还应找到这条笔记的来源，标记失效，写明只适用于当前进程，并为重启恢复配置持久后端。新的上下文应该检索到修正后的记录。这个例子提醒我们，记忆系统也需要回归问题集，而不是只统计写进去了多少条。','怎样证明这些改动让系统真的更可靠？',label='案例推演',cards=[['错误记忆','有 checkpoint 就不丢','未注明存储后端'],['核对证据','InMemorySaver 在 RAM','重启后不保留'],['修正记录','注明后端与适用范围','旧条目失效并补回归']],takeaway='纠错要同时更新当前回答、持久记录和回归用例。')
slide('eval','评测先对齐交付标准，再比较改动','用固定任务与独立验收，观察结果、成本和人工介入','本案例的评测设计｜阈值是建议，没有虚构实验成绩',['S20'],['C13','C14'],
'如果比较两个版本的 Skill，先固定一批任务：正常资料、失效链接、缺少渲染器、中断恢复、故意放入错误来源。不要只用这一次演讲做训练题又当考试题。结构检查可以自动化，事实是否被证据支持需要逐条审阅，讲得是否清楚还要初学者反馈。我们可以记录成功率、耗时、费用与人工介入次数，再决定改动是否值得保留。今天只实际验收这份交付，不把一次 build 通过说成系统成功率提高。','哪些检查机器能做，哪些必须另外审查？',label='设计建议',rows=[['事实可追溯','结论 → 官方原文 / commit','人工核支持关系'],['结构可交付','页数、备注、引用、文件完整','自动 check'],['视觉可阅读','溢出、重叠、中文、对比度','渲染 + 目检'],['运行成本','耗时、费用、人工介入','固定环境记录']],takeaway='修改前后用相同任务比较；未见任务留到最后验收。')
slide('validation','构建检查、事实审阅和视觉检查各有盲区','通过一项验收，不能替代另外两项','本次交付｜23 页已构建与渲染；详细检查结果见 QA.md',[],['C13'],
'把这次交付的三条证据线展示出来。build 证明生成器能产出文件；check 检查引用 ID、备注和 PPTX 的结构；render 才能暴露字体与布局问题。它们都不能独立证明某条技术陈述被官方支持，所以我们另外保存 claim 到 source 的映射和固定提交的代码片段。目前这三条检查线都已完成；QA 保存实际命令和范围。大家也可以问：如果模型负责生成又负责检查，会不会重复自己的盲点？这也是保留独立验收标准的原因。','当系统发现自己的失败后，改的究竟是哪一层？',label='实际案例 / 验收路径',cards=[['build + check','23 页 / 23 条讲者备注','文件结构与引用检查通过'],['claim → source','22 项来源 / 5 个仓库提交','静态阅读，未部署四项目'],['render + 目检','23 页已渲染并逐页审阅','现场软件兼容性仍未验证']],takeaway='事实出处、构建日志与渲染预览一起交付。')
slide('levels','重试、记忆积累与自修改不是同一种进步','先分清改了任务结果、保留信息，还是 Agent 程序','RSI：递归自我改进；本页为教学分层，不是统一标准',['S10','S18','S20'],['C16','C17'],
'模型发现一页挤不下，重新排版，这是任务内修正。把“标题应更短”的偏好留给下次，是记忆更新。改写工具或生成脚本，再用任务集验证，则开始触及系统自修改。RSI 更关心：改动能否进一步提升它产生后续改进的能力。几层之间没有一句提示词就能跨过去的保证。自修改也不一定修改模型权重，可能只是工具、上下文策略或 Agent 代码。我们本次修生成器是在人工目标约束下完成任务，不能据此声称复现了 RSI。','有没有研究系统真正尝试修改自己的 Agent 代码？',label='架构归纳 + 研究讨论',cards=[['任务内修正','换来源 / 修一页','目标产物变好'],['记忆积累','保存偏好与教训','后续输入可能改善'],['系统自修改','改工具 / Agent 代码','再评测后续改进能力']],takeaway='“自己改了代码”是现象；“持续可靠地变强”需要更强证据。')
slide('dgm','DGM 用编码评测筛查自修改的 Agent','从候选档案选父代 → 修改代码 → 评测 → 更新档案','研究案例｜不是数学证明，也没有在本次复现性能',['S08','S15','S20'],['C15'],
'Darwin Gödel Machine 给出一个具体研究例子。它维护不同 Agent 的档案，选择父候选，让基础模型生成修改，再通过编码任务评测。源码不是简单的“只留本代冠军”，档案更新可以保留多个可运行候选，从而探索不同分支。论文讨论的是受限编码实验中的经验结果，不是任意环境都可靠的证明。这里还有评测适配、搜索成本、结果泛化和人工监督等问题。我们只读取论文摘要和作者代码，没有重新运行那些实验，也不引用分数作横向排名。','回到这份 PPT：这些机制怎样接成一条改进链？',label='研究事实 + 边界',steps=['候选 Agent 档案','选择父候选','生成代码改动','编码任务评测','更新候选档案'],takeaway='经验评测能筛选候选；不足以保证开放环境中的无限递归改进。')
slide('system','可靠改进来自多个闭环彼此连接','Agent 做事；Harness 承载；Context / Memory 供给；Eval 检验','示意架构｜跨项目归纳，非任一官方完整架构',['S10','S11','S13','S18','S20'],['C08','C10','C13','C16'],
'现在把地图接起来。Agent 在 Harness 中行动，工具改变环境，反馈回到下一轮。State 保存当前任务，Memory 留下可复用信息；上下文工程决定哪些内容进入模型。Eval 在另一条线上判断产物和系统改动是否值得接受。只有改动进一步提升后续自改进能力并获得证据，才有资格讨论 RSI。各环节不能相互替代：长记忆不能代替核事实，强沙箱不能代替好评测，多 Agent 也不能代替清楚的交付标准。','如果只带走一个实践动作，你会从哪个闭环开始？',label='关系总图',takeaway='先做可观察、可验收的小闭环，再讨论更大的自主性。')
slide('reading','从设计问题进入源码，比从项目名入手更容易','每个问题都有一条可复查的阅读路径','完整直链、commit、代码摘录与 claims 对照见资料包',['S10','S11','S16','S13','S18','S17','S20'],['C01','C02','C03','C04','C15'],
'给想继续研究的校友留一条轻量路线。想看循环，读 Codex run_turn，再读工具编排。想看插件，读 DSH architecture 和 AgentLoop 的依赖。想看恢复，先对照 BaseCheckpointSaver 与 BaseStore。想看部署，读 OpenHands Conversation 的工厂分支。最后再看 DGM 的外层选择与评测循环。资料包不是链接堆，每个重要结论都有定位和不适用范围。代码会演进，链接固定到本次实际读取的提交，官网状态另记核查日期。','带着自己的任务，我们可以争论哪三个选择？',label='继续阅读',rows=[['运行控制','Codex: session/turn.rs → tools/orchestrator.rs'],['插件接缝','DSH: docs/architecture.md → AgentLoop'],['状态与记忆','LangGraph: BaseCheckpointSaver ↔ BaseStore'],['执行与演进','OpenHands: Conversation；DGM: DGM_outer.py']],takeaway='阅读重点是责任边界和失败路径，不是记住所有模块名。')
slide('discussion','用三个真实取舍，交换各自的实践','自主到哪一步？记住哪些东西？怎样证明改得更好？','建议 20 分钟｜每个问题先给一个亲身案例，再谈原则',[],['C17','C18'],
'最后把时间留给大家。第一题，请挑自己工作里的一项任务，说出哪一步可以自动做、哪一步你希望自己确认。第二题，请举一条应该长期保留的信息，以及一条必须过期的信息。第三题，假设 AI 改了自己的工具，你会拿哪组没见过的任务验收？不必追求统一答案。我们可以比较各自的约束：有人在乎速度，有人在乎可追溯，也有人必须处理复杂权限。今天这份资料的价值是让这些讨论有共同的案例和边界。','请选择一个问题，从你的实际经历开始。',label='开放讨论 / 20 MIN',cards=[['自主性边界','哪一个动作必须由你确认？','速度与控制怎么取舍'],['记忆的边界','哪条信息值得留下或过期？','连续性与错误累积怎么取舍'],['改进的证据','拿什么未见任务验收自修改？','指标提升与真实收益怎么取舍']],takeaway='没有标准答案；具体场景比泛泛站队更有价值。')
plan=dict(version='researched-2026-10-23',speaking_minutes=43,discussion_minutes=20,slides=slides)
save('content/slide_plan.json',plan)
cfg=json.loads((R/'event.json').read_text());cfg.update(target_slides=len(slides),speaking_minutes=43);save('event.json',cfg)
# Full speaker script with hyperlinks, source and claim mapping.
script=['# 逐页讲者备注\n\n建议讲述约 43 分钟，另留 20 分钟讨论。每页正文约一分钟，余下时间用于看图、互动与停顿。\n\n本场案例是本项目资料到 PPT 的制作；四个开源项目没有做同题性能实测。\n']
byid={s['id']:s for s in sources}
for s in slides:
 script += [f"\n## {s['id']:02d}｜{s['title']}\n\n结论：{s['main']}\n\n{s['notes']}\n\n过渡问题：{s['transition']}\n\n证据类型：{s['label']}；claims：{', '.join(s['claims']) or '演讲组织 / 本场案例'}。\n"]
 for sid in s['sources']:
  z=byid[sid];script += [f"- [{sid} · {z['name']}]({z['url']})；定位：{z['locator']}。\n"]
save('content/speaker_script.md',''.join(script))
# Research first: each entry includes what it does and doesn't support, and an example.
research=['# 官方资料与源码研究\n\n核查日期：2026-10-23（北京时间）。本次完成官方网页阅读、五个仓库的浅克隆与静态代码核对；未运行四个 Agent 项目，也未复现 DGM 实验。源码证据固定到实际提交，文档只记录核查日，不能保证此后页面不变。\n\n## 研究范围与顺序\n\n先用产品文档确认概念，再用源码定位职责。源码读的是局部实现，不由 README 营销语推断内部机制。场景设计与评测阈值属于本次归纳。\n\n## 仓库快照\n\n']
for k,v in repos.items():research += [f'- {v[0]}：`{commits[k]}`\n']
research += ['\n## 逐项证据\n']
for s in sources:
 research += [f"\n### {s['id']}｜{s['name']}\n\n- 官方链接：{s['url']}\n- 核查：{s['checked_on']}；版本：{s['version']}；定位：{s['locator']}\n- 支持什么：{s['says']}\n- 不支持什么：{s['does_not_claim']}\n- 本例：{s['example']}\n- 置信范围：{s['confidence']}\n"]
research += ['\n## 已纠正的 starter 问题\n\n1. 来源种子不视为已核实；原清单保留为 sources/starter_seed_sources.json。\n2. Codex 旧的 core/src/codex.rs 路径未找到；当前源码循环位于 core/src/session/turn.rs。\n3. 官网 DSH 状态仅采用页面“预览版”，不虚构稳定版承诺。\n4. State 改称“任务记录”，避免把数据库内容误说成必然为真。\n5. 明确 InMemorySaver 重启会丢失；Store 的语义搜索和 TTL 不是默认自动能力。\n6. DGM 的候选档案不是只留冠军；没有复现基准或引用排名。\n\n## 未核实与限制\n\n- 不保证本次静态阅读覆盖所有功能分支、平台与版本。没有运行 Codex/DSH/LangGraph/OpenHands 的集成测试。\n- 未复现 DGM 实验，未核实所有论文章节及 benchmark 配置；只采用摘要和作者代码能支持的机制。\n- 网页可能随时间更新；版本化结论以固定 commit 源码为准。\n- 本案例中的候选评测任务与阈值是设计建议，不是已完成的 A/B 研究。\n- 未做现场 PowerPoint / Keynote 的跨软件目检；LibreOffice 渲染只覆盖当前环境。\n']
save('knowledge/research.md',''.join(research))
save('knowledge/architecture-comparison.md','''# 按设计问题理解四个项目

这是阅读侧重点，不是独占能力表、兼容性保证或性能排名。

| 项目 | 最值得追问的问题 | 核实到的机制 | 本案例怎样借用 | 边界 |
|---|---|---|---|---|
| Codex | 模型提议怎样变成受控行动？ | run_turn、ToolOrchestrator、线程事件 | 研究、写文件、执行构建 | 沙箱不能保证事实正确 |
| DSH | 怎样替换能力而不复制整个产品？ | Cordis Service / events、profile / bundle / patch | 替换检索或工具 provider | 接口、生命周期、策略要回归 |
| LangGraph | 哪些进度能保存并继续？ | typed state、checkpointer、Store | 保存待核结论与生成进度 | 持久后端要配置；外部副作用要另管 |
| OpenHands SDK | 软件 Agent 放在哪里执行？ | Agent / Conversation / Workspace / Agent Server | 本地原型与远程渲染环境 | 本地 workspace 不等于自动沙箱 |

它们可以组合，但不是拿来就必然兼容。例如 LangGraph 节点调用 Codex，需另行约定 thread 对应关系、超时、重复请求与状态所有权。

## 最小源码阅读路线

- Codex：S10 run_turn → S11 ToolOrchestrator。
- DSH：S04 architecture → S16 AgentLoop → S19 ReactLoopAgent → S21 guarded tools。
- LangGraph：S12 compile → S13 BaseCheckpointSaver ↔ S18 BaseStore。
- OpenHands：S17 Conversation.__new__ → S14 Agent._step。

固定 commit 和直链见 [research.md](research.md) 与 sources/verified_sources.json。
''')
save('knowledge/concept-map.md','''# 概念地图：从一个任务出发

以下是教学工作定义，不强迫所有项目采用同一命名。事实/归纳/假设对应 claims.json。

| 词 | 通俗工作定义 | 在 PPT 案例中的例子 |
|---|---|---|
| LLM | 根据当前输入生成文字或动作提议的模型 | 提议读取一份架构文档 |
| Workflow | 代码规定主要执行路径 | JSON → PPTX → PDF |
| Agent | 根据目标与反馈动态选择后续行动的系统行为 | 链接失效后换官方源码 |
| Agent Loop | 请求模型、执行动作、接收反馈并继续或停止 | 搜索 → 阅读 → 核查 → 再搜索 |
| Harness | 承载循环的运行系统及控制机制，边界因项目而异 | 工具、权限、会话与日志 |
| Framework | 提供构建这些系统的抽象与库 | LangGraph 的图与持久化接口 |
| Tool | 有输入输出约定的动作接口 | 文件读取、渲染命令 |
| MCP | 连接模型应用与外部能力/资源的协议 | GitHub 工具连接 |
| Skill | 可按需读取的方法说明，可附脚本和资料 | ai-tech-talk 的研究到交付流程 |
| Context | 本轮模型实际收到的输入 | 相关片段、指令、工具返回 |
| State | 程序此刻保存并依赖的任务记录，可能记录错 | 页数、待办、已核 claim 列表 |
| Memory | 保留以供未来复用的信息，与 state 可重叠 | 听众偏好、知识、经历、方法 |
| Checkpoint | 某个执行位置的状态与相关调度信息 | 同一 thread 中的恢复点 |
| Eval | 按事先定义的任务与验收标准观察效果 | 事实、结构、视觉、成本、人工介入 |
| RSI | 递归自我改进：改进系统进一步产生改进的能力 | 修改 Agent 后检验其后续改进能力，属研究问题 |

## 关系与易混边界

Agent 行为在 Harness 中运行，framework 可帮助构建 Harness。上下文工程从状态、记忆、工具观察等挑选本轮输入。Checkpoint 管保存与恢复；Store 提供跨线程数据接口，但不代写入策略。长期记忆通常改变未来输入，并不等于修改模型权重。

语义记忆（知识）、情景记忆（经历）、程序性记忆（方法）是整理信息的角度，不要求各建一套数据库。短期/长期强调保存与使用跨度，不能与三类信息简单一一对应。

评测位于行动和改进的验收边界。任务内重试、记忆积累、工具/Agent 程序修改可分别发生；只有对后续改进能力的证据才支持更强的 RSI 论断。把修改后的代码提交给未见任务，仍不等于证明所有未来任务可靠。

## 多 Agent 的讨论位置

多 Agent 可以隔离上下文、分工与并行；是否值得取决于协调成本、共享状态和独立验收。当前制作没有启用子 Agent，也没有测量单/多 Agent 的差异。这个选择留作讨论，不写成优势结论。

证据依据：S10 / S11 / S13 / S14 / S18 / S20；术语区分参考 S22。详见 research.md 的链接和适用范围。
''')
save('content/discussion.md','''# 讨论引导：20 分钟

目标是交换具体实践，不是考名词。先邀请两位日常使用者，再邀请开发者补充约束。

1. **自主性到哪一步？（6 分钟）** 选一项工作：搜资料、写文件、安装依赖、覆盖文件、发出结果。哪一步允许自动执行，哪一步保留确认？讲一次你实际介入的经历。
2. **记什么，何时忘？（6 分钟）** 如果下个月再次办交流会，保留听众偏好、来源内容还是全部轨迹？哪一条必须复核或过期？怎样发现旧知识已经错误？
3. **怎样证明自己改得更好？（6 分钟）** AI 改了检索工具或 Skill，拿哪些未见任务验收？如果准确性提高但费用翻倍、人工介入增多，你接受吗？谁能修改验收标准？

最后 2 分钟：每人说一个愿意尝试的小闭环和一个还没解决的问题。

## 备用追问

- 用一个 Agent 加确定性验证够不够？什么时候多 Agent 的上下文隔离值得协调开销？
- 恢复后如果重新执行了外部动作，如何防重复？
- 生成器和检查器来自同一个模型时，如何保留独立标准？
- 评测集被 Agent 看到后，怎样避免只针对题库优化？

这些是情境假设与设计取舍，没有在本项目中做性能实验。RSI 只作为研究讨论，不宣称已实现通用持续自我提升。
''')
print('Prepared',len(sources),'sources,',len(claims),'claims,',len(slides),'slides')
