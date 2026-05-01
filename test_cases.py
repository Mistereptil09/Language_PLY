from eval_class import EvalClass
from language_ply import *   # lexer + parser rules
import ply.yacc as yacc
import io
import sys
from contextlib import redirect_stdout

parser = yacc.yacc()


# ============================================================
# TEST MODEL
# ============================================================

def ok(name, code, expected_output):
    return {
        "name": name,
        "code": code,
        "kind": "ok",
        "expected_output": expected_output,
    }

def runtime_error(name, code, expected_error_contains):
    return {
        "name": name,
        "code": code,
        "kind": "runtime_error",
        "expected_error_contains": expected_error_contains,
    }

def parse_error(name, code):
    return {
        "name": name,
        "code": code,
        "kind": "parse_error",
    }

def known_edge(name, code, note, expected_output=None, expected_error_contains=None):
    return {
        "name": name,
        "code": code,
        "kind": "known_edge",
        "note": note,
        "expected_output": expected_output,
        "expected_error_contains": expected_error_contains,
    }


# ============================================================
# 1. TESTS DE BASE - EXPRESSIONS ET OPÉRATEURS
# ============================================================

basic_tests = [
    ok("Addition simple", "sing(1+1)♪", "Miku said: 2"),
    ok("Priorité opérateurs", "sing(2*3+4)♪", "Miku said: 10"),
    ok("Parenthèses", "sing((2+3)*4)♪", "Miku said: 20"),
    ok("Division/soustraction", "sing(10/2-3)♪", "Miku said: 2.0"),
    ok("AND/OR", "sing(1@@0!@1)♪", "Miku said: 1"),
    ok("Comparaison <", "x=5♪ sing(x<10)♪", "Miku said: True"),
    ok("Égalité ==", "x=5♪ sing(x==5)♪", "Miku said: True"),
    ok("Différent !=", "x=5♪ sing(x!=10)♪", "Miku said: True"),
    ok("Plus grand >=", "sing(7>=7 | 7>=8 | 7>=6)♪", "Miku said: True False True"),
    ok("Plus petit <=", "sing(7<=7 | 7<=8 | 7<=6)♪", "Miku said: True True False"),
]

variable_tests = [
    ok("Variables multiples", "x=5♪ y=10♪ sing(x+y)♪", "Miku said: 15"),
    ok("Réassignation", "x=5♪ x=10♪ sing(x)♪", "Miku said: 10"),
    ok("Incrémentation ++", "x=10♪ x++♪ sing(x)♪", "Miku said: 11"),
    ok("Addition +=", "x=10♪ x+=5♪ sing(x)♪", "Miku said: 15"),
    ok("Soustraction -=", "x=10♪ x-=3♪ sing(x)♪", "Miku said: 7"),
    ok("Multiplication *=", "x=10♪ x*=2♪ sing(x)♪", "Miku said: 20"),
]

print_tests = [
    ok("Print nombre", "sing(42)♪", "Miku said: 42"),
    ok("Print string simple", "sing('Hello')♪", "Miku said: Hello"),
    ok("Print multiple", 'sing("a" | "b" | "c")♪', "Miku said: a b c"),
    ok("Print expression", "x=5♪ y=3♪ sing(x+y)♪", "Miku said: 8"),
]

control_tests = [
    ok(
        "If simple vrai",
        'x=3♪ soundcheck x<5 ? sing("OK")♪ !♪',
        "Miku said: OK"
    ),
    ok(
        "If simple faux",
        'x=7♪ soundcheck x<5 ? sing("OK")♪ !♪',
        ""
    ),
    ok(
        "If-else vrai",
        'x=3♪ soundcheck x<5 ? sing("petit")♪ ! but_actually ? sing("grand")♪ !♪',
        "Miku said: petit"
    ),
    ok(
        "If-else faux",
        'x=7♪ soundcheck x<5 ? sing("petit")♪ ! but_actually ? sing("grand")♪ !♪',
        "Miku said: grand"
    ),
    ok(
        "While simple",
        '''x=0♪
leek_spining x<3 ?
    sing(x)♪
    x++♪
!♪''',
        "Miku said: 0\nMiku said: 1\nMiku said: 2"
    ),
    ok(
        "For loop",
        'i=0♪ tracklist i=0 | i<5 | i++ ? sing(i)♪ !♪',
        "Miku said: 0\nMiku said: 1\nMiku said: 2\nMiku said: 3\nMiku said: 4"
    ),
]

