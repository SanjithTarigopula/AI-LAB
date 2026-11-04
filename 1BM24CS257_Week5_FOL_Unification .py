def parse_expr(expr_str):
    expr_str = expr_str.strip()
    if '(' not in expr_str:
        return expr_str
    
    pred_end = expr_str.index('(')
    pred = expr_str[:pred_end].strip()
    args_str = expr_str[pred_end + 1 : -1].strip()
    
    args = []
    current = []
    depth = 0
    for char in args_str:
        if char == ',' and depth == 0:
            args.append(parse_expr(''.join(current)))
            current = []
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            current.append(char)
    if current:
        args.append(parse_expr(''.join(current)))
    
    return [pred] + args

def is_variable(term):
    return isinstance(term, str) and len(term) == 1 and term.islower()

def occurs_check(var, expr):
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occurs_check(var, sub) for sub in expr)
    return False

def apply_subst(subst, expr):
    if isinstance(expr, str):
        return subst.get(expr, expr)
    if isinstance(expr, list):
        return [apply_subst(subst, sub) for sub in expr]
    return expr

def unify(psi1, psi2):
    if isinstance(psi1, str) or isinstance(psi2, str):
        if psi1 == psi2:
            return {}  
        elif is_variable(psi1):
            if occurs_check(psi1, psi2):
                return "FAILURE"
            return {psi1: psi2}
        elif is_variable(psi2):
            if occurs_check(psi2, psi1):
                return "FAILURE"
            return {psi2: psi1}
        else:
            return "FAILURE"

    if psi1[0] != psi2[0]:
        return "FAILURE"
    if len(psi1) != len(psi2):
        return "FAILURE"
    subst = {}
    l1 = psi1[1:]
    l2 = psi2[1:]

    for i in range(len(l1)):
        s = unify(l1[i], l2[i])

        if s == "FAILURE":
            return "FAILURE"

        if s:
            l1 = [apply_subst(s, item) for item in l1]
            l2 = [apply_subst(s, item) for item in l2]
            
            new_subst = {k: apply_subst(s, v) for k, v in subst.items()}
            new_subst.update(s)
            subst = new_subst

    return subst

def format_expr(parsed):
    if isinstance(parsed, str):
        return parsed
    return f"{parsed[0]}({', '.join(format_expr(arg) for arg in parsed[1:])})"

def main():
    print("== First-Order Logic (FOL) Unification Algorithm ==")
    print("Note: Single lowercase letters (e.g., x, y, z) are treated as variables.\n")

    e1_str = input("Enter Expression 1 (e.g., Eats(x, Apple)): ").strip()
    e2_str = input("Enter Expression 2 (e.g., Eats(Riya, y)): ").strip()

    psi1 = parse_expr(e1_str)
    psi2 = parse_expr(e2_str)

    result = unify(psi1, psi2)

    print("\n--- Output ---")
    if result == "FAILURE":
        print("Unification Result: FAILURE")
    else:
        print("Unification Result: SUCCESS")
        if not result:
            print("Substitutions: NIL (Expressions are already identical)")
        else:
            sub_strs = [f"{val}/{var}" for var, val in result.items()]
            print(f"Substitution Set (SUBST): {{ {', '.join(sub_strs)} }}")
            
            unified_psi1 = apply_subst(result, psi1)
            print(f"Unified Expression: {format_expr(unified_psi1)}")

if __name__ == "__main__":
    main()