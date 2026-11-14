(function(){
var root=document.getElementById("sca0");
if(!root||root.dataset.ok)return;root.dataset.ok="1";
var LIB=window.SCA0_LIBS||{pdflib:"https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js",pdfjs:"https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js",worker:"https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js"};
var PT=72/25.4,R=6,TH=2,HR=24;
var TXT={
en:{title:"A4 to A0 pattern converter",reset:"New file",drop:"Drop your PDF sewing pattern here",dropSub:"A4 or US Letter tiled pages. Your file stays on your device: nothing is uploaded.",choose:"Choose a PDF",libs:"Loading the converter…",reading:"Reading page {i} of {n}…",analyzing:"Finding the cut lines and the page layout…",refining:"Measuring the cut lines precisely…",errEnc:"This PDF is locked by its designer, so it can’t be converted here. Ask the designer for the A0 / copy shop file.",errPwd:"This PDF is protected with a password.",errRead:"This file could not be read as a PDF.",errLib:"The converter could not load. Check your connection and reload the page.",errOne:"Only one tile page was found, so there is nothing to assemble. Check the tile pages below.",errSize:"All tile pages must have the same size. Page {p} is different.",errPages:"Check the tile pages: use page numbers between 1 and {n}, for example 3-38.",layoutH:"1. Page layout",pagesL:"Tile pages",pagesHint:"{n} pages in the file. Leave out the cover and instruction pages.",colsL:"Columns",rowsL:"Rows",orderL:"Page order",orderRows:"Row by row",orderCols:"Column by column",gridInfo:"{c} columns × {r} rows · {e} empty space(s)",trimH:"2. Cut lines",left:"Left",top:"Top",right:"Right",bottom:"Bottom",trimHint:"Margin from the page edge to the cut line, in mm. Found automatically: change only if the preview shows a gap or an overlap.",frameCap:"Red = cut lines on page {p}",detect:"Detect again",outH:"3. Print",outL:"Paper",outA0:"A0 sheets",outOne:"One sheet, no cuts (recommended)",outRoll:"Roll 36″ / 914 mm",marginL:"White margin",rulerL:"Add a 10 cm and 4″ check ruler",sizeK:"Pattern size",sheetsK:"Sheets",dl:"Download the A0 PDF",building:"Building your PDF…",done:"Done ✓ Print it, then measure the ruler: it must be exactly 10 cm and 4″.",printNote:"At the copy shop, ask for 100% / actual size. Never “fit to page”.",pvH:"Preview",seams:"Joins",zoom:"Zoom",pvHint:"Click a page to put an empty square before it (for layouts with empty squares). Click an empty square to remove it.",ok:"Checked: {p}% of the pattern lines continue across the joins. The pages line up.",wa:"Check the preview: only {p}% of the lines continue across the joins. Compare with the layout page of your pattern.",unk:"There are too few lines on the joins to check them automatically. Compare the preview with the layout page of your pattern.",sheet:"Sheet {i} of {n}",joinR:"right: sheet {k}",joinB:"below: sheet {k}",pdfNote:"Print at 100% (actual size)",rul:"must measure",empty:"empty",wsPrompt:"This PDF has {n} pages. It may take a moment."},
fr:{title:"Convertisseur de patron A4 en A0",reset:"Nouveau fichier",drop:"Déposez votre patron PDF ici",dropSub:"Pages A4 ou US Letter à assembler. Le fichier reste sur votre appareil : rien n’est envoyé.",choose:"Choisir un PDF",libs:"Chargement du convertisseur…",reading:"Lecture de la page {i} sur {n}…",analyzing:"Recherche des lignes de coupe et de l’ordre des pages…",refining:"Mesure précise des lignes de coupe…",errEnc:"Ce PDF est verrouillé par sa créatrice : il ne peut pas être converti ici. Demandez-lui le fichier A0 / copy shop.",errPwd:"Ce PDF est protégé par un mot de passe.",errRead:"Ce fichier n’a pas pu être lu comme un PDF.",errLib:"Le convertisseur n’a pas pu se charger. Vérifiez votre connexion et rechargez la page.",errOne:"Une seule page à assembler a été trouvée. Vérifiez les pages ci-dessous.",errSize:"Toutes les pages à assembler doivent avoir la même taille. La page {p} est différente.",errPages:"Vérifiez les pages : numéros entre 1 et {n}, par exemple 3-38.",layoutH:"1. Disposition des pages",pagesL:"Pages à assembler",pagesHint:"{n} pages dans le fichier. Retirez la couverture et les pages d’instructions.",colsL:"Colonnes",rowsL:"Rangées",orderL:"Ordre des pages",orderRows:"Rangée par rangée",orderCols:"Colonne par colonne",gridInfo:"{c} colonnes × {r} rangées · {e} case(s) vide(s)",trimH:"2. Lignes de coupe",left:"Gauche",top:"Haut",right:"Droite",bottom:"Bas",trimHint:"Marge entre le bord de la page et la ligne de coupe, en mm. Trouvée automatiquement : ne changez que si l’aperçu montre un trou ou un chevauchement.",frameCap:"Rouge = lignes de coupe de la page {p}",detect:"Détecter à nouveau",outH:"3. Impression",outL:"Papier",outA0:"Feuilles A0",outOne:"Une seule feuille, sans coupure (conseillé)",outRoll:"Rouleau 914 mm (36″)",marginL:"Marge blanche",rulerL:"Ajouter une règle de contrôle 10 cm et 4″",sizeK:"Taille du patron",sheetsK:"Feuilles",dl:"Télécharger le PDF A0",building:"Création du PDF…",done:"Terminé ✓ Imprimez, puis mesurez la règle : elle doit faire exactement 10 cm et 4″.",printNote:"Au copy shop, demandez une impression à 100 % / taille réelle. Jamais « ajuster à la page ».",pvH:"Aperçu",seams:"Raccords",zoom:"Zoom",pvHint:"Cliquez sur une page pour insérer une case vide avant elle (plans avec cases vides). Cliquez sur une case vide pour la retirer.",ok:"Vérifié : {p} % des lignes du patron continuent d’une page à l’autre. Les pages s’alignent.",wa:"Vérifiez l’aperçu : seulement {p} % des lignes continuent d’une page à l’autre. Comparez avec le plan d’assemblage du patron.",unk:"Trop peu de lignes aux raccords pour les vérifier automatiquement. Comparez l’aperçu avec le plan d’assemblage du patron.",sheet:"Feuille {i} sur {n}",joinR:"à droite : feuille {k}",joinB:"en dessous : feuille {k}",pdfNote:"Imprimer à 100 % (taille réelle)",rul:"doit mesurer",empty:"vide",wsPrompt:"Ce PDF a {n} pages. Cela peut prendre un moment."},
de:{title:"Schnittmuster A4 in A0 umwandeln",reset:"Neue Datei",drop:"PDF-Schnittmuster hier ablegen",dropSub:"A4- oder US-Letter-Seiten zum Kleben. Die Datei bleibt auf deinem Gerät, nichts wird hochgeladen.",choose:"PDF auswählen",libs:"Konverter wird geladen…",reading:"Seite {i} von {n} wird gelesen…",analyzing:"Schnittlinien und Seitenreihenfolge werden gesucht…",refining:"Schnittlinien werden genau gemessen…",errEnc:"Diese PDF ist von der Designerin gesperrt und kann hier nicht umgewandelt werden. Frag nach der A0-/Copyshop-Datei.",errPwd:"Diese PDF ist mit einem Passwort geschützt.",errRead:"Diese Datei konnte nicht als PDF gelesen werden.",errLib:"Der Konverter konnte nicht geladen werden. Prüfe die Verbindung und lade die Seite neu.",errOne:"Es wurde nur eine Klebeseite gefunden. Prüfe die Seiten unten.",errSize:"Alle Klebeseiten müssen gleich groß sein. Seite {p} ist anders.",errPages:"Prüfe die Seiten: Seitenzahlen von 1 bis {n}, zum Beispiel 3-38.",layoutH:"1. Seitenanordnung",pagesL:"Klebeseiten",pagesHint:"{n} Seiten in der Datei. Deckblatt und Anleitungsseiten weglassen.",colsL:"Spalten",rowsL:"Reihen",orderL:"Reihenfolge",orderRows:"Reihe für Reihe",orderCols:"Spalte für Spalte",gridInfo:"{c} Spalten × {r} Reihen · {e} leere(s) Feld(er)",trimH:"2. Schnittlinien",left:"Links",top:"Oben",right:"Rechts",bottom:"Unten",trimHint:"Abstand vom Seitenrand bis zur Schnittlinie in mm. Automatisch erkannt: nur ändern, wenn die Vorschau eine Lücke oder Überlappung zeigt.",frameCap:"Rot = Schnittlinien auf Seite {p}",detect:"Neu erkennen",outH:"3. Drucken",outL:"Papier",outA0:"A0-Bögen",outOne:"Ein Bogen am Stück (empfohlen)",outRoll:"Rolle 914 mm (36″)",marginL:"Weißer Rand",rulerL:"Kontroll-Lineal 10 cm und 4″ hinzufügen",sizeK:"Schnittgröße",sheetsK:"Bögen",dl:"A0-PDF herunterladen",building:"PDF wird erstellt…",done:"Fertig ✓ Drucken und das Lineal messen: genau 10 cm und 4″.",printNote:"Im Copyshop 100 % / Originalgröße drucken lassen, nie „an Seite anpassen“.",pvH:"Vorschau",seams:"Übergänge",zoom:"Zoom",pvHint:"Klicke auf eine Seite, um davor ein leeres Feld einzufügen (für Klebepläne mit leeren Feldern). Klicke auf ein leeres Feld, um es zu entfernen.",ok:"Geprüft: {p} % der Schnittlinien laufen über die Übergänge weiter. Die Seiten passen.",wa:"Vorschau prüfen: nur {p} % der Linien laufen über die Übergänge weiter. Vergleiche mit dem Klebeplan.",unk:"Zu wenige Linien an den Übergängen für eine automatische Prüfung. Vergleiche die Vorschau mit dem Klebeplan.",sheet:"Bogen {i} von {n}",joinR:"rechts: Bogen {k}",joinB:"unten: Bogen {k}",pdfNote:"Mit 100 % drucken (Originalgröße)",rul:"muss messen",empty:"leer",wsPrompt:"Diese PDF hat {n} Seiten. Das kann einen Moment dauern."},
nl:{title:"Naaipatroon A4 naar A0 omzetten",reset:"Nieuw bestand",drop:"Sleep je PDF-naaipatroon hierheen",dropSub:"A4- of US Letter-pagina’s om te plakken. Je bestand blijft op je apparaat: er wordt niets geüpload.",choose:"Kies een PDF",libs:"Converter laden…",reading:"Pagina {i} van {n} lezen…",analyzing:"Kniplijnen en paginavolgorde zoeken…",refining:"Kniplijnen nauwkeurig meten…",errEnc:"Deze PDF is vergrendeld door de ontwerper en kan hier niet worden omgezet. Vraag de ontwerper om het A0-/copyshopbestand.",errPwd:"Deze PDF is beveiligd met een wachtwoord.",errRead:"Dit bestand kon niet als PDF worden gelezen.",errLib:"De converter kon niet laden. Controleer je verbinding en herlaad de pagina.",errOne:"Er is maar één plakpagina gevonden. Controleer de pagina’s hieronder.",errSize:"Alle plakpagina’s moeten even groot zijn. Pagina {p} is anders.",errPages:"Controleer de pagina’s: nummers van 1 tot {n}, bijvoorbeeld 3-38.",layoutH:"1. Indeling",pagesL:"Plakpagina’s",pagesHint:"{n} pagina’s in het bestand. Laat de omslag en de instructiepagina’s weg.",colsL:"Kolommen",rowsL:"Rijen",orderL:"Volgorde",orderRows:"Rij per rij",orderCols:"Kolom per kolom",gridInfo:"{c} kolommen × {r} rijen · {e} leeg vak/lege vakken",trimH:"2. Kniplijnen",left:"Links",top:"Boven",right:"Rechts",bottom:"Onder",trimHint:"Afstand van de paginarand tot de kniplijn, in mm. Automatisch gevonden: alleen aanpassen als de preview een gat of overlap toont.",frameCap:"Rood = kniplijnen op pagina {p}",detect:"Opnieuw zoeken",outH:"3. Printen",outL:"Papier",outA0:"A0-vellen",outOne:"Eén vel in één stuk (aanbevolen)",outRoll:"Rol 914 mm (36″)",marginL:"Witte rand",rulerL:"Controleliniaal 10 cm en 4″ toevoegen",sizeK:"Patroonmaat",sheetsK:"Vellen",dl:"A0-PDF downloaden",building:"PDF maken…",done:"Klaar ✓ Print en meet de liniaal: precies 10 cm en 4″.",printNote:"Vraag in de copyshop om 100% / ware grootte. Nooit “passend maken”.",pvH:"Preview",seams:"Naden",zoom:"Zoom",pvHint:"Klik op een pagina om er een leeg vak voor te zetten (voor plakplannen met lege vakken). Klik op een leeg vak om het te verwijderen.",ok:"Gecontroleerd: {p}% van de patroonlijnen loopt door over de naden. De pagina’s sluiten aan.",wa:"Controleer de preview: maar {p}% van de lijnen loopt door. Vergelijk met het plakplan van je patroon.",unk:"Te weinig lijnen op de naden om automatisch te controleren. Vergelijk de preview met het plakplan van je patroon.",sheet:"Vel {i} van {n}",joinR:"rechts: vel {k}",joinB:"onder: vel {k}",pdfNote:"Print op 100% (ware grootte)",rul:"moet meten",empty:"leeg",wsPrompt:"Deze PDF heeft {n} pagina’s. Dit kan even duren."}};
var lang=(document.documentElement.lang||"en").slice(0,2).toLowerCase();if(!TXT[lang])lang="en";var T=TXT[lang];
function t(k,o){var s=T[k]!=null?T[k]:(TXT.en[k]||k);if(o)s=s.replace(/\{(\w+)\}/g,function(a,b){return o[b]});return s}
root.querySelectorAll("[data-t]").forEach(function(e){e.textContent=t(e.getAttribute("data-t"))});
function $(i){return document.getElementById("a0-"+i)}
var S=null;

/* ---------- libraries ---------- */
function loadScript(u){return new Promise(function(res,rej){var s=document.createElement("script");s.src=u;s.async=true;s.onload=res;s.onerror=function(){rej(new Error("load"))};document.head.appendChild(s)})}
var libsP=null;
function libs(){if(libsP)return libsP;libsP=(async function(){var d=window.define;try{window.define=undefined;if(!window.PDFLib)await loadScript(LIB.pdflib);if(!window.pdfjsLib)await loadScript(LIB.pdfjs)}finally{window.define=d}
var pj=window.pdfjsLib||window["pdfjs-dist/build/pdf"];if(!pj||!window.PDFLib)throw new Error("lib");window.pdfjsLib=pj;
try{var tx=await (await fetch(LIB.worker)).text();pj.GlobalWorkerOptions.workerSrc=URL.createObjectURL(new Blob([tx],{type:"text/javascript"}))}catch(e){pj.GlobalWorkerOptions.workerSrc=LIB.worker}})();libsP.catch(function(){libsP=null});return libsP}

/* ---------- UI helpers ---------- */
function prog(p,msg){$("prog").style.display="block";$("bar").style.width=Math.round(p*100)+"%";if(msg!=null)$("msg").textContent=msg}
function err(m){$("err").textContent=m;$("err").style.display=m?"block":"none"}
function sleep0(){return new Promise(function(r){setTimeout(r,0)})}
function fmt(v,d){return Number(v).toLocaleString(lang==="en"?"en-US":lang,{maximumFractionDigits:d==null?1:d,minimumFractionDigits:0})}

/* ---------- rendering ---------- */
async function renderCanvas(pi,scale,ox,oy,w,h){var p=await S.pdf.getPage(pi+1);var vp=p.getViewport({scale:scale,offsetX:-(ox||0),offsetY:-(oy||0)});var c=document.createElement("canvas");c.width=w;c.height=h;var x=c.getContext("2d",{willReadFrequently:true});x.fillStyle="#fff";x.fillRect(0,0,w,h);await p.render({canvasContext:x,viewport:vp,annotationMode:0}).promise;return c}
function lum(d,j){return d[j]*299+d[j+1]*587+d[j+2]*114}
var DARK=200000;

/* ---------- load ---------- */
async function openFile(f){
err("");$("done").style.display="none";
if(!f)return;
prog(.02,t("libs"));
try{await libs()}catch(e){prog(0,"");$("prog").style.display="none";err(t("errLib"));return}
var buf;try{buf=new Uint8Array(await f.arrayBuffer())}catch(e){err(t("errRead"));return}
try{var tdoc=await PDFLib.PDFDocument.load(buf,{ignoreEncryption:true,updateMetadata:false});if(tdoc.isEncrypted){$("prog").style.display="none";err(t("errEnc"));return}}catch(e){$("prog").style.display="none";err(t("errRead"));return}
var pdf;try{var task=pdfjsLib.getDocument({data:buf.slice(0),isEvalSupported:false,disableAutoFetch:true});task.onPassword=function(){task.destroy()};pdf=await task.promise}catch(e){$("prog").style.display="none";err(/assword/.test(String(e&&e.name)+String(e&&e.message))?t("errPwd"):t("errRead"));return}
if(S&&S.pdf){try{S.pdf.destroy()}catch(e){}}
S={name:(f.name||"pattern.pdf").replace(/\.pdf$/i,""),bytes:buf,pdf:pdf,n:pdf.numPages,pg:[],cache:{}};
for(var i=0;i<S.n;i++){var p=await pdf.getPage(i+1);var vp=p.getViewport({scale:1});S.pg.push({w:vp.width/PT,h:vp.height/PT,rot:p.rotate||0})}
/* majority page size */
var cnt={},best=null;S.pg.forEach(function(g){var k=Math.round(g.w)+"x"+Math.round(g.h);cnt[k]=(cnt[k]||0)+1;if(!best||cnt[k]>cnt[best])best=k});
S.key=best;S.cand=[];S.pg.forEach(function(g,i){if(Math.round(g.w)+"x"+Math.round(g.h)===best)S.cand.push(i)});
var g0=S.pg[S.cand[0]];S.W=g0.w;S.H=g0.h;S.mw=Math.round(S.W*R);S.mh=Math.round(S.H*R);
/* render candidates */
var N=S.mw*S.mh,acc=new Uint16Array(N);
for(var k=0;k<S.cand.length;k++){var pi=S.cand[k];prog(.05+.75*k/S.cand.length,t("reading",{i:pi+1,n:S.n}));
var c=await renderCanvas(pi,R/PT,0,0,S.mw,S.mh);var d=c.getContext("2d").getImageData(0,0,S.mw,S.mh).data;var m=new Uint8Array((N+7)>>3);
for(var q=0,j=0;q<N;q++,j+=4){if(lum(d,j)<DARK){m[q>>3]|=1<<(q&7);acc[q]++}}
S.pg[pi].mask=m;var th=document.createElement("canvas");th.width=Math.round(S.W*TH);th.height=Math.round(S.H*TH);var tx=th.getContext("2d");tx.imageSmoothingEnabled=true;tx.imageSmoothingQuality="high";tx.drawImage(c,0,0,th.width,th.height);S.pg[pi].thumb=th;c.width=c.height=1;await sleep0()}
S.acc=acc;
prog(.82,t("analyzing"));await sleep0();
analyze();
prog(.9,t("refining"));await sleep0();
await refine();
prog(1,"");$("prog").style.display="none";
$("start").style.display="none";$("new").style.display="inline-block";$("main").style.display="block";
fillUI();update();
}
function bit(m,i){return (m[i>>3]>>(i&7))&1}

/* ---------- analysis ---------- */
function consistent(tiles){var N=S.mw*S.mh,acc,i;if(tiles.length===S.cand.length)acc=S.acc;else{acc=new Uint16Array(N);tiles.forEach(function(pi){var m=S.pg[pi].mask;for(var q=0;q<N;q++)if((m[q>>3]>>(q&7))&1)acc[q]++})}
var thr=Math.max(1,Math.ceil(.6*tiles.length));if(tiles.length>=4)thr=Math.max(thr,2);var c=new Uint8Array(N),n=0;for(i=0;i<N;i++)if(acc[i]>=thr){c[i]=1;n++}return {c:c,n:n}}
function analyze(){
var cand=S.cand.slice(),C=consistent(cand),N=S.mw*S.mh;
var tiles=cand;
if(C.n>R*20&&cand.length>2){tiles=cand.filter(function(pi){var m=S.pg[pi].mask,h=0;for(var q=0;q<N;q++)if(C.c[q]&&((m[q>>3]>>(q&7))&1))h++;return h/C.n>=.5});if(tiles.length<2)tiles=cand;else if(tiles.length!==cand.length)C=consistent(tiles)}
S.cons=C.c;S.cache={};
S.auto={tiles:tiles};
var cands=trimCands(tiles);S.cands=cands;
/* 1) start from the strongest guide line on each side, 2) choose the layout with those cut lines fixed, 3) re-check the cut lines with that layout */
var tr0={l:strongest(cands.l,S.mw),r:strongest(cands.r,S.mw),t:strongest(cands.t,S.mh),b:strongest(cands.b,S.mh)};
var best=chooseLayout(tiles,tr0),tr=tr0;
for(var it=0;it<2;it++){var Lb=layout(tiles.length,best.c,best.o===1,[]),v=bestPair(tiles,Lb,"v",cands.l,cands.r),h=bestPair(tiles,Lb,"h",cands.t,cands.b);
var cv=pairScore(tiles,Lb,"v",tr.l,tr.r),ch=pairScore(tiles,Lb,"h",tr.t,tr.b);function better(bp,cur){return bp.a&&bp.t>=6&&bp.r>.4&&bp.sc>=cur.sc+Math.max(6,.15*cur.t)}
var lockX=locked(tr.l,S.mh)&&locked(tr.r,S.mh),lockY=locked(tr.t,S.mw)&&locked(tr.b,S.mw);
var tr1={l:!lockX&&better(v,cv)?v.a:tr.l,r:!lockX&&better(v,cv)?v.b:tr.r,t:!lockY&&better(h,ch)?h.a:tr.t,b:!lockY&&better(h,ch)?h.b:tr.b};
if(tr1.l===tr.l&&tr1.r===tr.r&&tr1.t===tr.t&&tr1.b===tr.b)break;tr=tr1;best=chooseLayout(tiles,tr)}
if(best.tt<8){/* nothing on the joins to compare: start from a near-square layout */var twp=tr.r.v-tr.l.v,thp=tr.b.v-tr.t.v;best={c:Math.max(1,Math.min(tiles.length,Math.round(Math.sqrt(tiles.length*thp/Math.max(1,twp))))),o:0,tt:0,sc:0}}
S.auto.c=best.c;S.auto.colMajor=best.o===1;S.auto.trim=tr;S.auto.sc=best.sc;
S.tiles=tiles.slice();S.c=best.c;S.colMajor=best.o===1;S.trimSrc=tr;S.order=best.tt>=8?blanks(tiles.slice(),best.c,best.o===1,tr):tiles.slice();S.auto.order=S.order.slice();
}
function orderScore(o,c,cm,tr){var L=layout(o.length,c,cm,[]),sm=seamsOf(L),sc=0;sm.V.forEach(function(p){var A=o[p[0]],B=o[p[1]];if(A<0||B<0)return;var r=seamScore(A,B,"v",tr.r.v,tr.l.v);sc+=2*r[0]-r[1]});sm.H.forEach(function(p){var A=o[p[0]],B=o[p[1]];if(A<0||B<0)return;var r=seamScore(A,B,"h",tr.b.v,tr.t.v);sc+=2*r[0]-r[1]});return sc}
function blanks(o,c,cm,tr){/* layouts with empty squares: add an empty cell where it makes the joins match clearly better */var base=orderScore(o,c,cm,tr),lim=Math.max(c,Math.ceil(o.length/c));for(var it=0;it<lim;it++){var bi=-1,bk=1,bs=-1e9;for(var i=0;i<o.length;i++)for(var k=1;k<c;k++){var q=o.slice();for(var j=0;j<k;j++)q.splice(i,0,-1);var v=orderScore(q,c,cm,tr);if(v>bs){bs=v;bi=i;bk=k}}if(bi<0||bs<base+6)break;for(var j2=0;j2<bk;j2++)o.splice(bi,0,-1);base=bs}return o}
function locked(c,span){return c&&c.k==="line"&&c.s>=.8*span}
function pairScore(tiles,L,dir,a,b){var sm=seamsOf(L),P=dir==="v"?sm.V:sm.H,m=0,tt=0;P.forEach(function(p){var r=seamScore(tiles[p[0]],tiles[p[1]],dir,b.v,a.v);m+=r[0];tt+=r[1]});return {m:m,t:tt,sc:2*m-tt}}
function strongest(L,span){var b=null;L.forEach(function(x){if(x.k==="line"&&x.s>=4*R&&(!b||x.s>b.s))b=x});if(b)return b;L.forEach(function(x){if(x.k==="clip"&&!b)b=x});if(b)return b;L.forEach(function(x){if(x.k==="line"&&(!b||x.s>b.s))b=x});return b||L[L.length-1]}
function chooseLayout(tiles,tr){var best=null,Nt=tiles.length;for(var o=0;o<2;o++)for(var c=1;c<=Nt;c++){var L=layout(Nt,c,o===1,[]),sm=seamsOf(L),m=0,tt=0;
sm.V.forEach(function(p){var r=seamScore(tiles[p[0]],tiles[p[1]],"v",tr.r.v,tr.l.v);m+=r[0];tt+=r[1]});sm.H.forEach(function(p){var r=seamScore(tiles[p[0]],tiles[p[1]],"h",tr.b.v,tr.t.v);m+=r[0];tt+=r[1]});
var sc=2*m-tt;if(!best||sc>best.sc||(sc===best.sc&&tt>best.tt))best={sc:sc,tt:tt,c:c,o:o,r:(m+.5)/(tt+3)}}return best}
function groups(cnt,len,minc){var g=[],cur=null;for(var i=0;i<len;i++){if(cnt[i]>=minc){if(!cur)cur={a:i,s:0,w:0,mx:0};cur.s+=cnt[i]*(i+.5);cur.w+=cnt[i];cur.mx=Math.max(cur.mx,cnt[i]);cur.e=i}else if(cur){if(i-cur.e>1){g.push(cur);cur=null}}}if(cur)g.push(cur);return g.map(function(x){return {v:x.s/x.w,s:x.mx,k:"line"}})}
function trimCands(tiles){var mw=S.mw,mh=S.mh,c=S.cons,row=new Float64Array(mh),col=new Float64Array(mw),x,y;
for(y=0;y<mh;y++)for(x=0;x<mw;x++)if(c[y*mw+x]){row[y]++;col[x]++}
var minc=2.5*R,gr=groups(row,mh,minc),gc=groups(col,mw,minc);
function side(G,lo,hi){return G.filter(function(g){return g.v>=lo&&g.v<=hi}).sort(function(a,b){return b.s-a.s}).slice(0,5)}
var out={t:side(gr,0,.4*mh),b:side(gr,.6*mh,mh),l:side(gc,0,.4*mw),r:side(gc,.6*mw,mw)};
/* content (clip) edges from union of non-consistent ink */
var uc=new Float64Array(mw),ur=new Float64Array(mh);tiles.forEach(function(pi){var m=S.pg[pi].mask;for(y=0;y<mh;y++){var o=y*mw;for(x=0;x<mw;x++){var q=o+x;if(!c[q]&&((m[q>>3]>>(q&7))&1)){uc[x]++;ur[y]++}}}});
function clip(u,len,from){var mid=Array.prototype.slice.call(u,Math.round(.3*len),Math.round(.7*len)).sort(function(a,b){return a-b});var md=mid[mid.length>>1]||0;if(md<=0)return null;var th=.2*md,run=Math.round(2*R);
if(from){for(var i=0;i<len*.4;i++){var ok=true;for(var j=0;j<run;j++)if(u[i+j]<th){ok=false;break}if(ok){var k=i;while(k>0&&u[k-1]>0)k--;return k}}}else{for(var i2=len-1;i2>len*.6;i2--){var ok2=true;for(var j2=0;j2<run;j2++)if(u[i2-j2]<th){ok2=false;break}if(ok2){var k2=i2;while(k2<len-1&&u[k2+1]>0)k2++;return k2+1}}}return null}
var cl=clip(uc,mw,1),cr=clip(uc,mw,0),ct=clip(ur,mh,1),cb=clip(ur,mh,0);
function add(L,v,k){if(v==null)return;if(L.some(function(x){return Math.abs(x.v-v)<1.2*R}))return;L.push({v:v,s:0,k:k})}
add(out.l,cl,"clip");add(out.r,cr,"clip");add(out.t,ct,"clip");add(out.b,cb,"clip");
add(out.l,0,"edge");add(out.t,0,"edge");add(out.r,mw,"edge");add(out.b,mh,"edge");
return out}
function layout(n,c,colMajor,blanks){/* returns cells: [{p:index in order, row, col}] and seams */
var cells=[],k,rr,cc,R2;if(!colMajor){R2=Math.ceil(n/c);for(k=0;k<n;k++)cells.push({i:k,row:Math.floor(k/c),col:k%c});return {cells:cells,cols:c,rows:R2}}
R2=c;cc=Math.ceil(n/R2);for(k=0;k<n;k++)cells.push({i:k,row:k%R2,col:Math.floor(k/R2)});return {cells:cells,cols:cc,rows:R2}}
function seamsOf(L){var map={},V=[],H=[];L.cells.forEach(function(e){map[e.row+","+e.col]=e.i});L.cells.forEach(function(e){var r=map[e.row+","+(e.col+1)],b=map[(e.row+1)+","+e.col];if(r!=null)V.push([e.i,r]);if(b!=null)H.push([e.i,b])});return {V:V,H:H}}
function runs(pi,dir,pos){var key=pi+dir+pos,ch=S.cache[key];if(ch)return ch;var m=S.pg[pi].mask,c=S.cons,mw=S.mw,mh=S.mh,res=[],a=-1,i,q,lo,hi;
if(dir==="v"){pos=Math.max(0,Math.min(mw-1,pos));lo=Math.round(.03*mh);hi=Math.round(.97*mh);for(i=lo;i<=hi;i++){q=i*mw+pos;var d=i<hi&&!c[q]&&((m[q>>3]>>(q&7))&1);if(d){if(a<0)a=i}else if(a>=0){res.push([(a+i-1)/2,i-a]);a=-1}}}
else{pos=Math.max(0,Math.min(mh-1,pos));lo=Math.round(.03*mw);hi=Math.round(.97*mw);for(i=lo;i<=hi;i++){q=pos*mw+i;var d2=i<hi&&!c[q]&&((m[q>>3]>>(q&7))&1);if(d2){if(a<0)a=i}else if(a>=0){res.push([(a+i-1)/2,i-a]);a=-1}}}
S.cache[key]=res;return res}
function near(L,v,tol){var b=null,bd=tol;for(var i=0;i<L.length;i++){var d=Math.abs(L[i][0]-v);if(d<=bd){bd=d;b=L[i]}}return b}
function matchDir(a1,a2,b1,d,b2){var m=0,tt=0,mx=3*R;for(var i=0;i<a1.length;i++){var s=a1[i];if(s[1]>mx)continue;tt++;var n2=near(a2,s[0],d*1.6),sl=n2?(s[0]-n2[0])/d:0;var pred=s[0]+sl*2*d,tol=.5*R+Math.abs(sl)*d*.6+1+(n2?0:R*.6);if(near(b1,pred,tol)||(b2&&near(b2,s[0]+sl*3*d,tol+2)))m++}return [m,tt]}
function seamScore(A,B,dir,pa,pb){/* pa: trim position (px) on A's far side (right/bottom), pb: trim on B's near side (left/top) */
var d=Math.max(3,Math.round(.7*R));var a1=runs(A,dir,Math.floor(pa-d)),a2=runs(A,dir,Math.floor(pa-2*d)),b1=runs(B,dir,Math.floor(pb+d)),b2=runs(B,dir,Math.floor(pb+2*d));var x=matchDir(a1,a2,b1,d,b2),y=matchDir(b1,b2,a1,d,a2);return [x[0]+y[0],x[1]+y[1]]}
function bestPair(tiles,L,dir,A,B){var sm=seamsOf(L),P=dir==="v"?sm.V:sm.H,best={m:0,t:0,sc:-1};if(!P.length)return best;
A.forEach(function(a){B.forEach(function(b){var span=dir==="v"?S.mw:S.mh;if(b.v-a.v<.4*span)return;var m=0,tt=0;P.forEach(function(p){var r=seamScore(tiles[p[0]],tiles[p[1]],dir,b.v,a.v);m+=r[0];tt+=r[1]});var sc=2*m-tt;if(best.a==null||sc>best.sc)best={m:m,t:tt,sc:sc,r:(m+.5)/(tt+3),a:a,b:b}})});return best}

/* ---------- precise refinement (high resolution strips) ---------- */
async function refine(){var tr=S.trimSrc,tl=S.auto.tiles,use=tl.slice(0,Math.min(3,tl.length)),res={};
for(var side in tr){var c=tr[side],ax=(side==="l"||side==="r")?"x":"y",pos=c.v/R;/* mm */
if(c.k==="edge"){res[side]=side==="l"||side==="t"?0:(ax==="x"?S.W:S.H);continue}
var w=3,a0=pos-w/2,len=ax==="x"?S.H:S.W,lo=0,hi=len,profs=[];
for(var u=0;u<use.length;u++){var cw,chh,ox,oy;if(ax==="x"){cw=Math.round(w*HR);chh=Math.round((hi-lo)*HR);ox=a0*HR;oy=lo*HR}else{cw=Math.round((hi-lo)*HR);chh=Math.round(w*HR);ox=lo*HR;oy=a0*HR}
var cv=await renderCanvas(use[u],HR/PT,ox,oy,cw,chh),d=cv.getContext("2d").getImageData(0,0,cw,chh).data,n=ax==="x"?cw:chh,pr=new Float64Array(n),i,j;
for(j=0;j<chh;j++)for(i=0;i<cw;i++){var v=255-lum(d,(j*cw+i)*4)/1000;if(v>40){pr[ax==="x"?i:j]+=v/255}}profs.push(pr)}
var n2=profs[0].length,mn=new Float64Array(n2),k,best=null;
if(c.k==="line"){for(k=0;k<n2;k++){var v2=Infinity;profs.forEach(function(p){v2=Math.min(v2,p[k])});mn[k]=v2}var mx=0;for(k=0;k<n2;k++)mx=Math.max(mx,mn[k]);
/* the peak nearest the centre */
var thr=.5*mx,cen=n2/2,bk=-1;for(k=0;k<n2;k++)if(mn[k]>=thr&&(bk<0||Math.abs(k-cen)<Math.abs(bk-cen)))bk=k;var s=0,wt=0;if(bk>=0){var a=bk,b=bk;while(a>0&&mn[a-1]>=.15*mx)a--;while(b<n2-1&&mn[b+1]>=.15*mx)b++;for(k=a;k<=b;k++){s+=mn[k]*(k+.5);wt+=mn[k]}}best=wt>0?a0+s/wt/HR:pos;if(wt>0){var ea=a0+a/HR,eb=a0+(b+1)/HR,lim2=ax==="x"?S.W:S.H;if((side==="l"||side==="t")&&ea<=.06)best=0;if((side==="r"||side==="b")&&eb>=lim2-.06)best=lim2}}
else{/* clip: outermost ink across pages */var lowSide=(side==="l"||side==="t"),ext=null;profs.forEach(function(p){var mxp=0;for(k=0;k<n2;k++)mxp=Math.max(mxp,p[k]);var th=Math.max(.5,.02*mxp);if(lowSide){for(k=0;k<n2;k++)if(p[k]>th){ext=ext==null?k:Math.min(ext,k);break}}else{for(k=n2-1;k>=0;k--)if(p[k]>th){ext=ext==null?k+1:Math.max(ext,k+1);break}}});best=ext==null?pos:a0+ext/HR}
res[side]=best}
/* margins in mm */
S.trim={l:res.l,t:res.t,r:S.W-res.r,b:S.H-res.b};["l","t","r","b"].forEach(function(k){S.trim[k]=Math.max(0,Math.round(S.trim[k]*100)/100)});S.autoTrim=JSON.parse(JSON.stringify(S.trim))}

/* ---------- state from UI ---------- */
function parsePages(s){var out=[],ok=true;String(s).split(/[,; ]+/).forEach(function(p){if(!p)return;var m=p.match(/^(\d+)(?:-(\d+))?$/);if(!m){ok=false;return}var a=+m[1],b=m[2]?+m[2]:a;if(a<1||b<1||a>S.n||b>S.n){ok=false;return}if(a<=b)for(var i=a;i<=b;i++)out.push(i-1);else for(var j=a;j>=b;j--)out.push(j-1)});return ok?out:null}
function pagesStr(L){var out=[],i=0;while(i<L.length){var j=i;while(j+1<L.length&&L[j+1]===L[j]+1)j++;out.push(j>i?(L[i]+1)+"-"+(L[j]+1):String(L[i]+1));i=j+1}return out.join(", ")}
function fillUI(){$("pages").value=pagesStr(S.tiles);$("pagesHint").textContent=t("pagesHint",{n:S.n});$("cols").value=S.c;$("order").value=S.colMajor?"c":"r";["l","t","r","b"].forEach(function(k){$("t"+k).value=S.trim[k]});$("colsL").textContent=S.colMajor?t("rowsL"):t("colsL")}
function grid(){var n=S.order.length,L=layout(n,Math.max(1,Math.min(S.c,n)),S.colMajor,[]);return L}
function tileMM(){return {w:S.W-S.trim.l-S.trim.r,h:S.H-S.trim.t-S.trim.b}}
function checkScore(){var L=grid(),sm=seamsOf(L),m=0,tt=0,o=S.order;var pl=S.trim.l*R,pt=S.trim.t*R,pr=(S.W-S.trim.r)*R,pb=(S.H-S.trim.b)*R;
sm.V.forEach(function(p){var A=o[p[0]],B=o[p[1]];if(A<0||B<0||!S.pg[A].mask||!S.pg[B].mask)return;var r=seamScore(A,B,"v",pr,pl);m+=r[0];tt+=r[1]});
sm.H.forEach(function(p){var A=o[p[0]],B=o[p[1]];if(A<0||B<0||!S.pg[A].mask||!S.pg[B].mask)return;var r=seamScore(A,B,"h",pb,pt);m+=r[0];tt+=r[1]});return {m:m,t:tt}}
function update(){err("");$("done").style.display="none";var L=grid(),tm=tileMM(),bad=null;
S.order.forEach(function(pi){if(pi>=0&&!S.pg[pi].mask&&bad==null)bad=pi});
if(bad!=null){err(t("errSize",{p:bad+1}));$("dl").disabled=true;return}
var real=S.order.filter(function(x){return x>=0}).length;if(real<2){err(t("errOne"))}
$("dl").disabled=real<1||tm.w<=10||tm.h<=10;
$("gridInfo").textContent=t("gridInfo",{c:L.cols,r:L.rows,e:S.order.length-real});
var sc=checkScore(),bd=$("badge");if(sc.t<8){bd.className="a-badge wa";bd.textContent=t("unk")}else{var p=Math.round(100*sc.m/sc.t);bd.className="a-badge "+(p>=70?"ok":p>=45?"wa":"no");bd.textContent=t(p>=70?"ok":"wa",{p:p})}
drawFrame();drawPreview();var sh=sheets();$("size").textContent=fmt(L.cols*tm.w,0)+" × "+fmt(L.rows*tm.h,0)+" mm";$("sheets").textContent=$("out").value==="a0"?sh.list.length+" × A0":sh.list.length+" × "+fmt(sh.pw,0)+" × "+fmt(sh.ph,0)+" mm"}
function drawFrame(){var pi=S.order.filter(function(x){return x>=0})[0];if(pi==null)return;var th=S.pg[pi].thumb,c=$("frame");c.width=th.width;c.height=th.height;var x=c.getContext("2d");x.drawImage(th,0,0);x.strokeStyle="#E0002B";x.lineWidth=2;var l=S.trim.l*TH,tp=S.trim.t*TH,r=(S.W-S.trim.r)*TH,b=(S.H-S.trim.b)*TH;x.setLineDash([]);x.beginPath();x.moveTo(l,0);x.lineTo(l,c.height);x.moveTo(r,0);x.lineTo(r,c.height);x.moveTo(0,tp);x.lineTo(c.width,tp);x.moveTo(0,b);x.lineTo(c.width,b);x.stroke();$("frameCap").textContent=t("frameCap",{p:pi+1})}
function drawPreview(){var L=grid(),tm=tileMM(),tw=tm.w*TH,th=tm.h*TH,c=$("pv");c.width=Math.max(1,Math.round(L.cols*tw));c.height=Math.max(1,Math.round(L.rows*th));var x=c.getContext("2d");x.fillStyle="#fff";x.fillRect(0,0,c.width,c.height);
L.cells.forEach(function(e){var pi=S.order[e.i],X=e.col*tw,Y=e.row*th;if(pi<0){x.fillStyle="#F8EEF0";x.fillRect(X,Y,tw,th);x.fillStyle="#7A2340";x.font="bold "+Math.round(th/9)+"px sans-serif";x.textAlign="center";x.fillText(t("empty"),X+tw/2,Y+th/2);return}var g=S.pg[pi];if(!g.thumb)return;x.drawImage(g.thumb,S.trim.l*TH,S.trim.t*TH,tw,th,X,Y,tw,th)});
if(S.seams!==false){x.strokeStyle="rgba(122,35,64,.55)";x.lineWidth=1;x.setLineDash([6,4]);x.beginPath();for(var i=1;i<L.cols;i++){x.moveTo(i*tw,0);x.lineTo(i*tw,c.height)}for(var j=1;j<L.rows;j++){x.moveTo(0,j*th);x.lineTo(c.width,j*th)}x.stroke();x.setLineDash([]);x.font="bold "+Math.max(10,Math.round(th/12))+"px sans-serif";x.textAlign="left";L.cells.forEach(function(e){var pi=S.order[e.i];if(pi<0)return;var X=e.col*tw+4,Y=e.row*th+4,s=String(pi+1);x.fillStyle="rgba(20,33,61,.85)";var w2=x.measureText(s).width+8,h2=Math.max(10,Math.round(th/12))+6;x.fillRect(X,Y,w2,h2);x.fillStyle="#fff";x.fillText(s,X+4,Y+h2-5)})}}
/* ---------- sheets ---------- */
function sheets(){/* sheets are windows over the assembled pattern: no paper wasted, joins are exact */var L=grid(),tm=tileMM(),mg=+$("mg").value,out=$("out").value,W=L.cols*tm.w,H=L.rows*tm.h,MX=5000,best=null;
function win(cw,ch,pw,ph){if(cw<=0||ch<=0)return null;var nx=Math.max(1,Math.ceil(W/cw-1e-9)),ny=Math.max(1,Math.ceil(H/ch-1e-9));return {nx:nx,ny:ny,n:nx*ny,ww:W/nx,wh:H/ny,pw:pw,ph:ph}}
var o=[];if(out==="a0"){o.push(win(841-2*mg,1189-2*mg,841,1189));o.push(win(1189-2*mg,841-2*mg,1189,841))}
else if(out==="roll"){o.push(win(914-2*mg,MX-2*mg,914,null));o.push(win(MX-2*mg,914-2*mg,null,914))}
else o.push(win(MX-2*mg,MX-2*mg,null,null));
o.forEach(function(x){if(x&&(!best||x.n<best.n||(x.n===best.n&&(x.pw||0)*(x.ph||0)<(best.pw||0)*(best.ph||0))))best=x});
if(!best)return {list:[],pw:0,ph:0};var list=[];for(var sy=0;sy<best.ny;sy++)for(var sx=0;sx<best.nx;sx++)list.push({sx:sx,sy:sy,x0:sx*best.ww,y0:sy*best.wh,w:best.ww,h:best.wh});
return {list:list,pw:best.pw==null?best.ww+2*mg:best.pw,ph:best.ph==null?best.wh+2*mg:best.ph,nx:best.nx,ny:best.ny,mg:mg}}

/* ---------- PDF output (vector, 100% scale) ---------- */
async function build(){var P=PDFLib,src=await P.PDFDocument.load(S.bytes,{updateMetadata:false}),out=await P.PDFDocument.create(),cp=P.PDFObjectCopier.for(src.context,out.context);
var L=grid(),tm=tileMM(),sh=sheets(),mg=sh.mg,tw=tm.w*PT,th=tm.h*PT,xo={};
var used={};S.order.forEach(function(pi){if(pi>=0)used[pi]=1});
for(var key in used){var pi=+key,pg=src.getPage(pi),node=pg.node,ne=node.normalizedEntries(),jp=await S.pdf.getPage(pi+1),vp=jp.getViewport({scale:1});
/* displayed tile rect -> PDF user space */
var X0=S.trim.l*PT,Y0=S.trim.t*PT,X1=(S.W-S.trim.r)*PT,Y1=(S.H-S.trim.b)*PT,pts=[vp.convertToPdfPoint(X0,Y0),vp.convertToPdfPoint(X1,Y0),vp.convertToPdfPoint(X0,Y1),vp.convertToPdfPoint(X1,Y1)];
var bl=Math.min.apply(null,pts.map(function(p){return p[0]})),bb=Math.min.apply(null,pts.map(function(p){return p[1]})),br=Math.max.apply(null,pts.map(function(p){return p[0]})),bt=Math.max.apply(null,pts.map(function(p){return p[1]}));
var parts=[],Cn=ne.Contents;if(Cn){for(var k=0;k<Cn.size();k++){var st=Cn.lookup(k);if(st instanceof P.PDFRawStream)parts.push(P.decodePDFRawStream(st).decode());else if(st instanceof P.PDFContentStream)parts.push(st.getUnencodedContents())}}
var tot=0;parts.forEach(function(a){tot+=a.length+1});var all=new Uint8Array(tot+4),o=0;all.set([113,10],0);o=2;parts.forEach(function(a){all.set(a,o);o+=a.length;all[o++]=10});all.set([81,10],o);o+=2;
var res=ne.Resources?cp.copy(ne.Resources):out.context.obj({});
var form=out.context.flateStream(all.subarray(0,o),{Type:"XObject",Subtype:"Form",FormType:1,BBox:[bl,bb,br,bt],Matrix:[1,0,0,1,-bl,-bb],Resources:res});
xo[pi]={ref:out.context.register(form),uw:br-bl,uh:bt-bb,rot:((jp.rotate||0)%360+360)%360}}
/* optional content (layers) */
try{var oc=src.catalog.lookup(P.PDFName.of("OCProperties"));if(oc)out.catalog.set(P.PDFName.of("OCProperties"),cp.copy(oc))}catch(e){}
var font=await out.embedFont(P.StandardFonts.Helvetica),fontB=await out.embedFont(P.StandardFonts.HelveticaBold),ink=P.rgb(.08,.13,.24),rose=P.rgb(.48,.14,.25);
var idx={};sh.list.forEach(function(s,i){idx[s.sx+","+s.sy]=i+1});
sh.list.forEach(function(s,si){var PW=sh.pw*PT,PH=sh.ph*PT,page=out.addPage([PW,PH]),ops=[],cx=mg*PT,cy=PH-mg*PT-s.h*PT;
ops.push(P.pushGraphicsState(),P.rectangle(cx,cy,s.w*PT,s.h*PT),P.clip(),P.endPath());
L.cells.forEach(function(e){var pi=S.order[e.i];if(pi<0)return;var ex=e.col*tm.w,ey=e.row*tm.h;if(ex>=s.x0+s.w-1e-6||ex+tm.w<=s.x0+1e-6||ey>=s.y0+s.h-1e-6||ey+tm.h<=s.y0+1e-6)return;
var X=(mg+ex-s.x0)*PT,Y=PH-(mg+ey-s.y0)*PT-th,x=xo[pi],a,b,c,d,tx,ty;
if(x.rot===0){a=1;b=0;c=0;d=1;tx=X;ty=Y}else if(x.rot===90){a=0;b=-1;c=1;d=0;tx=X;ty=Y+x.uw}else if(x.rot===180){a=-1;b=0;c=0;d=-1;tx=X+x.uw;ty=Y+x.uh}else{a=0;b=1;c=-1;d=0;tx=X+x.uh;ty=Y}
var nm=page.node.newXObject("SCt",x.ref);ops.push(P.pushGraphicsState(),P.concatTransformationMatrix(a,b,c,d,tx,ty),P.drawObject(nm),P.popGraphicsState())});
ops.push(P.popGraphicsState());page.pushOperators.apply(page,ops);
if(sh.list.length>1){/* thin trim line around the printed area so sheets can be butted together */page.drawRectangle({x:cx,y:cy,width:s.w*PT,height:s.h*PT,borderColor:rose,borderWidth:.4,borderDashArray:[3,2]})}
if(mg>=5){var fs=Math.min(7,mg*PT*.45),yT=PH-mg*PT/2-fs/3,lab=t("sheet",{i:si+1,n:sh.list.length}),j=[];var rk=idx[(s.sx+1)+","+s.sy],bk=idx[s.sx+","+(s.sy+1)];if(rk)j.push(t("joinR",{k:rk}));if(bk)j.push(t("joinB",{k:bk}));
var line=safe(lab+(j.length?"  ·  "+j.join("  ·  "):"")+"  ·  "+t("pdfNote"));page.drawText(line,{x:mg*PT,y:yT,size:fs,font:fontB,color:rose});var site="sewcraftlypatterns.com";page.drawText(site,{x:PW-mg*PT-font.widthOfTextAtSize(site,fs),y:yT,size:fs,font:font,color:ink});
if(si===0&&$("ruler").checked)ruler(page,mg,font,fs,ink,rose)}});
out.setTitle(S.name+" – A0");out.setProducer("SewCraftly A4 to A0 converter");out.setCreator("sewcraftlypatterns.com");
return await out.save({useObjectStreams:true})}
function safe(s){return s.replace(/[″]/g,"in").replace(/[“”]/g,'"').replace(/[’]/g,"'").replace(/[^\x20-\x7E -ÿ·]/g,"")}
function ruler(page,mg,font,fs,ink,rose){var P=PDFLib,y=mg*PT*.32,h=Math.min(3.2,mg*.45)*PT,x0=mg*PT;
function bar(x,len,step,lab){page.drawLine({start:{x:x,y:y},end:{x:x+len,y:y},thickness:.6,color:ink});var n=Math.round(len/step);for(var i=0;i<=n;i++){var hh=(i===0||i===n)?h:h*.5;page.drawLine({start:{x:x+i*step,y:y},end:{x:x+i*step,y:y+hh},thickness:.6,color:ink})}page.drawText(safe(lab),{x:x+len+6,y:y+h*.15,size:fs,font:font,color:rose})}
bar(x0,100*PT,10*PT,"10 cm - "+t("rul")+" 100 mm");bar(x0+100*PT+95,4*72,72,"4 in - "+t("rul")+" 4 in")}

/* ---------- events ---------- */
var drop=$("drop"),fi=$("file");
fi.addEventListener("change",function(){if(fi.files&&fi.files[0])go(fi.files[0])});
["dragenter","dragover"].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.add("on")})});
["dragleave","drop"].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.remove("on")})});
drop.addEventListener("drop",function(e){var f=e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0];if(f)go(f)});
var busy=false;async function go(f){if(busy)return;busy=true;try{await openFile(f)}catch(e){console.error(e);$("prog").style.display="none";err(t("errRead"))}busy=false;fi.value=""}
$("new").onclick=function(){$("main").style.display="none";$("start").style.display="block";$("new").style.display="none";err("");if(S&&S.pdf){try{S.pdf.destroy()}catch(e){}}S=null};
$("pages").addEventListener("change",function(){var L=parsePages(this.value);if(!L||!L.length){err(t("errPages",{n:S.n}));return}S.tiles=L;S.order=L.slice();update()});
$("cols").addEventListener("input",function(){var v=parseInt(this.value,10);if(v>=1){S.c=v;update()}});
$("order").addEventListener("change",function(){S.colMajor=this.value==="c";$("colsL").textContent=S.colMajor?t("rowsL"):t("colsL");update()});
["l","t","r","b"].forEach(function(k){$("t"+k).addEventListener("input",function(){var v=parseFloat(String(this.value).replace(",","."));if(v>=0&&v<(k==="l"||k==="r"?S.W:S.H)/2){S.trim[k]=v;update()}})});
$("redo").onclick=function(){S.trim=JSON.parse(JSON.stringify(S.autoTrim));S.tiles=S.auto.tiles.slice();S.order=(S.auto.order||S.tiles).slice();S.c=S.auto.c;S.colMajor=S.auto.colMajor;fillUI();update()};
["out","mg"].forEach(function(k){$(k).addEventListener("change",update)});
$("seams").onclick=function(){S.seams=S.seams===false;this.classList.toggle("on",S.seams!==false);drawPreview()};
$("zoom").onclick=function(){var w=$("pvw");w.classList.toggle("z");this.classList.toggle("on",w.classList.contains("z"))};
$("pv").addEventListener("click",function(e){var c=this,r=c.getBoundingClientRect(),L=grid(),tm=tileMM(),x=(e.clientX-r.left)*c.width/r.width,y=(e.clientY-r.top)*c.height/r.height,col=Math.floor(x/(tm.w*TH)),row=Math.floor(y/(tm.h*TH));var cell=L.cells.filter(function(q){return q.col===col&&q.row===row})[0];if(!cell)return;if(S.order[cell.i]<0)S.order.splice(cell.i,1);else S.order.splice(cell.i,0,-1);update()});
$("dl").onclick=async function(){var b=this;if(b.disabled)return;b.disabled=true;var lbl=b.textContent;b.textContent=t("building");try{var bytes=await build();var blob=new Blob([bytes],{type:"application/pdf"}),u=URL.createObjectURL(blob),a=document.createElement("a");a.href=u;a.download=S.name+"_A0.pdf";document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(u);a.remove()},4000);$("done").style.display="block";window.__sca0last=bytes}catch(e){console.error(e);err(t("errRead")+" ("+(e&&e.message)+")")}b.textContent=lbl;b.disabled=false};
window.__sca0=function(){return S};window.__sca0dbg={orderScore:orderScore,blanks:blanks,chooseLayout:chooseLayout,layout:layout,seamsOf:seamsOf,seamScore:seamScore,runs:runs,bestPair:bestPair,matchDir:matchDir};window.__sca0build=build;
})();
