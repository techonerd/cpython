import doctest
import textwrap
import unittest


doctests = """
########### Tests borrowed from or inspired by test_genexps.py ############

Test simple loop with conditional

    >>> sum([i*i for i in range(100) if i&1 == 1])
    166650

Test simple nesting

    >>> [(i,j) for i in range(3) for j in range(4)]
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3)]

Test nesting with the inner expression dependent on the outer

    >>> [(i,j) for i in range(4) for j in range(i)]
    [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]

Test the idiom for temporary variable assignment in comprehensions.

    >>> [j*j for i in range(4) for j in [i+1]]
    [1, 4, 9, 16]
    >>> [j*k for i in range(4) for j in [i+1] for k in [j+1]]
    [2, 6, 12, 20]
    >>> [j*k for i in range(4) for j, k in [(i+1, i+2)]]
    [2, 6, 12, 20]

Not assignment

    >>> [i*i for i in [*range(4)]]
    [0, 1, 4, 9]
    >>> [i*i for i in (*range(4),)]
    [0, 1, 4, 9]

Make sure the induction variable is not exposed

    >>> i = 20
    >>> sum([i*i for i in range(100)])
    328350

    >>> i
    20

Verify that syntax error's are raised for listcomps used as lvalues

    >>> [y for y in (1,2)] = 10          # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    SyntaxError: ...

    >>> [y for y in (1,2)] += 10         # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    SyntaxError: ...


########### Tests borrowed from or inspired by test_generators.py ############

Make a nested list comprehension that acts like range()

    >>> def frange(n):
    ...     return [i for i in range(n)]
    >>> frange(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Same again, only as a lambda expression instead of a function definition

    >>> lrange = lambda n:  [i for i in range(n)]
    >>> lrange(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Generators can call other generators:

    >>> def grange(n):
    ...     for x in [i for i in range(n)]:
    ...         yield x
    >>> list(grange(5))
    [0, 1, 2, 3, 4]


Make sure that None is a valid return value

    >>> [None for i in range(10)]
    [None, None, None, None, None, None, None, None, None, None]

"""