loop_control_tests = [
    ok(
        "Break",
        '''x=0♪
leek_spining x<10 ?
    soundcheck x==5 ?
        black_out♪
    !♪
    sing(x)♪
    x++♪
!♪''',
        "Miku said: 0\nMiku said: 1\nMiku said: 2\nMiku said: 3\nMiku said: 4"
    ),
    ok(
        "Continue",
        '''x=0♪
leek_spining x<5 ?
    x++♪
    soundcheck x==3 ?
        encore♪
    !♪
    sing(x)♪
!♪''',
        "Miku said: 1\nMiku said: 2\nMiku said: 4\nMiku said: 5"
    ),
]

function_tests = [
    ok(
        "Fonction sans params",
        '''compose greet() ?
    sing("Hello!")♪
!♪
greet()♪''',
        "Miku said: Hello!"
    ),
    ok(
        "Fonction avec params",
        '''compose add(a | b) ?
    arigato a + b♪
!♪
result = add(3 | 5)♪
sing(result)♪''',
        "Miku said: 8"
    ),
    ok(
        "Factorielle récursive",
        '''compose factorial(n) ?
    soundcheck n == 0 ?
        arigato 1♪
    !♪
    arigato n * factorial(n - 1)♪
!♪
sing(factorial(5))♪''',
        "Miku said: 120"
    ),
    ok(
        "Fonction 4 paramètres",
        '''compose show(a | b | c | d) ?
    sing(a | b | c | d)♪
!♪
show(1 | 2 | 3 | 4)♪''',
        "Miku said: 1 2 3 4"
    ),
]

scope_tests = [
    ok(
        "Globale accessible",
        '''x=100♪
compose test() ?
    sing(x)♪
!♪
test()♪''',
        "Miku said: 100"
    ),
    ok(
        "Locale isolée",
        '''compose test() ?
    y=50♪
    sing(y)♪
!♪
test()♪''',
        "Miku said: 50"
    ),
    ok(
        "Locale vs globale",
        '''x=100♪
compose test() ?
    x=200♪
    sing(x)♪
!♪
test()♪
sing(x)♪''',
        "Miku said: 200\nMiku said: 100"
    ),
    ok(
        "Scope lexical",
        '''x=100♪
compose inner() ?
    sing(x)♪
!♪
compose main() ?
    y=50♪
    inner()♪
!♪
main()♪''',
        "Miku said: 100"
    ),
]

comment_tests = [
    ok(
        "Commentaire simple",
        '''# Ceci est un commentaire
sing("OK")♪''',
        "Miku said: OK"
    ),
    ok(
        "Commentaires multiples",
        '''# Ligne 1
# Ligne 2
x=5♪ # Inline
sing(x)♪''',
        "Miku said: 5"
    ),
]


# ============================================================
# 2. TESTS D’ERREURS ATTENDUES
# ============================================================

runtime_error_tests = [
    runtime_error(
        "Variable non définie",
        "sing(x)♪",
        "Variable 'x' not defined"
    ),
    runtime_error(
        "Fonction non définie",
        "foo()♪",
        "Function 'foo' not defined"
    ),
    runtime_error(
        "Mauvais nombre d'arguments",
        '''compose add(a | b) ?
    arigato a + b♪
!♪
sing(add(1))♪''',
        "expects 2 arguments"
    ),
    runtime_error(
        "Redéfinition fonction",
        '''compose test() ?
    sing(1)♪
!♪
compose test() ?
    sing(2)♪
!♪''',
        "Function 'test' already defined"
    ),
    runtime_error(
        "Division par zéro",
        "sing(10/0)♪",
        "division by zero"
    ),
]

parse_error_tests = [
    parse_error("Parenthèse manquante", "sing((1+2)♪"),
    parse_error("Bloc if non fermé", 'soundcheck 1 ? sing("x")♪'),
    parse_error("For incomplet", 'tracklist i=0 | i<5 ? sing(i)♪ !♪'),
    parse_error("Affectation incomplète", "x=♪"),
]


# ============================================================
# 3. EDGE CASES / LIMITATIONS CONNUES
# ============================================================

