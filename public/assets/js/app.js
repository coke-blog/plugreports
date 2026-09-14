
/* plugreports.com — app.js */
(function(){
"use strict";

/* ---------------- i18n: UI chrome in top 10 world languages ---------------- */
var I18N = {
 en:{crisis:"Overdose or emergency? Call now",hotline:"Hotlines",drugs:"Drug Library",news:"News",busts:"Busts",topics:"Guides",sentencing:"Sentencing",pharmacies:"Pharmacies",rehabs:"Rehabs",about:"About",search:"Search the library…",effects:"Effects",risks:"Risks",od:"Overdose signs",price:"Street price",legal:"Legal status",updated:"Last updated",sources:"Sources",related:"You may also want to know",call:"Call now",ageTitle:"Before you continue",ageBody:"This site contains educational information about drugs and harm reduction. It is not medical or legal advice. You must be of legal age or accessing with intent to help yourself or someone else.",ageYes:"I understand — enter",ageNo:"Leave",disclaimerShort:"Educational harm-reduction content only — not medical or legal advice."},
 es:{crisis:"¿Sobredosis o emergencia? Llama ahora",hotline:"Líneas de ayuda",drugs:"Biblioteca de drogas",news:"Noticias",busts:"Incautaciones",topics:"Guías",sentencing:"Sentencias",pharmacies:"Farmacias",rehabs:"Rehabilitación",about:"Nosotros",search:"Buscar en la biblioteca…",effects:"Efectos",risks:"Riesgos",od:"Signos de sobredosis",price:"Precio en la calle",legal:"Situación legal",updated:"Última actualización",sources:"Fuentes",related:"También te puede interesar",call:"Llamar ahora",ageTitle:"Antes de continuar",ageBody:"Este sitio contiene información educativa sobre drogas y reducción de riesgos. No es asesoramiento médico ni legal. Debes ser mayor de edad o acceder con la intención de ayudarte a ti mismo o a otra persona.",ageYes:"Entiendo — entrar",ageNo:"Salir",disclaimerShort:"Contenido educativo de reducción de riesgos — no es asesoramiento médico ni legal."},
 zh:{crisis:"服药过量或紧急情况？立即拨打",hotline:"求助热线",drugs:"毒品资料库",news:"新闻",busts:"缉获",topics:"指南",sentencing:"量刑",pharmacies:"药店",rehabs:"康复中心",about:"关于我们",search:"搜索资料库…",effects:"作用",risks:"风险",od:"过量征兆",price:"黑市价格",legal:"法律状态",updated:"最后更新",sources:"来源",related:"你可能还想了解",call:"立即拨打",ageTitle:"继续之前",ageBody:"本网站包含有关毒品和减少伤害的教育信息。这不是医疗或法律建议。你必须已成年，或出于帮助自己/他人的目的访问。",ageYes:"我明白——进入",ageNo:"离开",disclaimerShort:"仅供减少伤害教育用途——非医疗或法律建议。"},
 hi:{crisis:"ओवरडोज या आपातकाल? अभी कॉल करें",hotline:"हेल्पलाइन",drugs:"ड्रग लाइब्रेरी",news:"समाचार",busts:"जब्ती",topics:"गाइड",sentencing:"सज़ा",pharmacies:"फार्मेसी",rehabs:"पुनर्वास",about:"हमारे बारे में",search:"लाइब्रेरी खोजें…",effects:"प्रभाव",risks:"जोखिम",od:"ओवरडोज के लक्षण",price:"स्ट्रीट मूल्य",legal:"कानूनी स्थिति",updated:"अंतिम अद्यतन",sources:"स्रोत",related:"आप यह भी जानना चाहेंगे",call:"अभी कॉल करें",ageTitle:"जारी रखने से पहले",ageBody:"यह साइट ड्रग्स और हानि-न्यूनीकरण की शैक्षिक जानकारी रखती है। यह चिकित्सा या कानूनी सलाह नहीं है। आप वयस्क हों या खुद/किसी और की मदद के उद्देश्य से यहाँ हों।",ageYes:"समझ गया — प्रवेश",ageNo:"बाहर जाएं",disclaimerShort:"केवल शैक्षिक हानि-न्यूनीकरण सामग्री — चिकित्सा या कानूनी सलाह नहीं।"},
 ar:{crisis:"جرعة زائدة أو طارئ؟ اتصل الآن",hotline:"خطوط المساعدة",drugs:"مكتبة المخدرات",news:"أخبار",busts:"حجوزات",topics:"أدلة",sentencing:"الأحكام",pharmacies:"صيدليات",rehabs:"مراكز علاج",about:"من نحن",search:"ابحث في المكتبة…",effects:"التأثيرات",risks:"المخاطر",od:"علامات الجرعة الزائدة",price:"سعر الشارع",legal:"الوضع القانوني",updated:"آخر تحديث",sources:"المصادر",related:"قد يهمك أيضًا",call:"اتصل الآن",ageTitle:"قبل المتابعة",ageBody:"يحتوي هذا الموقع على معلومات تعليمية حول المخدرات والحد من الضرر. ليس نصيحة طبية أو قانونية. يجب أن تكون بالغًا أو تدخل بهدف مساعدة نفسك أو شخص آخر.",ageYes:"أفهم — دخول",ageNo:"خروج",disclaimerShort:"محتوى تعليمي للحد من الضرر فقط — ليس نصيحة طبية أو قانونية."},
 pt:{crisis:"Overdose ou emergência? Ligue agora",hotline:"Linhas de ajuda",drugs:"Biblioteca de drogas",news:"Notícias",busts:"Apreensões",topics:"Guias",sentencing:"Penas",pharmacies:"Farmácias",rehabs:"Reabilitação",about:"Sobre nós",search:"Pesquisar na biblioteca…",effects:"Efeitos",risks:"Riscos",od:"Sinais de overdose",price:"Preço na rua",legal:"Situação legal",updated:"Última atualização",sources:"Fontes",related:"Você também pode querer saber",call:"Ligar agora",ageTitle:"Antes de continuar",ageBody:"Este site contém informações educativas sobre drogas e redução de danos. Não é aconselhamento médico ou jurídico. Você deve ser maior de idade ou acessar com o objetivo de ajudar a si mesmo ou outra pessoa.",ageYes:"Entendi — entrar",ageNo:"Sair",disclaimerShort:"Conteúdo educativo de redução de danos — não é aconselhamento médico ou jurídico."},
 ru:{crisis:"Передозировка или экстренная ситуация? Звоните сейчас",hotline:"Телефоны помощи",drugs:"Библиотека веществ",news:"Новости",busts:"Изъятия",topics:"Гайды",sentencing:"Наказания",pharmacies:"Аптеки",rehabs:"Реабилитация",about:"О нас",search:"Поиск по библиотеке…",effects:"Эффекты",risks:"Риски",od:"Признаки передозировки",price:"Цена на улице",legal:"Легальный статус",updated:"Обновлено",sources:"Источники",related:"Вам также может быть интересно",call:"Позвонить",ageTitle:"Прежде чем продолжить",ageBody:"На сайте образовательная информация о наркотиках и снижении вреда. Это не медицинская или юридическая консультация. Вам должно быть 18+ или вы зашли, чтобы помочь себе или другому человеку.",ageYes:"Понимаю — войти",ageNo:"Выйти",disclaimerShort:"Только образовательный контент о снижении вреда — не медицинская или юридическая консультация."},
 ja:{crisis:"過量服薬や緊急時は今すぐ電話を",hotline:"ホットライン",drugs:"ドラッグ図書館",news:"ニュース",busts:"摘発",topics:"ガイド",sentencing:"量刑",pharmacies:"薬局",rehabs:"リハビリ施設",about:"私たちについて",search:"ライブラリを検索…",effects:"効果",risks:"リスク",od:"過量の兆候",price:"街の値段",legal:"法的状況",updated:"最終更新",sources:"出典",related:"こちらも参照",call:"今すぐ電話",ageTitle:"続行する前に",ageBody:"このサイトはドラッグとハームリダクションに関する教育的な情報を含みます。医療・法律的な助言ではありません。成年であるか、自分自身や他者を助ける目的でアクセスしてください。",ageYes:"理解しました — 进入",ageNo:"退出",disclaimerShort:"教育的なハームリダクション情報のみ — 医療・法律的助言ではありません。"},
 de:{crisis:"Überdosis oder Notfall? Jetzt anrufen",hotline:"Hotlines",drugs:"Drogen-Bibliothek",news:"Neuigkeiten",busts:"Funde",topics:"Ratgeber",sentencing:"Strafen",pharmacies:"Apotheken",rehabs:"Reha-Zentren",about:"Über uns",search:"Bibliothek durchsuchen…",effects:"Wirkungen",risks:"Risiken",od:"Überdosis-Anzeichen",price:"Straßenpreis",legal:"Rechtsstatus",updated:"Zuletzt aktualisiert",sources:"Quellen",related:"Das könnte Sie auch interessieren",call:"Jetzt anrufen",ageTitle:"Bevor Sie fortfahren",ageBody:"Diese Seite enthält Bildungsinhalte über Drogen und Schadensminimierung. Es ist keine medizinische oder Rechtsberatung. Sie müssen volljährig sein oder die Seite mit der Absicht besuchen, sich oder jemandem anderem zu helfen.",ageYes:"Ich verstehe — weiter",ageNo:"Verlassen",disclaimerShort:"Nur Bildungsinhalte zur Schadensminimierung — keine medizinische oder Rechtsberatung."},
 fr:{crisis:"Surdose ou urgence ? Appelez maintenant",hotline:"Lignes d'aide",drugs:"Bibliothèque des drogues",news:"Actualités",busts:"Saisies",topics:"Guides",sentencing:"Peines",pharmacies:"Pharmacies",rehabs:"Centres de soins",about:"À propos",search:"Rechercher dans la bibliothèque…",effects:"Effets",risks:"Risques",od:"Signes de surdose",price:"Prix dans la rue",legal:"Statut légal",updated:"Dernière mise à jour",sources:"Sources",related:"Vous voudrez peut-être aussi savoir",call:"Appeler maintenant",ageTitle:"Avant de continuer",ageBody:"Ce site contient des informations éducatives sur les drogues et la réduction des risques. Ce n'est pas un avis médical ou juridique. Vous devez être majeur ou consulter ce site dans l'intention d'aider quelqu'un.",ageYes:"Je comprends — entrer",ageNo:"Quitter",disclaimerShort:"Contenu éducatif de réduction des risques uniquement — pas d'avis médical ou juridique."}
};

function getLang(){
  var l=localStorage.getItem('pr-lang');
  if(l && I18N[l]) return l;
  try{ var u=new URLSearchParams(location.search).get('lang'); if(u && I18N[u]) return u; }catch(e){}
  var n=(navigator.language||navigator.userLanguage||'en').slice(0,2).toLowerCase();
  if(I18N[n]) return n;
  return 'en';
}
function t(k){ var l=getLang(); return (I18N[l] && I18N[l][k]) || I18N.en[k] || k; }
function applyI18n(){
  var l=getLang();
  document.querySelectorAll('[data-i18n]').forEach(function(el){ el.textContent = t(el.getAttribute('data-i18n')); });
  document.documentElement.lang = l;
  document.documentElement.dir = (l==='ar') ? 'rtl' : 'ltr';
  document.querySelectorAll('.lang-switch button').forEach(function(b){ b.style.borderColor = (b.getAttribute('data-lang')===l) ? '#f59e0b' : '#374151'; });
  try{ history.replaceState(null,'','?lang='+l); }catch(e){}
}
function setLang(l){ localStorage.setItem('pr-lang',l); applyI18n(); }
document.addEventListener('click',function(e){ var b=e.target.closest('.lang-switch button'); if(b){ setLang(b.getAttribute('data-lang')); }});

/* ---------------- age gate ---------------- */
function gate(){
  if(localStorage.getItem('pr-age')==='1') return;
  var g=document.getElementById('agegate'); if(!g) return;
  g.hidden=false;
  g.querySelector('[data-gate-yes]').addEventListener('click',function(){ localStorage.setItem('pr-age','1'); g.hidden=true; });
  g.querySelector('[data-gate-no]').addEventListener('click',function(){ location.href='https://www.google.com'; });
}

/* ---------------- tabs ---------------- */
document.addEventListener('click',function(e){
  var tab=e.target.closest('.tab'); if(!tab) return;
  var group=tab.closest('[data-tabs]'); if(!group) return;
  group.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active');});
  group.querySelectorAll('.tab-pane').forEach(function(x){x.hidden=true;});
  tab.classList.add('active');
  var pane=group.querySelector('.tab-pane[data-pane="'+tab.getAttribute('data-tab')+'"]'); if(pane) pane.hidden=false;
});

/* ---------------- search (client-side over embedded index) ---------------- */
var searchIdx=[];
function initSearch(){
  var inp=document.getElementById('libsearch'); if(!inp||!window.DRUG_INDEX) return;
  var box=document.getElementById('searchresults'); if(!box) return;
  inp.addEventListener('input',function(){
    var q=inp.value.trim().toLowerCase();
    if(q.length<2){ box.innerHTML=''; box.hidden=true; return; }
    var hits=window.DRUG_INDEX.filter(function(d){ return (d.n+' '+d.a+' '+d.c).toLowerCase().indexOf(q)>-1; }).slice(0,12);
    if(!hits.length){ box.innerHTML='<div class="panel" style="padding:14px 18px">No matches. Try a street name or category.</div>'; box.hidden=false; return; }
    box.innerHTML='<div class="panel" style="padding:10px">'+hits.map(function(h){
      return '<a href="'+h.u+'" style="display:flex;gap:10px;align-items:center;padding:9px 10px;border-radius:10px" onmouseover="this.style.background=\'#fffbeb\'" onmouseout="this.style.background=\'\'"><span class="mini" style="width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:#fff;font-size:12px;font-weight:800;background:'+h.col+'">'+h.n[0]+'</span><span><b style="font-size:14px">'+h.n+'</b><br><span style="font-size:12px;color:#667085">'+h.c+' · '+h.a+'</span></span></a>';
    }).join('')+'</div>';
    box.hidden=false;
  });
}

/* ---------------- suggest form ---------------- */
function initSuggest(){
  var f=document.getElementById('suggestform'); if(!f) return;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var data={type:f.type.value,name:f.name.value,contact:f.contact.value,message:f.message.value,page:location.pathname};
    var btn=f.querySelector('button'); btn.disabled=true; btn.textContent='Sending…';
    fetch('/api/suggest',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){ return r.json(); })
      .then(function(){ document.getElementById('suggest-ok').hidden=false; f.reset(); })
      .catch(function(){ document.getElementById('suggest-ok').hidden=false; f.reset(); })
      .finally(function(){ btn.disabled=false; btn.textContent='Submit'; });
  });
}

