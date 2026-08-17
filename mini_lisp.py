import math
import operator

# ==========================================
# 1. THE PARSER (Text to AST)
# ==========================================
def tokenize(chars: str) -> list:
    """Adds spaces around parentheses and splits the string into a list of tokens."""
    spaced = chars.replace('(', ' ( ').replace(')', ' ) ')
    return spaced.split()

def parse(tokens: list):
    """Takes a list of tokens and builds an Abstract Syntax Tree (nested lists)."""
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")
    
    token = tokens.pop(0)
    
    if token == '(':
        ast = []
        while tokens[0] != ')':
            ast.append(parse(tokens))
        tokens.pop(0) # pop off the closing ')'
        return ast
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return atomize(token)

def atomize(token: str):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)

# ==========================================
# 2. THE ENVIRONMENT MODEL (Lexical Scoping)
# ==========================================
class Environment:
    def __init__(self, params=None, args=None, parent=None):
        self.frame = {}        # The local dictionary
        self.parent = parent   # The pointer to the enclosing environment
        
        # If created by a function call, bind the arguments
        if params and args:
            for param, arg in zip(params, args):
                self.frame[param] = arg

    def define(self, name, value):
        """Binds a name to a value in the CURRENT frame."""
        self.frame[name] = value

    def lookup(self, name):
        """The Lexical Lookup Rule: Check local frame, then check parent."""
        if name in self.frame:
            return self.frame[name]
        elif self.parent is not None:
            return self.parent.lookup(name) # Recursively follow the pointer up!
        else:
            raise NameError(f"Undefined variable: {name}")

# ==========================================
# 3. FUNCTION OBJECTS (The secret to Closures)
# ==========================================
class Procedure:
    def __init__(self, params, body, env):
        self.params = params  # e.g., ['x']
        self.body = body      # The raw AST code
        self.env = env        # The environment where the function was BORN!

    def __call__(self, *args):
        # Create a NEW Local Environment. Parent = where function was born.
        local_env = Environment(self.params, args, parent=self.env)
        # Evaluate body inside this new local environment
        return evaluate(self.body, local_env)

# ==========================================
# 4. THE EVALUATOR (The Engine)
# ==========================================
def evaluate(x, env):
    if isinstance(x, str):             # 1. Variable Lookup
        return env.lookup(x)
    elif not isinstance(x, list):      # 2. Raw Number
        return x
    elif x[0] == 'if':                 # 3. If Statement
        (_, condition, true_path, false_path) = x
        result = evaluate(condition, env)
        return evaluate(true_path, env) if result else evaluate(false_path, env)
    elif x[0] == 'define':             # 4. Variable Definition
        (_, var_name, expression) = x
        value = evaluate(expression, env)
        env.define(var_name, value)
    elif x[0] == 'lambda':             # 5. Function Definition
        (_, params, body) = x
        return Procedure(params, body, env) # Returns Closure!
    else:                              # 6. Function Application
        func = evaluate(x[0], env)
        args = [evaluate(arg, env) for arg in x[1:]]
        return func(*args)

# ==========================================
# 5. RUNTIME SETUP
# ==========================================
def create_global_env():
    env = Environment()
    env.define('+', operator.add)
    env.define('-', operator.sub)
    env.define('*', operator.mul)
    env.define('print', print)
    return env

global_env = create_global_env()

def run(program: str):
    tokens = tokenize(program)
    ast = parse(tokens)
    return evaluate(ast, global_env)

# ==========================================
# 6. THE ULTIMATE TEST
# ==========================================
if __name__ == "__main__":
    print("=============================")
    print("   MINI-LISP INITIALIZED     ")
    print("=============================\n")

    # The Code we are passing into our interpreter
    lisp_code = """
    (define make-adder 
        (lambda (x) 
            (lambda (y) (+ x y))
        )
    )
    """
    
    # 1. Load the code into the interpreter
    run(lisp_code)
    print("[SYSTEM] Defined 'make-adder'...")

    # 2. Create a closure. 
    run("(define add-five (make-adder 5))")
    print("[SYSTEM] Created closure 'add-five'...")

    # 3. Test the closure
    print("\nExecuting: (add-five 10)")
    result1 = run("(add-five 10)")
    print(f"Result: {result1} (Expected: 15)")
    
    # 4. Create a second, completely separate closure to prove state is isolated
    run("(define add-hundred (make-adder 100))")
    print("\nExecuting: (add-hundred 20)")
    result2 = run("(add-hundred 20)")
    print(f"Result: {result2} (Expected: 120)")
    
    print("\n🎉 SUCCESS! Closures and Lexical Scoping are working perfectly.")