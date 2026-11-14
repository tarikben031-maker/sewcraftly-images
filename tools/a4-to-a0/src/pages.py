import json, html
BLOCK = "{{BLOCK}}"
def para(cls, txt): return '<!-- wp:paragraph {"className":"%s"} -->\n<p class="%s">%s</p>\n<!-- /wp:paragraph -->' % (cls, cls, txt)
def p(txt): return '<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->' % txt
def h2(txt): return '<!-- wp:heading -->\n<h2 class="wp-block-heading">%s</h2>\n<!-- /wp:heading -->' % txt
def ol(items, ordered=True):
    tag = 'ol' if ordered else 'ul'
    attr = ' {"ordered":true}' if ordered else ''
    li = '\n\n'.join('<!-- wp:list-item -->\n<li>%s</li>\n<!-- /wp:list-item -->' % i for i in items)
    return '<!-- wp:list%s -->\n<%s class="wp-block-list">%s\n\n</%s>\n<!-- /wp:list -->' % (attr, tag, li, tag)
def facts(pairs):
    inner = ''.join('<!-- wp:paragraph -->\n<p><strong>%s</strong> %s</p>\n<!-- /wp:paragraph -->' % kv for kv in pairs)
    return '<!-- wp:group {"className":"pp-facts","layout":{"type":"constrained"}} -->\n<div class="wp-block-group pp-facts">%s</div>\n<!-- /wp:group -->' % inner
def card(h, txt):
    return '<!-- wp:group {"className":"pp-card","layout":{"type":"constrained"}} -->\n<div class="wp-block-group pp-card"><!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">%s</h3>\n<!-- /wp:heading --><!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph --></div>\n<!-- /wp:group -->' % (h, txt)
def faq(q, a): return '<!-- wp:details {"className":"pp-faq"} -->\n<details class="wp-block-details pp-faq"><summary>%s</summary><!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph --></details>\n<!-- /wp:details -->' % (q, a)
def ad(n): return '<!-- wp:html -->\n<div class="pp-ad" data-ad="%d"><!-- AD %d: paste AdSense code here --></div>\n<!-- /wp:html -->' % (n, n)
def strip(s):
    import re; return re.sub('<[^>]+>', '', s)

def page(L):
    parts = ['<!-- wp:block {"ref":1823} /-->', '<!-- wp:group {"className":"pp-post sc-tutorial sc-tool","layout":{"type":"constrained"}} -->\n<div class="wp-block-group pp-post sc-tutorial sc-tool">' + para('pp-intro', L['intro']),
             facts(L['facts']), '<!-- wp:block {"ref":%s} /-->' % BLOCK, para('pp-seo', L['seo']), para('pp-banner', L['banner']),
             h2(L['h_use']), ol(L['use']), h2(L['h_print']), p(L['print']), ol(L['print_list'], False), para('pp-note', L['tip']), ad(1),
             h2(L['h_size']), p(L['size']), card(L['card_h'], L['card']), ad(2), h2(L['h_faq'])]
    parts += [faq(q, a) for q, a in L['faq']]
    if L.get('more'): parts.append('<!-- wp:block {"ref":%d} /-->' % L['more'])
    parts.append(para('pp-closing', L['closing']))
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in L['faq']]}
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": L['app'], "description": L['meta_d'], "url": L['url'], "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": L['lang'], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@type": "Organization", "name": "SewCraftly", "url": "https://sewcraftlypatterns.com"}}
    parts.append('<!-- wp:html -->\n<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>\n<!-- /wp:html -->' % (json.dumps(fq, ensure_ascii=False), json.dumps(app, ensure_ascii=False)))
    content = '\n\n'.join(parts) + '\n\n</div>\n<!-- /wp:group -->'
    return {"title": L['title'], "slug": L['slug'], "status": "publish", "content": content, "comment_status": "closed",
            "meta": {"rank_math_title": L['meta_t'], "rank_math_description": L['meta_d'], "rank_math_focus_keyword": L['kw']}}

