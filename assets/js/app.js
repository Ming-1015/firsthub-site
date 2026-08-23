/* ---------- i18n ---------- */
let LANG = localStorage.getItem('frc_lang') || (navigator.language || 'en').toLowerCase().split('-')[0];
if(LANG==='zh') LANG='zh-CN';
if(!I18N[LANG]) LANG='en';
Object.assign(I18N.en,{sort_hot:"By popularity",sort_team:"By team number",teams_sorted_number:" teams (team number order)",sort_label:"Open team sorting"});
Object.assign(I18N['zh-CN'],{sort_hot:"按热度排序",sort_team:"按队号排序",teams_sorted_number:" 支队伍（按队号顺序）",sort_label:"开源队伍排序方式"});
Object.assign(I18N['zh-TW'],{sort_hot:"依熱度排序",sort_team:"依隊號排序",teams_sorted_number:" 支隊伍（依隊號順序）",sort_label:"開源隊伍排序方式"});
Object.assign(I18N.ja,{sort_hot:"人気順",sort_team:"チーム番号順",teams_sorted_number:"チーム（チーム番号順）",sort_label:"Open Teams の並び順"});
Object.assign(I18N.ko,{sort_hot:"인기순",sort_team:"팀 번호순",teams_sorted_number:"팀(팀 번호순)",sort_label:"Open Teams 정렬"});
Object.assign(I18N.en,{c1:"See the GitHub README for contribution and data-maintenance instructions.",contrib_repo:"View GitHub repository",contrib_issue:"Report a data issue or suggest an addition"});
Object.assign(I18N['zh-CN'],{c1:"贡献说明与数据维护方式请查看 GitHub README。",contrib_repo:"查看 GitHub 仓库",contrib_issue:"提交数据问题或补充建议"});
Object.assign(I18N['zh-TW'],{c1:"貢獻說明與資料維護方式請查看 GitHub README。",contrib_repo:"查看 GitHub 儲存庫",contrib_issue:"回報資料問題或補充建議"});
Object.assign(I18N.ja,{c1:"貢献方法とデータ管理については GitHub README をご覧ください。",contrib_repo:"GitHub リポジトリを見る",contrib_issue:"データの問題や追加案を報告"});
Object.assign(I18N.ko,{c1:"기여 및 데이터 관리 방법은 GitHub README를 확인하세요.",contrib_repo:"GitHub 저장소 보기",contrib_issue:"데이터 문제 또는 추가 제안 제출"});
Object.assign(I18N.es,{c1:"Consulta el README de GitHub para contribuir y mantener los datos.",contrib_repo:"Ver repositorio de GitHub",contrib_issue:"Informar un problema o proponer datos"});
Object.assign(I18N.fr,{c1:"Consultez le README GitHub pour contribuer et maintenir les données.",contrib_repo:"Voir le dépôt GitHub",contrib_issue:"Signaler un problème ou proposer un ajout"});
Object.assign(I18N.de,{c1:"Hinweise zu Beiträgen und Datenpflege stehen in der GitHub-README.",contrib_repo:"GitHub-Repository ansehen",contrib_issue:"Datenproblem oder Ergänzung melden"});
Object.assign(I18N.pt,{c1:"Consulte o README do GitHub para contribuir e manter os dados.",contrib_repo:"Ver repositório no GitHub",contrib_issue:"Relatar problema ou sugerir dados"});
Object.assign(I18N.th,{c1:"ดูวิธีมีส่วนร่วมและดูแลข้อมูลได้ใน GitHub README",contrib_repo:"ดูที่เก็บ GitHub",contrib_issue:"แจ้งปัญหาข้อมูลหรือเสนอข้อมูลเพิ่ม"});
Object.assign(I18N.vi,{c1:"Xem GitHub README để biết cách đóng góp và bảo trì dữ liệu.",contrib_repo:"Xem kho GitHub",contrib_issue:"Báo lỗi dữ liệu hoặc đề xuất bổ sung"});
Object.assign(I18N.id,{c1:"Lihat README GitHub untuk panduan kontribusi dan pemeliharaan data.",contrib_repo:"Lihat repositori GitHub",contrib_issue:"Laporkan masalah atau usulkan data"});
Object.assign(I18N.en,{
  site_title:"FIRSTHub · FRC Open Resource Library",site_subtitle:"Open resources for teams, by teams.",built_by:"Built by FRC Team 5449 for the FRC community.",footer_built_by:"Built by FRC Team 5449",
  hero_kicker:"FRC · FIRST Robotics Competition · Open to the entire community",
  hero_sub:"A multi-season archive of Impact Award resources, Open Alliance teams (CAD, code, and Build Threads), Hall of Fame teams, and technical resources from 2021–2026.",
  select_season:"Choose a season",tab_home:"Overview",tab_impact:"Impact Award Archive",tab_open:"Open Alliance Teams",tab_tech:"Technical Resources",
  stat_impact:"Impact Award team entries",stat_open:"Open Alliance team entries",stat_hall:"Hall of Fame teams",stat_tech:"Technical resources",
  home_what:"Explore the archive",
  home_lead:"Browse six seasons of Impact Award essays, videos, and presentations; Open Alliance teams sharing CAD, code, or Build Threads; the official FIRST Hall of Fame; and a curated collection of technical and learning resources.",
  home_usage:"Choose a season above to update the archive. Use “Impact Award Archive” for winning-team materials, browse “Open Alliance Teams” by Build Thread views or team number, and filter “Technical Resources” by category. Add an anchor such as #2024 to share a specific season.",
  home_impact_t:"Impact Award Archive",home_impact_d:"Essays, videos, and presentations from 514 award-winning team entries across the 2021–2026 seasons.",
  home_open_t:"Open Alliance Teams",home_open_d:"2,092 team entries across six seasons, with public Build Threads, CAD, code, and video links.",
  home_tech_t:"Technical Resources",home_tech_d:"Curated CAD, software, data, strategy, and learning resources, filterable by category.",
  sources_head:"Data Sources",src_impact_n:"Official annual award essays (PDF) and judging criteria.",
  src_hof_n:"Official list of Championship Chairman’s Award and FIRST Impact Award winners, 1992–2026.",
  src_cd_n:"Community-maintained Open Alliance directory for each season.",src_tba_n:"Competition, match, results, and team data, with a public API.",
  impact_lead:"Essays link to official FIRST PDFs; videos come from team YouTube or Instagram accounts; presentations link to publicly shared Google Drive or Canva files.",
  open_lead:"Sorted by Build Thread views as a rough indicator of community interest. The CAD icon marks teams that publish robot CAD, including direct Onshape previews where available. Public GitHub repositories are tagged by subsystem or software area when identifiable.",
  hall_head:"FIRST Hall of Fame",hall_lead:"Teams officially recognized by FIRST for winning the Championship Chairman’s Award (1992–2022) or FIRST Impact Award (2023–present).",
  tech_head:"FRC Technical Resources",tech_lead:"Official documentation, software frameworks, design tools, data platforms, and community learning resources.",
  f_all:"All",f_cad:"Public CAD",f_code:"Public code",f_video:"Public video",f_site:"Has a website",
  imp_f_all:"All",imp_f_video:"Has video",imp_f_pres:"Has presentation/materials",imp_f_champ:"Championship",
  search_ph:"Search by team number or name…",op_search_ph:"Search by team number, name, or tag…",site_label:"Website",
  champ_prefix:"Championship Impact Award winner:",teams_suffix:" teams",teams_sorted:" teams, ranked by Build Thread views",showing:"Showing",hall_count:" teams (1992–2026)",tech_count:" resources",
  footer_src:"Data Sources",footer_contrib:"Contribute Data",footer_roadmap:"Roadmap",
  c1:"See the GitHub README for contribution and data-maintenance instructions.",c2:"Submit new Impact Award or Open Alliance team records through GitHub.",
  c3:"Contributions of team GitHub, Onshape, YouTube, and other public resource links are welcome.",c4:"Found an error or a missing resource? Open an issue and help improve the archive.",
  r1:"Add Impact Award data for the 2020 season and earlier.",r2:"Add more awards, including Dean’s List, Woodie Flowers, and Engineering Excellence.",r3:"Expand the China team section and Chinese-language open-source tutorials.",r4:"Build a mechanism-based index of Open Alliance CAD and code.",
  footer_copy:"FIRSTHub · FRC Open Resource Library · community-built resources for the 2021–2026 FRC seasons · open data, open collaboration",
  tag_chassis:"Drivetrain",tag_vision:"Vision",tag_intake:"Intake",tag_shooter:"Shooter",tag_climb:"Climb",tag_auto:"Autonomous",tag_scout:"Scouting",lang_label:"Language",
  directory_zh:"Chinese search directory",directory_en:"English search directory",sitemap_label:"Sitemap",resource_open:"Open resource",team_page:"FIRST team page",cad_preview:"CAD preview",views_suffix:" views"
});
Object.assign(I18N['zh-CN'],{site_title:"FRC 智库网",site_subtitle:"FIRSTHub · FRC Open Resource Library",built_by:"由 FRC Team 5449 建设 · 面向整个 FRC 社区",footer_built_by:"由 FRC Team 5449 建设",directory_zh:"中文搜索目录",directory_en:"英文搜索目录",sitemap_label:"站点地图",resource_open:"打开资源",team_page:"FIRST 队伍页",cad_preview:"CAD 预览"});
const AWARD_UI_EN={tab_scripts:"Award Scripts",home_scripts_t:"Award Scripts",home_scripts_d:"Search official judge-written award citations by team, award, and event—not just Impact Award entries.",scripts_lead:"Official team award citations published on FIRST event pages. Competitive results, individual awards, and records without a public citation are excluded.",scripts_original:"Official text is preserved in English, and every card links to the corresponding FIRST event page for verification.",scripts_search:"Search by team, award, event, or citation…",scripts_all_awards:"All awards",scripts_all_events:"All events",scripts_title:"Official Award Scripts",scripts_originals:" official citations",scripts_events:" events",scripts_showing:"Showing",scripts_load_more:"Load more",scripts_remaining:"remaining",scripts_empty:"No award citations match the current filters.",scripts_official_en:"Official English text",scripts_source:"View FIRST event page",scripts_loading:"Loading award scripts…",scripts_load_failed:"Award-script data could not be loaded.",scripts_retry:"Try again",scripts_no_data:"No reliable public data",scripts_no_data_lead:"FIRST event pages for the 2021 season do not provide a reliable archive of team award citations, so this section is intentionally left blank.",scripts_no_data_box:"No reliable official award citations are available for this season. Impact Award materials remain available in the Impact Award Archive."};
Object.keys(I18N).forEach(lang=>Object.assign(I18N[lang],AWARD_UI_EN));
Object.assign(I18N['zh-CN'],{tab_scripts:"颁奖词库",home_scripts_t:"颁奖词库",home_scripts_d:"不只限于 Impact：按队伍、奖项和赛事查找 FIRST 官方评委颁奖词。",scripts_lead:"收录官方赛事页面公开的队伍奖项颁奖词原文；不包含比赛名次、个人奖项或没有公开颁奖词的记录。",scripts_original:"原文优先：颁奖词保持 FIRST 官方英文原文，每张卡片都可回到官方赛事页面核对。",scripts_search:"搜队号、队名、奖项或颁奖词…",scripts_all_awards:"全部奖项",scripts_all_events:"全部赛事",scripts_title:"全奖项颁奖词库",scripts_originals:" 条官方原文",scripts_events:" 场赛事",scripts_showing:"显示",scripts_load_more:"加载更多",scripts_remaining:"还剩",scripts_empty:"没有符合当前筛选条件的颁奖词。",scripts_official_en:"官方英文原文",scripts_source:"查看官方来源",scripts_loading:"正在载入颁奖词…",scripts_load_failed:"赛季数据载入失败。",scripts_retry:"重新载入",scripts_no_data:"暂无可靠公开数据",scripts_no_data_lead:"2021 赛季官方赛事页面没有形成可可靠归档的队伍颁奖词数据，因此这里明确留空，不补写、不推测。",scripts_no_data_box:"该赛季暂无可靠的官方颁奖词原文。你仍可在 Impact 智库查看获奖材料。"});
Object.assign(I18N['zh-TW'],{tab_scripts:"頒獎詞庫",home_scripts_t:"頒獎詞庫",home_scripts_d:"不限於 Impact：依隊伍、獎項與賽事查找 FIRST 官方評審頒獎詞。",scripts_lead:"收錄官方賽事頁面公開的隊伍獎項頒獎詞原文；不包含比賽名次、個人獎項或未公開頒獎詞的記錄。",scripts_original:"原文優先：頒獎詞保留 FIRST 官方英文原文，每張卡片都可回到官方賽事頁面核對。",scripts_search:"搜尋隊號、隊名、獎項或頒獎詞…",scripts_all_awards:"全部獎項",scripts_all_events:"全部賽事",scripts_title:"全獎項頒獎詞庫",scripts_originals:" 條官方原文",scripts_events:" 場賽事",scripts_showing:"顯示",scripts_load_more:"載入更多",scripts_remaining:"剩餘",scripts_empty:"沒有符合目前篩選條件的頒獎詞。",scripts_official_en:"官方英文原文",scripts_source:"查看官方來源",scripts_loading:"正在載入頒獎詞…",scripts_load_failed:"賽季資料載入失敗。",scripts_retry:"重新載入",scripts_no_data:"暫無可靠公開資料",scripts_no_data_lead:"2021 賽季官方賽事頁面沒有可靠的隊伍頒獎詞存檔，因此此處明確留空。",scripts_no_data_box:"此賽季暫無可靠的官方頒獎詞原文；Impact 智庫仍可查看獲獎資料。"});
Object.keys(I18N).forEach(lang=>Object.assign(I18N[lang],{champ_finalists:"5 finalists: "}));
Object.assign(I18N['zh-CN'],{champ_finalists:"5 支决赛入围："});
Object.assign(I18N['zh-TW'],{champ_finalists:"5 支決賽入圍："});
function t(k){ return (I18N[LANG]&&I18N[LANG][k])||I18N['en'][k]||k; }
function applyI18n(){
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const k=el.dataset.i18n;
    if(el.tagName==='INPUT') el.placeholder=t(k);
    else if(el.tagName==='BUTTON'||el.tagName==='A') el.textContent=t(k);
    else el.textContent=t(k);
  });
  document.documentElement.lang = LANG==='zh-CN'?'zh-CN':LANG;
}
function renderLangSelector(){
  const opts=Object.keys(I18N).map(l=>'<option value="'+l+'"'+(l===LANG?' selected':'')+'>'+l+'</option>').join('');
  const el=document.getElementById('langSel');
  if(el){ el.innerHTML=opts; el.value=LANG; }
}
function setLang(l){
  if(!I18N[l]) return;
  LANG=l; localStorage.setItem('frc_lang',l);
  applyI18n(); renderLangSelector();
  renderStats(); renderImpact(); fillAwardScriptFilters(); renderAwardScripts(); renderOpen(); renderHall(); renderTech(); renderChampBox();
}