/* ---------------- PWA ---------------- */
if('serviceWorker' in navigator){ window.addEventListener('load',function(){ navigator.serviceWorker.register('/sw.js').catch(function(){}); }); }

function injectSettings(){
  fetch('/api/public/content?type=settings').then(function(r){return r.json()}).then(function(d){
    var s=(d.items&&d.items[0])||{};
    function meta(n,c){if(c&&!document.querySelector('meta[name="'+n+'"]')){var m=document.createElement('meta');m.name=n;m.content=c;document.head.appendChild(m)}}
    meta('google-site-verification',s.gsc); meta('msvalidate.01',s.bing);
    if(s.clarity&&!window.clarity){var t=document.createElement('script');t.async=1;t.src='https://www.clarity.ms/tag/'+s.clarity;document.head.appendChild(t)}
    if(s.ga&&!window.gtag){var g=document.createElement('script');g.async=1;g.src='https://www.googletagmanager.com/gtag/js?id='+s.ga;document.head.appendChild(g);
      window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',s.ga)}
  }).catch(function(){});
}
function initTranslate(){
  var host=document.getElementById('langswitch'); if(!host) return;
  var names={es:'Español',zh:'中文',hi:'हिन्दी',ar:'العربية',pt:'Português',ru:'Русский',ja:'日本語',de:'Deutsch',fr:'Français'};
  var sel=document.createElement('select'); sel.id='tlang';
  sel.innerHTML='<option value="">🌐 Translate page…</option>'+Object.keys(I18N).filter(function(l){return l!=='en'}).map(function(l){return '<option value="'+l+'">'+(names[l]||l)+'</option>'}).join('')+'<option value="en">Original (English)</option>';
  sel.style.cssText='display:block;margin-top:10px;padding:6px 10px;border:1px solid #374151;background:#1f2937;color:#cbd5e1;border-radius:8px;font-size:12px';
  host.parentNode.insertBefore(sel, host.nextSibling);
  sel.onchange=function(){ if(sel.value) translateContent(sel.value); };
}
function translateContent(lang){
  var els=[].slice.call(document.querySelectorAll('main p, main h1, main h2, main h3, main li, main td, main th, .fact span, .card p, .card h3, .hl-card .who, .hl-card h3'))
    .filter(function(e){ var t=e.textContent.trim(); return t.length>2 && t.length<1200 && !e.querySelector('script,img,select'); });
  if(lang==='en'){ els.forEach(function(e){ if(e.dataset.tSrc!=null) e.textContent=e.dataset.tSrc; }); return; }
  els.forEach(function(e){ if(e.dataset.tSrc==null) e.dataset.tSrc=e.textContent; });
  var CH=20;
  (function batch(start){
    var slice=els.slice(start,start+CH); if(!slice.length) return;
    fetch('/api/translate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({texts:slice.map(function(e){return e.dataset.tSrc}),target:lang})})
      .then(function(r){return r.json()}).then(function(d){
        if(d.ok) slice.forEach(function(e,i){ if(d.results&&d.results[i]) e.textContent=d.results[i]; });
        batch(start+CH);
      }).catch(function(){ batch(start+CH); });
  })(0);
}
document.addEventListener('DOMContentLoaded',function(){ applyI18n(); gate(); initSearch(); initSuggest(); injectSettings(); initTranslate();
  var b=document.querySelector('.burger'); if(b){ b.addEventListener('click',function(){ document.querySelector('.nav-links').classList.toggle('open'); }); }
});
})();