EN = dict(lang='en', slug='a4-to-a0-pattern-converter', url='https://sewcraftlypatterns.com/a4-to-a0-pattern-converter/', app='A4 to A0 Pattern Converter',
 title='A4 to A0 Pattern Converter: Turn a PDF Sewing Pattern into a Copy Shop File',
 meta_t='A4 to A0 Pattern Converter – Free PDF Copy Shop Tool',
 meta_d='Free A4 to A0 converter for PDF sewing patterns: joins your A4 or US Letter pages into a 100% scale A0 copy shop file, right in your browser.',
 kw='a4 to a0 pattern converter,convert pdf pattern to a0,copy shop sewing pattern',
 intro='Printed your PDF sewing pattern on A4 and tired of taping 40 pages together? This free A4 to A0 pattern converter joins the tiled A4 or US Letter pages of your pattern into one large copy shop file, on A0 sheets or a 36″ plotter roll. It finds the cut lines and the page order on its own, keeps the pattern in vector quality at exactly 100% scale, and your file never leaves your device.',
 facts=[('Time','1 min'),('Input','A4 or US Letter PDF'),('Output','A0 or plotter roll'),('Upload','None, stays on your device')],
 seo='Below you will see how the converter works, how to print an A0 sewing pattern at a copy shop, and what to check before you cut.',
 banner='<strong>In short:</strong> drop the PDF, check that the preview matches the layout page of your pattern, download the A0 file, and ask the copy shop to print it at 100% (actual size).',
 h_use='How to use the A4 to A0 pattern converter',
 use=['<strong>Drop your PDF.</strong> Use the print-at-home file with the tiled pages (A4 or US Letter). The cover and instruction pages are left out automatically.',
      '<strong>Check the layout.</strong> The tool finds the number of columns, the page order and the cut lines, then checks that the pattern lines continue from one page to the next. Compare the preview with the layout page of your pattern. If the layout has empty squares, click the page that comes after an empty square to add it.',
      '<strong>Choose the paper.</strong> A0 sheets (841 × 1189 mm) for most copy shops, one sheet at the exact size, or a 36″ (914 mm) roll for plotters.',
      '<strong>Download and print.</strong> The file opens in any PDF reader. Print it at 100% (actual size) and measure the check ruler before you cut.'],
 h_print='How to print a sewing pattern at a copy shop',
 print='Copy shops print large plans on wide-format plotters. Send them the A0 PDF by email or on a USB stick, and ask for a black and white print at 100% or “actual size” on plain paper. If the pattern is larger than one A0 sheet, the converter splits it along page joins, and each sheet says which sheet goes on its right and below it.',
 print_list=['Ask for 100% scale, never “fit to page”.','Measure the 10 cm and 4″ ruler on sheet 1 before you cut.','Keep the file as it is: layers, colors and line weights stay the same as in the A4 file.'],
 tip='<strong>Tip:</strong> layers (one per size) are kept in the A0 file. To print one size only, open the layers panel in Adobe Acrobat Reader, hide the other sizes, then print or send the file.',
 h_size='Will the A0 pattern be the right size?',
 size='Yes, as long as it is printed at 100%. The converter does not resize anything: it cuts each page along its cut lines and places the pages edge to edge, in vector quality. You get the same pattern as when you trim and tape the A4 pages, without the small gaps and overlaps that taping adds.',
 card_h='What if the preview does not look right?',
 card='Check the tile pages (leave out the cover and instructions), the number of columns and the page order (row by row or column by column). The cut lines are measured automatically: change them only if the preview shows a gap or an overlap between pages. Locked PDF files cannot be converted, so ask the designer for the A0 or copy shop file.',
 h_faq='Questions',
 faq=[('Is this A4 to A0 converter free?','Yes. It is free, with no account, and the conversion runs in your browser, so your pattern is never uploaded.'),
      ('Does it work with US Letter patterns?','Yes. It works with tiled PDF patterns in A4, US Letter and other page sizes, portrait or landscape. You can print the result on A0 sheets or on a 36″ roll.'),
      ('What size is A0 paper?','A0 is 841 × 1189 mm (33.1 × 46.8 in). Most copy shops can also print on rolls 914 mm (36″) wide.'),
      ('Why can’t my PDF be converted?','Some designers lock their PDF files. The converter respects that lock: ask the designer for the A0 or copy shop version, which is often included with the pattern.')],
 more=1847,
 closing='New to PDF patterns? Read <a href="/tutorials/how-to-print-and-assemble-pdf-sewing-patterns/">how to print and assemble a PDF sewing pattern</a>.')