const SEASONS = DATA.seasons;   // {"2021":{game,impact[],open[],openNote?}, ...}
const HALL    = DATA.hall;      // [{y,n,nm,loc}]
const YEARS   = Object.keys(SEASONS).sort();   // ["2021".."2026"]
let AWARD_SCRIPTS = [];
let AWARD_META = {events:[]};
let awardVisible = 48;
const AWARD_CACHE = {};
let awardLoadToken = 0;

/* ---------- 技术资源（全局） ---------- */
const CATS = [
{id:"cad",nm:"机械与 CAD",en:"Mechanical Design & CAD"},
{id:"code",nm:"程序与软件",en:"Programming & Software"},
{id:"data",nm:"数据与策略",en:"Data & Strategy"},
{id:"learn",nm:"学习与教学",en:"Learning & Training"},
{id:"com",nm:"社区与平台",en:"Community & Platforms"}
];
const TECH = [
{cat:"cad",t:"Onshape for FRC",u:"https://www.onshape.com/edu/frc",d:"官方教育版免费 + FRC 零件库 + 场地模型，多数强队首选 CAD 平台"},
{cat:"cad",t:"FRCDesign.org",u:"https://www.frcdesign.org",d:"Onshape FRC 设计系统课程，新队员强烈推荐从这入门"},
{cat:"cad",t:"Onshape 学习中心",u:"https://learn.onshape.com",d:"官方免费课程，从零学 CAD"},
{cat:"cad",t:"GrabCAD FRC 社区",u:"https://grabcad.com/library",d:"搜索 FRC：整机、机构、零件、3D 打印件海量模型"},
{cat:"cad",t:"FIRST CAD Library",u:"https://www.firstcadlibrary.com",d:"COTS 零件 + 场地模型合集，设计必备素材库"},
{cat:"cad",t:"RoboChargers 暑期课程",u:"https://onshape4frc.com/robochargers-curriculum",d:"暑期 CAD 培训视频 + 课件（老牌免费课程）"},
{cat:"cad",t:"机制照片库 (Spectrum 3847)",u:"https://photos.spectrum3847.org/Robot-Mechanisms",d:"各种机构实拍照片，找灵感神器"},
{cat:"cad",t:"Chief Delphi CAD 版块",u:"https://www.chiefdelphi.com/c/technical/cad",d:"CAD 发布与设计讨论主阵地，各队 CAD 发布帖"},
{cat:"cad",t:"WCP 产品库",u:"https://www.wcproducts.com",d:"Swerve 模组 / 变速箱等 COTS 件，附 CAD 模型"},
{cat:"cad",t:"REV Robotics",u:"https://www.revrobotics.com",d:"REV 零件 + 官方 CAD + 教程"},
{cat:"code",t:"WPILib 官方文档",u:"https://docs.wpilib.org",d:"官方全套编程文档，Zero to Robot 从零入门"},
{cat:"code",t:"AdvantageKit",u:"https://github.com/Mechanical-Advantage/AdvantageKit",d:"日志 / 回放 / 仿真框架（6328 出品），现代 FRC 标准"},
{cat:"code",t:"AdvantageScope",u:"https://github.com/Mechanical-Advantage/AdvantageScope",d:"日志可视化 / 仿真工具"},
{cat:"code",t:"PathPlanner",u:"https://github.com/mjansen4857/pathplanner",d:"自动路径规划首选，GUI 可视化编辑"},
{cat:"code",t:"Choreo",u:"https://github.com/SleipnirGroup/Choreo",d:"基于物理仿真的路径规划（1678 等强队使用）"},
{cat:"code",t:"PhotonVision",u:"https://photonvision.org",d:"开源视觉定位方案（AprilTag / 目标追踪）"},
{cat:"code",t:"Limelight",u:"https://docs.limelightvision.io",d:"即插即用视觉硬件 + 文档"},
{cat:"code",t:"Elastic Dashboard",u:"https://github.com/Gold872/elastic-dashboard",d:"新一代机器人仪表盘（Shuffleboard 替代者）"},
{cat:"code",t:"CTRE Phoenix",u:"https://docs.ctr-electronics.com",d:"Talon FX / CANcoder 电机控制文档"},
{cat:"code",t:"REVLib",u:"https://docs.revrobotics.com",d:"SPARK MAX / NEO 电机控制文档"},
{cat:"code",t:"xRC Simulator",u:"https://xrcsimulator.org",d:"无硬件代码模拟器，编程入门神器"},
{cat:"code",t:"Java 入门（中文）",u:"https://www.runoob.com/java/java-tutorial.html",d:"中文 Java 教程，编程零基础友好"},
{cat:"data",t:"The Blue Alliance",u:"https://www.thebluealliance.com",d:"赛事 / 成绩 / 队伍数据总站，含 API"},
{cat:"data",t:"TBA API 文档",u:"https://www.thebluealliance.com/apidocs",d:"官方数据接口，可做数据分析 / 侦察工具"},
{cat:"data",t:"Statbotics",u:"https://statbotics.io",d:"现代化数据预测分析，看强队趋势"},
{cat:"data",t:"ScoutRadio (1678)",u:"https://github.com/frcteam1678/ScoutRadio",d:"开源数据收集系统，跟队侦察标配"},
{cat:"learn",t:"WPILib Zero to Robot",u:"https://docs.wpilib.org/en/stable/docs/zero-to-robot/introduction.html",d:"官方编程零基础路线图"},
{cat:"learn",t:"FRC 971 Workshops",u:"https://www.frc971.org/workshops",d:"设计 / CAD / 策略 / 材料全套课件"},
{cat:"learn",t:"Stryke Force 资源",u:"https://www.strykeforce.org/resources",d:"高质量培训课件合集"},
{cat:"learn",t:"Spectrum 推荐阅读",u:"https://www.spectrum3847.org/recommendedreading",d:"学长推荐书单 / 文章"},
{cat:"learn",t:"FIRST 技术资源库",u:"https://www.firstinspires.org/resource-library/frc/technical-resources",d:"FIRST 官方技术文档大全"},
{cat:"learn",t:"Open Alliance 目录帖",u:"https://www.chiefdelphi.com/t/2026-frc-open-alliance-information-and-directory/508112",d:"本赛季全部开源队伍实时目录"},
{cat:"com",t:"Chief Delphi",u:"https://www.chiefdelphi.com",d:"FRC 第一论坛，技术 / 策略 / 奖项讨论都在这里"},
{cat:"com",t:"FRC Discord",u:"https://discord.gg/frc",d:"全球 FRC 社区实时交流"},
{cat:"com",t:"r/FRC",u:"https://www.reddit.com/r/FRC/",d:"FRC 子版块，提问 / 分享"},
{cat:"com",t:"FIRST 官网",u:"https://www.firstinspires.org/robotics/frc",d:"规则 / 赛事 / 官方资源总入口"}
];
const TECH_EN = {
"https://www.onshape.com/edu/frc":["Onshape for FRC","Free Onshape Education access, FRC parts libraries, and field models on a widely used cloud CAD platform."],
"https://www.frcdesign.org":["FRCDesign.org","A structured Onshape and FRC mechanical-design course; an excellent starting point for new design students."],
"https://learn.onshape.com":["Onshape Learning Center","Official self-paced courses for learning Onshape from the fundamentals."],
"https://grabcad.com/library":["GrabCAD Community Library","Search for FRC robots, mechanisms, components, and 3D-printable parts shared by the community."],
"https://www.firstcadlibrary.com":["FIRST CAD Library","A consolidated library of COTS components and field models for robot design."],
"https://onshape4frc.com/robochargers-curriculum":["RoboChargers CAD Curriculum","A free summer CAD curriculum with training videos and lesson materials."],
"https://photos.spectrum3847.org/Robot-Mechanisms":["Robot Mechanism Photo Library (Spectrum 3847)","Reference photos of real FRC mechanisms for design research and inspiration."],
"https://www.chiefdelphi.com/c/technical/cad":["Chief Delphi CAD","The main community forum for CAD releases, design reviews, and mechanical discussion."],
"https://www.wcproducts.com":["WestCoast Products","COTS drivetrain, gearbox, and swerve components with downloadable CAD models."],
"https://www.revrobotics.com":["REV Robotics","REV components, official CAD files, product documentation, and tutorials."],
"https://docs.wpilib.org":["WPILib Documentation","Official FRC programming documentation, including the Zero to Robot learning path."],
"https://github.com/Mechanical-Advantage/AdvantageKit":["AdvantageKit","A logging, replay, and simulation framework from FRC 6328 for robust robot software workflows."],
"https://github.com/Mechanical-Advantage/AdvantageScope":["AdvantageScope","A desktop visualization and analysis tool for robot logs, live data, and simulation."],
"https://github.com/mjansen4857/pathplanner":["PathPlanner","Visual autonomous path planning and command generation for FRC robots."],
"https://github.com/SleipnirGroup/Choreo":["Choreo","Physics-based trajectory optimization used by high-performing FRC teams."],
"https://photonvision.org":["PhotonVision","Open-source AprilTag localization and vision-targeting software."],
"https://docs.limelightvision.io":["Limelight Documentation","Documentation for plug-and-play FRC vision hardware and software."],
"https://github.com/Gold872/elastic-dashboard":["Elastic Dashboard","A modern, customizable FRC robot dashboard and Shuffleboard alternative."],
"https://docs.ctr-electronics.com":["CTRE Phoenix Documentation","Motor-control and sensor documentation for Talon FX, CANcoder, and the Phoenix ecosystem."],
"https://docs.revrobotics.com":["REVLib Documentation","Programming reference for SPARK motor controllers, NEO motors, and REV hardware."],
"https://xrcsimulator.org":["xRC Simulator","A hardware-free robot simulator for practicing FRC driving and programming concepts."],
"https://www.runoob.com/java/java-tutorial.html":["Java Tutorial (Chinese)","A beginner-friendly Chinese-language Java tutorial for students new to programming."],
"https://www.thebluealliance.com":["The Blue Alliance","Competition, match, results, and team data with a public API."],
"https://www.thebluealliance.com/apidocs":["The Blue Alliance API Documentation","Public API documentation for analytics, scouting tools, and event-data applications."],
"https://statbotics.io":["Statbotics","Modern FRC performance analytics, predictions, rankings, and team trends."],
"https://github.com/frcteam1678/ScoutRadio":["ScoutRadio (FRC 1678)","An open-source scouting data collection and synchronization system."],
"https://docs.wpilib.org/en/stable/docs/zero-to-robot/introduction.html":["WPILib: Zero to Robot","The official step-by-step path from a new control system to a functioning robot project."],
"https://www.frc971.org/workshops":["FRC 971 Workshops","Workshop materials covering mechanical design, CAD, strategy, controls, and manufacturing."],
"https://www.strykeforce.org/resources":["Stryke Force Resources","A collection of high-quality team training materials and technical presentations."],
"https://www.spectrum3847.org/recommendedreading":["Spectrum Recommended Reading","A curated reading list of books, articles, and resources for FRC students and mentors."],
"https://www.firstinspires.org/resource-library/frc/technical-resources":["FIRST Technical Resources","FIRST’s official hub for FRC manuals, technical documentation, and support resources."],
"https://www.chiefdelphi.com/t/2026-frc-open-alliance-information-and-directory/508112":["Open Alliance Directory","The current season’s community-maintained directory of Open Alliance teams."],
"https://www.chiefdelphi.com":["Chief Delphi","The primary FRC community forum for technical, strategic, program, and award discussion."],
"https://discord.gg/frc":["FRC Discord","Real-time discussion and support across the global FRC community."],
"https://www.reddit.com/r/FRC/":["r/FRC","The FRC subreddit for questions, project updates, and community discussion."],
"https://www.firstinspires.org/robotics/frc":["FIRST Robotics Competition","The official entry point for FRC rules, events, program information, and resources."]
};

