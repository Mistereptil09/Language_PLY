from eval_class import EvalClass
from language_ply import * # Importe tout le lexer et le parser
import ply.yacc as yacc

yacc.yacc()

# ==================== TESTS ORGANISÉS ====================

# ==================== TESTS ORGANISÉS ====================

# 1. Tests de base - Expressions et opérateurs
basic_tests = [
    # Arithmétique simple
    ("Addition simple", "sing(1+1)♪", "Miku said: 2"),
    ("Priorité opérateurs", "sing(2*3+4)♪", "Miku said: 10"),
    ("Parenthèses", "sing((2+3)*4)♪", "Miku said: 20"),
    ("Division/soustraction", "sing(10/2-3)♪", "Miku said: 2.0"),

    # Opérateurs logiques
    ("AND/OR", "sing(1@@0!@1)♪", "Miku said: 1"),

    # Comparaisons
    ("Comparaison <", "x=5♪ sing(x<10)♪", "Miku said: True"),  # ← Sans 'this'
    ("Égalité ==", "x=5♪ sing(x==5)♪", "Miku said: True"),
    ("Différent !=", "x=5♪ sing(x!=10)♪", "Miku said: True"),
    ("Plus grand >=", "sing(7>=7 | 7>=8 | 7>=6)♪", "Miku said: True False True"),
    ("Plus petit <=", "sing(7<=7 | 7<=8 | 7<=6)♪", "Miku said: True True False"),
]

# 2. Tests variables et assignation
variable_tests = [
    # Déclaration et usage
    ("Variables multiples", "x=5♪ y=10♪ sing(x+y)♪", "Miku said: 15"),
    ("Réassignation", "x=5♪ x=10♪ sing(x)♪", "Miku said: 10"),

    # Opérateurs composés
    ("Incrémentation ++", "x=10♪ x++♪ sing(x)♪", "Miku said: 11"),
    ("Addition +=", "x=10♪ x+=5♪ sing(x)♪", "Miku said: 15"),
    ("Soustraction -=", "x=10♪ x-=3♪ sing(x)♪", "Miku said: 7"),
    ("Multiplication *=", "x=10♪ x*=2♪ sing(x)♪", "Miku said: 20"),
]

# 3. Tests print et strings
print_tests = [
    ("Print nombre", "sing(42)♪", "Miku said: 42"),
    ("Print string", "sing('Hello')♪", "Miku said: Hello"),
    ("Print multiple", 'sing("a" | "b" | "c")♪', "Miku said: a b c"),
    ("Print expression", "x=5♪ y=3♪ sing(x+y)♪", "Miku said: 8"),
]

# 4. Tests structures de contrôle
control_tests = [
    # If-else
    ("If simple vrai",
     'x=3♪ soundcheck x<5 ? sing("OK")♪ !♪',
     "Miku said: OK"),

    ("If simple faux",
     'x=7♪ soundcheck x<5 ? sing("OK")♪ !♪',
     ""),

    ("If-else vrai",
     'x=3♪ soundcheck x<5 ? sing("petit")♪ ! but_actually ? sing("grand")♪ !♪',
     "Miku said: petit"),

    ("If-else faux",
     'x=7♪ soundcheck x<5 ? sing("petit")♪ ! but_actually ? sing("grand")♪ !♪',
     "Miku said: grand"),

    # While
    ("While simple",
     '''x=0♪ 
        leek_spining x<3 ? 
            sing(x)♪ 
            x++♪ 
        !♪''',
     "Miku said: 0\nMiku said: 1\nMiku said: 2"),

    # For
    ("For loop",
     'i=0♪ tracklist i=0 | i<5 | i++ ? sing(i)♪ !♪',
     "Miku said: 0\nMiku said: 1\nMiku said: 2\nMiku said: 3\nMiku said: 4"),
]

# 5. Tests break et continue
loop_control_tests = [
    ("Break",
     '''x=0♪
        leek_spining x<10 ?
            soundcheck x==5 ?
                black_out♪
            !♪
            sing(x)♪
            x++♪
        !♪''',
     "Miku said: 0\nMiku said: 1\nMiku said: 2\nMiku said: 3\nMiku said: 4"),

    ("Continue",
     '''x=0♪
        leek_spining x<5 ?
            x++♪
            soundcheck x==3 ?
                encore♪
            !♪
            sing(x)♪
        !♪''',
     "Miku said: 1\nMiku said: 2\nMiku said: 4\nMiku said: 5"),
]

