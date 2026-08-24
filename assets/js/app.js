/* ---------- i18n ---------- */
Object.assign(I18N.en,{tab_tsite:"Team Resource Sites",tab_style:"Season Style Guide",ts_head:"Team Resource Sites",ts_lead:"Independent technical sites built and maintained by FRC teams — CAD, electrical, programming, and training resources.",ts_n:"Team",ts_visit:"Visit site",ts_all:"All",ts_cat_cad:"CAD / Mechanical",ts_cat_elect:"Electrical",ts_cat_code:"Programming",ts_cat_train:"Training",ts_community:"Community project",sg_head:"Season Style Guide",sg_lead:"Official brand assets and visual guides for each season — style guides, logos, social templates, and wallpapers released by FIRST.",sg_open:"Official page",sg_pdf:"PDF",sg_zip:"ZIP",sg_ppt:"PPT",sg_img:"Image",sg_count:" sites",sg_count2:" resources",scripts_award_filter:"Filter by award",scripts_event_filter:"Filter by event"});
Object.assign(I18N['zh-CN'],{tab_open:"队伍公开资料",tab_tech:"技术资源库",tab_tsite:"队伍技术站",tab_style:"赛季风格指南",ts_head:"队伍技术站",ts_lead:"由 FRC 队伍或社区建设并持续维护的独立技术网站，涵盖 CAD、电气、编程与综合培训。",ts_n:"队伍",ts_visit:"访问网站",ts_all:"全部",ts_cat_cad:"CAD / 机械",ts_cat_elect:"电气",ts_cat_code:"编程",ts_cat_train:"综合培训",ts_community:"社区项目",sg_head:"赛季风格指南",sg_lead:"各赛季官方品牌素材与视觉规范，含风格指南、Logo、社媒模板与壁纸，方便平面设计师与队伍宣传查找。",sg_open:"官方入口",sg_pdf:"PDF",sg_zip:"ZIP",sg_ppt:"PPT",sg_img:"图片",sg_count:" 个站点",sg_count2:" 项资源",scripts_award_filter:"按奖项筛选",scripts_event_filter:"按赛事筛选"});
Object.assign(I18N['zh-TW'],{tab_open:"隊伍公開資源",tab_tech:"技術資源庫",tab_tsite:"隊伍建站",tab_style:"賽季風格指南",ts_head:"隊伍建站",ts_lead:"由 FRC 隊伍自建、持續更新、面向社群的獨立技術站點：CAD／電氣／程式／綜合培訓。",ts_n:"隊伍",ts_visit:"造訪網站",ts_all:"全部",ts_cat_cad:"CAD／機械",ts_cat_elect:"電氣",ts_cat_code:"程式",ts_cat_train:"綜合培訓",ts_community:"社群專案",sg_head:"賽季風格指南",sg_lead:"各賽季官方品牌素材與視覺規範，含風格指南、Logo、社群模板與桌布。",sg_open:"官方入口",sg_pdf:"PDF",sg_zip:"ZIP",sg_ppt:"PPT",sg_img:"圖片",sg_count:" 個站點",sg_count2:" 項資源",scripts_award_filter:"依獎項篩選",scripts_event_filter:"依賽事篩選"});
const SUPPORTED_LANGS=['en','zh-CN','zh-TW'];
const savedLang=localStorage.getItem('frc_lang');
let LANG=SUPPORTED_LANGS.includes(savedLang)?savedLang:'en';
Object.assign(I18N.en,{sort_hot:"By popularity",sort_team:"By team number",teams_sorted_number:" teams (team number order)",sort_label:"Team-resource sorting"});
Object.assign(I18N['zh-CN'],{sort_hot:"按热度排序",sort_team:"按队号排序",teams_sorted_number:" 支队伍（按队号顺序）",sort_label:"队伍公开资料排序方式"});
Object.assign(I18N['zh-TW'],{sort_hot:"依熱度排序",sort_team:"依隊號排序",teams_sorted_number:" 支隊伍（依隊號順序）",sort_label:"隊伍公開資源排序方式"});
Object.assign(I18N.ja,{sort_hot:"人気順",sort_team:"チーム番号順",teams_sorted_number:"チーム（チーム番号順）",sort_label:"チーム公開資料の並び順"});
Object.assign(I18N.ko,{sort_hot:"인기순",sort_team:"팀 번호순",teams_sorted_number:"팀(팀 번호순)",sort_label:"팀 공개 자료 정렬"});
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
  hero_sub:"A multi-season archive of Impact Award resources, team-published CAD, code and Build Threads, Hall of Fame teams, and technical resources from 2021–2026.",
  select_season:"Choose a season",tab_home:"Overview",tab_impact:"Impact Award Archive",tab_open:"Team-Published Resources",tab_tech:"Technical Resources",
  stat_impact:"Impact Award team entries",stat_open:"Team resource entries",stat_hall:"Hall of Fame teams",stat_tech:"Technical resources",
  home_what:"Explore the archive",
  home_lead:"Browse six seasons of Impact Award essays, videos, and presentations; team-published CAD, code and Build Threads; the official FIRST Hall of Fame; and a curated collection of technical and learning resources.",
  home_usage:"Open the Impact Award Archive, Award Scripts, or Team-Published Resources to choose a season. Browse team resources by Build Thread views or team number, and filter Technical Resources by category. Add an anchor such as #2024 to share a specific season.",
  home_impact_t:"Impact Award Archive",home_impact_d:"Essays, videos, and presentations from 514 award-winning team entries across the 2021–2026 seasons.",
  home_open_t:"Team-Published Resources",home_open_d:"2,092 team-published resource entries across six seasons, including Build Threads, CAD, code, and video links.",
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
  c1:"See the GitHub README for contribution and data-maintenance instructions.",c2:"Submit new Impact Award or team-published resource records through GitHub.",
  c3:"Contributions of team GitHub, Onshape, YouTube, and other public resource links are welcome.",c4:"Found an error or a missing resource? Open an issue and help improve the archive.",
  r1:"Add Impact Award data for the 2020 season and earlier.",r2:"Add more awards, including Dean’s List, Woodie Flowers, and Engineering Excellence.",r3:"Expand the China team section and Chinese-language open-source tutorials.",r4:"Build a mechanism-based index of team-published CAD and code.",
  footer_copy:"FIRSTHub · FRC Open Resource Library · community-built resources for the 2021–2026 FRC seasons · open data, open collaboration",
  tag_chassis:"Drivetrain",tag_vision:"Vision",tag_intake:"Intake",tag_shooter:"Shooter",tag_climb:"Climb",tag_auto:"Autonomous",tag_scout:"Scouting",lang_label:"Language",
  directory_zh:"Chinese search directory",directory_en:"English search directory",sitemap_label:"Sitemap",resource_open:"Open resource",team_page:"FIRST team page",cad_preview:"CAD preview",views_suffix:" views"
});
Object.assign(I18N['zh-CN'],{site_title:"FRC 智库网",site_subtitle:"FIRSTHub · FRC Open Resource Library",built_by:"由 FRC Team 5449 建设 · 面向整个 FRC 社区",footer_built_by:"由 FRC Team 5449 建设",directory_zh:"中文搜索目录",directory_en:"英文搜索目录",sitemap_label:"站点地图",resource_open:"打开资源",team_page:"FIRST 队伍页",cad_preview:"CAD 预览",hero_sub:"汇集 2021–2026 六个赛季的 Impact Award 获奖材料、队伍公开的 CAD / 代码 / Build Thread、名人堂队伍和技术资源。",stat_open:"赛季队伍资料",home_lead:"这里汇集六个赛季的 Impact Award 获奖材料、队伍公开的 CAD / 代码 / Build Thread、FIRST 官方名人堂，以及常用工具和学习资源。切换上方赛季即可更新内容。",home_usage:"用法：点赛季键切换年份；在「Impact 智库」查看获奖材料；在「队伍公开资料」中按 Build Thread 访问量或队号浏览 CAD、代码和视频；在「技术资源」中按分类查找工具。网址后加 #2024 这类锚点即可分享指定赛季。",home_open_d:"六赛季共 2,092 条由队伍公开的 Build Thread、CAD、代码和视频资料，支持检索与排序。",c2:"Impact / 队伍公开资料：通过 GitHub 提交新的队伍记录。",r4:"按机构类型建立队伍公开 CAD / 代码速查。"});
Object.assign(I18N['zh-TW'],{hero_sub:"彙整 2021–2026 六個賽季的 Impact Award 獲獎資料、隊伍公開的 CAD／程式碼／Build Thread、名人堂隊伍與技術資源。",stat_open:"賽季隊伍資源",home_open_d:"六個賽季共 2,092 筆由隊伍公開的 Build Thread、CAD、程式碼與影片資源，可搜尋與排序。",c2:"Impact／隊伍公開資源：透過 GitHub 提交新的隊伍記錄。",r4:"依機構類型建立隊伍公開 CAD／程式碼索引。"});
const TEAM_RESOURCE_LABELS={ja:"チーム公開資料",ko:"팀 공개 자료",'zh-TW':"隊伍公開資源",ms:"Sumber Diterbitkan Pasukan",de:"Von Teams veröffentlichte Ressourcen",nl:"Door teams gepubliceerde bronnen",ru:"Материалы команд",pl:"Materiały publikowane przez zespoły",en:"Team-Published Resources",'zh-CN':"队伍公开资料",es:"Recursos publicados por equipos",pt:"Recursos publicados por equipes",fr:"Ressources publiées par les équipes",it:"Risorse pubblicate dai team",tr:"Takımların Yayınladığı Kaynaklar",he:"משאבים שפורסמו על ידי קבוצות",ar:"موارد نشرتها الفرق",hi:"टीमों द्वारा प्रकाशित संसाधन",th:"แหล่งข้อมูลที่ทีมเผยแพร่",vi:"Tài nguyên do đội công bố",id:"Sumber Daya yang Diterbitkan Tim"};
Object.entries(TEAM_RESOURCE_LABELS).forEach(([lang,label])=>Object.assign(I18N[lang],{tab_open:label,home_open_t:label}));
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
  document.querySelectorAll('[data-i18n-aria]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.i18nAria)));
  document.documentElement.lang = LANG==='zh-CN'?'zh-CN':LANG;
}
function renderLangSelector(){
  const names={en:'English','zh-CN':'简体中文','zh-TW':'繁體中文'};
  const opts=SUPPORTED_LANGS.map(l=>'<option value="'+l+'"'+(l===LANG?' selected':'')+'>'+names[l]+'</option>').join('');
  const el=document.getElementById('langSel');
  if(el){ el.innerHTML=opts; el.value=LANG; }
}
function setLang(l){
  if(!I18N[l]) return;
  LANG=l; localStorage.setItem('frc_lang',l);
  applyI18n(); renderLangSelector();
  renderStats(); renderImpact(); fillAwardScriptFilters(); renderAwardScripts(); renderOpen(); renderHall(); renderTech(); renderTsChips(); renderTsite(); renderSeasonGuide(); renderChampBox();
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
  $('seasonBar').hidden=!['impact','scripts','open'].includes(tab);
  // 修复移动端：切换后滚动到内容区顶部而非页面最顶，避免每次点导航都跳回首屏
  const main = document.querySelector('main');
  if(main){
    const top = Math.max(0, main.getBoundingClientRect().top + window.pageYOffset - 8);
    window.scrollTo({top,behavior:'smooth'});
  } else {
    window.scrollTo({top:0,behavior:'smooth'});
  }
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

/* ---- 队伍建设站（全局独立栏目） ---- */
const TS_CATS = [
{id:"all",key:"ts_all"},
{id:"cad",key:"ts_cat_cad"},
{id:"elect",key:"ts_cat_elect"},
{id:"code",key:"ts_cat_code"},
{id:"train",key:"ts_cat_train"}
];
const TEAM_SITES = [
{cat:"elect",n:"",t:"FRCElectrical",u:"https://frcelectrical.org",d:"社区共建的 FRC 电气培训百科：电路、元件、电源分配等基础知识。",dEn:"A community-maintained FRC electrical reference covering circuits, components, and power distribution.",community:true},
{cat:"elect",n:"2928",t:"2928 FRC Electrical Training",u:"https://2928-frc-electrical-training.readthedocs.io",d:"FRC 2928 的电气培训文档（PDH、roboRIO、传感器）。",dEn:"FRC 2928's electrical training documentation for the PDH, roboRIO, sensors, and wiring."},
{cat:"code",n:"2928",t:"2928 FRC Programmer Training",u:"https://2928-frc-programmer-training.readthedocs.io",d:"FRC 2928 的编程培训文档（Romi、Swerve Drive、机器学习）。",dEn:"FRC 2928's programming curriculum covering Romi, swerve drive, and machine learning."},
{cat:"train",n:"3847",t:"Spectrum 3847 Training",u:"https://training.spectrum3847.org",d:"FRC 3847 的综合培训课程：FRC 概述、竞赛和赛事角色等。",dEn:"FRC 3847's general training curriculum covering FRC, competition, and event roles."},
{cat:"cad",n:"3847",t:"Spectrum CAD Collection",u:"https://cadcollection.spectrum3847.org",d:"FRC 3847 的 CAD 模型资源站，支持浏览与提交机器人 CAD。",dEn:"FRC 3847's collection for browsing and submitting robot CAD models."},
{cat:"train",n:"1678",t:"Citrus Circuits Fall Workshops",u:"https://www.citruscircuits.org/fall-workshops",d:"FRC 1678 多年秋季工作坊，汇集技术分享与培训材料。",dEn:"FRC 1678's multi-year fall workshops and technical training materials."},
{cat:"train",n:"971",t:"FRC 971 Workshops",u:"https://www.spartanrobotics.org/workshops",d:"FRC 971 的 Workshop 课件：机械、CAD、策略、编程与制造。",dEn:"FRC 971 workshop materials covering mechanical design, CAD, strategy, programming, and manufacturing."},
{cat:"code",n:"971",t:"FRC 971 Training Wiki",u:"https://github.com/frc971/training-2026/wiki",d:"FRC 971 软件培训 Wiki（Git、WPILib、子系统与 PID）。",dEn:"FRC 971's software training wiki covering Git, WPILib, subsystems, and PID control."}
];
let tsFilter = "all";
const TS_TEAM_EN={on:"Team",off:""};
function renderTsite(){
  const ZH = LANG==='zh-CN'||LANG==='zh-TW';
  const list = TEAM_SITES.filter(s=>tsFilter==="all"||s.cat===tsFilter);
  $('tsCount').textContent = list.length+' / '+TEAM_SITES.length+t('sg_count');
  const catName = cid=>t((TS_CATS.find(x=>x.id===cid)||{}).key||'ts_all');
  $('tsGrid').innerHTML = list.map(s=>{
    const badge = s.community
      ? '<span class="badge purple">'+t('ts_community')+'</span>'
      : '<span class="badge blue">'+s.n+'</span>';
    return '<div class="card"><div class="num">'+badge+' <span class="badge teal">'+catName(s.cat)+'</span></div><div class="nm">'+esc(s.t)+'</div><div class="note">'+esc(ZH?s.d:(s.dEn||s.d))+'</div><div class="links">'+btn('site',t('ts_visit'),s.u)+'</div></div>';
  }).join('');
}
function renderTsChips(){
  $('tsChips').innerHTML = TS_CATS.map(c=>'<button class="chip'+(tsFilter===c.id?' active':'')+'" onclick="setTsFilter(\''+c.id+'\')">'+t(c.key)+'</button>').join('');
}
function setTsFilter(id){tsFilter=id;renderTsChips();renderTsite();}

/* ---- 赛季风格指南（全局独立栏目） ---- */
const STYLE = {
"2026":{game:"FIRST AGE · REBUILT",note:"2026 赛季素材最完整，含完整 Style Guide、Logo、PPT 模板、社媒模板与壁纸。",noteEn:"The 2026 collection is the most complete, with style guides, logos, a presentation template, social templates, and wallpapers.",list:[
{t:"Style Guide (PDF)",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/FIRST_AGE_Styleguide_.pdf",k:"pdf"},
{t:"FRC Style Guide",u:"https://info.firstinspires.org/hubfs/2026%20Season/Season%20Assets/FIRST_AGE-FRC-style-guide.pdf",k:"pdf"},
{t:"Logo Files (zip)",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/FIRST_AGE-logos.zip",k:"zip"},
{t:"Social Media Toolkit",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/first_age_social_media_toolkit.pdf",k:"pdf"},
{t:"社媒图形模板",tEn:"Social Graphic Templates",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/age_frc_social_media_toolkit.pdf",k:"pdf"},
{t:"PowerPoint 模板",tEn:"PowerPoint Template",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/FIRST_AGE-powerpoint-template.pptx",k:"ppt"},
{t:"壁纸 · Light",tEn:"Wallpaper · Light",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/FIRST_AGE-wallpaper-light.jpg",k:"img"},
{t:"壁纸 · Dark",tEn:"Wallpaper · Dark",u:"https://www.firstinspires.org/hubfs/2026%20Season/Season%20Assets/FIRST_AGE-wallpaper-dark.jpg",k:"img"} ]},
"2025":{game:"REEFSCAPE · FIRST DIVE",note:"官方社媒工具包包含 Logo 与风格规范；官方页面提供其他赛季资料入口。",noteEn:"The official social media toolkit includes logo and style guidance; FIRST's official pages provide access to other season materials.",list:[
{t:"Social Media Toolkit（含 Logo 与风格规范）",tEn:"Social Media Toolkit (Logo & Style)",u:"https://info.firstinspires.org/hubfs/2025%20Season/Season%20Assets/FIRST_DIVE_Social-media-toolkit.pdf",k:"pdf"},
{t:"赛季主题页 · 素材入口",tEn:"Game & Season · Asset Portal",u:"https://www.firstinspires.org/robotics/frc/game-and-season",k:"ext"},
{t:"Season Materials 官方资料",tEn:"Official Season Materials",u:"https://www.firstinspires.org/resources/library/frc/season-materials",k:"ext"} ]},
"2024":{game:"CRESCENDO",note:"暂未找到可可靠核验的 CRESCENDO 专属风格指南直链；以下保留 FIRST 官方品牌与赛季资料入口，不混用其他赛季素材。",noteEn:"No reliable direct CRESCENDO style-guide link has been verified. These official FIRST brand and season-resource pages are provided without substituting another season's assets.",list:[
{t:"FIRST 品牌与素材",tEn:"FIRST Brand & Assets",u:"https://www.firstinspires.org/about/brand",k:"ext"},
{t:"赛季主题页 · 素材入口",tEn:"Game & Season · Asset Portal",u:"https://www.firstinspires.org/robotics/frc/game-and-season",k:"ext"},
{t:"Season Materials 官方资料",tEn:"Official Season Materials",u:"https://www.firstinspires.org/resources/library/frc/season-materials",k:"ext"} ]},
"2023":{game:"CHARGED UP",note:"官方志愿者页面提供壁纸与社媒图等数字素材。",noteEn:"An official FIRST volunteer page provides digital assets such as wallpapers and social graphics.",list:[
{t:"数字内容（壁纸 / 社媒图）",tEn:"Digital Assets (Wallpapers / Social Graphics)",u:"https://info.firstinspires.org/volunteers-gear-up-for-first-energize-season",k:"ext"},
{t:"赛季主题页 · 素材入口",tEn:"Game & Season · Asset Portal",u:"https://www.firstinspires.org/robotics/frc/game-and-season",k:"ext"},
{t:"Season Materials 官方资料",tEn:"Official Season Materials",u:"https://www.firstinspires.org/resources/library/frc/season-materials",k:"ext"} ]},
"2022":{game:"RAPID REACT",note:"官方 Style Guide 含标志间距、颜色版本、缩放规范等完整品牌规范。",noteEn:"The official style guide covers logo clear space, color variants, scaling, and other brand rules.",list:[
{t:"FRC RAPID REACT Style Guide",u:"https://info.firstinspires.org/hubfs/2022%20Season%20Assets/free-season-assets/fr%20-%20rapid%20react/firstforward-frc-rapidreact-styleguide.pdf",k:"pdf"},
{t:"赛季主题页 · 素材入口",tEn:"Game & Season · Asset Portal",u:"https://www.firstinspires.org/robotics/frc/game-and-season",k:"ext"},
{t:"Season Materials 官方资料",tEn:"Official Season Materials",u:"https://www.firstinspires.org/resources/library/frc/season-materials",k:"ext"} ]},
"2021":{game:"INFINITE RECHARGE",note:"2021 为虚拟赛季，官方直接素材较少，主要提供赛季资料与 At Home 手册入口。",noteEn:"The virtual 2021 season has fewer direct brand assets; official season materials and the At Home manual are provided instead.",list:[
{t:"赛季主题页 · 素材入口",tEn:"Game & Season · Asset Portal",u:"https://www.firstinspires.org/robotics/frc/game-and-season",k:"ext"},
{t:"Season Materials 官方资料",tEn:"Official Season Materials",u:"https://www.firstinspires.org/resources/library/frc/season-materials",k:"ext"},
{t:"At Home 手册（官方 PDF）",tEn:"At Home Manual (Official PDF)",u:"https://firstfrc.blob.core.windows.net/frc2021/Manual/AtHomeManualSections/2021AtHomeChallengesManualSection02.pdf",k:"pdf"} ]}
};
let sgSeason = "2026";
const SG_LABEL = k=>{const m={pdf:t('sg_pdf'),zip:t('sg_zip'),ppt:t('sg_ppt'),img:t('sg_img')};return m[k]||k.toUpperCase();};
function renderSeasonGuide(){
  const ZH = LANG==='zh-CN'||LANG==='zh-TW';
  $('sgSeasonList').innerHTML = Object.keys(STYLE).sort().reverse().map(y=>{
    const s=STYLE[y];
    return '<button class="season-btn'+(y===sgSeason?' active':'')+'" onclick="setSeasonGuide(\''+y+'\')"><span class="yr">'+y+'</span><span class="gm">'+s.game+'</span></button>';
  }).join('');
  const s = STYLE[sgSeason];
  $('sgCount').textContent = s.list.length + t('sg_count2');
  $('sgNote').textContent = ZH ? s.note : (s.noteEn||s.note);
  $('sgGrid').innerHTML = s.list.map(x=>{
    const isExt = x.k==='ext';
    const label = isExt ? t('sg_open') : SG_LABEL(x.k);
    return '<div class="card"><div class="num"><span class="badge gray">'+(isExt?'WEB':(x.k==='img'?t('sg_img'):x.k.toUpperCase()))+'</span></div><div class="nm">'+esc(ZH?x.t:(x.tEn||x.t))+'</div><div class="links">'+btn(isExt?'site':'essay',label,x.u)+'</div></div>';
  }).join('');
}
function setSeasonGuide(y){sgSeason=y;renderSeasonGuide();}

/* ---- 初始化 ---- */
const FTC_DEMO_DATA={
  awards:[
    {season:'2025',type:'official',meta:'OFFICIAL · 2025–2026',title:'FTC Season Awards',desc:'按日期汇总本赛季全部官方赛事奖项，可继续按奖项类别筛选。',source:'FIRST · FTC Events',url:'https://ftc-events.firstinspires.org/2025/awards'},
    {season:'2025',type:'official',meta:'OFFICIAL EVENT · MISSOURI',title:'St. Louis Meet Awards',desc:'示例赛事页：包含 Inspire、Think、Connect、Control、Design、Innovate 和联盟奖项。',source:'FIRST · FTC Events',url:'https://ftc-events.firstinspires.org/2025/USMOKSSTLMLT/awards'},
    {season:'2025',type:'official',meta:'OFFICIAL · CHINA',title:'China FTC Shanghai #1',desc:'中国区公开结果示例：Inspire Award 为 25720，Think Award 为 22389。',source:'FIRST · FTC Events season index',url:'https://ftc-events.firstinspires.org/2025/awards?id=22'},
    {season:'2025',type:'manual',meta:'OFFICIAL RULEBOOK',title:'DECODE Award Criteria',desc:'当前赛季评审奖项、作品集提交方式和晋级规则的官方依据。',source:'FIRST · Competition Manual',url:'https://ftc-resources.firstinspires.org/ftc/archive/2026/game/cm-html/DECODE_Competition_Manual_TU32.htm'},
    {season:'2024',type:'official',meta:'OFFICIAL · 2024–2025',title:'INTO THE DEEP Season Awards',desc:'2024–2025 赛季官方赛事奖项总索引。',source:'FIRST · FTC Events',url:'https://ftc-events.firstinspires.org/2024/awards'},
    {season:'2023',type:'official',meta:'OFFICIAL · 2023–2024',title:'CENTERSTAGE Season Awards',desc:'2023–2024 赛季官方赛事奖项总索引。',source:'FIRST · FTC Events',url:'https://ftc-events.firstinspires.org/2023/awards'}
  ],
  portfolios:[
    {season:'all',type:'community',meta:'COMMUNITY LIBRARY',title:'FTC Portfolio Lab',desc:'可按赛季、赛事层级与奖项浏览评分后的公开 Engineering Portfolio。',source:'PortfolioLab · team submissions',url:'https://www.ftcportfoliolab.org/portfolio'},
    {season:'2024',type:'team',meta:'2024–2025 · TEAM 21573',title:'Tecra Bot — INTO THE DEEP',desc:'公开作品集案例；资料页标注 Inspire 1st、Design 1st 与 Think 2nd。',source:'OpenVault · team-submitted',url:'https://www.open-vault-ftc.org/portfolios/portfolios'},
    {season:'2025',type:'team',meta:'2025–2026 · TEAM 19706',title:'Potential Energy — DECODE',desc:'队伍公开的当季 Worlds Engineering Portfolio，可直接查看其最新文档。',source:'Team 19706 website',url:'https://www.potentialenergyftc.com/resources'},
    {season:'all',type:'team',meta:'MULTI-SEASON · TEAM 9929',title:'MechaHamsters Archive',desc:'队伍保存的历年 Engineering Notebooks 与 Portfolios，适合比较资料结构演进。',source:'FTC 9929 team website',url:'https://ftc9929.com/past-season-engineering-notebooks/'},
    {season:'all',type:'community',meta:'MULTI-SEASON ARCHIVE',title:'OpenVault Portfolio Collection',desc:'面向 FTC 队伍的公开作品集集合，可检索队号、赛季与获奖情况。',source:'OpenVault community archive',url:'https://www.open-vault-ftc.org/portfolios/portfolios'}
  ],
  open:[
    {season:'2025',type:'directory',meta:'DIRECTORY · 2025–2026',title:'FTC Open Alliance Season',desc:'当前赛季 FTC Open Alliance 总入口与参与方式。',source:'Chief Delphi · FTC Open Alliance',url:'https://www.chiefdelphi.com/t/the-2025-26-ftc-open-alliance-season/505867'},
    {season:'2025',type:'thread',meta:'TEAM 12527 · PROTOTYPE',title:'2026 Build Thread',desc:'Team Prototype 的 DECODE 赛季公开研发记录。',source:'Chief Delphi build thread',url:'https://www.chiefdelphi.com/t/ftc-12527-prototype-2026-build-thread/506197'},
    {season:'2025',type:'thread',meta:'TEAM 23619 · OVERTURE',title:'2025–2026 Build Blog',desc:'Overture 的 FTC Open Alliance 赛季 Build Blog。',source:'Chief Delphi build thread',url:'https://www.chiefdelphi.com/t/overture-23619-ftc-build-blog-2025-2026-open-alliance/508083'},
    {season:'2025',type:'thread',meta:'TEAM 26154 · 7DOF',title:'7 Degrees of Freedom',desc:'公开记录 DECODE 赛季设计、制造与程序进展。',source:'Chief Delphi build thread',url:'https://www.chiefdelphi.com/t/ftc-26154-7-degrees-of-freedom-2025-26-build-thread/506059'},
    {season:'2025',type:'thread',meta:'TEAM 17012',title:'Precision Guessworks',desc:'连续参与 FTC Open Alliance 的 2025–2026 赛季 Build Thread。',source:'Chief Delphi build thread',url:'https://www.chiefdelphi.com/t/ftc-17012-precision-guessworks-2025-2026-build-thread/506118'}
  ],
  resources:[
    {type:'official',meta:'OFFICIAL DOCS',title:'FTC Documentation',desc:'机器人控制系统、编程、硬件配置、AprilTag 与赛季技术说明。',source:'FIRST official',url:'https://ftc-docs.firstinspires.org/'},
    {type:'official',meta:'OFFICIAL CODE',title:'FTC Robot Controller SDK',desc:'官方 Android Studio 项目、示例 OpMode 与版本发布记录。',source:'FIRST-Tech-Challenge · GitHub',url:'https://github.com/FIRST-Tech-Challenge/FtcRobotController'},
    {type:'community',meta:'COMMUNITY GUIDE',title:'Game Manual 0',desc:'从机械、电子、编程到比赛策略的高质量社区入门指南。',source:'gm0 community documentation',url:'https://gm0.org/'},
    {type:'community',meta:'MOTION PLANNING',title:'Road Runner',desc:'FTC 常用的轨迹规划与运动控制库及其文档。',source:'Acme Robotics',url:'https://rr.brott.dev/'},
    {type:'community',meta:'PATHING',title:'Pedro Pathing',desc:'面向 FTC 的路径跟随库，包含快速入门和 API 文档。',source:'FTC community project',url:'https://pedropathing.com/'},
    {type:'community',meta:'TELEMETRY',title:'FTC Dashboard',desc:'实时遥测、图表、配置变量与摄像头画面的调试工具。',source:'acmerobotics · GitHub',url:'https://github.com/acmerobotics/ftc-dashboard'}
  ]
};
const FTC_SEASONS={2023:'CENTERSTAGE',2024:'INTO THE DEEP',2025:'DECODE'};
const FTC_PANEL_COPY={
  awards:['获奖结果','官方赛事奖项结果；每张卡片都可回到 FTC Events 核对。'],
  portfolios:['工程作品集','队伍主动公开的 Engineering Portfolio 与社区资料库，不代表 FIRST 官方背书。'],
  open:['队伍公开资料','公开记录机器人研发过程的 Build Thread 与队伍资料；“公开资料”不等同于 Open Alliance 身份。'],
  sites:['FTC 技术站','长期维护的队伍知识库、社区教程站与工具网站；此栏目不受赛季限制。'],
  resources:['FTC 技术资源','官方文档、常用框架和成熟社区工具；按技术方向筛选，不受赛季限制。']
};
let ftcSeason='2025',ftcCategory='overview',ftcFilter='all',ftcDetailFilter='all',ftcSort='default';
let FTC_AUTO_DATA=null,ftcDataLoading=false;
async function loadFtcAutoData(){
  if(FTC_AUTO_DATA||ftcDataLoading)return;
  ftcDataLoading=true;$('ftcCount').textContent='正在载入自动采集数据…';
  try{
    const response=await fetch('data/ftc-demo-v4.json');
    if(!response.ok)throw new Error('HTTP '+response.status);
    FTC_AUTO_DATA=await response.json();
    const total=FTC_AUTO_DATA.awards.length+FTC_AUTO_DATA.portfolios.length+FTC_AUTO_DATA.openTeams.length+(FTC_AUTO_DATA.sites||[]).length+FTC_AUTO_DATA.resources.length;
    $('ftcCount').textContent=total.toLocaleString()+' 条自动采集记录';
    if(ftcCategory!=='overview')renderFtcCards();
  }catch(error){$('ftcCount').textContent='自动数据载入失败';console.warn('FTC demo data:',error);}
  finally{ftcDataLoading=false;}
}
function renderFtcSeasons(){
  $('ftcSeasons').innerHTML=Object.keys(FTC_SEASONS).map(y=>'<button class="ftc-season-btn'+(y===ftcSeason?' active':'')+'" onclick="selectFtcSeason(\''+y+'\')"><strong>'+(y+'–'+String(Number(y)+1).slice(-2))+'</strong><small>'+FTC_SEASONS[y]+'</small></button>').join('');
}
function selectFtcSeason(y){ftcSeason=y;renderFtcSeasons();if(ftcCategory!=='overview')renderFtcCards();}
function renderFtcFromCard(category){const button=[...document.querySelectorAll('#ftcNav button')].find(node=>node.getAttribute('onclick')?.includes("'"+category+"'"));if(button)renderFtc(category,button);}
function renderFtc(category,button){
  const overview=$('ftcOverview'),panel=$('ftcPanel');ftcCategory=category;ftcFilter='all';ftcDetailFilter='all';ftcSort='default';
  document.querySelector('.ftc-seasonbar').hidden=(category==='overview'||category==='resources'||category==='sites');
  document.querySelectorAll('#ftcNav button').forEach(b=>b.classList.toggle('active',b===button));
  if(category==='overview'){
    overview.hidden=false;panel.hidden=true;$('ftcCount').textContent='精选入口';return;
  }
  overview.hidden=true;panel.hidden=false;$('ftcSearch').value='';
  $('ftcPanelTitle').textContent=FTC_PANEL_COPY[category][0];$('ftcPanelLead').textContent=FTC_PANEL_COPY[category][1];
  renderFtcCards();
}
function setFtcFilter(value,button){ftcFilter=value;document.querySelectorAll('#ftcFilters .chip').forEach(b=>b.classList.toggle('active',b===button));renderFtcCards();}
function setFtcDetail(value){ftcDetailFilter=value;renderFtcCards();}
function setFtcSort(value){ftcSort=value;renderFtcCards();}
function ftcSourceGroup(item){if(item.type==='official'||item.type==='manual')return'official';if(item.type==='team'||item.type==='thread')return'team';return'community';}
function ftcAutoItems(){
  if(!FTC_AUTO_DATA)return null;
  if(ftcCategory==='awards')return FTC_AUTO_DATA.awards.map(x=>({season:x.season,type:'official',detail:x.category||'other',event:x.eventCode,number:x.teamNumber,meta:x.award,title:'#'+x.teamNumber+' '+(x.teamName||'FTC Team '+x.teamNumber),desc:x.eventName+' · '+x.date,source:'FIRST FTC Events · '+x.eventCode,url:x.source}));
  if(ftcCategory==='portfolios')return FTC_AUTO_DATA.portfolios.map(x=>({season:x.season,type:x.sourceType==='official'?'official':'community',detail:x.level||x.award||'未标注层级',number:x.teamNumber,meta:(x.seasonLabel||'Season not specified')+(x.level?' · '+x.level:''),title:'#'+x.teamNumber+' '+(x.teamName||x.title||'FTC Team'),desc:[x.award,x.rating,x.score].filter(Boolean).join(' · ')||'Public Engineering Portfolio',source:x.source.includes('portfoliolab')?'FTC PortfolioLab':'OpenVault',url:x.pdf||x.source}));
  if(ftcCategory==='open')return FTC_AUTO_DATA.openTeams.map(x=>({season:x.season,type:'team',detail:(x.tags||['build-thread'])[0],tags:x.tags||['build-thread'],links:x.links||[],number:x.teamNumber||999999,activity:x.activity||x.posts||0,meta:(x.teamNumber?'TEAM '+x.teamNumber+' · ':'')+(x.posts||0).toLocaleString()+' 次更新',title:(x.teamName?x.teamName+' — ':'')+x.title,desc:'队伍公开 Build Thread；标签只描述已识别的公开内容，不代表官方认证。',source:'Chief Delphi',url:x.source}));
  if(ftcCategory==='sites')return (FTC_AUTO_DATA.sites||[]).map(x=>({season:'all',type:x.owner==='official'?'official':'community',detail:x.category,tags:[x.category],meta:(x.owner||'community').toUpperCase()+' · '+x.category,title:x.title,desc:x.description,source:'Reviewed public website',url:x.url}));
  if(ftcCategory==='resources')return FTC_AUTO_DATA.resources.map(x=>({season:'all',type:x.sourceType==='official'?'official':'community',detail:x.category,tags:[x.category],meta:x.sourceType==='official'?'OFFICIAL · '+x.category:'COMMUNITY · '+x.category,title:x.title,desc:x.description,source:x.sourceType==='official'?'FIRST / official project':'FTC community project',url:x.url}));
  return [];
}
function renderFtcCards(){
  const all=ftcAutoItems()||FTC_DEMO_DATA[ftcCategory]||[],q=($('ftcSearch').value||'').trim().toLowerCase();
  const seasonItems=all.filter(item=>ftcCategory==='resources'||ftcCategory==='sites'||!item.season||item.season==='all'||item.season===ftcSeason);
  const details=[...new Set(seasonItems.flatMap(x=>ftcCategory==='open'?(x.tags||[]):[x.detail]).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b)));
  let controls='';
  if(ftcCategory==='open')controls+='<div class="sort-toggle"><button type="button" class="sort-btn'+(ftcSort==='default'?' active':'')+'" onclick="setFtcSort(\'default\')">按热度排序</button><button type="button" class="sort-btn'+(ftcSort==='number'?' active':'')+'" onclick="setFtcSort(\'number\')">按队号排序</button></div>';
  controls+='<button class="chip'+(ftcFilter==='all'?' active':'')+'" onclick="setFtcFilter(\'all\',this)">全部</button>';
  if(ftcCategory==='resources'||ftcCategory==='sites'||ftcCategory==='portfolios')controls+='<button class="chip'+(ftcFilter==='official'?' active':'')+'" onclick="setFtcFilter(\'official\',this)">官方</button><button class="chip'+(ftcFilter==='community'?' active':'')+'" onclick="setFtcFilter(\'community\',this)">社区</button>';
  if(details.length)controls+='<select onchange="setFtcDetail(this.value)"><option value="all">'+(ftcCategory==='awards'?'全部奖项':ftcCategory==='portfolios'?'全部层级/奖项':'全部类型')+'</option>'+details.map(x=>'<option value="'+esc(x)+'"'+(x===ftcDetailFilter?' selected':'')+'>'+esc(x)+'</option>').join('')+'</select>';
  $('ftcFilters').innerHTML=controls;
  let items=seasonItems.filter(item=>(ftcFilter==='all'||ftcSourceGroup(item)===ftcFilter)&&(ftcDetailFilter==='all'||item.detail===ftcDetailFilter||(ftcCategory==='open'&&(item.tags||[]).includes(ftcDetailFilter)))&&(!q||(item.meta+' '+item.title+' '+item.desc+' '+item.source).toLowerCase().includes(q)));
  if(ftcCategory==='open')items.sort((a,b)=>ftcSort==='number'?a.number-b.number:ftcSort==='title'?a.title.localeCompare(b.title):b.activity-a.activity);
  const visible=items.slice(0,60);
  $('ftcPanelTotal').textContent=seasonItems.length+' 条资料';$('ftcCount').textContent=items.length+' / '+seasonItems.length;$('ftcResultCount').textContent='显示 '+items.length+' / '+seasonItems.length;
  const renderCard=item=>{
    if(ftcCategory==='open'){
      const direct=(item.links||[]).slice(0,5).map(link=>'<a class="btn '+({cad:'cad',code:'gh',video:'video',website:'site'}[link.type]||'site')+'" href="'+esc(link.url)+'" target="_blank" rel="noopener">'+esc(link.type==='code'?'Code':link.type==='video'?'Video':link.type==='website'?'Website':'CAD')+'</a>').join('');
      const tags=(item.tags||[]).filter(tag=>tag!=='build-thread').map(tag=>'<span class="tag-chip">'+esc(tag)+'</span>').join('');
      const cad=(item.tags||[]).includes('cad')?'<span class="cad-prev"><span class="cad-dot"></span>3D</span>':'';
      const views=item.activity?'<span class="views">'+item.activity+' posts</span>':'';
      return '<div class="card"><div class="num">'+item.number+cad+views+'</div><div class="nm">'+esc(item.title)+'</div>'+(tags?'<div>'+tags+'</div>':'')+'<div class="links">'+direct+'<a class="btn cd" href="'+esc(item.url)+'" target="_blank" rel="noopener">Build Thread</a></div></div>';
    }
    const tags=item.tags&&item.tags.length?'<div>'+item.tags.map(tag=>'<span class="tag-chip">'+esc(tag)+'</span>').join('')+'</div>':'';
    return '<div class="card"><div class="nm">'+esc(item.title)+'</div><div class="note">'+esc(item.desc)+'</div>'+tags+'<div class="loc">来源：'+esc(item.source)+'</div><div class="links"><a class="btn essay" href="'+esc(item.url)+'" target="_blank" rel="noopener">查看来源</a></div></div>';
  };
  $('ftcContent').innerHTML=items.length?visible.map(renderCard).join('')+(items.length>visible.length?'<div class="info-box">当前先渲染前 '+visible.length+' 条；搜索和筛选会作用于全部 '+items.length+' 条记录。</div>':''):'<div class="info-box">这个赛季还没有符合条件的公开资料。</div>';
}
function setProgram(program){
  const ftc = program === 'ftc';
  document.body.classList.toggle('ftc-mode',ftc);
  $('programFrc').classList.toggle('active',!ftc);
  $('programFtc').classList.toggle('active',ftc);
  $('programFrc').setAttribute('aria-pressed',String(!ftc));
  $('programFtc').setAttribute('aria-pressed',String(ftc));
  if(ftc){
    loadFtcAutoData();
    document.querySelector('[data-i18n="hero_kicker"]').textContent='FTC · FIRST Tech Challenge · Open resources for the whole community';
    document.querySelector('[data-i18n="site_title"]').textContent='FTC 资源库';
    document.querySelector('[data-i18n="site_subtitle"]').textContent='FIRSTHub · FTC Open Resource Library';
    document.querySelector('[data-i18n="hero_sub"]').textContent='FTC award results, public engineering portfolios, team-published resources, technical sites, and tools — organized with sources attached.';
    document.querySelector('[data-i18n="built_by"]').textContent='A FIRSTHub preview built by FRC Team 5449 for the FTC community.';
    const ftcStats=[['5','资料方向'],['3','已整理赛季'],['100%','来源可追溯'],['0','虚构记录']];
    document.querySelectorAll('.stat').forEach((node,i)=>{node.querySelector('.num').textContent=ftcStats[i][0];node.querySelector('.lbl').textContent=ftcStats[i][1];});
    history.replaceState(null,'',location.pathname+location.search+'#ftc');
  }else if(location.hash==='#ftc'){
    applyI18n();renderStats();
    history.replaceState(null,'',location.pathname+location.search+'#2026');
  }
}
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
  renderFtcSeasons();
  if(h==='ftc') setProgram('ftc');
  renderTsChips();
  renderTsite();
  renderSeasonGuide();
})();