/* ---------- 名人堂额外链接（已知的开源/官网资源） ---------- */
const HALL_LINKS = {
254:{gh:"https://github.com/Team254",site:"https://www.team254.com"},
341:{site:"https://www.team341.com"},
1114:{gh:"https://github.com/Simbotics",site:"https://www.simbotics.org"},
1538:{site:"https://team1538.org"},
1902:{site:"https://www.explodingbacon.com"},
67:{site:"https://www.thehotteam.org"},
111:{site:"https://www.wildstang.org"},
5985:{site:"https://www.projectb.net.au"}
};

/* ---------- 各赛季世锦赛冠军补充说明 ---------- */
const CHAMP_FINALISTS = {
2026:[1880,9277,8393,359,9545]
};

/* ================================================================
   RENDER 逻辑
   ================================================================ */
const $ = id => document.getElementById(id);

let currentSeason = "2026";

/* ---- 工具 ---- */
function btn(cls,label,href,ext){
  return '<a class="btn '+cls+'" href="'+href+'" target="_blank" rel="noopener">'+label+'</a>';
}
function vlabel(u){
  return /instagram/i.test(u) ? 'Reel' : 'Video';
}
function essayUrl(y,n){
  // 2021–2026 essay 均遵循官方统一 URL 规律；个别队存有显式 e 则优先
  return 'https://info.firstinspires.org/hubfs/web/program/frc/awards/fia-essays/'+y+'/'+n+'.pdf';
}
function esc(value){
  return String(value==null?'':value).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}

