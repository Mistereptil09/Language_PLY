from genereTreeGraphviz2 import printTreeGraph

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakLoop(Exception):
    """Exception pour break"""
    pass

class ContinueLoop(Exception):
    """Exception pour continue"""
    pass

class EvalClass:
    def __init__(self):
        self.global_scope = {}
        self.local_scopes = []
        self.functions = {}


    def get_variable(self, name: str):
        if self.local_scopes:
            if name in self.local_scopes[-1]:
                return self.local_scopes[-1][name]
        if name in self.global_scope:
            return self.global_scope[name]

        raise Exception(f"Error: Variable '{name}' not defined")

    def set_variable(self, name: str, value: str):
        if self.local_scopes:
            self.local_scopes[-1][name] = value # dernier dictionnaire de la pile de scopes locaux
        else:
            self.global_scope[name] = value

    def evalInst(self, inst : tuple | str | int | list):
        """Évalue une instruction"""

        # Liste est un bloc
        if isinstance(inst, list):
            for instruction in inst:
                self.evalInst(instruction)
            return

        if not isinstance(inst, tuple):
            return

        operation = inst[0]

        # Print (une ou plusieurs expressions)
        if operation == 'print':
            result = [self.evalExpr(argument) for argument in inst[1]]  # Évaluer chaque argument du tuple
            print(*result)
            return None

        # Assignment (nom de variable, expression)
        elif operation == 'assign':
            var_name = inst[1]
            var_value = self.evalExpr(inst[2])
            self.set_variable(var_name, var_value)
            return None

        # Conditionnelle (condition, bloc, bloc/else optionnel)
        elif operation == 'if':
            if self.evalExpr(inst[1]):  # Condition
                self.evalInst(inst[2])  # Bloc "then"
            elif inst[3]:
                self.evalInst(inst[3])  # Bloc "else"
            return None

        # Boucle while (condition, bloc)
        elif operation == 'while':
            try:
                while self.evalExpr(inst[1]): # Condition
                    try:
                        self.evalInst(inst[2]) # Bloc
                    except ContinueLoop:
                        continue  # Recommence la boucle
            except BreakLoop:
                pass  # Sort de la boucle

        # Boucle for (initialisation, condition, incrémentation, bloc)
        elif operation == 'for':
            self.evalInst(inst[1])  # Init
            try:
                while self.evalExpr(inst[2]): # Condition
                    try:
                        self.evalInst(inst[4])  # Bloc
                    except ContinueLoop:
                        pass  # Continue vers l'increment
                    self.evalInst(inst[3])  # Increment
            except BreakLoop:
                pass


        # Définition de fonction (nom, liste de paramètres, bloc)
        elif operation == 'def':
            func_name = inst[1]
            if func_name in self.functions:
                raise Exception(f"Error: Function '{func_name}' already defined")

            params = inst[2]  # Liste de noms ['a', 'b', 'c']
            body = inst[3]  # Bloc d'instructions

            self.functions[func_name] = {
                'params': params,
                'body': body
            }

        # Appel de fonction (nom, liste d'arguments)
        elif operation == 'call':
            func_name = inst[1]
            if func_name not in self.functions:
                raise Exception(f"Error: Function '{func_name}' not defined")

            func = self.functions[func_name]
            arguments = [self.evalExpr(arg) for arg in inst[2]]

            # Vérifier le nombre d'arguments
            if len(arguments) != len(func['params']):
                raise Exception(f"Error: Function '{func_name}' expects {len(func['params'])} arguments, got {len(arguments)}")

            # 1. Créer un nouveau scope local
            local_scope = {}
            for param, arg in zip(func['params'], arguments):
                local_scope[param] = arg

            # 2. Empiler le scope
            self.local_scopes.append(local_scope)

            # Exécuter et capturer return
            return_value = None
            try:
                # 3. Exécuter le body
                self.evalInst(func['body'])
            except ReturnValue as ret:
                return_value = ret.value
            # 4. Dépiler le scope
            self.local_scopes.pop()

            return return_value

        elif operation == 'return':
            value = self.evalExpr(inst[1])
            raise ReturnValue(value)

        # Dans evalInst
        elif operation == 'continue':  # break
            raise ContinueLoop()

        elif operation == 'break':  # continue
            raise BreakLoop()

        # Si c'est juste une expression seule
        else:
            self.evalExpr(inst)
            return None

    def evalExpr(self, value):
        """Évalue une expression et retourne sa valeur"""
        # Cas de base : nombres
        if isinstance(value, (int, float, bool)):
            return value

        if isinstance(value, str):
            return value

        # Si ce n'est pas un tuple, erreur
        if not isinstance(value, tuple):
            return 0

        operator = value[0]

        # si une variable reçoit le resultat d'une expression en valeur, on doit évaluer l'expression avant de l'assigner à la variable
        if operator == 'call':
            return self.evalInst(value)

        # Variable : chercher dans le scope puis dans le global
        if operator == 'variable':
            var_name = value[1]
            return self.get_variable(var_name)

        # Opérations arithmétiques et logiques
        if operator == '+':
            return self.evalExpr(value[1]) + self.evalExpr(value[2])
        elif operator == '-':
            return self.evalExpr(value[1]) - self.evalExpr(value[2])
        elif operator == '*':
            return self.evalExpr(value[1]) * self.evalExpr(value[2])
        elif operator == '/':
            return self.evalExpr(value[1]) / self.evalExpr(value[2])
        elif operator == '^':
            return self.evalExpr(value[1]) ** self.evalExpr(value[2])
        elif operator == '%':
            return self.evalExpr(value[1]) % self.evalExpr(value[2])
        elif operator == '<':
            return self.evalExpr(value[1]) < self.evalExpr(value[2])
        elif operator == '>':
            return self.evalExpr(value[1]) > self.evalExpr(value[2])
        elif operator == '==':
            return self.evalExpr(value[1]) == self.evalExpr(value[2])
        elif operator == '!=':
            return self.evalExpr(value[1]) != self.evalExpr(value[2])
        elif operator == '<=':
            return self.evalExpr(value[1]) <= self.evalExpr(value[2])
        elif operator == '>=':
            return self.evalExpr(value[1]) >= self.evalExpr(value[2])
        elif operator == '@@':
            return self.evalExpr(value[1]) and self.evalExpr(value[2])
        elif operator == '!@':
            return self.evalExpr(value[1]) or self.evalExpr(value[2])

        return 0


if __name__ == "__main__":
    # Tests
    evaluator = EvalClass()

    # Test 1 : Expressions simples
    print(evaluator.evalExpr(('*', ('+', 2, 5), 3)))  # 21 ✓
    print(evaluator.evalExpr(('*', ('+', 2, 5), ('-', 10, 4))))  # 42 ✓

    # Test 2 : Variables
    evaluator.evalInst(('assign', 'x', 5))
    print(evaluator.evalExpr(('variable', 'x')))  # 5 ✓

    # Test 3 : Assignment avec expression
    evaluator.evalInst(('assign', 'y', ('+', ('variable', 'x'), 3)))
    print(evaluator.variables['y'])  # 8 ✓

    # Test 4 : Print
    evaluator.evalInst(('print', ('*', ('variable', 'y'), 2)))  # Affiche: 16 ✓

    # Test 5 : Bloc d'instructions
    bloc = ('bloc',
        ('assign', 'a', 10),
        ('bloc',
            ('assign', 'b', 20),
            ('print', ('+', ('variable', 'a'), ('variable', 'b')))
        )
    )
    evaluator.evalInst(bloc)  # Affiche: 30 ✓
    printTreeGraph(bloc)