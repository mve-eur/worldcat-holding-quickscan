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
Zorg dat je ook een `.env` bestand aanmaakt (zie Configuratie).

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

### 🔹 Stap 1 – `.env` aanmaken

In de map staat een bestand:

env_template.txt

Kopieer dit bestand en hernoem het naar:

.env

### 🔹 Stap 2 – gegevens invullen

Open `.env` en vul de benodigde gegevens in:

WSKEY=
WSKEY_SECRET=
INSTITUTION_SYMBOL=

Deze gegevens zijn nodig om verbinding te maken met de WorldCat API.

---

## 🔐 Belangrijk

- De `.env` bevat gevoelige gegevens (API keys)
- Dit bestand wordt **niet gedeeld via GitHub**
- Deel deze gegevens nooit extern

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