edge_case_tests = [
    known_edge(
        "Break hors boucle",
        "black_out♪",
        note="Selon l'implémentation actuelle, break hors boucle peut lever une erreur ou se comporter bizarrement. Ce test documente le comportement.",
        expected_error_contains=None
    ),
    known_edge(
        "Continue hors boucle",
        "encore♪",
        note="Selon l'implémentation actuelle, continue hors boucle peut lever une erreur ou se comporter bizarrement. Ce test documente le comportement.",
        expected_error_contains=None
    ),
    known_edge(
        "Return hors fonction",
        "arigato 42♪",
        note="Dans certaines implémentations, return hors fonction n'est pas bloqué proprement.",
        expected_error_contains=None
    ),
    known_edge(
        "Récursion profonde",
        '''compose countdown(n) ?
    soundcheck n == 0 ?
        arigato 0♪
    !♪
    arigato countdown(n-1)♪
!♪
sing(countdown(300))♪''',
        note="Peut échouer selon la profondeur de récursion et l'implémentation actuelle de evalInst/evalExpr."
    ),
    known_edge(
        "Short-circuit logique avec division dangereuse",
        'sing(0@@(10/0))♪',
        note="Devrait idéalement court-circuiter sans division par zéro si l'évaluation logique est correcte.",
        expected_output="Miku said: 0"
    ),
    known_edge(
        "Or logique avec division dangereuse",
        'sing(1!@(10/0))♪',
        note="Devrait idéalement court-circuiter sans division par zéro si l'évaluation logique est correcte.",
        expected_output="Miku said: 1"
    ),
    known_edge(
        "String vide",
        'sing("")♪',
        note="Permet de documenter la gestion d'une chaîne vide.",
        expected_output="Miku said: "
    ),
    known_edge(
        "Commentaires inline multiples",
        '''x=1♪ # commentaire 1
y=2♪ # commentaire 2
sing(x+y)♪''',
        note="Documente si les commentaires inline sont correctement ignorés partout.",
        expected_output="Miku said: 3"
    ),
    known_edge(
        "Else sans if",
        'but_actually ? sing("oops")♪ !♪',
        note="Doit normalement être rejeté par le parseur.",
        expected_error_contains=None
    ),
    known_edge(
        "Variable locale inaccessible hors fonction",
        '''compose build() ?
    y=99♪
    sing(y)♪
!♪
build()♪
sing(y)♪''',
        note="Le premier sing devrait marcher, le second devrait échouer car y est locale.",
        expected_error_contains="Variable 'y' not defined"
    ),
]


# ============================================================
# HELPERS
# ============================================================

def normalize_output(s: str) -> str:
    return s.strip().replace('\r\n', '\n').replace('\r', '\n')


def parse_program(code: str):
    ast = parser.parse(code)
    return ast


def execute_program(ast):
    evaluator = EvalClass()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        evaluator.evalInst(ast)
    return normalize_output(buffer.getvalue())