class ListComprehensionTest(unittest.TestCase):
    def _check_in_scopes(self, code, outputs=None, ns=None, scopes=None, raises=()):
        code = textwrap.dedent(code)
        scopes = scopes or ["module", "class", "function"]
        for scope in scopes:
            with self.subTest(scope=scope):
                if scope == "class":
                    newcode = textwrap.dedent("""
                        class _C:
                            {code}
                    """).format(code=textwrap.indent(code, "    "))
                    def get_output(moddict, name):
                        return getattr(moddict["_C"], name)
                elif scope == "function":
                    newcode = textwrap.dedent("""
                        def _f():
                            {code}
                            return locals()
                        _out = _f()
                    """).format(code=textwrap.indent(code, "    "))
                    def get_output(moddict, name):
                        return moddict["_out"][name]
                else:
                    newcode = code
                    def get_output(moddict, name):
                        return moddict[name]
                newns = ns.copy() if ns else {}
                try:
                    exec(newcode, newns)
                except raises as e:
                    # We care about e.g. NameError vs UnboundLocalError
                    self.assertIs(type(e), raises)
                else:
                    for k, v in (outputs or {}).items():
                        self.assertEqual(get_output(newns, k), v)

    def test_lambdas_with_iteration_var_as_default(self):
        code = """
            items = [(lambda i=i: i) for i in range(5)]
            y = [x() for x in items]
        """
        outputs = {"y": [0, 1, 2, 3, 4]}
        self._check_in_scopes(code, outputs)

    def test_lambdas_with_free_var(self):
        code = """
            items = [(lambda: i) for i in range(5)]
            y = [x() for x in items]
        """
        outputs = {"y": [4, 4, 4, 4, 4]}
        self._check_in_scopes(code, outputs)

    def test_class_scope_free_var_with_class_cell(self):
        class C:
            def method(self):
                super()
                return __class__
            items = [(lambda: i) for i in range(5)]
            y = [x() for x in items]

        self.assertEqual(C.y, [4, 4, 4, 4, 4])
        self.assertIs(C().method(), C)

    def test_inner_cell_shadows_outer(self):
        code = """
            items = [(lambda: i) for i in range(5)]
            i = 20
            y = [x() for x in items]
        """
        outputs = {"y": [4, 4, 4, 4, 4], "i": 20}
        self._check_in_scopes(code, outputs)

    def test_inner_cell_shadows_outer_no_store(self):
        code = """
            def f(x):
                return [lambda: x for x in range(x)], x
            fns, x = f(2)
            y = [fn() for fn in fns]
        """
        outputs = {"y": [1, 1], "x": 2}
        self._check_in_scopes(code, outputs)

    def test_closure_can_jump_over_comp_scope(self):
        code = """
            items = [(lambda: y) for i in range(5)]
            y = 2
            z = [x() for x in items]
        """
        outputs = {"z": [2, 2, 2, 2, 2]}
        self._check_in_scopes(code, outputs, scopes=["module", "function"])

    def test_cell_inner_free_outer(self):
        code = """
            def f():
                return [lambda: x for x in (x, [1])[1]]
            x = ...
            y = [fn() for fn in f()]
        """
        outputs = {"y": [1]}
        self._check_in_scopes(code, outputs, scopes=["module", "function"])

    def test_free_inner_cell_outer(self):
        code = """
            g = 2
            def f():
                return g
            y = [g for x in [1]]
        """
        outputs = {"y": [2]}
        self._check_in_scopes(code, outputs, scopes=["module", "function"])
        self._check_in_scopes(code, scopes=["class"], raises=NameError)

    def test_inner_cell_shadows_outer_redefined(self):
        code = """
            y = 10
            items = [(lambda: y) for y in range(5)]
            x = y
            y = 20
            out = [z() for z in items]
        """
        outputs = {"x": 10, "out": [4, 4, 4, 4, 4]}
        self._check_in_scopes(code, outputs)

    def test_shadows_outer_cell(self):
        code = """
            def inner():
                return g
            [g for g in range(5)]
            x = inner()
        """
        outputs = {"x": -1}
        self._check_in_scopes(code, outputs, ns={"g": -1})

    def test_explicit_global(self):
        code = """
            global g
            x = g
            g = 2
            items = [g for g in [1]]
            y = g
        """
        outputs = {"x": 1, "y": 2, "items": [1]}
        self._check_in_scopes(code, outputs, ns={"g": 1})

    def test_explicit_global_2(self):
        code = """
            global g
            x = g
            g = 2
            items = [g for x in [1]]
            y = g
        """
        outputs = {"x": 1, "y": 2, "items": [2]}
        self._check_in_scopes(code, outputs, ns={"g": 1})

    def test_explicit_global_3(self):
        code = """
            global g
            fns = [lambda: g for g in [2]]
            items = [fn() for fn in fns]
        """
        outputs = {"items": [2]}
        self._check_in_scopes(code, outputs, ns={"g": 1})

    def test_assignment_expression(self):
        code = """
            x = -1
            items = [(x:=y) for y in range(3)]
        """
        outputs = {"x": 2}
        # assignment expression in comprehension is disallowed in class scope
        self._check_in_scopes(code, outputs, scopes=["module", "function"])

    def test_free_var_in_comp_child(self):
        code = """
            lst = range(3)
            funcs = [lambda: x for x in lst]
            inc = [x + 1 for x in lst]
            [x for x in inc]
            x = funcs[0]()
        """
        outputs = {"x": 2}
        self._check_in_scopes(code, outputs)

    def test_shadow_with_free_and_local(self):
        code = """
            lst = range(3)
            x = -1
            funcs = [lambda: x for x in lst]
            items = [x + 1 for x in lst]
        """
        outputs = {"x": -1}
        self._check_in_scopes(code, outputs)

    def test_shadow_comp_iterable_name(self):
        code = """
            x = [1]
            y = [x for x in x]
        """
        outputs = {"x": [1]}
        self._check_in_scopes(code, outputs)

    def test_nested_free(self):
        code = """
            x = 1
            def g():
                [x for x in range(3)]
                return x
            g()
        """
        outputs = {"x": 1}
        self._check_in_scopes(code, outputs, scopes=["module", "function"])

    def test_introspecting_frame_locals(self):
        code = """
            import sys
            [i for i in range(2)]
            i = 20
            sys._getframe().f_locals
        """
        outputs = {"i": 20}
        self._check_in_scopes(code, outputs)

    def test_nested(self):
        code = """
            l = [2, 3]
            y = [[x ** 2 for x in range(x)] for x in l]
        """
        outputs = {"y": [[0, 1], [0, 1, 4]]}
        self._check_in_scopes(code, outputs)

    def test_nested_2(self):
        code = """
            l = [1, 2, 3]
            x = 3
            y = [x for [x ** x for x in range(x)][x - 1] in l]
        """
        outputs = {"y": [3, 3, 3]}
        self._check_in_scopes(code, outputs, scopes=["module", "function"])
        self._check_in_scopes(code, scopes=["class"], raises=NameError)

    def test_nested_3(self):
        code = """
            l = [(1, 2), (3, 4), (5, 6)]
            y = [x for (x, [x ** x for x in range(x)][x - 1]) in l]
        """
        outputs = {"y": [1, 3, 5]}
        self._check_in_scopes(code, outputs)

    def test_nested_4(self):
        code = """
            items = [([lambda: x for x in range(2)], lambda: x) for x in range(3)]
            out = [([fn() for fn in fns], fn()) for fns, fn in items]
        """
        outputs = {"out": [([1, 1], 2), ([1, 1], 2), ([1, 1], 2)]}
        self._check_in_scopes(code, outputs)

    def test_nameerror(self):
        code = """
            [x for x in [1]]
            x
        """

        self._check_in_scopes(code, raises=NameError)

    def test_dunder_name(self):
        code = """
            y = [__x for __x in [1]]
        """
        outputs = {"y": [1]}
        self._check_in_scopes(code, outputs)

    def test_unbound_local_after_comprehension(self):
        def f():
            if False:
                x = 0
            [x for x in [1]]
            return x

        with self.assertRaises(UnboundLocalError):
            f()

    def test_unbound_local_inside_comprehension(self):
        def f():
            l = [None]
            return [1 for (l[0], l) in [[1, 2]]]

        with self.assertRaises(UnboundLocalError):
            f()

    def test_global_outside_cellvar_inside_plus_freevar(self):
        code = """
            a = 1
            def f():
                func, = [(lambda: b) for b in [a]]
                return b, func()
            x = f()
        """
        self._check_in_scopes(
            code, {"x": (2, 1)}, ns={"b": 2}, scopes=["function", "module"])
        # inside a class, the `a = 1` assignment is not visible
        self._check_in_scopes(code, raises=NameError, scopes=["class"])

    def test_cell_in_nested_comprehension(self):
        code = """
            a = 1
            def f():
                (func, inner_b), = [[lambda: b for b in c] + [b] for c in [[a]]]
                return b, inner_b, func()
            x = f()
        """
        self._check_in_scopes(
            code, {"x": (2, 2, 1)}, ns={"b": 2}, scopes=["function", "module"])
        # inside a class, the `a = 1` assignment is not visible
        self._check_in_scopes(code, raises=NameError, scopes=["class"])

    def test_name_error_in_class_scope(self):
        code = """
            y = 1
            [x + y for x in range(2)]
        """
        self._check_in_scopes(code, raises=NameError, scopes=["class"])

    def test_global_in_class_scope(self):
        code = """
            y = 2
            vals = [(x, y) for x in range(2)]
        """
        outputs = {"vals": [(0, 1), (1, 1)]}
        self._check_in_scopes(code, outputs, ns={"y": 1}, scopes=["class"])

    def test_in_class_scope_inside_function_1(self):
        code = """
            class C:
                y = 2
                vals = [(x, y) for x in range(2)]
            vals = C.vals
        """
        outputs = {"vals": [(0, 1), (1, 1)]}
        self._check_in_scopes(code, outputs, ns={"y": 1}, scopes=["function"])

    def test_in_class_scope_inside_function_2(self):
        code = """
            y = 1
            class C:
                y = 2
                vals = [(x, y) for x in range(2)]
            vals = C.vals
        """
        outputs = {"vals": [(0, 1), (1, 1)]}
        self._check_in_scopes(code, outputs, scopes=["function"])

    def test_in_class_scope_with_global(self):
        code = """
            y = 1
            class C:
                global y
                y = 2
                # Ensure the listcomp uses the global, not the value in the
                # class namespace
                locals()['y'] = 3
                vals = [(x, y) for x in range(2)]
            vals = C.vals
        """
        outputs = {"vals": [(0, 2), (1, 2)]}
        self._check_in_scopes(code, outputs, scopes=["module", "class"])
        outputs = {"vals": [(0, 1), (1, 1)]}
        self._check_in_scopes(code, outputs, scopes=["function"])

    def test_in_class_scope_with_nonlocal(self):
        code = """
            y = 1
            class C:
                nonlocal y
                y = 2
                # Ensure the listcomp uses the global, not the value in the
                # class namespace
                locals()['y'] = 3
                vals = [(x, y) for x in range(2)]
            vals = C.vals
        """
        outputs = {"vals": [(0, 2), (1, 2)]}
        self._check_in_scopes(code, outputs, scopes=["function"])

    def test_nested_has_free_var(self):
        code = """
            items = [a for a in [1] if [a for _ in [0]]]
        """
        outputs = {"items": [1]}
        self._check_in_scopes(code, outputs, scopes=["class"])

    def test_nested_free_var_not_bound_in_outer_comp(self):
        code = """
            z = 1
            items = [a for a in [1] if [x for x in [1] if z]]
        """
        self._check_in_scopes(code, {"items": [1]}, scopes=["module", "function"])
        self._check_in_scopes(code, {"items": []}, ns={"z": 0}, scopes=["class"])

    def test_nested_free_var_in_iter(self):
        code = """
            items = [_C for _C in [1] for [0, 1][[x for x in [1] if _C][0]] in [2]]
        """
        self._check_in_scopes(code, {"items": [1]})

    def test_nested_free_var_in_expr(self):
        code = """
            items = [(_C, [x for x in [1] if _C]) for _C in [0, 1]]
        """
        self._check_in_scopes(code, {"items": [(0, []), (1, [1])]})

    def test_nested_listcomp_in_lambda(self):
        code = """
            f = [(z, lambda y: [(x, y, z) for x in [3]]) for z in [1]]
            (z, func), = f
            out = func(2)
        """
        self._check_in_scopes(code, {"z": 1, "out": [(3, 2, 1)]})

    def test_lambda_in_iter(self):
        code = """
            (func, c), = [(a, b) for b in [1] for a in [lambda : a]]
            d = func()
            assert d is func
            # must use "a" in this scope
            e = a if False else None
        """
        self._check_in_scopes(code, {"c": 1, "e": None})

    def test_assign_to_comp_iter_var_in_outer_function(self):
        code = """
            a = [1 for a in [0]]
        """
        self._check_in_scopes(code, {"a": [1]}, scopes=["function"])

    def test_no_leakage_to_locals(self):
        code = """
            def b():
                [a for b in [1] for _ in []]
                return b, locals()
            r, s = b()
            x = r is b
            y = list(s.keys())
        """
        self._check_in_scopes(code, {"x": True, "y": []}, scopes=["module"])
        self._check_in_scopes(code, {"x": True, "y": ["b"]}, scopes=["function"])
        self._check_in_scopes(code, raises=NameError, scopes=["class"])

    def test_iter_var_available_in_locals(self):
        code = """
            l = [1, 2]
            y = 0
            items = [locals()["x"] for x in l]
            items2 = [vars()["x"] for x in l]
            items3 = [("x" in dir()) for x in l]
            items4 = [eval("x") for x in l]
            # x is available, and does not overwrite y
            [exec("y = x") for x in l]
        """
        self._check_in_scopes(
            code,
            {
                "items": [1, 2],
                "items2": [1, 2],
                "items3": [True, True],
                "items4": [1, 2],
                "y": 0
            }
        )

    def test_comp_in_try_except(self):
        template = """
            value = ["a"]
            try:
                [{func}(value) for value in value]
            except:
                pass
        """
        for func in ["str", "int"]:
            code = template.format(func=func)
            raises = func != "str"
            with self.subTest(raises=raises):
                self._check_in_scopes(code, {"value": ["a"]})

    def test_comp_in_try_finally(self):
        code = """
            def f(value):
                try:
                    [{func}(value) for value in value]
                finally:
                    return value
            ret = f(["a"])
        """
        self._check_in_scopes(code, {"ret": ["a"]})

    def test_exception_in_post_comp_call(self):
        code = """
            value = [1, None]
            try:
                [v for v in value].sort()
            except:
                pass
        """
        self._check_in_scopes(code, {"value": [1, None]})


__test__ = {'doctests' : doctests}

def load_tests(loader, tests, pattern):
    tests.addTest(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    unittest.main()
