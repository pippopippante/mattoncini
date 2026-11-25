<!-- Codice di Emanuele Parmegiani -->
# Mattoncini

Gioco 2D nel browser: fai comparire dei mattoncini, li agganci tra loro, li stacchi e costruisci. C'è la fisica: le costruzioni sbilanciate cadono e gli sbalzi troppo lunghi si rompono.

## Come si gioca
- **Colore e misura** nella barra in basso: ogni misura fa cadere un mattoncino.
- **Trascina** un pezzo per spostarlo. Vicino a un altro compare la sagoma, lo lasci e si aggancia.
- **Tieni premuto** (o tocca) un mattoncino per staccarlo da quello sotto. Viene via con tutto quello che ha sopra.
- **Cestino**: spunta la casella per farlo comparire, poi regola la grandezza. Quello che entra dalla bocca sparisce, anche lanciato come a basket.

## Come si apre
Con un piccolo server locale (è così che è stato provato):

```
python -m http.server 8791
```

poi apri http://localhost:8791. Serve internet: la libreria della fisica si carica da cdnjs.

## File
- `index.html`: tutto il gioco (usa [Matter.js](https://brm.io/matter-js/) per la fisica)
- `cestino.png`: il cestino, ricavato da `images.jpg` con `strumenti/prepara_cestino.py`
- `images.jpg`: immagine di partenza del cestino, scaricata da internet. **Licenza da verificare** prima di pubblicare il gioco.