/* ---- Tab 切换 ---- */
document.querySelectorAll('.tab-btn').forEach(b=>{
  b.addEventListener('click',()=>switchTab(b.dataset.tab));
});
function switchTab(tab){
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab));
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active',p.id==='tab-'+tab));
  window.scrollTo({top:0,behavior:'smooth'});
}

/* ---- 赛季选择键 ---- */
function renderSeasonList(){
  $('seasonList').innerHTML = YEARS.map(y=>{
    const s = SEASONS[y];
    return '<button class="season-btn'+(y===currentSeason?' active':'')+'" onclick="selectSeason(\''+y+'\')"><span class="yr">'+y+'</span><span class="gm">'+s.game+'</span></button>';
  }).join('');
}
function selectSeason(y){
  currentSeason = y;
  renderSeasonList();
  renderStats();
  renderImpact();
  loadAwardScripts(y);
  renderOpen();
  renderChampBox();
  try{ history.replaceState(null,'','#'+y); }catch(e){}
}

/* ---- 顶部统计 ---- */
function renderStats(){
  const s = SEASONS[currentSeason];
  $('stImpact').textContent = s.impact.length;
  $('stOpen').textContent = s.open.length;
  $('stHall').textContent = HALL.length;
  $('stTech').textContent = TECH.length;
}