# 6. Tests fonctions
function_tests = [
    # Fonction simple
    ("Fonction sans params",
     '''compose greet() ?
            sing("Hello!")♪
        !♪
        greet()♪''',
     "Miku said: Hello!"),

    # Fonction avec paramètres
    ("Fonction avec params",
     '''compose add(a | b) ?
            arigato a + b♪
        !♪
        result = add(3 | 5)♪
        sing(result)♪''',
     "Miku said: 8"),

    # Récursion
    ("Factorielle récursive",
     '''compose factorial(n) ?
            soundcheck n == 0 ?
                arigato 1♪
            !♪
            arigato n * factorial(n - 1)♪
        !♪
        sing(factorial(5))♪''',
     "Miku said: 120"),

    # Fonction avec plusieurs paramètres
    ("Fonction 4 paramètres",
     '''compose show(a | b | c | d) ?
            sing(a | b | c | d)♪
        !♪
        show(1 | 2 | 3 | 4)♪''',
     "Miku said: 1 2 3 4"),
]

# 7. Tests scope (portée des variables)
scope_tests = [
    ("Globale accessible",
     '''x=100♪
        compose test() ?
            sing(x)♪
        !♪
        test()♪''',
     "Miku said: 100"),

    ("Locale isolée",
     '''compose test() ?
            y=50♪
            sing(y)♪
        !♪
        test()♪''',
     "Miku said: 50"),

    ("Locale vs globale",
     '''x=100♪
        compose test() ?
            x=200♪
            sing(x)♪
        !♪
        test()♪
        sing(x)♪''',
     "Miku said: 200\nMiku said: 100"),

    ("Scope lexical",
     '''x=100♪
        compose inner() ?
            sing(x)♪
        !♪
        compose main() ?
            y=50♪
            inner()♪
        !♪
        main()♪''',
     "Miku said: 100"),
]

# 8. Tests commentaires
comment_tests = [
    ("Commentaire simple",
     '''# Ceci est un commentaire
        sing("OK")♪''',
     "Miku said: OK"),

    ("Commentaires multiples",
     '''# Ligne 1
        # Ligne 2
        x=5♪ # Inline
        sing(x)♪''',
     "Miku said: 5"),
]

# ==================== EXÉCUTION DES TESTS ====================

def run_test_suite(suite_name, tests):
    """Exécute une suite de tests"""
    print(f"\n{'=' * 60}")
    print(f" {suite_name}")
    print('=' * 60)

    passed = 0
    failed = 0

    for name, code, expected in tests:
        print(f"\n{name}")

        # todo comment to hide the code being tested
        print(f"Code: {code[:50]}..." if len(code) > 50 else f"Code: {code}")

        evaluator = EvalClass()
        try:
            ast = yacc.parse(code)
            # Capture la sortie
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            evaluator.evalInst(ast)

            # todo uncomment to show the AST of the code being tested
            # print("AST:", ast)
            # printTreeGraph(ast)

            # Récupère la sortie
            output = buffer.getvalue().strip()
            sys.stdout = old_stdout

            # Compare avec attendu (si fourni)
            if expected:
                if output == expected or expected == "":
                    print(f"✅ Résultat: {output if output else '(aucune sortie)'}")
                    passed += 1
                else:
                    print(f"❌ Attendu: {expected}")
                    print(f"❌ Obtenu: {output}")
                    failed += 1
            else:
                print(f"✅ Exécuté: {output}")
                passed += 1

        except Exception as e:
            # Si une erreur est attendue
            if "Error:" in expected:
                print(f"✅ Erreur attendue: {e}")
                passed += 1
            else:
                print(f"❌ Erreur: {e}")
                failed += 1

    print(f"\n{'=' * 60}")
    print(f"Résultats: {passed} réussis, {failed} échoués")
    print('=' * 60)

    return passed, failed


# Exécution de toutes les suites
if __name__ == "__main__":
    total_passed = 0
    total_failed = 0

    suites = [
        ("TESTS DE BASE", basic_tests),
        ("VARIABLES & ASSIGNATION", variable_tests),
        ("PRINT & STRINGS", print_tests),
        ("STRUCTURES DE CONTRÔLE", control_tests),
        ("BREAK & CONTINUE", loop_control_tests),
        ("FONCTIONS", function_tests),
        ("SCOPE (PORTÉE)", scope_tests),
        ("COMMENTAIRES", comment_tests),
    ]

    for name, tests in suites:
        p, f = run_test_suite(name, tests)
        total_passed += p
        total_failed += f

    # Résumé final
    print(f"\n\n{'🎉' * 20}")
    print(f"RÉSULTATS FINAUX")
    print(f"{'🎉' * 20}")
    print(f"✅ Tests réussis: {total_passed}")
    print(f"❌ Tests échoués: {total_failed}")
    print(f"📊 Taux de réussite: {total_passed / (total_passed + total_failed) * 100:.1f}%")

    #
    # # Mode interactif
    # print("\n" + "=" * 60)
    # print("MODE INTERACTIF")
    # print("=" * 60)
    # while True:
    #     try:
    #         s = input('\ncalc > ')
    #         if not s:
    #             continue
    #         evaluator = EvalClass()
    #         ast = yacc.parse(s)
    #         evaluator.evalInst(ast)
    #     except EOFError:
    #         break
    #     except Exception as e:
    #         print(f"Erreur: {e}")
