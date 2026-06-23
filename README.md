# WorldCat Holding Quickscan

Een interne tool voor het snel controleren en verrijken van holdings via de WorldCat API.

---

## 🚀 Wat doet deze tool?

Deze applicatie:

- Leest een Excelbestand
- Zoekt bijbehorende OCN's via WorldCat
- Controleert holdings
- Genereert een nieuw Excelbestand met resultaten

---

## 📦 Gebruik

### Stap 1 – Downloaden
Download de volledige `quickscan` map en pak deze uit.

### Stap 2 – Starten
Dubbelklik op:

ui.pyw

Er opent een venster (geen terminal).

---

## 📂 Bestand selecteren

- Sleep een Excelbestand in het venster  
OF  
- Klik op het veld om een bestand te kiezen

---

## ▶️ Scan starten

Klik op:

▶ Start

Tijdens de scan zie je:

- voortgang (%)
- aantal verwerkte rijen
- geschatte resterende tijd

---

## ⛔ Stoppen

Klik op:

⛔ Stop

De scan wordt afgebroken (resultaten worden niet opgeslagen)

---

## 📄 Output

Na afloop:

- Een nieuw Excelbestand wordt aangemaakt in dezelfde map
- Bestandsnaam:  
  origineelbestand-qs.xlsx

---

## 📝 Logbestand

Klik op:

📄 Log

Dit opent log.txt met details van de verwerking (handig bij fouten)

---

## ⚙️ Configuratie

De tool gebruikt een `.env` bestand met API-configuratie.

Dit bestand zit al in de map en hoeft niet aangepast te worden.

---

## 🔐 Belangrijk

- De tool gebruikt een gedeelde WorldCat API key
- Alleen bedoeld voor intern gebruik binnen het team
- Niet extern delen

---

## 🛠️ Problemen / foutmeldingen

- Controleer log.txt voor details
- Zorg dat je de volledige map hebt uitgepakt
- Start altijd via ui.pyw

---

## 💡 Tips

- Gebruik bij voorkeur .xlsx bestanden
- Houd bestanden gesloten tijdens verwerking
- Grote bestanden kunnen langer duren

---

## ✅ Status

Deze tool is ontwikkeld voor intern gebruik en wordt actief gebruikt binnen het team.

---

Veel succes met scannen 🎉