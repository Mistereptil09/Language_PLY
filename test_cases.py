from eval_class import EvalClass
from language_ply import * # Importe tout le lexer et le parser
import ply.yacc as yacc

yacc.yacc()

# ==================== TESTS ORGANISÉS ====================

# ==================== TESTS ORGANISÉS ====================

# 1. Tests de base - Expressions et opérateurs
basic_tests = [
    # Arithmétique simple
    ("Addition simple", "print(1+1)²", "2"),
    ("Priorité opérateurs", "print(2*3+4)²", "10"),
    ("Parenthèses", "print((2+3)*4)²", "20"),
    ("Division/soustraction", "print(10/2-3)²", "2.0"),

    # Opérateurs logiques
    ("AND/OR", "print(1@@0!@1)²", "1"),

    # Comparaisons
    ("Comparaison <", "x=5² print(x<10)²", "True"),  # ← Sans 'this'
    ("Égalité ==", "x=5² print(x==5)²", "True"),
    ("Différent !=", "x=5² print(x!=10)²", "True"),
    ("Plus grand >=", "print(7>=7 | 7>=8 | 7>=6)²", "True False True"),
    ("Plus petit <=", "print(7<=7 | 7<=8 | 7<=6)²", "True True False"),
]

# 2. Tests variables et assignation
variable_tests = [
    # Déclaration et usage
    ("Variables multiples", "x=5² y=10² print(x+y)²", "15"),
    ("Réassignation", "x=5² x=10² print(x)²", "10"),

    # Opérateurs composés
    ("Incrémentation ++", "x=10² x++² print(x)²", "11"),
    ("Addition +=", "x=10² x+=5² print(x)²", "15"),
    ("Soustraction -=", "x=10² x-=3² print(x)²", "7"),
    ("Multiplication *=", "x=10² x*=2² print(x)²", "20"),
]

# 3. Tests print et strings
print_tests = [
    ("Print nombre", "print(42)²", "42"),
    ("Print string", "print('Hello')²", "Hello"),
    ("Print multiple", 'print("a" | "b" | "c")²', "a b c"),
    ("Print expression", "x=5² y=3² print(x+y)²", "8"),
]

# 4. Tests structures de contrôle
control_tests = [
    # If-else
    ("If simple vrai",
     'x=3² onlydoso x<5 ? print("OK")² !²',
     "OK"),

    ("If simple faux",
     'x=7² onlydoso x<5 ? print("OK")² !²',
     ""),

    ("If-else vrai",
     'x=3² onlydoso x<5 ? print("petit")² ! notlongas ? print("grand")² !²',
     "petit"),

    ("If-else faux",
     'x=7² onlydoso x<5 ? print("petit")² ! notlongas ? print("grand")² !²',
     "grand"),

    # While
    ("While simple",
     '''x=0² 
        aslongas x<3 ? 
            print(x)² 
            x++² 
        !²''',
     "0\n1\n2"),

    # For
    ("For loop",
     'i=0² untilreaches i=0 | i<5 | i++ ? print(i)² !²',
     "0\n1\n2\n3\n4"),
]

# 5. Tests break et continue
loop_control_tests = [
    ("Break",
     '''x=0²
        aslongas x<10 ?
            onlydoso x==5 ?
                stop²
            !²
            print(x)²
            x++²
        !²''',
     "0\n1\n2\n3\n4"),

    ("Continue",
     '''x=0²
        aslongas x<5 ?
            x++²
            onlydoso x==3 ?
                dontstop²
            !²
            print(x)²
        !²''',
     "1\n2\n4\n5"),
]

# 6. Tests fonctions
function_tests = [
    # Fonction simple
    ("Fonction sans params",
     '''basically greet() ?
            print("Hello!")²
        !²
        greet()²''',
     "Hello!"),

    # Fonction avec paramètres
    ("Fonction avec params",
     '''basically add(a | b) ?
            comeback a + b²
        !²
        result = add(3 | 5)²
        print(result)²''',
     "8"),

    # Récursion
    ("Factorielle récursive",
     '''basically factorial(n) ?
            onlydoso n == 0 ?
                comeback 1²
            !²
            comeback n * factorial(n - 1)²
        !²
        print(factorial(5))²''',
     "120"),

    # Fonction avec plusieurs paramètres
    ("Fonction 4 paramètres",
     '''basically show(a | b | c | d) ?
            print(a | b | c | d)²
        !²
        show(1 | 2 | 3 | 4)²''',
     "1 2 3 4"),
]

# 7. Tests scope (portée des variables)
scope_tests = [
    ("Globale accessible",
     '''x=100²
        basically test() ?
            print(x)²
        !²
        test()²''',
     "100"),

    ("Locale isolée",
     '''basically test() ?
            y=50²
            print(y)²
        !²
        test()²''',
     "50"),

    ("Locale vs globale",
     '''x=100²
        basically test() ?
            x=200²
            print(x)²
        !²
        test()²
        print(x)²''',
     "200\n100"),

    ("Scope lexical",
     '''x=100²
        basically inner() ?
            print(x)²
        !²
        basically main() ?
            y=50²
            inner()²
        !²
        main()²''',
     "100"),
]

# 8. Tests commentaires
comment_tests = [
    ("Commentaire simple",
     '''# Ceci est un commentaire
        print("OK")²''',
     "OK"),

    ("Commentaires multiples",
     '''# Ligne 1
        # Ligne 2
        x=5² # Inline
        print(x)²''',
     "5"),
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
