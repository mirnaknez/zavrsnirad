Sustav za prepoznavanje opasnih situacija u prometu temeljen na GeoPandas biblioteci

Ovaj repozitorij sadrži sustav za prepoznavanje opasnih situacija u prometu razvijen uz pomoć GeoPandas biblioteke. Cilj ovog projekta je analizirati i prepoznati opasne prometne situacije, korištenjem geoprostornih operatora unutar GeoPandas-a.

Ključne značajke:

Učitavanje i obrada geoprostornih podataka s OpenStreetMap (OSM) karti za izradu logičkog modela prometne mreže.
Obrada GPS podataka: tragovi kretanja vozila predstavljeni su nizom zemljopisnih koordinata prikupljenih iz GPS prijemnika, u ovom slučaju nacrtani u QGIS alatu za potrebe testiranja sustava.
Implementacija geoprostornih operatora za prepoznavanje opasnih situacija u prometu i upozoravanje vozača u stvarnom vremenu.
Izlazni podaci uključuju vrstu prepoznate opasne situacije i popis vozila koja su u dometu i kojima je potrebno poslati upozorenje.
Provodeno ispitivanje točnosti i performansi sustava na različitim prometnim konfiguracijama, uključujući guste gradske mreže, prorijeđene ruralne mreže i raskršća.

Arhitektura sustava:

Projekt koristi GeoPandas za izvođenje prostornih analiza na prometnim mrežama i tragovima vozila.
Radni tok uključuje učitavanje podataka s OpenStreetMap-a, njihovu pretvorbu u odgovarajući format za analizu, te primjenu geoprostornih operatora kao što su provjere blizine i presjeka za identifikaciju opasnih situacija.
Provodeno ispitivanje brzine i točnosti sustava na različitim prometnim mrežama kako bi se osigurala pouzdanost i učinkovitost.

Moguće primjene:

Praćenje prometa u stvarnom vremenu i upozoravanje vozača na opasne situacije.
Prevencija prometnih nesreća prepoznavanjem rizičnih ponašanja u vožnji.
Primjena u sustavima za upravljanje prometom u pametnim gradovima i autonomnim vozilima.