/* ---- 世锦赛冠军框 ---- */
function renderChampBox(){
  const y = currentSeason;
  const champs = HALL.filter(h=>String(h.y)===String(y));
  if(!champs.length){ $('champBox').innerHTML=''; return; }
  const inner = champs.map(h=>'<b>'+h.n+' '+h.nm+'</b> ('+h.loc+')').join(' & ');
  const extra = CHAMP_FINALISTS[y] ? ' '+t('champ_finalists')+CHAMP_FINALISTS[y].join(' / ')+'.' : '';
  const btnTxt = champs.map(h=>btn('essay','Essay',essayUrl(y,h.n))).join(' ');
  $('champBox').innerHTML = '<b>'+y+' '+t('champ_prefix')+'</b> '+inner+'.'+extra+' '+btnTxt;
}

/* ---- Impact 智库（按当前赛季） ---- */
function impactFilters(){ return [
{id:"all",nm:t("imp_f_all")},
{id:"video",nm:t("imp_f_video")},
{id:"pres",nm:t("imp_f_pres")},
{id:"champ",nm:t("imp_f_champ")}
]; }
let impFilter = "all";
function renderImpact(){
  const y = currentSeason;
  const champNums = HALL.filter(h=>String(h.y)===String(y)).map(h=>h.n);
  const listAll = SEASONS[y].impact.map(t=>{
    // 给该赛季世锦赛冠军自动打上 champ 标记（2026 已含 finalist 标记则保留）
    if(!t.tag && champNums.includes(t.n)) return Object.assign({},t,{tag:"champ"});
    return t;
  });
  const q = ($('imSearch').value||'').toLowerCase().trim();
  const list = listAll.filter(t=>{
    if(q && !(String(t.n).includes(q)||(t.nm||'').toLowerCase().includes(q))) return false;
    if(impFilter==="video" && !t.v1 && !t.v2) return false;
    if(impFilter==="pres" && !t.pres && !t.fold && !t.pres2 && !t.fold2) return false;
    if(impFilter==="champ" && !t.tag) return false;
    return true;
  });
  $('imTitle').textContent = y+' · '+SEASONS[y].game+' — '+t('tab_impact');
  buildChips('imChips',impactFilters(),impFilter,'setImpFilter');
  $('impactTotal').textContent = listAll.length + t('teams_suffix');
  $('imCount').textContent = t('showing')+' ' + list.length + ' / ' + listAll.length;
  $('imGrid').innerHTML = list.map(t=>{
    const tag = t.tag==='champ' ? '<span class="badge gold">Champ Winner</span>' : t.tag==='finalist' ? '<span class="badge green">Finalist</span>' : '';
    const links = [btn('essay','Essay',essayUrl(y,t.n))];
    if(t.v1) links.push(btn('video',vlabel(t.v1),t.v1));
    if(t.v2) links.push(btn('video','Video 2',t.v2));
    if(t.pres) links.push(btn('pres','Pres',/^http/.test(t.pres)?t.pres:'https://drive.google.com/file/d/'+t.pres+'/view'));
    if(t.pres2) links.push(btn('pres','Pres 2','https://drive.google.com/file/d/'+t.pres2+'/view'));
    if(t.fold) links.push(btn('folder','Folder','https://drive.google.com/drive/folders/'+t.fold));
    if(t.fold2) links.push(btn('folder','Folder 2','https://drive.google.com/drive/folders/'+t.fold2));
    const events = (t.events||[]).map(e=>'<a href="'+e.url+'" target="_blank" rel="noopener">🏆 '+e.name+'</a>').join('<br>');
    return '<div class="card"><div class="num">'+t.n+' '+tag+'</div><div class="nm">'+(t.nm||'')+'</div>'+(t.loc?'<div class="loc">'+t.loc+'</div>':'')+(events?'<div class="loc impact-events">'+events+'</div>':'')+'<div class="links">'+links.join('')+'</div></div>';
  }).join('');
}
function buildChips(el,filters,state,fn){
  $(el).innerHTML = filters.map(f=>'<button class="chip'+(state===f.id?' active':'')+'" onclick="'+fn+'(\''+f.id+'\')">'+f.nm+'</button>').join('');
}
buildChips('imChips',impactFilters(),impFilter,'setImpFilter');
function setImpFilter(id){impFilter=id;renderImpact();}

