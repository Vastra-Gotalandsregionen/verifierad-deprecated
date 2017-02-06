#Changelog

## 0.1 - Google Mobile-friendly test (2017-01-31)
Första kodexempel som skript är Googles test mobile-friendly. Det annonserades nyligen ut på [Google Webmaster Central-bloggen](https://webmasters.googleblog.com/2017/01/introducing-mobile-friendly-test-api.html). Dessvärre verkar inte APIet vara uppe ännu, det svarar bara "HTTPError: HTTP Error 403: Forbidden", men det finns nu kod för stickprov i 'test.py'. När APIet verkar må bättre kommer en mer automatiserad/storskalig version.

För det mer storskaliga finns under mappen 'exempelfiler' textfiler med adresser. Du som vill förbereda dig kan börja samla på dig URLar på detta vis, en webbsidas adress per rad. Dessa kommer sedan att kunna läsas in och köras en och en mot respektive API.

## 0.2 Test av HTTP-status
Nu innehåller default.py ett test som läser in textfil (en webbadress per rad) och kollar vilken HTTP-status adressen returnerar. Går allt som det ska kommer en '200', saknas sidan ska en '404' anges, eller om domänen saknas kommer '520' eller '522' tillbaka. Svaret skrivs till en kommaseparerad CSV-fil, enkel att läsa in i kalkylprogram.

Denna funktion är användbar för att kolla _långa_ listor av domäner, eller granska att alla inarbetade adresser på en webbplats faktiskt funkar.