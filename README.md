# Mini-Langage - Projet Théorie des Langages

**Auteurs** : CIORBA Antonio, GERAULT Nathan
**Date** : Février 2026  
**Cours** : Théorie des Langages & Outils pour la Compilation

## Description
Ce projet implémente un mini-langage de programmation complet avec :
- Analyse lexicale et syntaxique (PLY)
- Évaluation d'AST (et affichage)
- Séparation de l'analyse et de l'exécution
- Scope lexical pour les variables (global/local)
- Structures de contrôle (if/while/for/break/continue)
- support de fonctions avec paramètres et return (récursion incluse)
- gestion d'erreurs simple et messages explicites
- types de données : int, string
- opérateurs arithmétiques, de comparaison et logiques

## Fonctionnalités implémentées

### Version minimale
1. **Variables multi-caractères** : `factorial`, `result`, etc.
2. **Affectation** : `x = 5²`
3. **Affichage d'expressions** : `print(x + y)²`
4. **Structures conditionnelles** :
   - If-then-else : `onlydoso x < 5 ? ... ! notlongas ? ... !²`
   - If-then : `onlydoso x < 5 ? ... !²`
5. **Boucles** :
   - While : `aslongas x < 10 ? ... !²`
   - For : `untilreaches init | condition | increment ? ... !²`
6. **Affichage de l'AST** : Automatique à chaque parsing

### Améliorations majeures
1. **Fonctions avec paramètres et return**
   - Définition : `basically nom(param1 | param2) ? ... !²`
   - Appel : `resultat = fonction(arg1 | arg2)²`
   - Return : `comeback expression²`

2. **Scope lexical**
   - Variables globales accessibles dans les fonctions
   - Variables locales isolées par fonction
   - Pas de pollution du scope global

3. **Récursion terminale**
   - Support complet de la récursion
   - Exemple : factorielle récursive
   - Limite de profondeur gérée par python directement

### Améliorations mineures 
1. **Gestion des erreurs** : Messages explicites
2. **Type string** : `"hello"` ou `'hello'`
3. **Variables globales** : Scope distinct global/local
4. **Print multiple** : `print(a | b | c)²`
5. **Opérateurs composés** : `x++`, `x+=`, `x-=`, `x*=`
6. **Commentaires** : `# commentaire`

### Fonctionnalités bonus
- Break : `stop²`
- Continue : `dontstop²`
- Opérateurs de comparaison : `==`, `!=`, `>=`, `<=`
- Opérateurs logiques : `@@` (AND), `!@` (OR)

### fichier de tests :
`test_cases.py` : Contient des exemples de codes pour tester les différentes fonctionnalités du langage. Chaque programme est accompagné d'un commentaire expliquant ce qu'il fait et les résultats attendus.