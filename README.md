# Automātiskā sludinājumu rasmošanas un cenas salīdzināšanas atskaites izveides programma

## Par projektu
Vairākus gadus, ļoti regulāri veru vaļā sludinājumu mājaslapu un skatos cauri katram sludinājumam, dažreiz esmu aizmirsis aktuālās video karšu cenas un tad tās man ir arī jāiet pašam un jāpārbauda.<br><br>
Tādēļ šāds projekts tika izstrādāts - lai vieglāk un ātrāk būtu iespēja aplūkot un salīdzināt video karšu sludinājumus.

Projekta mērķis ir izveidota programma, kas automātiski ģenerē atskaites ar vajadzīgo sludinājumu saturu un to cenu salīdzinātu ar video kartes tagadējo vidējo cenu datiem.

Atkarībā no cenas izmaiņas starp sludinājuma cenu un tās video kartes vidējo cenu, cenas aile atskaitē priekš attiecīgā sludinājuma tiktu iekrāsota attiecīgā krāsā, no sarkana toņa(vissliktākais piedāvājums) līdz zaļam tonim(vislabākais piedāvājums).

## Izmantotās bibliotēkas

Projekts tika veidots izmantojot Python, kā arī sekojošās bibliotēkas priekš Python:
* Openpyxl - Bibliotēka tika izmantota, lai izveidotu un formatētu excel failu priekš programmas izvades
* Selenium - Bibliotēka tika izmantota priekš izvades un apstrādes datu iegūšanas un tīmekļa automatizācijas, lai varētu navigēt uz citām lapām, tādejādi, simulējot lietotāja darbības
* Iebūvētās bibliotēkas:
  * Time, sleep funkcija - Funkcija, lai aizkavētu programmas darbību, programmā tiek izmantota trīs reizes, lai programma uzgaidītu kamēr mājaslapa ir atvērusies
  * Os, path un mkdir funkcijas - Funkcijas priekš programmas izveidotā faila saglabāšanas sistēmā
  * Io, BytesIO funkcija - Funkcija, lai izveidotu bildes objektu iekšēji atmiņai no Selenium izveidotā ekrānšāviņa bildes baitu datiem

## Priekšnosacījumi

**⚠️⚠️⚠️ Programmas darbības laikā ir iespējams, ka parādīsies spilgta balta mirgošana iekš Selenium izveidotā tīmekļa sludinājumu mājaslapas datu apstrādes laikā.**<br>
**Tādēļ ir ļoti ieteicams programmas darbības laikā Selenium izveidoto tīmekļa lapu minimizēt, ja jums ir jūtīgums pret ātru spilgtu gaismas attēlu izmaiņām. ⚠️⚠️⚠️**

Šī programma ir paredzēta vienīgi informācijas iegūšanai no publiskiem mājaslapu resursiem un neapdraud privātumu vai citus juridiskos normatīvos likumus.<br>

Programmas mērķis ir tikai iegūt pārskatamāku sludinājumu izvadi un salīdzināšanu ar citas mājaslapas resursiem.<br>
Visas programmas darbības tiek veiktas saskaņā ar Latvijas likumdošanas nosacījumiem un ētiskiem standartiem, programma neievāc nekādus sensitīvus datus par personām.

## Programmas instalācija

Programmas darbībai ir nepieciešams būt uzinstalētam Python 3.7 vai jaunākai Python versijai.

1. Noklonējiet repozitoriju:
   - Izmantojot SSH(ieteicams): ```git clone git@github.com:KristiansUtmans/dip225_5.git```
   - Caur HTTPS: ```git clone https://github.com/KristiansUtmans/dip225_5.git```
2. Instalējiet vajadzīgās projekta bibliotēkas: ```pip install -r requirements.txt```<br>
Šis requirements.txt fails tika automātiski ģenerēts izmantojot: [pipreqs](https://github.com/bndr/pipreqs)

## Programmas lietošana

Programmu var palaist izmantojot ```source.py``` failu, caur jebkādu IDE vai termināli ierakstot: ```python source.py```.

Programmas darbības laikā jums atvērsies Selenium izveidotā tīmekļa lapa kurā risināsies programmas darbība, lai iegūtu izvades un apstrādes datus priekš izvades atskaites.<br>
Programmas darbības laikā varat terminālī tiks izvadīta programmas gaita, vidējās cenas tiek meklētas divas reizes: priekš jaunām video kartēm un vecām video kartēm.

Pēc programmas faila saglabāšanas jums terminālī tiks pateikts kur fails tika saglabāts jūsu Projekta direktorijā, tas vienmēr tiks saglabāts iekš "output" mapes.

**Ja programmai ir kādas problēmas, tas varētu būt jūsu interneta savienojuma dēļ, tādēļ ieteicams atrast projektā 3 vietās izsaukto sleep funkciju un palielināt tās vērtību.**

## Programmas koda struktūra

Programmas kodu veidoju izmantojot sev nepieciešamos OOP principus, lai veidotu kodu lasāmāku un atkārtoti lietojamu.

Tādēļ ir vairāki Python faili:
* ```source.py``` - Galvenais programmas fails, šeit tiek atvērtas tīmekļa lapas, veikta izvades formatēšana un izsaukta pārējā funkcionalitāte no pārējo projekta python failu funkcijas
* ```helper.py``` - Fails ar palīgfunkcijām, programmas kods kas ir jāizpilda vairākas reizes citās vietās
* ```averagepricefetcher.py``` - Sastāv no funkcijas, kas iegūst vajadzīgos datus priekš video karšu vidējām cenām, veic nepieciešamo navigāciju, lai iegūtu visus datus.
* ```listingfetcher.py``` - Sastāv no funkcijas, kas iegūst vajadzīgos datus par video karšu sludinājumiem, veic nepieciešamo navigāciju, lai iegūtu visus datus. Šeit ir iespējams arī mainīt sludinājumu filtrāciju: 
  * includedModels - Video karšu modeļi kurus jūs vēlaties atrast;
  * excludedModels - Video karšu modeļi kurus jūs vēlaties izfiltrēt ārā no jūsu izvades;
  * excludedRegions - Reģioni no kuriem jūs nevēlaties redzēt video karšu sludinājumus, jo varbūt tie atrodas pārāk tālu no jums.