FR = dict(lang='fr', slug='convertir-patron-a4-en-a0', url='https://sewcraftlypatterns.com/fr/convertir-patron-a4-en-a0/', app='Convertisseur de patron A4 en A0',
 title='Convertir un patron A4 en A0 : le PDF prêt pour le copy shop',
 meta_t='Convertir un patron A4 en A0 – Outil PDF gratuit',
 meta_d='Outil gratuit pour convertir un patron de couture PDF A4 en A0 : les pages A4 ou US Letter sont assemblées à l’échelle 100 %, directement dans le navigateur.',
 kw='convertir patron a4 en a0,patron pdf a0,patron couture copy shop',
 intro='Votre patron de couture PDF est en A4 et vous n’avez pas envie de coller 40 pages ? Ce convertisseur gratuit assemble les pages A4 ou US Letter de votre patron en un grand fichier pour le copy shop, sur des feuilles A0 ou un rouleau de traceur de 914 mm. Il trouve seul les lignes de coupe et l’ordre des pages, garde le patron en qualité vectorielle à l’échelle exacte de 100 %, et le fichier ne quitte jamais votre appareil.',
 facts=[('Durée','1 min'),('Fichier','PDF A4 ou US Letter'),('Résultat','A0 ou rouleau'),('Envoi','Aucun, tout reste sur l’appareil')],
 seo='Plus bas, vous verrez comment fonctionne le convertisseur, comment imprimer un patron A0 au copy shop et ce qu’il faut vérifier avant de couper.',
 banner='<strong>En bref :</strong> déposez le PDF, vérifiez que l’aperçu correspond au plan d’assemblage du patron, téléchargez le fichier A0 et demandez une impression à 100 % (taille réelle).',
 h_use='Comment utiliser le convertisseur A4 en A0',
 use=['<strong>Déposez le PDF.</strong> Prenez le fichier « à imprimer chez soi » avec les pages à assembler (A4 ou US Letter). La couverture et les pages d’instructions sont écartées automatiquement.',
      '<strong>Vérifiez la disposition.</strong> L’outil trouve le nombre de colonnes, l’ordre des pages et les lignes de coupe, puis vérifie que les lignes du patron continuent d’une page à l’autre. Comparez l’aperçu avec le plan d’assemblage du patron. S’il y a des cases vides dans le plan, cliquez sur la page qui suit une case vide pour l’ajouter.',
      '<strong>Choisissez le papier.</strong> Feuilles A0 (841 × 1189 mm) pour la plupart des copy shops, une seule feuille à la taille exacte, ou un rouleau de 914 mm (36″) pour les traceurs.',
      '<strong>Téléchargez et imprimez.</strong> Le fichier s’ouvre dans n’importe quel lecteur PDF. Imprimez à 100 % (taille réelle) et mesurez la règle de contrôle avant de couper.'],
 h_print='Comment imprimer un patron de couture au copy shop',
 print='Les copy shops impriment les grands plans sur des traceurs grand format. Envoyez-leur le PDF A0 par e-mail ou sur une clé USB, et demandez une impression noir et blanc à 100 % ou « taille réelle » sur papier ordinaire. Si le patron dépasse une feuille A0, le convertisseur le partage le long des raccords de pages, et chaque feuille indique quelle feuille se place à droite et en dessous.',
 print_list=['Demandez l’échelle 100 %, jamais « ajuster à la page ».','Mesurez la règle de 10 cm et 4″ sur la feuille 1 avant de couper.','Le fichier reste fidèle : calques, couleurs et épaisseurs de traits sont les mêmes que dans le fichier A4.'],
 tip='<strong>Astuce :</strong> les calques (un par taille) sont conservés dans le fichier A0. Pour n’imprimer qu’une taille, ouvrez le panneau des calques dans Adobe Acrobat Reader, masquez les autres tailles, puis imprimez ou envoyez le fichier.',
 h_size='Le patron A0 sera-t-il à la bonne taille ?',
 size='Oui, s’il est imprimé à 100 %. Le convertisseur ne redimensionne rien : il coupe chaque page sur ses lignes de coupe et place les pages bord à bord, en qualité vectorielle. Vous obtenez le même patron qu’en recoupant et en collant les pages A4, sans les petits décalages que le collage ajoute.',
 card_h='Et si l’aperçu ne semble pas correct ?',
 card='Vérifiez les pages à assembler (sans la couverture ni les instructions), le nombre de colonnes et l’ordre des pages (rangée par rangée ou colonne par colonne). Les lignes de coupe sont mesurées automatiquement : ne les changez que si l’aperçu montre un trou ou un chevauchement. Les PDF verrouillés ne peuvent pas être convertis : demandez le fichier A0 ou copy shop à la créatrice.',
 h_faq='Questions fréquentes',
 faq=[('Ce convertisseur A4 en A0 est-il gratuit ?','Oui. Il est gratuit, sans compte, et la conversion se fait dans votre navigateur : votre patron n’est jamais envoyé.'),
      ('Fonctionne-t-il avec les patrons US Letter ?','Oui. Il fonctionne avec les patrons PDF à assembler en A4, US Letter et autres formats, portrait ou paysage. Le résultat s’imprime sur feuilles A0 ou sur un rouleau de 914 mm.'),
      ('Quelle est la taille d’une feuille A0 ?','Une feuille A0 mesure 841 × 1189 mm. La plupart des copy shops impriment aussi sur des rouleaux de 914 mm (36″) de large.'),
      ('Pourquoi mon PDF ne peut-il pas être converti ?','Certaines créatrices verrouillent leurs fichiers PDF. Le convertisseur respecte ce verrou : demandez la version A0 ou copy shop, souvent fournie avec le patron.')],
 closing='Découvrez aussi nos autres <a href="/fr/outils-couture/">outils de couture gratuits</a>.')

