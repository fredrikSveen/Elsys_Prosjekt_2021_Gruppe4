# Oppsett av Git

## Her kommer en liten guide på hvordan dere kan bruke git hvis dere aldri har brukt det før.

Programmer du må laste ned for å enkelt kunne bruke Git:
- [Git](https://git-scm.com/downloads) (Velg Visual Studio Code som standard editor, ellers er det bare å tryke next til du er ferdig.)
- VSCode (Gjør ting veldig mye enklere å bruke VSCode. Arduinokoden trenger ikke være på Github nå.)

Til info: 
- Når jeg skriver $ på starten av en kodesnutt så er det et standardtegn som Git Bash allerede har lagt inn. Du skal altså bare skrive inn det etter $-tegnet. 
- For å lime tekst inn i terminalen trykker du `ctrl+insert`.


### Step 0 - Github
Hvis du ikke allerede har en bruker på Github, så må du lage dette. Når du har gjort det, så må du sende Fredrik en melding med epostadressen du har satt for Github-kontoen, så han kan gi deg tilgang.  

### Step 1 - Oppsett av Git Bash
Git Bash skal ha blitt lastet ned når du lastet ned Git. Hvis ikke, last ned Git Bash.
Åpne Git Bash (vil se ut som en terminal).

Sett brukernavn for Git (Dette kan fint bare være fornavnet ditt)

    $ git config --global user.name "Mona Lisa"

og sjekk at brukernavnet er definert

    $ git config --global user.name
    > Mona Lisa

Videre må du også sette en email for git-brukeren. (Dette er ikke automatisk den samme som du har satt som brukernavn på Github, men bør settes til det samme.)

    $ git config --global user.email "youremail@mail.com"

og sjekk at den ble satt

    $ git config --global user.email
    > youremail@mail.com


### Step 2 - Generere SSH-nøkkel og legge den til i Github
Skriv inn kodesnutten nedenfor og sett inn din email.

    $ ssh-keygen -t ed25519 -C "your_email@example.com"

Du blir videre bedt om en fil å lagre nøkkelen i, men bare trykk enter.
Du blir også bedt om å sette et passord, men det er lettest å ikke sette noe, så bare trykk enter uten å skrive inn passord.

Nå er du nødt til å legge til denne SSH-nøkkelen i Github profilen din. For å gjøre det kan du følge denne [guiden](https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account). (Start på punkt 1)

For å teste om du har lagt inn SSH-nøkkelen riktig, kan du bruke denne [linken](https://docs.github.com/en/github/authenticating-to-github/testing-your-ssh-connection). (Start på punkt 1)

### Step 3 - Klone Github repoet (koden på Github) til din PC.
Nå skal du hente koden fra Github til din PC, og etablere en kobling mellom din PC og Github så du enkelt kan laste opp filer og hente de siste endringene. 

Du skal nå kunne kjøre følgende kommando i Git Bash

    $ git clone git@github.com:fredrikSveen/Elsys_Prosjekt_2021_Gruppe4.git

Her kan det hende at må du logge inn med brukernavn og passord for Github (Hvis du ikke har fått tilgang av Fredrik enda, så vil ikke dette fungere).

Skriv så

    $ cd Elsys_Prosjekt_2021_Gruppe4

og deretter

    $ code .

for å åpne hele prosjektet i VScode.
Du skal nå kunne redigere koden. Hvordan du laster opp dine endringer og henter de nyeste endringene, vil det komme en guide på snart.