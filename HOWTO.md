#Hur man gör
Här följer en handledning i hur man går tillväga för att köra koden från sin egen dator. Det förutsätter förstås att du kan installera saker på din dator. Har du en nedlåst dator är det ett missförhållande du behöver åtgärda först.

## 1. Säkerställ att du har Python på datorn
Det här projektet förutsätter att datorn har Python version 3.5 eller nyare. Snabbaste knepet för att kolla om du redan har Python installerat är att på Windows starta programmet CMD, eller Linux/Mac starta terminalen, skriva *python* och klicka på Enter. Då kommer du få reda på om du har Python eller inte. Har du Python behöver du säkerställa att det är minst version 3.5.

Saknar du Python eller har 2.x behöver du ladda ner och installera den senaste varianten från [Python.org](https://www.python.org/downloads/)

## 2. Ladda ner den senaste Verifierad-koden
Har du ingen GIT-klient rekommenderas [Github Desktop](https://desktop.github.com/), den finns till Windows och Mac. När den är nedladdad och installerad går du till [detta projekts rot](https://github.com/Vastra-Gotalandsregionen/verifierad.nu), letar rätt på knappen "Clone or download" och klickar på den.

En dialogruta kommer fråga dig var du vill spara ner allt. Välj något logiskt ställe. Nu har du all kod och dokumentation där du valde att lägga det på din egen dator.

## 3. Samla in adresser du vill analysera
Det finns två huvudsakliga metoder för att samla in många adresser. Enklast är om webbplatsen ifråga har en sitemap, i annat fall kan man använda tillägg för webbläsaren.

### Hämta adresser via en sitemap
Om du inte redan känner till adressen till webbplatsens sitemap kan du kolla om webbplatsen har en robots.txt i webbplatsens rot. Exempelvis om du skriver in "webbplatsensdomän.se/robots.txt" i adressfältet i webbläsaren.

I en robots.txt kan innehållet se ut ungefär så här:  
> User-agent: *  
> Disallow: /wp-admin/  
> Sitemap: http://webbplatsensdomän.se/sitemap.xml

Det är det som anges som adress efter "Sitemap: " du är ute efter. Mata in den i adressfältet i webbläsaren och kolla på vad som dyker upp. I värsta fall är det ett siteindex, det vill säga en lista med flera sitemaps. Det framgår av innehållet. Om det är vanliga webbplatsadresser som listas är det en normal sitemap och du kan hoppa till nedan rubrik att extrahera adresserna.

Har du fått en lista över flera sitemaps är det respektive adress som listas som är en unik sitemap. Ofta framgår det av namnet på respektive sitemap vad det är för innehåll den har. Exempelvis kan det vara en sitemap för bloggposter, en annan för artiklar, en tredje för FAQ. Klistra in adressen till respektive sitemap enligt nedan tips.

#### Extrahera adresser ur en sitemap
För att enkelt få ut adresserna ur en sitemap kan man använda Rob Hammonds webbtjänst [XML Sitemap Extractor](https://robhammond.co/tools/xml-extract). Klistra in adressen till sitemapen i fältet och klicka på knappen "Run report". Det som möter dig då är en tabell med adresser till sidor som finns i sitemapen.

Markera hela tabellens innehåll och öppna ditt kalkylprogram. I kalkylprogrammet markerar du de två första kolumnerna och klistrar in resultatet från tabellen.

För att sedan få ut endast kolumnen med adresserna markerar du den andra kolumnen (de med adresserna i), kopierar hela kolumnen och startar en textredigerare. Klistra in adresserna i textfilen, spara textfilen i samma mapp där du har Python-skripten.

### Hämta adresser via webbläsartillägg
Om du inte lyckas fånga adresser med sitemap kan du istället samla in länkar direkt via webbläsaren. Nedan tipsas om tillägg.  
Tillvägagångssättet är att du söker upp den sidan på webbplatsen som har fler länkar du är intresserad av. Ofta är webbplatsens webbplatskarta bäst, men finns ingen sådan kanske det är startsidan eller en landningssida som ger flest länkar att samla in.

Du som kör med webbläsaren Chrome kan använda tillägget [Link Klipper](https://chrome.google.com/webstore/detail/link-klipper-extract-all/fahollcgofmpnehocdgofnhkkchiekoo) för att fånga in adresser. Kör du Firefox funkar [Link Gopher](https://addons.mozilla.org/en-US/firefox/addon/link-gopher/?src=search) bra. Link Gopher är att föredra då den ger dig enbart adresserna, Link Klipper ger dig även länktexten vilket i detta fallet mest är i vägen och måste städas bort.

## 4. Hämta API-nyckel hos Googles API Console
Skapa ett projekt hos [Googles API Console (IAM & Admin)](https://console.developers.google.com/dcredirect/). I biblioteket med APIer som Google erbjuder väljer du "PageSpeed Insights API". Leta upp projektets "Credentials", det du är ute efter är en lång sträng med text och siffror. Liknande nedan:

> AIzaSyAgBT5Bq29DmCan0OsEWR0eecHz4BGZ69E

Kom ihåg att välja hur du vill begränsa användningen av projektets nyckel. Är du bekymmerslös väljer du "None" och låter bli att sprida din kod.

Denna kod ska du klistra in i nedan moment.

## 5. Redigera dina skript
Förslag på redigeringsprogram är [Sublime Text](https://www.sublimetext.com/3) (Windows, Mac), [Atom](https://atom.io/) (Mac, Linux, Windows) eller [Notepad++](https://notepad-plus-plus.org/) (Windows).

### Redigera filen *_privatekeys.py*
Om du ska anropa något av Googles APIer (behövs inte för HTTP-testet) behöver du göra en liten justering.  
I variablen *googlePageSpeedApiKey* eller *googleMobileFriendlyApiKey* (mellan citationstecknen) anger du den kod du fått via Google API Console.

### Redigera filen *default.py*
I slutet på filen hittar du en rad likt nedan:  
> oneOffProcess('ÄNDRA-MIG.txt')

La du din fil med adresser i samma mapp som Pythonfilen ändrar du *ÄNDRA-MIG.txt* till filens namn.

## 6. Köra Python-skriptet
Kör du Windows och inte är van vid kommandoprompten kan du behöva läsa på lite. Här finns en [nybörjarguide till Windows kommandoprompt](http://www.online-tech-tips.com/computer-tips/how-to-use-dos-command-prompt/). Det du behöver kunna för detta är primärt att navigera mellan olika mappar på din dator.

1. Öppna kommandoprompten (terminalen på Mac/Linux).
2. Navigera dig fram till mappen där du la Python-filerna från Github.
3. Kör kommandot "python default.py" fast utan citationstecken och tryck på Enter-tangenten.

Det som ska hända nu är att det rasslar förbi en massa logginformation där skriptet försöker berätta för dig vad som händer, om skriptet tycker att den lyckas med sina förehavanden eller inte. Förhoppningsvis kommer du hitta en ny fil i mappen du la Python-filerna, det är en så kallad CSV-fil. Det innebär att den innehåller en massa strukturerad information som du kan öppna i ett kalkylprogram eller om du har analysprogram.

Saknar du program för att öppna CSV-filer (kommaseparerade filer) kan du gratis ladda ner [LibreOffice](https://sv.libreoffice.org/ladda-ner-libreoffice/) där det finns ett kalkylprogram, öppna det som en vanlig textfil eller om du vill visualisera det kan du köra testversioner av [Qlik](http://www.qlik.com/) eller [Tableau Public](https://public.tableau.com).

## Felsökning
*Återkommer. Tills vidare, googla felmeddelanden och läs noga när du får träffar på Stackoverflow (det är så utvecklare överlever :)*

## Vanliga frågor
*Bidra gärna genom att rikta frågor till [Marcus Österberg via Twitter](https://twitter.com/marcusosterberg)*