DE = dict(lang='de', slug='schnittmuster-a4-in-a0', url='https://sewcraftlypatterns.com/de/schnittmuster-a4-in-a0/', app='Schnittmuster A4 in A0 umwandeln',
 title='Schnittmuster A4 in A0 umwandeln: die Copyshop-Datei aus deinem PDF',
 meta_t='Schnittmuster A4 in A0 umwandeln – kostenloses PDF-Tool',
 meta_d='Kostenloses Tool: Schnittmuster-PDF von A4 in A0 umwandeln. Die A4- oder US-Letter-Seiten werden im Browser im Maßstab 100 % zur Copyshop-Datei zusammengesetzt.',
 kw='schnittmuster a4 in a0 umwandeln,schnittmuster a0 copyshop,pdf schnittmuster a0',
 intro='Dein PDF-Schnittmuster ist in A4 und du hast keine Lust, 40 Seiten zu kleben? Dieses kostenlose Tool setzt die A4- oder US-Letter-Seiten deines Schnittmusters zu einer großen Copyshop-Datei zusammen, auf A0-Bögen oder einer 914-mm-Plotterrolle. Es findet die Schnittlinien und die Seitenreihenfolge selbst, behält die Vektorqualität im exakten Maßstab 100 %, und die Datei verlässt nie dein Gerät.',
 facts=[('Dauer','1 Min.'),('Datei','PDF in A4 oder US Letter'),('Ergebnis','A0 oder Rolle'),('Upload','Keiner, alles bleibt auf dem Gerät')],
 seo='Weiter unten siehst du, wie das Tool arbeitet, wie du ein A0-Schnittmuster im Copyshop druckst und was du vor dem Zuschneiden prüfen solltest.',
 banner='<strong>Kurz gesagt:</strong> PDF ablegen, Vorschau mit dem Klebeplan vergleichen, A0-Datei herunterladen und im Copyshop mit 100 % (Originalgröße) drucken lassen.',
 h_use='So nutzt du den A4-in-A0-Konverter',
 use=['<strong>PDF ablegen.</strong> Nimm die Datei zum Ausdrucken zu Hause mit den Klebeseiten (A4 oder US Letter). Deckblatt und Anleitungsseiten werden automatisch weggelassen.',
      '<strong>Anordnung prüfen.</strong> Das Tool findet Spaltenzahl, Seitenreihenfolge und Schnittlinien und prüft, ob die Linien des Schnittmusters von Seite zu Seite weiterlaufen. Vergleiche die Vorschau mit dem Klebeplan. Hat der Klebeplan leere Felder, klicke auf die Seite nach einem leeren Feld, um es einzufügen.',
      '<strong>Papier wählen.</strong> A0-Bögen (841 × 1189 mm) für die meisten Copyshops, ein Bogen in genauer Größe oder eine 914-mm-Rolle (36″) für Plotter.',
      '<strong>Herunterladen und drucken.</strong> Die Datei öffnet sich in jedem PDF-Reader. Mit 100 % (Originalgröße) drucken und vor dem Zuschneiden das Kontroll-Lineal messen.'],
 h_print='So druckst du ein Schnittmuster im Copyshop',
 print='Copyshops drucken große Pläne auf Großformat-Plottern. Schick ihnen die A0-PDF per E-Mail oder auf einem USB-Stick und bitte um einen Schwarz-Weiß-Druck mit 100 % bzw. „Originalgröße“ auf Normalpapier. Ist das Schnittmuster größer als ein A0-Bogen, teilt das Tool es entlang der Seitenübergänge, und auf jedem Bogen steht, welcher Bogen rechts und darunter anschließt.',
 print_list=['100 % verlangen, nie „an Seite anpassen“.','Vor dem Zuschneiden das Lineal mit 10 cm und 4″ auf Bogen 1 messen.','Die Datei bleibt originalgetreu: Ebenen, Farben und Linienstärken wie in der A4-Datei.'],
 tip='<strong>Tipp:</strong> Ebenen (eine pro Größe) bleiben in der A0-Datei erhalten. Um nur eine Größe zu drucken, öffne in Adobe Acrobat Reader die Ebenen, blende die anderen Größen aus und drucke oder verschicke die Datei dann.',
 h_size='Hat das A0-Schnittmuster die richtige Größe?',
 size='Ja, wenn es mit 100 % gedruckt wird. Das Tool skaliert nichts: Es schneidet jede Seite an ihren Schnittlinien und legt die Seiten Kante an Kante, in Vektorqualität. Du bekommst dasselbe Schnittmuster wie beim Zuschneiden und Kleben der A4-Seiten, nur ohne die kleinen Lücken und Überlappungen vom Kleben.',
 card_h='Was tun, wenn die Vorschau nicht stimmt?',
 card='Prüfe die Klebeseiten (ohne Deckblatt und Anleitung), die Spaltenzahl und die Reihenfolge (Reihe für Reihe oder Spalte für Spalte). Die Schnittlinien werden automatisch gemessen: Ändere sie nur, wenn die Vorschau eine Lücke oder Überlappung zeigt. Gesperrte PDFs lassen sich nicht umwandeln, frag dann nach der A0- oder Copyshop-Datei.',
 h_faq='Häufige Fragen',
 faq=[('Ist der A4-in-A0-Konverter kostenlos?','Ja. Er ist kostenlos, ohne Konto, und die Umwandlung läuft in deinem Browser, dein Schnittmuster wird also nie hochgeladen.'),
      ('Funktioniert er mit US-Letter-Schnittmustern?','Ja. Er funktioniert mit PDF-Schnittmustern zum Kleben in A4, US Letter und anderen Formaten, hoch oder quer. Das Ergebnis kannst du auf A0-Bögen oder auf einer 914-mm-Rolle drucken.'),
      ('Wie groß ist ein A0-Bogen?','A0 misst 841 × 1189 mm. Die meisten Copyshops drucken auch auf 914 mm (36″) breiten Rollen.'),
      ('Warum lässt sich meine PDF nicht umwandeln?','Manche Designerinnen sperren ihre PDF-Dateien. Das Tool respektiert diese Sperre: Frag nach der A0- oder Copyshop-Version, die oft beim Schnittmuster dabei ist.')],
 closing='Entdecke auch unsere anderen <a href="/de/naeh-rechner/">kostenlosen Näh-Rechner</a>.')