/* ---- 全奖项颁奖词库 Demo ---- */
function fillAwardScriptFilters(){
  const selectedAward = $('asAward').value;
  const selectedEvent = $('asEvent').value;
  const awards = [...new Set(AWARD_SCRIPTS.map(x=>x.awardName))].sort();
  const events = [...new Map(AWARD_SCRIPTS.map(x=>[x.eventCode,x.eventName])).entries()];
  $('asAward').innerHTML = '<option value="">'+t('scripts_all_awards')+'</option>'+awards.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join('');
  $('asEvent').innerHTML = '<option value="">'+t('scripts_all_events')+'</option>'+events.map(x=>'<option value="'+esc(x[0])+'">'+esc(x[1])+'</option>').join('');
  $('asAward').value = selectedAward;
  $('asEvent').value = selectedEvent;
}
function renderAwardScripts(){
  $('asTitle').textContent = currentSeason+' · '+t('scripts_title');
  const q = ($('asSearch').value||'').toLowerCase().trim();
  const award = $('asAward').value;
  const event = $('asEvent').value;
  const list = AWARD_SCRIPTS.filter(x=>{
    const haystack = [x.teamNumber,x.teamName,x.awardName,x.eventName,x.script].join(' ').toLowerCase();
    return (!q||haystack.includes(q)) && (!award||x.awardName===award) && (!event||x.eventCode===event);
  }).sort((a,b)=>a.awardName.localeCompare(b.awardName)||a.teamNumber-b.teamNumber);
  const visible = list.slice(0,awardVisible);
  $('asTotal').textContent = AWARD_SCRIPTS.length+t('scripts_originals')+' · '+AWARD_META.events.length+t('scripts_events');
  $('asCount').textContent = t('scripts_showing')+' '+visible.length+' / '+list.length;
  $('asMore').hidden = visible.length>=list.length;
  $('asMore').textContent = t('scripts_load_more')+' ('+t('scripts_remaining')+' '+Math.max(0,list.length-visible.length)+')';
  $('asGrid').innerHTML = visible.length ? visible.map(x=>
    '<article class="card script-card">'+
      '<div class="award-name">'+esc(x.awardName)+'</div>'+
      '<div class="num">'+esc(x.teamNumber)+'</div>'+
      '<div class="nm">'+esc(x.teamName)+'</div>'+
      '<blockquote lang="en">'+esc(x.script)+'</blockquote>'+
      '<div class="script-meta"><span class="badge purple">'+esc(x.eventCode)+'</span><span>'+esc(x.eventName)+'</span><span>· '+t('scripts_official_en')+'</span></div>'+
      '<div class="links">'+btn('essay',t('scripts_source'),x.source)+'</div>'+
    '</article>'
  ).join('') : '<div class="card"><div class="note">'+t('scripts_empty')+'</div></div>';
}
function resetAwardScripts(){awardVisible=48;renderAwardScripts();}
function showMoreAwardScripts(){awardVisible+=48;renderAwardScripts();}
async function loadAwardScripts(year=currentSeason){
  const token = ++awardLoadToken;
  $('asTitle').textContent = year+' · '+t('scripts_title');
  $('asTotal').textContent = t('scripts_loading');
  $('asGrid').innerHTML = '<div class="card"><div class="note">'+year+' · '+t('scripts_loading')+'</div></div>';
  if(year==='2021'){
    AWARD_SCRIPTS=[]; AWARD_META={events:[]};
    fillAwardScriptFilters();
    $('asTotal').textContent=t('scripts_no_data');
    $('asCount').textContent=''; $('asMore').hidden=true;
    $('asLead').textContent=t('scripts_no_data_lead');
    $('asGrid').innerHTML='<div class="warn-box">'+t('scripts_no_data_box')+'</div>';
    return;
  }
  try{
    let payload = AWARD_CACHE[year];
    if(!payload){
      let lastError;
      for(let attempt=1;attempt<=3;attempt++){
        try{
          const response = await fetch('data/award-scripts/'+year+'.json',{cache:'no-store'});
          if(!response.ok) throw new Error('HTTP '+response.status);
          payload = await response.json();
          break;
        }catch(error){
          lastError=error;
          if(attempt<3) await new Promise(resolve=>setTimeout(resolve,attempt*500));
        }
      }
      if(!payload) throw lastError||new Error('unknown load error');
      AWARD_CACHE[year]=payload;
    }
    if(token!==awardLoadToken) return;
    AWARD_SCRIPTS = payload.records||[];
    AWARD_META = payload;
    $('asLead').textContent = t('scripts_lead');
    fillAwardScriptFilters();
    resetAwardScripts();
  }catch(error){
    if(token!==awardLoadToken) return;
    $('asTotal').textContent = t('scripts_load_failed');
    $('asGrid').innerHTML = '<div class="warn-box">'+year+' · '+t('scripts_load_failed')+'<button class="chip" type="button" style="margin-left:8px" onclick="loadAwardScripts(\''+year+'\')">'+t('scripts_retry')+'</button></div>';
  }
}

