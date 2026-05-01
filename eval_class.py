class EvalClass:
    def __init__(self):
        self.global_scope = {}
        self.local_scopes = []
        self.functions = {}
        self._return_value = None  # return value register for function calls

    def get_variable(self, name: str):
        if self.local_scopes and name in self.local_scopes[-1]:
            return self.local_scopes[-1][name]
        if name in self.global_scope:
            return self.global_scope[name]
        raise Exception(f"Error: Variable '{name}' not defined")

    def set_variable(self, name: str, value):
        if self.local_scopes:
            self.local_scopes[-1][name] = value
        else:
            self.global_scope[name] = value

    def evalInst(self, initial_inst: tuple | str | int | list):
        """Évalue une instruction via une pile explicite"""
        stack = [initial_inst]

        while stack:
            inst = stack.pop()

            # Block (list) → push reversed so first instruction is on top
            if isinstance(inst, list):
                for instruction in reversed(inst):
                    stack.append(instruction)
                continue

            if not isinstance(inst, tuple):
                if inst is not None:
                    self.evalExpr(inst)
                continue

            op = inst[0]

            # ── Internal sentinels ────────────────────────────────────────
            if op in ('start_loop', 'end_loop'):
                pass  # consumed by break/continue scans

            elif op == '__func_end__':
                # Reached only when no 'return' was hit (void function)
                self.local_scopes.pop()
                self._return_value = None

            # ── Instructions ──────────────────────────────────────────────
            elif op == 'print':
                print("Miku said:", *[self.evalExpr(arg) for arg in inst[1]])

            elif op == 'assign':
                # Name then expression
                self.set_variable(inst[1], self.evalExpr(inst[2]))

            elif op == 'if':
                # condition
                if self.evalExpr(inst[1]):
                    # if block
                    stack.append(inst[2])
                # else condition
                elif inst[3]:
                    # else block
                    stack.append(inst[3])

            elif op == 'while':
                stack.append(('end_loop',))
                # condition and then block
                stack.append(('while_loop', inst[1], inst[2]))

            elif op == 'while_loop':
                condition, body = inst[1], inst[2]
                if self.evalExpr(condition):
                    stack.append(inst)             # re-check condition next iteration
                    stack.append(('start_loop',))  # continue target
                    stack.append(body)

            elif op == 'for':
                stack.append(('end_loop',))
                # condition, increment expression, block
                stack.append(('for_loop', inst[2], inst[3], inst[4]))
                stack.append(inst[1])  # init runs first

            elif op == 'for_loop':
                condition, increment, body = inst[1], inst[2], inst[3]
                if self.evalExpr(condition):
                    stack.append(inst)             # re-check condition next iteration
                    stack.append(increment)        # increment runs after body
                    stack.append(('start_loop',))  # continue target
                    stack.append(body)

            elif op == 'def':
                func_name = inst[1]
                if func_name in self.functions:
                    raise Exception(f"Error: Function '{func_name}' already defined")
                self.functions[func_name] = {'params': inst[2], 'body': inst[3]}

            elif op == 'call':
                func_name = inst[1]
                if func_name not in self.functions:
                    raise Exception(f"Error: Function '{func_name}' not defined")
                func = self.functions[func_name]
                args = [self.evalExpr(a) for a in inst[2]]
                if len(args) != len(func['params']):
                    raise Exception(
                        f"Error: Function '{func_name}' expects {len(func['params'])} arguments, got {len(args)}"
                    )
                self.local_scopes.append(dict(zip(func['params'], args)))
                stack.append(('__func_end__',))   # scope cleanup if no return
                stack.append(func['body'])

            elif op == 'return':
                if not self.local_scopes:
                    raise Exception("Error: 'return' outside of a function")
                self._return_value = self.evalExpr(inst[1])
                # Drain work stack up to (and including) the function boundary
                while stack:
                    item = stack.pop()
                    if isinstance(item, tuple) and item[0] == '__func_end__':
                        self.local_scopes.pop()
                        break

            elif op == 'continue':
                # Discard remaining body instructions; keep loop re-entry on the stack
                while stack:
                    item = stack.pop()
                    if isinstance(item, tuple) and item[0] == 'start_loop':
                        break

            elif op == 'break':
                # Discard the entire loop (body + loop sentinel + end marker)
                while stack:
                    item = stack.pop()
                    if isinstance(item, tuple) and item[0] == 'end_loop':
                        break

            else:
                self.evalExpr(inst)

        return None

    def evalExpr(self, value):
        """Évalue une expression et retourne sa valeur"""
        if isinstance(value, (int, float, bool)):
            return value
        if isinstance(value, str):
            return value
        if not isinstance(value, tuple):
            return 0

        op = value[0]

        if op == 'call':
            self.evalInst(value)       # runs the call, stores result in _return_value
            return self._return_value  # always valid: set by return, or None for void

        if op == 'variable':
            return self.get_variable(value[1])

        if op == '+':  return self.evalExpr(value[1]) + self.evalExpr(value[2])
        if op == '-':  return self.evalExpr(value[1]) - self.evalExpr(value[2])
        if op == '*':  return self.evalExpr(value[1]) * self.evalExpr(value[2])
        if op == '/':  return self.evalExpr(value[1]) / self.evalExpr(value[2])
        if op == '^':  return self.evalExpr(value[1]) ** self.evalExpr(value[2])
        if op == '%':  return self.evalExpr(value[1]) % self.evalExpr(value[2])
        if op == '<':  return self.evalExpr(value[1]) < self.evalExpr(value[2])
        if op == '>':  return self.evalExpr(value[1]) > self.evalExpr(value[2])
        if op == '==': return self.evalExpr(value[1]) == self.evalExpr(value[2])
        if op == '!=': return self.evalExpr(value[1]) != self.evalExpr(value[2])
        if op == '<=': return self.evalExpr(value[1]) <= self.evalExpr(value[2])
        if op == '>=': return self.evalExpr(value[1]) >= self.evalExpr(value[2])
        if op == '@@': return self.evalExpr(value[1]) and self.evalExpr(value[2])
        if op == '!@': return self.evalExpr(value[1]) or self.evalExpr(value[2])

        return 0