NL = dict(lang='nl', slug='patroon-a4-naar-a0', url='https://sewcraftlypatterns.com/nl/patroon-a4-naar-a0/', app='Naaipatroon A4 naar A0 omzetten',
 title='Naaipatroon A4 naar A0 omzetten: je PDF klaar voor de copyshop',
 meta_t='Naaipatroon A4 naar A0 omzetten – gratis PDF-tool',
 meta_d='Gratis tool om een PDF-naaipatroon van A4 naar A0 om te zetten: je A4- of US Letter-pagina’s worden in de browser op 100% schaal tot een copyshopbestand samengevoegd.',
 kw='patroon a4 naar a0,naaipatroon a0 copyshop,pdf patroon a0',
 intro='Is je PDF-naaipatroon in A4 en heb je geen zin om 40 pagina’s te plakken? Deze gratis tool voegt de A4- of US Letter-pagina’s van je patroon samen tot één groot copyshopbestand, op A0-vellen of een plotterrol van 914 mm. Hij vindt zelf de kniplijnen en de paginavolgorde, houdt het patroon in vectorkwaliteit op precies 100% schaal, en je bestand verlaat nooit je apparaat.',
 facts=[('Tijd','1 min'),('Bestand','PDF in A4 of US Letter'),('Resultaat','A0 of rol'),('Upload','Geen, alles blijft op je apparaat')],
 seo='Verderop lees je hoe de tool werkt, hoe je een A0-patroon in de copyshop print en wat je controleert voor je knipt.',
 banner='<strong>In het kort:</strong> sleep de PDF erin, vergelijk de preview met het plakplan van je patroon, download het A0-bestand en laat het in de copyshop printen op 100% (ware grootte).',
 h_use='Zo gebruik je de A4 naar A0 converter',
 use=['<strong>Sleep je PDF erin.</strong> Gebruik het bestand om thuis te printen, met de plakpagina’s (A4 of US Letter). De omslag en instructiepagina’s worden automatisch weggelaten.',
      '<strong>Controleer de indeling.</strong> De tool vindt het aantal kolommen, de paginavolgorde en de kniplijnen, en controleert of de patroonlijnen van pagina naar pagina doorlopen. Vergelijk de preview met het plakplan. Heeft het plakplan lege vakken, klik dan op de pagina na een leeg vak om het toe te voegen.',
      '<strong>Kies het papier.</strong> A0-vellen (841 × 1189 mm) voor de meeste copyshops, één vel op exacte maat, of een rol van 914 mm (36″) voor plotters.',
      '<strong>Download en print.</strong> Het bestand opent in elke PDF-lezer. Print op 100% (ware grootte) en meet de controleliniaal voor je knipt.'],
 h_print='Zo print je een naaipatroon in de copyshop',
 print='Copyshops printen grote plannen op grootformaat-plotters. Stuur ze de A0-PDF per e-mail of op een USB-stick, en vraag om een zwart-witprint op 100% of “ware grootte” op gewoon papier. Is het patroon groter dan één A0-vel, dan deelt de tool het langs de paginanaden, en op elk vel staat welk vel rechts en eronder komt.',
 print_list=['Vraag om 100% schaal, nooit “passend maken”.','Meet de liniaal van 10 cm en 4″ op vel 1 voor je knipt.','Het bestand blijft trouw: lagen, kleuren en lijndiktes zijn hetzelfde als in het A4-bestand.'],
 tip='<strong>Tip:</strong> lagen (één per maat) blijven in het A0-bestand. Wil je maar één maat printen, open dan het lagenpaneel in Adobe Acrobat Reader, verberg de andere maten en print of verstuur het bestand.',
 h_size='Heeft het A0-patroon de juiste maat?',
 size='Ja, als het op 100% wordt geprint. De tool verkleint of vergroot niets: hij knipt elke pagina op de kniplijnen en legt de pagina’s rand aan rand, in vectorkwaliteit. Je krijgt hetzelfde patroon als wanneer je de A4-pagina’s knipt en plakt, zonder de kleine gaatjes en overlappingen van het plakken.',
 card_h='Wat als de preview niet klopt?',
 card='Controleer de plakpagina’s (zonder omslag en instructies), het aantal kolommen en de volgorde (rij per rij of kolom per kolom). De kniplijnen worden automatisch gemeten: verander ze alleen als de preview een gat of overlap toont. Vergrendelde PDF’s kunnen niet worden omgezet; vraag de ontwerper dan om het A0- of copyshopbestand.',
 h_faq='Veelgestelde vragen',
 faq=[('Is deze A4 naar A0 converter gratis?','Ja. Hij is gratis, zonder account, en het omzetten gebeurt in je browser, dus je patroon wordt nooit geüpload.'),
      ('Werkt hij met US Letter-patronen?','Ja. Hij werkt met PDF-patronen om te plakken in A4, US Letter en andere formaten, staand of liggend. Het resultaat print je op A0-vellen of op een rol van 914 mm.'),
      ('Hoe groot is een A0-vel?','A0 is 841 × 1189 mm. De meeste copyshops printen ook op rollen van 914 mm (36″) breed.'),
      ('Waarom kan mijn PDF niet worden omgezet?','Sommige ontwerpers vergrendelen hun PDF-bestanden. De tool respecteert die vergrendeling: vraag om de A0- of copyshopversie, die vaak bij het patroon zit.')],
 more=1987,
 closing='Nieuw met PDF-patronen? Lees <a href="/nl/naaihandleidingen/pdf-naaipatroon-printen-en-plakken/">een PDF-naaipatroon printen en plakken</a>.')

out = {L['lang']: page(L) for L in (EN, FR, DE, NL)}
json.dump(out, open('dist/pages.json', 'w', encoding='utf8'), ensure_ascii=False)
for k, v in out.items(): print(k, len(v['content']), v['title'])