/* ---- 开源队伍（按当前赛季） ---- */
function openFilters(){ return [
{id:"all",nm:t("f_all")},
{id:"cad",nm:t("f_cad")},
{id:"code",nm:t("f_code")},
{id:"video",nm:t("f_video")},
{id:"site",nm:t("f_site")}
]; }
let opFilter = "all";
let opSort = localStorage.getItem('frc_open_sort') === 'team' ? 'team' : 'hot';
function renderOpSort(){
  const el = $('opSort');
  el.setAttribute('aria-label',t('sort_label'));
  el.innerHTML = [
    {id:'hot',label:t('sort_hot')},
    {id:'team',label:t('sort_team')}
  ].map(option=>'<button type="button" class="sort-btn'+(opSort===option.id?' active':'')+'" aria-pressed="'+(opSort===option.id)+'" onclick="setOpSort(\''+option.id+'\')">'+option.label+'</button>').join('');
}
function renderOpen(){
  const y = currentSeason;
  const listAll = SEASONS[y].open;
  const q = ($('opSearch').value||'').toLowerCase().trim();
  const list = listAll.filter(t=>{
    if(opFilter==="cad" && !t.cad) return false;
    if(opFilter==="code" && !t.gh) return false;
    if(opFilter==="video" && !t.yt && !t.ph) return false;
    if(opFilter==="site" && !t.site) return false;
    if(q && !(String(t.n).includes(q)||(t.nm||'').toLowerCase().includes(q)||(t.tags||[]).some(tag=>tag.toLowerCase().includes(q)))) return false;
    return true;
  }).sort((a,b)=>opSort==='team'
    ? Number(a.n)-Number(b.n) || (a.nm||'').localeCompare(b.nm||'')
    : (Number(b.views)||0)-(Number(a.views)||0) || Number(a.n)-Number(b.n));
  renderOpSort();
  buildChips('opChips',openFilters(),opFilter,'setOpFilter');
  $('opTitle').textContent = y+' · '+SEASONS[y].game+' — '+t('tab_open');
  $('openTotal').textContent = listAll.length + t(opSort==='team'?'teams_sorted_number':'teams_sorted');
  $('opCount').textContent = t('showing')+' ' + list.length + ' / ' + listAll.length;
  const siteLabel = t('site_label');
  const cadPreviewLabel = t('cad_preview');
  const viewsSuffix = t('views_suffix');
  $('opGrid').innerHTML = list.map(team=>{
    const links = [];
    if(team.cad) links.push(btn('cad','CAD',team.cad));
    if(team.gh) links.push(btn('gh','Code',team.gh));
    if(team.yt) links.push(btn('video','YouTube',team.yt));
    if(team.ph) links.push(btn('pres','Photos',team.ph));
    if(team.site) links.push(btn('site',siteLabel,team.site));
    if(team.cd) links.push(btn('cd','Build Thread',team.cd));
    // CAD preview 图标：有 CAD 的队伍在队号旁标一个小图标
    const cadIcon = team.cad ? '<a class="cad-prev" href="'+team.cad+'" target="_blank" rel="noopener" title="'+cadPreviewLabel+'"><span class="cad-dot"></span>3D</a>' : '';
    // 程序方向标签
    const tagKeys = {"底盘":"tag_chassis","自瞄":"tag_vision","吸取":"tag_intake","射击":"tag_shooter","爬升":"tag_climb","自动":"tag_auto","侦察":"tag_scout"};
    const tags = (team.tags||[]).map(x=>'<span class="tag-chip">'+esc(tagKeys[x]?window.t(tagKeys[x]):x)+'</span>').join('');
    // 访问量
    const views = team.views ? '<span class="views">'+(team.views>=1000?(team.views/1000).toFixed(1)+'k'+viewsSuffix:team.views+viewsSuffix)+'</span>' : '';
    return '<div class="card"><div class="num">'+team.n+cadIcon+views+'</div><div class="nm">'+(team.nm||'')+'</div>'+(tags?'<div>'+tags+'</div>':'')+'<div class="links">'+links.join('')+'</div></div>';
  }).join('');
  // 赛季备注（如 2021 虚拟赛季说明）
  $('opNote').innerHTML = SEASONS[y].openNote ? '<div class="info-box">'+SEASONS[y].openNote+'</div>' : '';
}
buildChips('opChips',openFilters(),opFilter,'setOpFilter');
function setOpFilter(id){opFilter=id;renderOpen();}
function setOpSort(id){
  if(id!=='hot' && id!=='team') return;
  opSort=id;
  localStorage.setItem('frc_open_sort',id);
  renderOpen();
}

