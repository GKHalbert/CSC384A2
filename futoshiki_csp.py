#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    all_vars = []
    var_table = []
    inequal_table = []
    n = len(futo_grid)
    dom = [i + 1 for i in range(n)]

    col_len = len(futo_grid[0])
    inequal_op = ['.' ,'>', '<']

    cons = []

    for i in range(n):
        row_var = []
        row_ieq = []
        for j in range(col_len):
            if futo_grid[i][j] not in inequal_op:
                if futo_grid[i][j]  == 0:
                    var = Variable("V{}{}".format(i, j//2), dom)
                else:
                    var = Variable("V{}{}".format(i, j//2), [futo_grid[i][j]])
                    var.assign(futo_grid[i][j])
                
                row_var.append(var)
                all_vars.append(var)

            else:
                row_ieq.append(futo_grid[i][j])
        
        var_table.append(row_var)
        inequal_table.append(row_ieq)

    for i in range(n):
        for j in range(n):
            for k in range(j+1, n):
                cur_var = var_table[i][j]
                var_row = var_table[i][k]
                con = Constraint("C(V{}{},V{}{})".format(i,j,i,k), [cur_var, var_row])

                dom_cur = cur_var.cur_domain()
                dom_row = var_row.cur_domain()

                if k == j+1:
                    sat_tuples = sat_tuple_generator(inequal_table[i][j], dom_cur, dom_row)
                else:
                    sat_tuples = sat_tuple_generator('.', dom_cur, dom_row)

                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

                cur_var = var_table[j][i]
                var_col = var_table[k][i]
                con = Constraint("C(V{}{},V{}{})".format(j,i,k,i), [cur_var, var_col])
                dom_cur = cur_var.cur_domain()
                dom_row = var_col.cur_domain()
                sat_tuples = sat_tuple_generator('.', dom_cur, dom_row)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
        
    csp = CSP("size {} model 1 csp".format(n), all_vars)
    
    for c in cons:
        csp.add_constraint(c)

    return csp, var_table


def sat_tuple_generator(ieq, dom1, dom2):
    result = []
    for t in itertools.product(dom1, dom2):
        if ieq_check(ieq, t[0], t[1]):
            result.append(t)
    return result

def ieq_check(ieq, v1, v2):
    if ieq == '.':
        return v1 != v2
    elif ieq == '>':
        return v1 > v2
    else:
        return v1 < v2


def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT 
    all_vars = []
    var_table = []
    inequal_table = []
    n = len(futo_grid)
    dom = [i + 1 for i in range(n)]

    col_len = len(futo_grid[0])
    inequal_op = ['.' ,'>', '<']

    cons = []

    for i in range(n):
        row_var = []
        row_ieq = []
        for j in range(col_len):
            if futo_grid[i][j] not in inequal_op:
                if futo_grid[i][j]  == 0:
                    var = Variable("V{}{}".format(i, j//2), dom)
                else:
                    var =  Variable("V{}{}".format(i, j//2), [futo_grid[i][j]])
                    var.assign(futo_grid[i][j])
                
                row_var.append(var)
                all_vars.append(var)

            else:
                row_ieq.append(futo_grid[i][j])
        
        var_table.append(row_var)
        inequal_table.append(row_ieq)

    for i in range(n):
        row_vars = var_table[i]
        col_vars = []
        row_doms = []
        col_doms = []

        for j in range(n):
            row_doms.append(row_vars[j].cur_domain())
            col_vars.append(var_table[j][i])
            col_doms.append(var_table[j][i].cur_domain())

            if j < n - 1 and inequal_table[i][j] != '.':
                var1 = var_table[i][j]
                var2 = var_table[i][j+1]

                dom1 = var1.cur_domain()
                dom2 = var2.cur_domain()

                con = Constraint("C(V{}{},V{}{})".format(i,j,i,j+1), [var1, var2])

                sat_tuples = sat_tuple_generator(inequal_table[i][j], dom1, dom2)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
        
        con_row = Constraint("C(Row{})".format(i), row_vars)
        con_col = Constraint("C(Col{})".format(i), col_vars)

        row_tuples = all_diff_tuple_generator(row_doms)
        col_tuples = all_diff_tuple_generator(col_doms)

        con_row.add_satisfying_tuples(row_tuples)
        con_col.add_satisfying_tuples(col_tuples)

        cons.append(con_row)
        cons.append(con_col)

    
    csp = CSP("size {} model 2 futoshiki".format(n), all_vars)
    for c in cons:
        csp.add_constraint(c)

    return csp, var_table

def all_diff_tuple_generator(doms):
    result = []
    for t in itertools.product(*doms):
        if len(t) == len(set(t)):
            result.append(t)

    return result



    
