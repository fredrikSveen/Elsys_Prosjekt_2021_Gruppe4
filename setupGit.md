# Oppsett av Git

## Her kommer en liten guide på hvordan dere kan bruke git hvis dere aldri har brukt det før.

Programmer du må laste ned for å enkelt kunne bruke Git:
    - [Git](https://git-scm.com/downloads)
    - VSCode

### Step 0 - Github
Hvis du ikke allerede har en bruker på Github, så må du laste ned denne. Når du har gjort det, så må du sende Fredrik en melding med epostadressen du har satt for Github-kontoen, så han kan gi deg tilgang.  

### Step 1 - Oppsett av Git Bash
Git Bash skal ha blitt lastet ned når du lastet ned Git. Hvis ikke, last ned Git Bash.
Åpne Git Bash (vil se ut som en terminal).

Sett brukernavn for Git

`$ git config --global user.name "Mona Lisa"`

og sjekk at brukernavnet er definert

    $ git config --global user.name
    > Mona Lisa

Videre må du også sette en email for git-brukeren. (Dette er ikke den samme som du har satt som brukernavn på Github, men kan gjerne settes til det samme.)

    $ git config --global user.email "youremail@mail.com"

og sjekk at den ble satt

    $ git config --global user.email
    > youremail@mail.com


### Step 2 - Generere SSH-nøkkel og legge den til i Github
Skriv inn kodesnutten nedenfor og sett inn din email.

    $ ssh-keygen -t ed25519 -C "your_email@example.com"

Du blir videre bedt om en fil å lagre nøkkelen i, men bare trykk enter.
Du blir også bedt om å sette et passord, men det er lettest å ikke sette noe, så bare trykk enter uten å skrive inn passord.

Nå er du nødt til å legge til denne SSH-nøkkelen i Github profilen din. For å gjøre det kan du følge denne [guiden]($ ssh-keygen -t ed25519 -C "your_email@example.com").