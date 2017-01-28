#Hur man gör
Här följer en handledning i hur man går tillväga för att köra koden från sin egen dator. Det förutsätter förstås att du kan installera saker på din dator, kan du inte det är det där du börjar.

## 1. Säkerställ att du har Python på datorn
*Återkommer med guide.*

## 2. Ladda ner den senaste koden
*Återkommer med guide.*

## 3. Samla in adresser du vill analysera
Det finns två huvudsakliga metoder för att samla in många adresser. Enklast är om webbplatsen ifråga har en sitemap, i annat fall kan man använda tillägg för webbläsare.

### Hämta adresser via sitemap
Om du inte redan känner till adressen till webbplatsens sitemap kan du kolla om webbplatsen har en robots.txt i webbplatsens rot. Exempelvis om du skriver in webbplatsensdomän.se/robots.txt i adressfältet i webbläsaren.

I en robots.txt kan innehållet se ut ungefär så här:  
> User-agent: *
> Disallow: /wp-admin/
> Sitemap: http://webbplatsensdomän.se/sitemap.xml

Det är det som anges som adress efter "Sitemap" du är ute efter. Mata in den i adressfältet i webbläsaren och kolla på vad som dyker upp. I värsta fall är det ett siteindex, det vill säga en lista med flera sitemaps. Det framgår av innehållet. Om det är "vanliga" webbplatsadresser är det en vanlig sitemap och du kan hoppa till att extrahera adresserna.

Har du fått en lista över flera sitemaps är det respektive adress som listas som är en unik sitemap. Ofta framgår det av namnet på respektive sitemap vad det är för innehåll den har. Exempelvis kan det vara en sitemap för bloggposter, en annan för artiklar, en tredje för FAQ. Klistra in adressen till respektive sitemap enligt nedan tips.

#### Extrahera adresser ur en sitemap
För att enkelt få ut adresserna ur en sitemap kan man använda Rob Hammonds webbtjänst [XML Sitemap Extractor](https://robhammond.co/tools/xml-extract). Klistra in adressen till sitemapen i fältet och klicka på knappen "Run report". Det som möter dig då är en tabell med adresser till sidor som finns i sitemapen.

Markera hela tabellens innehåll och öppna ditt kalkylprogram. I kalkylprogrammet markerar du de två första kolumnerna och klistrar in resultatet från tabellen.

För att sedan få ut endast kolumnen med adresserna markerar du den andra kolumnen (de med adresserna i), kopierar hela kolumnen och startar en textredigerare. Klistra in adresserna i textfilen, spara textfilen i samma mapp där du har Python-skripten.

### Hämta adresser via webbläsartillägg
Om du inte lyckas fånga adresser med sitemap kan du istället samla in länkar direkt via webbläsaren. Nedan tipsas om tillägg.  
Tillvägagångssättet är att du söker upp den sidan på webbplatsen som har fler länkar du är intresserad av. Ofta är webbplatsens webbplatskarta bäst, men finns ingen sådan kanske det är startsidan eller en landningssida som ger flest länkar att samla in.

Du som kör med webbläsaren Chrome kan använda tillägget [Link Klipper](https://chrome.google.com/webstore/detail/link-klipper-extract-all/fahollcgofmpnehocdgofnhkkchiekoo) för att fånga in adresser. Kör du Firefox funkar [Link Gopher](https://addons.mozilla.org/en-US/firefox/addon/link-gopher/?src=search) bra.

## 4. Köra Python-skriptet
*Återkommer.*