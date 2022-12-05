# FileCryptor

Scrieți un script care primește la intrare un fișier , o comanda și o parola (text) și în funcție de
comanda criptează sau decripteaza fișierul primit. Criptarea se face în felul următor: pentru
fiecare caracter din fișierul de intrare, se afla codul lui ascii și se adaugă valoarea data de
codul ascii al caracterului (cu indexul egal cu offsetul caracterului curent MODULO numărul
de caractere din parola) din parola. Mai exact, dacă parola este “ABCD”, și primim un fișier de
100 de octeți, primul OCTET se înlocuiește cu valoarea lui plus 65 (codul ascii a lui ‘A’), al
doilea cu valoare lui plus 66 (codul ascii a lui ‘B’), al treilea cu valoare lui plus 67 (codul ascii a
lui ‘C’), al patrulea cu valoare lui plus 68 (codul ascii a lui ‘D’), al cincilea cu valoare lui plus 65
(codul ascii a lui ‘A’), al șaselea cu valoare lui plus 66 (codul ascii a lui ‘B’), s.a.m.d
Dacă suma depășește 255 (8 biți) se pastreaza primii 8 biti din suma.
Decriptarea se face identic doar ca în loc de suma se face diferenta.
Asigurati-va ca în fisierul criptat aveți un hash al fișierului inițial ca sa puteți valida că parola
de decriptare este corecta.