def run_single_test(test):
    name = test["name"]
    code = test["code"]
    kind = test["kind"]

    print(f"\n{name}")
    print(f"Type: {kind}")
    print(f"Code: {code[:80]}..." if len(code) > 80 else f"Code: {code}")

    try:
        ast = parse_program(code)

        if kind == "parse_error":
            if ast is None:
                print("✅ Parse error attendu détecté (AST = None)")
                return "passed"
            else:
                print(f"❌ Parse error attendu, mais AST produit: {ast}")
                return "failed"

        if ast is None:
            print("❌ Le parseur a retourné None")
            return "failed" if kind != "known_edge" else "known-failed"

        output = execute_program(ast)

        if kind == "ok":
            expected = normalize_output(test["expected_output"])
            if output == expected:
                print(f"✅ Résultat: {output if output else '(aucune sortie)'}")
                return "passed"
            else:
                print(f"❌ Attendu: {expected}")
                print(f"❌ Obtenu: {output}")
                return "failed"

        if kind == "runtime_error":
            print("❌ Une erreur runtime était attendue, mais le programme s'est exécuté.")
            print(f"❌ Sortie obtenue: {output}")
            return "failed"

        if kind == "known_edge":
            expected_output = test.get("expected_output")
            if expected_output is not None:
                expected_output = normalize_output(expected_output)
                if output == expected_output:
                    print(f"🟡 EDGE CASE OK: {output if output else '(aucune sortie)'}")
                    print(f"   Note: {test['note']}")
                    return "known-passed"
                else:
                    print(f"🟡 EDGE CASE ÉCHOUÉ (accepté)")
                    print(f"   Attendu idéalement: {expected_output}")
                    print(f"   Obtenu: {output}")
                    print(f"   Note: {test['note']}")
                    return "known-failed"

            print(f"🟡 EDGE CASE exécuté: {output if output else '(aucune sortie)'}")
            print(f"   Note: {test['note']}")
            return "known-passed"

        print("❌ Type de test inconnu")
        return "failed"

    except Exception as e:
        msg = str(e)

        if kind == "runtime_error":
            expected_error = test["expected_error_contains"]
            if expected_error in msg:
                print(f"✅ Erreur attendue: {msg}")
                return "passed"
            else:
                print(f"❌ Mauvaise erreur")
                print(f"❌ Attendu contient: {expected_error}")
                print(f"❌ Obtenu: {msg}")
                return "failed"

        if kind == "parse_error":
            print(f"✅ Parse error attendu via exception: {msg}")
            return "passed"

        if kind == "known_edge":
            expected_error = test.get("expected_error_contains")
            if expected_error:
                if expected_error in msg:
                    print(f"🟡 EDGE CASE: erreur attendue/acceptable détectée: {msg}")
                    print(f"   Note: {test['note']}")
                    return "known-passed"
                else:
                    print(f"🟡 EDGE CASE ÉCHOUÉ (accepté)")
                    print(f"   Erreur obtenue: {msg}")
                    print(f"   Note: {test['note']}")
                    return "known-failed"

            print(f"🟡 EDGE CASE a levé une erreur (accepté): {msg}")
            print(f"   Note: {test['note']}")
            return "known-failed"

        print(f"❌ Erreur inattendue: {msg}")
        return "failed"


def run_test_suite(suite_name, tests):
    print(f"\n{'=' * 70}")
    print(f"{suite_name}")
    print(f"{'=' * 70}")

    passed = 0
    failed = 0
    known_passed = 0
    known_failed = 0

    for test in tests:
        result = run_single_test(test)

        if result == "passed":
            passed += 1
        elif result == "failed":
            failed += 1
        elif result == "known-passed":
            known_passed += 1
        elif result == "known-failed":
            known_failed += 1

    print(f"\n{'-' * 70}")
    print(f"Suite: {suite_name}")
    print(f"✅ Réussis: {passed}")
    print(f"❌ Échoués: {failed}")
    print(f"🟡 Edge cases OK: {known_passed}")
    print(f"🟠 Edge cases en échec accepté: {known_failed}")
    print(f"{'-' * 70}")

    return passed, failed, known_passed, known_failed


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    total_passed = 0
    total_failed = 0
    total_known_passed = 0
    total_known_failed = 0

    suites = [
        ("TESTS DE BASE", basic_tests),
        ("VARIABLES & ASSIGNATION", variable_tests),
        ("PRINT & STRINGS", print_tests),
        ("STRUCTURES DE CONTRÔLE", control_tests),
        ("BREAK & CONTINUE", loop_control_tests),
        ("FONCTIONS", function_tests),
        ("SCOPE (PORTÉE)", scope_tests),
        ("COMMENTAIRES", comment_tests),
        ("ERREURS RUNTIME ATTENDUES", runtime_error_tests),
        ("ERREURS DE PARSE ATTENDUES", parse_error_tests),
        ("EDGE CASES / LIMITATIONS CONNUES", edge_case_tests),
    ]

    for suite_name, tests in suites:
        p, f, kp, kf = run_test_suite(suite_name, tests)
        total_passed += p
        total_failed += f
        total_known_passed += kp
        total_known_failed += kf

    total_strict = total_passed + total_failed
    strict_rate = (total_passed / total_strict * 100) if total_strict else 0.0

    print(f"\n\n{'🎉' * 20}")
    print("RÉSULTATS FINAUX")
    print(f"{'🎉' * 20}")
    print(f"✅ Tests stricts réussis: {total_passed}")
    print(f"❌ Tests stricts échoués: {total_failed}")
    print(f"📊 Taux de réussite strict: {strict_rate:.1f}%")
    print(f"🟡 Edge cases OK: {total_known_passed}")
    print(f"🟠 Edge cases en échec accepté: {total_known_failed}")