/* ---- 名人堂（全局） ---- */
function renderHall(){
  $('hallTotal').textContent = HALL.length + t('hall_count');
  $('hallGrid').innerHTML = HALL.slice().reverse().map(h=>{
    const links = [btn('team',t('team_page'),'https://frc-events.firstinspires.org/team/'+h.n)];
    const extra = HALL_LINKS[h.n]||{};
    if(extra.gh) links.push(btn('gh','GitHub',extra.gh));
    if(extra.site) links.push(btn('site',t('site_label'),extra.site));
    return '<div class="card"><div class="num"><span class="badge gold">'+h.y+'</span> '+h.n+'</div><div class="nm">'+h.nm+'</div><div class="loc">'+(h.loc||'')+'</div><div class="links">'+links.join('')+'</div></div>';
  }).join('');
}

/* ---- 技术资源 ---- */
function techFilters(){
  return [{id:"all",nm:LANG==='en'?t('f_all'):"全部"}].concat(CATS.map(c=>({id:c.id,nm:LANG==='en'?c.en:c.nm})));
}
let tcFilter = "all";
function renderTech(){
  const list = TECH.filter(t=>tcFilter==="all"||t.cat===tcFilter);
  $('techTotal').textContent = TECH.length + t('tech_count');
  $('tcCount').textContent = t('showing')+' ' + list.length + ' / ' + TECH.length;
  const catName = id => { const c=CATS.find(c=>c.id===id)||{}; return LANG==='en'?(c.en||c.nm):(c.nm||''); };
  $('tcGrid').innerHTML = list.map(item=>{
    const localized = LANG==='en' ? TECH_EN[item.u] : null;
    const title = localized ? localized[0] : item.t;
    const description = localized ? localized[1] : item.d;
    return '<div class="card"><div class="nm">'+title+' <span class="badge gray" style="margin-left:6px">'+catName(item.cat)+'</span></div><div class="note">'+description+'</div><div class="links">'+btn('essay',t('resource_open'),item.u)+'</div></div>';
  }).join('');
  buildChips('tcChips',techFilters(),tcFilter,'setTcFilter');
}
buildChips('tcChips',techFilters(),tcFilter,'setTcFilter');
function setTcFilter(id){tcFilter=id;renderTech();}

/* ---- 初始化 ---- */
(function init(){
  const h = (location.hash||'').replace('#','');
  if(SEASONS[h]) currentSeason = h;
  applyI18n(); renderLangSelector();
  renderSeasonList();
  renderStats();
  renderChampBox();
  renderImpact();
  loadAwardScripts(currentSeason);
  renderOpen();
  renderHall();
  renderTech();
})();
