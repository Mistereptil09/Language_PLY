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
2. **Affectation** : `x = 5♪`
3. **Affichage d'expressions** : `sing(x + y)♪`
4. **Structures conditionnelles** :
   - If-then-else : `soundcheck x < 5 ? ... ! but_actually ? ... !♪`
   - If-then : `soundcheck x < 5 ? ... !♪`
5. **Boucles** :
   - While : `leek_spining x < 10 ? ... !♪`
   - For : `tracklist init | condition | increment ? ... !♪`
6. **Affichage de l'AST** : Automatique à chaque parsing

### Améliorations majeures
1. **Fonctions avec paramètres et return**
   - Définition : `compose nom(param1 | param2) ? ... !♪`
   - Appel : `resultat = fonction(arg1 | arg2)♪`
   - Return : `arigato expression♪`

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
4. **Print multiple** : `sing(a | b | c)♪`
5. **Opérateurs composés** : `x++`, `x+=`, `x-=`, `x*=`
6. **Commentaires** : `# commentaire`

### Fonctionnalités bonus
- Break : `black_out♪`
- Continue : `encore♪`
- Opérateurs de comparaison : `==`, `!=`, `>=`, `<=`, `<`, `>`
- Opérateurs logiques : `@@` (AND), `!@` (OR)

### fichier de tests :
`test_cases.py` : Contient des exemples de codes pour tester les différentes fonctionnalités du langage. Chaque programme est accompagné d'un commentaire expliquant ce qu'il fait et les résultats attendus.

## Syntaxe Complète du Langage

### Mots-clés réservés
| Mot-clé | Utilisation |
|---------|------------|
| `sing` | Affiche une ou plusieurs expressions : `sing(expr1 | expr2)♪` |
| `soundcheck` | Condition if : `soundcheck condition ? bloc !♪` |
| `leek_spining` | Boucle while : `leek_spining condition ? bloc !♪` |
| `but_actually` | Clause else : `soundcheck cond ? bloc1 ! but_actually ? bloc2 !♪` |
| `tracklist` | Boucle for : `tracklist init \| condition \| increment ? bloc !♪` |
| `compose` | Définition de fonction : `compose nom(params) ? bloc !♪` |
| `black_out` | Break - Sortir d'une boucle : `black_out♪` |
| `encore` | Continue - Aller à l'itération suivante : `encore♪` |
| `arigato` | Return - Retourner une valeur : `arigato expression♪` |

### Symboles spéciaux
| Symbole | Utilisation |
|---------|------------|
| `♪` | Terminateur de statement/instruction |
| `?` | Début de bloc (if/while/for/fonction) |
| `!` | Fin de bloc (if/while/for/fonction) |
| `\|` | Séparateur d'arguments/paramètres |
| `(` `)` | Parenthèses pour grouper expressions et appels |

### Opérateurs
| Opérateur | Description |
|-----------|------------|
| `+` `-` `*` `/` | Arithmétique |
| `=` | Assignation |
| `++` | Incrémentation : `x++♪` |
| `+=` | Addition assignée : `x+=5♪` |
| `-=` | Soustraction assignée : `x-=3♪` |
| `*=` | Multiplication assignée : `x*=2♪` |
| `==` | Égalité |
| `!=` | Inégalité |
| `<` `>` | Comparaison |
| `<=` `>=` | Comparaison |
| `@@` | AND logique |
| `!@` | OR logique |

### Types de données supportés
- **Entiers et floats** : `42`, `3.14`
- **Strings** : `"hello"` ou `'hello'`
- **Booléens** : Résultats des comparaisons (`True`, `False`)

## Exemples d'utilisation

### Variables et affectation
```
x=5♪
y=10♪
sing(x+y)♪
```

### Structures de contrôle
```
# If-else
soundcheck x<5 ? sing("petit")♪ ! but_actually ? sing("grand")♪ !♪

# While
leek_spining x<3 ? sing(x)♪ x++♪ !♪

# For
tracklist i=0 | i<5 | i++ ? sing(i)♪ !♪
```

### Fonctions
```
compose add(a | b) ?
    arigato a + b♪
!♪
result = add(3 | 5)♪
sing(result)♪
```

### Récursion
```
compose factorial(n) ?
    soundcheck n == 0 ?
        arigato 1♪
    !♪
    arigato n * factorial(n - 1)♪
!♪
sing(factorial(5))♪
```
