
from math import factorial

#----- Set the associated legendre polynomial functions -----#

associated_legendre_polynomials = {
    (0, 0): lambda x: f"1",
    (1, 0): lambda x: f"{x}",
    (1, 1): lambda x: f"-sqrt(1-{x}*{x})",
    (2, 0): lambda x: f"1/2*(3*{x}*{x}-1)",
    (2, 1): lambda x: f"-3*{x}*sqrt(1-{x}*{x})",
    (2, 2): lambda x: f"3*(1-{x}*{x})",
    (3, 0): lambda x: f"1/2*(5*{x}*{x}*{x}-3*{x})",
    (3, 1): lambda x: f"3/2*(1-5*{x}*{x})*sqrt(1-{x}*{x})",
    (3, 2): lambda x: f"15*{x}*(1-{x}*{x})",
    (3, 3): lambda x: f"-15*sqrt(1-{x}*{x})*sqrt(1-{x}*{x})*sqrt(1-{x}*{x})",
    (4, 0): lambda x: f"1/8*(35*{x}*{x}*{x}*{x}-30*{x}*{x}+3)",
    (4, 1): lambda x: f"-5/2*(7*{x}*{x}*{x}-3*{x})*sqrt(1-{x}*{x})",
    (4, 2): lambda x: f"15/2*(7*{x}*{x}-1)*(1-{x}*{x})",
    (4, 3): lambda x: f"-105*{x}*sqrt(1-{x}*{x})*sqrt(1-{x}*{x})*sqrt(1-{x}*{x})",
    (4, 4): lambda x: f"105*(1-{x}*{x})*(1-{x}*{x})",
}

def get_associated_legendre_polynomial(x,l,m,cosine_sine_names=[]):

    if l>4: raise ValueError("l must be <= 4")

    # Handle negative l
    l = l if l>=0 else -l-1

    # Handle m>l
    if abs(m) > l:
        return "0"

    # Get the base formula
    p_lm = associated_legendre_polynomials[(l, abs(m))](x)

    # Reassign with trig identities
    if len(cosine_sine_names)>0 and cosine_sine_names[0] in x:
        new_x = x.replace(cosine_sine_names[0], cosine_sine_names[1])
        p_lm = p_lm.replace(f"sqrt(1-{x}*{x})", new_x)
        p_lm = p_lm.replace(f"(1-{x}*{x})", f"{new_x}*{new_x}")

    # Deal with m<0
    if m < 0:
        m = abs(m) #NOTE: IMPORTANT!
        p_lm = f"({(-1)**m})*({factorial(l-m)})/({factorial(l+m)})*({p_lm})"

    return p_lm

#----- Set the legendre polynomial functions -----#

legendre_polynomials = {
    (0, 0): lambda x: f"1",
    (1, 0): lambda x: f"{x}",
    (1, 1): lambda x: f"sqrt(1-{x}*{x})",
    (2, 0): lambda x: f"1/2*(3*{x}*{x}-1)",
    (2, 1): lambda x: f"2*{x}*sqrt(1-{x}*{x})",
    (2, 2): lambda x: f"(1-{x}*{x})",
}

def get_legendre_polynomial(x,l,m,cosine_sine_names=[]):

    # Check l
    if l<0 or l>2: raise ValueError(f"l must be in (0,1,2) but l = {l}")

    # Check m
    if abs(m) > l: raise ValueError(f"m must satisfy |m| <= l but encountered (l, m) = ({l}, {m})")

    # Get the base formula
    p_lm = legendre_polynomials[(l, abs(m))](x)

    # Reassign with trig identities
    if len(cosine_sine_names)>0 and cosine_sine_names[0] in x:
        new_x = x.replace(cosine_sine_names[0], cosine_sine_names[1])
        p_lm = p_lm.replace(f"sqrt(1-{x}*{x})", new_x)
        p_lm = p_lm.replace(f"(1-{x}*{x})", f"{new_x}*{new_x}")

    return p_lm


# Test P_lm functions
# # Set parameters
# x = "cos(theta)"
# x = 'x'
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# lmax = 4

# # Loop and print formulas
# for l in range(0, lmax+1):
#     for m in range(-l, l+1):
#         p_lm = get_associated_legendre_polynomial(x, l, m, cosine_sine_names=cosine_sine_names)
#         print(f"P_[{l},{m}]({x}) = {p_lm}")

#----- Set the depolarization factor functions -----#
def get_depol_denom_a(e, y):
    if e == "" and y != "":
        return f"(1-{y}+0.5*{y}*{y})"
    elif e != "" and y != "":
        return f"({y}*{y}/(2*(1-{e})))"
    else:
        return "depol_denom_a"

def get_depol_a(e, y):
    if e == "" and y != "":
        return "1.0"
    elif e != "" and y != "":
        return "1.0"
    return "depol_a"

def get_depol_b(e, y):
    if e == "" and y != "":
        return f"((1-{y})/{get_depol_denom_a(e,y)})"
    elif e != "" and y != "":
        return e
    else:
        return "depol_b"

def get_depol_c(e, y):
    if e == "" and y != "":
        return f"({y}*(1-0.5*{y})/{get_depol_denom_a(e,y)})"
    elif e != "" and y != "":
        return f"sqrt(1-{e}*{e})"
    else:
        return "depol_c"

def get_depol_v(e, y):
    if e == "" and y != "":
        return f"((2-{y})*sqrt(1-{y})/{get_depol_denom_a(e,y)})"
    elif e != "" and y != "":
        return f"sqrt(2*{e}*(1+{e}))"
    else:
        return "depol_v"

def get_depol_w(e, y):
    if e == "" and y != "":
        return f"({y}*sqrt(1-{y})/{get_depol_denom_a(e,y)})"
    elif e != "" and y != "":
        return f"sqrt(2*{e}*(1-{e}))"
    else:
        return "depol_w"


print("DEBUGGING:",get_depol_denom_a("",""),"=",get_depol_denom_a("","y"))
print("DEBUGGING:",get_depol_a("",""),"=",get_depol_a("","y"))
print("DEBUGGING:",get_depol_b("",""),"=",get_depol_b("","y"))
print("DEBUGGING:",get_depol_c("",""),"=",get_depol_c("","y"))
print("DEBUGGING:",get_depol_v("",""),"=",get_depol_v("","y"))
print("DEBUGGING:",get_depol_w("",""),"=",get_depol_w("","y"))

print("DEBUGGING:",get_depol_denom_a("",""),"=",get_depol_denom_a("e","y"))
print("DEBUGGING:",get_depol_a("",""),"=",get_depol_a("e","y"))
print("DEBUGGING:",get_depol_b("",""),"=",get_depol_b("e","y"))
print("DEBUGGING:",get_depol_c("",""),"=",get_depol_c("e","y"))
print("DEBUGGING:",get_depol_v("",""),"=",get_depol_v("e","y"))
print("DEBUGGING:",get_depol_w("",""),"=",get_depol_w("e","y"))


#----- Set the cross section functions UU -----#

def get_xs_uu(e, y, costheta, phi_h, phi_r, lmax=2, asyms_name='sgasyms', asym_idx=0, cosine_sine_names=[]):
    xs_uu = ""
    depol_a = get_depol_a(e,y)
    depol_b = get_depol_b(e,y)
    depol_v = get_depol_v(e,y)

    depols = [depol_a, depol_b, depol_v]
    asyms  = []
    asym_formulas = {depol_a:[], depol_b:[], depol_v:[]}

    #----- Set first set of asymmetries -----#
    # Loop l values
    xs_uu_a = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(0, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_uu_a != "":
                xs_uu_a += "+"
            #NOTE: This is what you would use except that the F_XX,L terms are all zero. See: http://arxiv.org/abs/1408.5721.
            # asym_formula= f"{p_lm}*cos({m}*({phi_h}-{phi_r}))*({asyms_name}[{asym_idx}]+{e}*{asyms_name}[{asym_idx+1}])" if m!=0 else f"{p_lm}*({asyms_name}[{asym_idx}]+{e}*{asyms_name}[{asym_idx+1}])"
            # asym_idx += 2
            asym_formula = f"{p_lm}*cos({m}*({phi_h}-{phi_r}))*({asyms_name}[{asym_idx}])" if m!=0 else f"{p_lm}*({asyms_name}[{asym_idx}])"
            asym_idx += 1
            xs_uu_a += asym_formula
            asym_formulas[depol_a].append(asym_formula)
            asym_name = f"A_UU,T^[ P_({l},{m}) cos({m}({phi_h}-{phi_r})) ]" if m!=0 else f"A_UU,T^[ P_({l},{m}) ]"
            asyms.append(asym_name)
            # asym_name = f"A_UU,L^[ P_({l},{m}) cos({m}({phi_h}-{phi_r})) ]" if m!=0 else f"A_UU,L^[ P_({l},{m}) ]"
            # asyms.append(asym_name)

    # Set the xs value
    xs_uu_a = f"{depol_a}*({xs_uu_a})"

    #----- Set second set of asymmetries -----#
    # Loop l values
    xs_uu_b = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_uu_b != "":
                xs_uu_b += "+"
            asym_formula = f"{p_lm}*cos({m}*{phi_r})*{asyms_name}[{asym_idx}]" if m==2 \
                            else f"{p_lm}*cos({2-m}*{phi_h})*{asyms_name}[{asym_idx}]" if m==0 \
                            else f"{p_lm}*cos({2-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_uu_b += asym_formula
            asym_formulas[depol_b].append(asym_formula)
            asym_name = f"A_UU^[ P_({l},{m}) cos({m} {phi_r}) ]" if m==2 \
                        else f"A_UU^[ P_({l},{m}) cos({2-m} {phi_h}) ]" if m==0 \
                        else f"A_UU^[ P_({l},{m}) cos({2-m} {phi_h} + {m} {phi_r}) ]"
            asyms.append(asym_name)

    # Set the xs value
    xs_uu_b = f"{depol_b}*({xs_uu_b})"

    #----- Set third set of asymmetries -----#
    # Loop l values
    xs_uu_v = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_uu_v != "":
                xs_uu_v += "+"
            asym_formula = f"{p_lm}*cos({m}*{phi_r})*{asyms_name}[{asym_idx}]" if m==1 \
                            else f"{p_lm}*cos({1-m}*{phi_h})*{asyms_name}[{asym_idx}]" if m==0 \
                            else f"{p_lm}*cos({1-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_uu_v += asym_formula
            asym_formulas[depol_v].append(asym_formula)
            asym_name = f"A_UU^[ P_({l},{m}) cos({m}{phi_r}) ]" if m==1 \
                        else f"A_UU^[ P_({l},{m}) cos({1-m}{phi_h}) ]" if m==0 \
                        else f"A_UU^[ P_({l},{m}) cos({1-m}{phi_h}+{m}{phi_r}) ]"
            asyms.append(asym_name)

    # Set the xs formula
    xs_uu_v = f"{depol_v}*({xs_uu_v})"

    # Set the full XS formula
    xs_uu = f"{xs_uu_a} + {xs_uu_b} + {xs_uu_v}"

    # Clean up formulas
    xs_uu = xs_uu.replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for key in asym_formulas:
        for idx in range(len(asym_formulas[key])):
            asym_formulas[key][idx] = asym_formulas[key][idx].replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for idx in range(len(asyms)):
        asyms[idx] = asyms[idx].replace("--","").replace("-+","-").replace("+-","-").replace(f"1{phi_h}",f"{phi_h}").replace(f"1{phi_r}",f"{phi_r}")

    return xs_uu, depols, asyms, asym_formulas

# # Test the unpolarized formula
# e = 'e'
# y = 'y'
# costheta = 'cos(theta)'
# phi_h = 'phi_h'
# phi_r = 'phi_r'
# lmax = 0
# asyms_name = 'sgasyms'
# asym_idx = 0
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# xs_uu, depols_uu, asyms_uu, asym_formulas_uu = get_xs_uu(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


# print("xs_uu = ",xs_uu)
# print("depols_uu = [")
# for depol in depols_uu:
#     print(f"    {depol}")
# print("]")
# print("asyms_uu = [")
# for asym in asyms_uu:
#     print(f"    {asym}")
# print("]")
# print("asym_formulas_uu = {")
# for key in asym_formulas_uu:
#     print("\t"+key+" : [")
#     for el in asym_formulas_uu[key]:
#         print("\t\t"+el+",")
#     print("]")
# print("}")


#----- Set the cross section functions LU -----#

def get_xs_lu(e, y, costheta, phi_h, phi_r, lmax=2, asyms_name='sgasyms', asym_idx=0, cosine_sine_names=[]):
    xs_lu = ""
    depol_c = get_depol_c(e,y)
    depol_w = get_depol_w(e,y)

    depols = [depol_c, depol_w]
    asyms  = []
    asym_formulas = {depol_c:[], depol_w:[]}

    #----- Set first set of asymmetries -----#
    # Loop l values
    xs_lu_c = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(1, l+1): #NOTE: Start at m=1 because sin(0)=0
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_lu_c != "":
                xs_lu_c += "+"
            #NOTE: This is what you would use except that the F_XX,L terms are all zero. See: http://arxiv.org/abs/1408.5721.
            # asym_formula = f"{p_lm}*sin({m}*({phi_h}-{phi_r}))*2*({asyms_name}[{asym_idx}]+{e}*{asyms_name}[{asym_idx+1}])"
            # asym_idx += 2
            asym_formula = f"{p_lm}*sin({m}*({phi_h}-{phi_r}))*2*({asyms_name}[{asym_idx}])"
            asym_idx += 1
            xs_lu_c += asym_formula
            asym_formulas[depol_c].append(asym_formula)
            asyms.append(f"A_LU,T^[ P_({l},{m}) sin({m}({phi_h}-{phi_r})) ]")
            # asyms.append(f"A_LU,L^[ P_({l},{m}) sin({m}({phi_h}-{phi_r})) ]")

    # Set the xs value
    xs_lu_c = f"{depol_c}*({xs_lu_c})"

    #----- Set third set of asymmetries -----#
    # Loop l values
    xs_lu_w = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_lu_w != "":
                xs_lu_w += "+"
            asym_formula = f"{p_lm}*cos({m}*{phi_r})*{asyms_name}[{asym_idx}]" if m==1 \
                        else f"{p_lm}*cos({1-m}*{phi_h})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*cos({1-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_lu_w += asym_formula
            asym_formulas[depol_w].append(asym_formula)
            asym_name = f"A_LU^[ P_({l},{m}) cos({m}{phi_r}) ]" if m==1 \
                    else f"A_LU^[ P_({l},{m}) cos({1-m}{phi_h}) ]" if m==0 \
                    else f"A_LU^[ P_({l},{m}) cos({1-m}{phi_h}+{m}{phi_r}) ]"
            asyms.append(asym_name)

    # Set the xs formula
    xs_lu_w = f"{depol_w}*({xs_lu_w})"

    # Set the full XS formula
    xs_lu = f"{xs_lu_c} + {xs_lu_w}"

    # Clean up formulas
    xs_lu = xs_lu.replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for key in asym_formulas:
        for idx in range(len(asym_formulas[key])):
            asym_formulas[key][idx] = asym_formulas[key][idx].replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for idx in range(len(asyms)):
        asyms[idx] = asyms[idx].replace("--","").replace("-+","-").replace("+-","-").replace(f"1{phi_h}",f"{phi_h}").replace(f"1{phi_r}",f"{phi_r}")

    return xs_lu, depols, asyms, asym_formulas

# # Test the UU formula
# e = 'e'
# y = 'y'
# costheta = 'cos(theta)'
# phi_h = 'phi_h'
# phi_r = 'phi_r'
# lmax = 0
# asyms_name = 'sgasyms'
# asym_idx = 0
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# xs_lu, depols_lu, asyms_lu, asym_formulas_lu = get_xs_lu(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


# print("xs_lu = ",xs_lu)
# print("depols_lu = [")
# for depol in depols_lu:
#     print(f"    {depol}")
# print("]")
# print("asyms_lu = [")
# for asym in asyms_lu:
#     print(f"    {asym}")
# print("]")
# print("asym_formulas_lu = {")
# for key in asym_formulas_lu:
#     print("\t"+key+" : [")
#     for el in asym_formulas_lu[key]:
#         print("\t\t"+el+",")
#     print("]")
# print("}")

#----- Set the cross section functions UL -----#

def get_xs_ul(e, y, costheta, phi_h, phi_r, lmax=2, asyms_name='sgasyms', asym_idx=0, cosine_sine_names=[]):
    xs_ul = ""
    depol_a = get_depol_a(e,y)
    depol_b = get_depol_b(e,y)
    depol_v = get_depol_v(e,y)

    depols = [depol_a, depol_b, depol_v]
    asyms  = []
    asym_formulas = {depol_a:[], depol_b:[], depol_v:[]}

    #----- Set first set of asymmetries -----#
    # Loop l values
    xs_ul_a = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(1, l+1): #NOTE: Start at m=1 because sin(0)=0
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_ul_a != "":
                xs_ul_a += "+"
            asym_formula = f"{p_lm}*sin(-{m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ul_a += asym_formula
            asym_formulas[depol_a].append(asym_formula)
            asyms.append(f"A_UL^[ P_({l},{m}) sin(-{m}{phi_h}+{m}{phi_r}) ]")

    # Set the xs value
    xs_ul_a = f"{depol_a}*({xs_ul_a})"

    #----- Set second set of asymmetries -----#
    # Loop l values
    xs_ul_b = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_ul_b != "":
                xs_ul_b += "+"
            asym_formula = f"{p_lm}*sin({m}*{phi_r})*{asyms_name}[{asym_idx}]" if m==2 \
                        else f"{p_lm}*sin({2-m}*{phi_h})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*sin({2-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ul_b += asym_formula
            asym_formulas[depol_b].append(asym_formula)
            asym_name = f"A_UL^[ P_({l},{m}) sin({m}{phi_r}) ]" if m==2 \
                    else f"A_UL^[ P_({l},{m}) sin({2-m}{phi_h}) ]" if m==0 \
                    else f"A_UL^[ P_({l},{m}) sin({2-m}{phi_h}+{m}{phi_r}) ]"
            asyms.append(asym_name)

    # Set the xs value
    xs_ul_b = f"{depol_b}*({xs_ul_b})"

    #----- Set third set of asymmetries -----#
    # Loop l values
    xs_ul_v = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_ul_v != "":
                xs_ul_v += "+"
            asym_formula = f"{p_lm}*sin({m}*{phi_r})*{asyms_name}[{asym_idx}]" if m==1 \
                        else f"{p_lm}*sin({1-m}*{phi_h})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*sin({1-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ul_v += asym_formula
            asym_formulas[depol_v].append(asym_formula)
            asym_name = f"A_UL^[ P_({l},{m}) sin({m}{phi_r}) ]" if m==1 \
                    else f"A_UL^[ P_({l},{m}) sin({1-m}{phi_h}) ]" if m==0 \
                    else f"A_UL^[ P_({l},{m}) sin({1-m}{phi_h}+{m}{phi_r}) ]"
            asyms.append(asym_name)

    # Set the xs formula
    xs_ul_v = f"{depol_v}*({xs_ul_v})"

    # Set the full XS formula
    xs_ul = f"{xs_ul_a} + {xs_ul_b} + {xs_ul_v}"

    # Clean up formulas
    xs_ul = xs_ul.replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for key in asym_formulas:
        for idx in range(len(asym_formulas[key])):
            asym_formulas[key][idx] = asym_formulas[key][idx].replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for idx in range(len(asyms)):
        asyms[idx] = asyms[idx].replace("--","").replace("-+","-").replace("+-","-").replace(f"1{phi_h}",f"{phi_h}").replace(f"1{phi_r}",f"{phi_r}")

    return xs_ul, depols, asyms, asym_formulas

# # Test the UL formula
# e = 'e'
# y = 'y'
# costheta = 'cos(theta)'
# phi_h = 'phi_h'
# phi_r = 'phi_r'
# lmax = 0
# asyms_name = 'sgasyms'
# asym_idx = 0
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# xs_ul, depols_ul, asyms_ul, asym_formulas_ul = get_xs_ul(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


# print("xs_ul = ",xs_ul)
# print("depols_ul = [")
# for depol in depols_ul:
#     print(f"    {depol}")
# print("]")
# print("asyms_ul = [")
# for asym in asyms_ul:
#     print(f"    {asym}")
# print("]")
# print("asym_formulas_ul = {")
# for key in asym_formulas_ul:
#     print("\t"+key+" : [")
#     for el in asym_formulas_ul[key]:
#         print("\t\t"+el+",")
#     print("]")
# print("}")


#----- Set the cross section functions LL -----#

def get_xs_ll(e, y, costheta, phi_h, phi_r, lmax=2, asyms_name='sgasyms', asym_idx=0, cosine_sine_names=[]):
    xs_ll = ""
    depol_c = get_depol_c(e,y)
    depol_w = get_depol_w(e,y)

    depols = [depol_c, depol_w]
    asyms  = []
    asym_formulas = {depol_c:[], depol_w:[]}

    #----- Set first set of asymmetries -----#
    # Loop l values
    xs_ll_c = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(0, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_ll_c != "":
                xs_ll_c += "+"
            asym_formula = f"4*{p_lm}*cos({m}*({phi_h}-{phi_r}))*{asyms_name}[{asym_idx}]" if m!=0 else f"2*{p_lm}*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ll_c += asym_formula
            asym_formulas[depol_c].append(asym_formula)
            asym_name = f"A_LL^[ P_({l},{m}) cos({m}({phi_h}-{phi_r})) ]" if m!=0 else f"A_LL^[ P_({l},{m}) ]"
            asyms.append(asym_name)

    # Set the xs value
    xs_ll_c = f"{depol_c}*({xs_ll_c})"

    #----- Set second set of asymmetries -----#
    # Loop l values
    xs_ll_w = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_ll_w != "":
                xs_ll_w += "+"
            asym_formula = f"{p_lm}*cos({m}*{phi_r})*{asyms_name}[{asym_idx}]" if m==1 \
                        else f"{p_lm}*cos({1-m}*{phi_h})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*cos({1-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ll_w += asym_formula
            asym_formulas[depol_w].append(asym_formula)
            asym_name = f"A_LL^[ P_({l},{m}) cos({m}{phi_r}) ]" if m==1 \
                    else f"A_LL^[ P_({l},{m}) cos({1-m}{phi_h}) ]" if m==0 \
                    else f"A_LL^[ P_({l},{m}) cos({1-m}{phi_h}+{m}{phi_r}) ]"
            asyms.append(asym_name)

    # Set the xs formula
    xs_ll_w = f"{depol_w}*({xs_ll_w})"

    # Set the full XS formula
    xs_ll = f"{xs_ll_c} + {xs_ll_w}"

    # Clean up formulas
    xs_ll = xs_ll.replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for key in asym_formulas:
        for idx in range(len(asym_formulas[key])):
            asym_formulas[key][idx] = asym_formulas[key][idx].replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for idx in range(len(asyms)):
        asyms[idx] = asyms[idx].replace("--","").replace("-+","-").replace("+-","-").replace(f"1{phi_h}",f"{phi_h}").replace(f"1{phi_r}",f"{phi_r}")

    return xs_ll, depols, asyms, asym_formulas

# # Test the LL formula
# e = 'e'
# y = 'y'
# costheta = 'cos(theta)'
# phi_h = 'phi_h'
# phi_r = 'phi_r'
# lmax = 0
# asyms_name = 'sgasyms'
# asym_idx = 0
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# xs_ll, depols_ll, asyms_ll, asym_formulas_ll = get_xs_ll(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


# print("xs_ll = ",xs_ll)
# print("depols_ll = [")
# for depol in depols_ll:
#     print(f"    {depol}")
# print("]")
# print("asyms_ll = [")
# for asym in asyms_ll:
#     print(f"    {asym}")
# print("]")
# print("asym_formulas_ll = {")
# for key in asym_formulas_ll:
#     print("\t"+key+" : [")
#     for el in asym_formulas_ll[key]:
#         print("\t\t"+el+",")
#     print("]")
# print("}")

#----- Set the cross section functions UT -----#

def get_xs_ut(e, y, costheta, phi_h, phi_r, phi_s, lmax=2, asyms_name='sgasyms', asym_idx=0, cosine_sine_names=[]):
    xs_ut = ""
    depol_a = get_depol_a(e,y)
    depol_b = get_depol_b(e,y)
    depol_v = get_depol_v(e,y)

    depols = [depol_a, depol_b, depol_v]
    asyms  = []
    asym_formulas = {depol_a:[], depol_b:[], depol_v:[]}

    #----- Set first set of asymmetries -----#
    # Loop l values
    xs_ut_a = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_ut_a != "":
                xs_ut_a += "+"
            #NOTE: This is what you would use except that the F_XX,L terms are all zero. See: http://arxiv.org/abs/1408.5721.
            # asym_formula = f"{p_lm}*sin({m+1}*{phi_h}-{phi_s})*({asyms_name}[{asym_idx}]+{e}*{asyms_name}[{asym_idx+1}])" if m==0 \
            #             else f"{p_lm}*sin({m}*{phi_r}-{phi_s})*({asyms_name}[{asym_idx}]+{e}*{asyms_name}[{asym_idx+1}])" if m==-1 \
            #             else f"{p_lm}*sin({m+1}*{phi_h}-{m}*{phi_r}-{phi_s})*({asyms_name}[{asym_idx}]+{e}*{asyms_name}[{asym_idx+1}])"
            # asym_idx += 2
            asym_formula = f"{p_lm}*sin({m+1}*{phi_h}-{phi_s})*({asyms_name}[{asym_idx}])" if m==0 \
                        else f"{p_lm}*sin({m}*{phi_r}-{phi_s})*({asyms_name}[{asym_idx}])" if m==-1 \
                        else f"{p_lm}*sin({m+1}*{phi_h}-{m}*{phi_r}-{phi_s})*({asyms_name}[{asym_idx}])"
            asym_idx += 1
            xs_ut_a += asym_formula
            asym_formulas[depol_a].append(asym_formula)
            asym_name = f"A_UT,T^[ P_({l},{m}) sin({m+1}{phi_h}-{phi_s}) ]" if m==0 \
                    else f"A_UT,T^[ P_({l},{m}) sin({m}{phi_r}-{phi_s}) ]" if m==-1 \
                    else f"A_UT,T^[ P_({l},{m}) sin({m+1}{phi_h}-{m}{phi_r}-{phi_s}) ]"
            asyms.append(asym_name)
            # asym_name = f"A_UT,L^[ P_({l},{m}) sin({m+1}{phi_h}-{phi_s}) ]" if m==0 \
            #         else f"A_UT,L^[ P_({l},{m}) sin({m}{phi_r}-{phi_s}) ]" if m==-1 \
            #         else f"A_UT,L^[ P_({l},{m}) sin({m+1}{phi_h}-{m}{phi_r}-{phi_s}) ]"
            # asyms.append(asym_name)

    # Set the xs value
    xs_ut_a = f"{depol_a}*({xs_ut_a})"

    #----- Set second set of asymmetries -----#
    # Loop l values
    xs_ut_b = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)

            # First term
            if xs_ut_b != "":
                xs_ut_b += "+"
            asym_formula = f"{p_lm}*sin({m}*{phi_r}+{phi_s})*{asyms_name}[{asym_idx}]" if m==1 \
                        else f"{p_lm}*sin({1-m}*{phi_h}+{phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*sin({1-m}*{phi_h}+{m}*{phi_r}+{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ut_b += asym_formula
            asym_formulas[depol_b].append(asym_formula)
            asym_name = f"A_UT^[ P_({l},{m}) sin({m}{phi_r}+{phi_s}) ]" if m==1 \
                    else f"A_UT^[ P_({l},{m}) sin({1-m}{phi_h}+{phi_s}) ]" if m==0 \
                    else f"A_UT^[ P_({l},{m}) sin({1-m}{phi_h}+{m}{phi_r}+{phi_s}) ]"
            asyms.append(asym_name)

            # And second term
            if xs_ut_b != "":
                xs_ut_b += "+"
            asym_formula = f"{p_lm}*sin({m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]" if m==3 \
                        else f"{p_lm}*sin({3-m}*{phi_h}-{phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*sin({3-m}*{phi_h}+{m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ut_b += asym_formula
            asym_formulas[depol_b].append(asym_formula)
            asym_name = f"A_UT^[ P_({l},{m}) sin({m}{phi_r}-{phi_s}) ]" if m==3 \
                    else f"A_UT^[ P_({l},{m}) sin({3-m}{phi_h}-{phi_s}) ]" if m==0 \
                    else f"A_UT^[ P_({l},{m}) sin({3-m}{phi_h}+{m}{phi_r}-{phi_s}) ]"
            asyms.append(asym_name)

    # Set the xs value
    xs_ut_b = f"{depol_b}*({xs_ut_b})"

    #----- Set third set of asymmetries -----#
    # Loop l values
    xs_ut_v = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)

            # First term
            if xs_ut_v != "":
                xs_ut_v += "+"
            asym_formula = f"{p_lm}*sin({phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*sin(-{m}*{phi_h}+{m}*{phi_r}+{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ut_v += asym_formula
            asym_formulas[depol_v].append(asym_formula)
            asym_name = f"A_UT^[ P_({l},{m}) sin({phi_s}) ]" if m==0 \
                    else f"A_UT^[ P_({l},{m}) sin(-{m}{phi_h}+{m}{phi_r}+{phi_s}) ]"
            asyms.append(asym_name)

            # And second term
            if xs_ut_v != "":
                xs_ut_v += "+"
            asym_formula = f"{p_lm}*sin({m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]" if m==2 \
                        else f"{p_lm}*sin({2-m}*{phi_h}-{phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                        else f"{p_lm}*sin({2-m}*{phi_h}+{m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_ut_v += asym_formula
            asym_formulas[depol_v].append(asym_formula)
            asym_name = f"A_UT^[ P_({l},{m}) sin({m}{phi_r}-{phi_s}) ]" if m==2 \
                    else f"A_UT^[ P_({l},{m}) sin({2-m}{phi_h}-{phi_s}) ]" if m==0 \
                    else f"A_UT^[ P_({l},{m}) sin({2-m}{phi_h}+{m}{phi_r}-{phi_s}) ]"
            asyms.append(asym_name)

    # Set the xs formula
    xs_ut_v = f"{depol_v}*({xs_ut_v})"

    # Set the full XS formula
    xs_ut = f"{xs_ut_a} + {xs_ut_b} + {xs_ut_v}"

    # Clean up formulas
    xs_ut = xs_ut.replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for key in asym_formulas:
        for idx in range(len(asym_formulas[key])):
            asym_formulas[key][idx] = asym_formulas[key][idx].replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for idx in range(len(asyms)):
        asyms[idx] = asyms[idx].replace("--","").replace("-+","-").replace("+-","-").replace(f"1{phi_h}",f"{phi_h}").replace(f"1{phi_r}",f"{phi_r}")

    return xs_ut, depols, asyms, asym_formulas

# # Test the UT formula
# e = 'e'
# y = 'y'
# costheta = 'cos(theta)'
# phi_h = 'phi_h'
# phi_r = 'phi_r'
# phi_s = 'phi_s_up'
# lmax = 0
# asyms_name = 'sgasyms'
# asym_idx = 0
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# xs_ut, depols_ut, asyms_ut, asym_formulas_ut = get_xs_ut(e, y, costheta, phi_h, phi_r, phi_s, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


# print("xs_ut = ",xs_ut)
# print("depols_ut = [")
# for depol in depols_ut:
#     print(f"    {depol}")
# print("]")
# print("asyms_ut = [")
# for asym in asyms_ut:
#     print(f"    {asym}")
# print("]")
# print("asym_formulas_ut = {")
# for key in asym_formulas_ut:
#     print("\t"+key+" : [")
#     for el in asym_formulas_ut[key]:
#         print("\t\t"+el+",")
#     print("]")
# print("}")


#----- Set the cross section functions LT -----#

def get_xs_lt(e, y, costheta, phi_h, phi_r, phi_s, lmax=2, asyms_name='sgasyms', asym_idx=0, cosine_sine_names=[]):
    xs_lt = ""
    depol_c = get_depol_c(e,y)
    depol_w = get_depol_w(e,y)

    depols = [depol_c, depol_w]
    asyms  = []
    asym_formulas = {depol_c:[], depol_w:[]}

    #----- Set first set of asymmetries -----#
    # Loop l values
    xs_lt_c = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(0, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            if xs_lt_c != "":
                xs_lt_c += "+"
            asym_formula = f"2*{p_lm}*cos({m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]" if m==1 \
                            else f"2*{p_lm}*cos({1-m}*{phi_h}-{phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                            else f"2*{p_lm}*cos({1-m}*{phi_h}+{m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_lt_c += asym_formula
            asym_formulas[depol_c].append(asym_formula)
            asym_name = f"A_LT^[ P_({l},{m}) cos({m}{phi_r}-{phi_s}) ]" if m==1 \
                        else f"A_LT^[ P_({l},{m}) cos({1-m}{phi_h}-{phi_s}) ]" if m==0 \
                        else f"A_LT^[ P_({l},{m}) cos({1-m}{phi_h}+{m}{phi_r}-{phi_s}) ]"
            asyms.append(asym_name)

    # Set the xs value
    xs_lt_c = f"{depol_c}*({xs_lt_c})"

    #----- Set second set of asymmetries -----#
    # Loop l values
    xs_lt_w = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)

            # First term
            if xs_lt_w != "":
                xs_lt_w += "+"
            asym_formula = f"{p_lm}*cos({phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                            else f"{p_lm}*cos(-{m}*{phi_h}+{m}*{phi_r}+{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_lt_w += asym_formula
            asym_formulas[depol_w].append(asym_formula)
            asym_name = f"A_LT^[ P_({l},{m}) cos({phi_s}) ]" if m==0 \
                        else f"A_LT^[ P_({l},{m}) cos(-{m}{phi_h}+{m}{phi_r}+{phi_s}) ]"
            asyms.append(asym_name)

            # And second term
            if xs_lt_w != "":
                xs_lt_w += "+"
            asym_formula = f"{p_lm}*cos({m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]" if m==2 \
                            else f"{p_lm}*cos({2-m}*{phi_h}-{phi_s})*{asyms_name}[{asym_idx}]" if m==0 \
                            else f"{p_lm}*cos({2-m}*{phi_h}+{m}*{phi_r}-{phi_s})*{asyms_name}[{asym_idx}]"
            asym_idx += 1
            xs_lt_w += asym_formula
            asym_formulas[depol_w].append(asym_formula)
            asym_name = f"A_LT^[ P_({l},{m}) cos({m}{phi_r}-{phi_s}) ]" if m==2 \
                        else f"A_LT^[ P_({l},{m}) cos({2-m}{phi_h}-{phi_s}) ]" if m==0 \
                        else f"A_LT^[ P_({l},{m}) cos({2-m}{phi_h}+{m}{phi_r}-{phi_s}) ]"
            asyms.append(asym_name)

    # Set the xs formula
    xs_lt_w = f"{depol_w}*({xs_lt_w})"

    # Set the full XS formula
    xs_lt = f"{xs_lt_c} + {xs_lt_w}"

    # Clean up formulas
    xs_lt = xs_lt.replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for key in asym_formulas:
        for idx in range(len(asym_formulas[key])):
            asym_formulas[key][idx] = asym_formulas[key][idx].replace("--","").replace("-+","-").replace("+-","-").replace("-1*","-").replace("+1*","+").replace("(1*","(").replace("*1*","*")
    for idx in range(len(asyms)):
        asyms[idx] = asyms[idx].replace("--","").replace("-+","-").replace("+-","-").replace(f"1{phi_h}",f"{phi_h}").replace(f"1{phi_r}",f"{phi_r}")

    return xs_lt, depols, asyms, asym_formulas

# # Test the LT formula
# e = 'e'
# y = 'y'
# costheta = 'cos(theta)'
# phi_h = 'phi_h'
# phi_r = 'phi_r'
# phi_s = 'phi_s_up'
# lmax = 0
# asyms_name = 'sgasyms'
# asym_idx = 0
# cosine_sine_names = ['cos(theta)', 'sin(theta)']
# xs_lt, depols_lt, asyms_lt, asym_formulas_lt = get_xs_lt(e, y, costheta, phi_h, phi_r, phi_s, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


# print("xs_lt = ",xs_lt)
# print("depols_lt = [")
# for depol in depols_lt:
#     print(f"    {depol}")
# print("]")
# print("asyms_lt = [")
# for asym in asyms_lt:
#     print(f"    {asym}")
# print("]")
# print("asym_formulas_lt = {")
# for key in asym_formulas_lt:
#     print("\t"+key+" : [")
#     for el in asym_formulas_lt[key]:
#         print("\t\t"+el+",")
#     print("]")
# print("}")


#---------- Get the RGC pi+pi- INJECTION formulas for UL and LU ----------#

e = '' #epsilon #epsilon_mc
y = '' #y #y_mc
costheta = 'cos(theta_p1_pipim)'
phi_h = 'phi_h_pipim'
phi_r = 'phi_rt_pipim'
phi_s = 'phi_s_up'
lmax = 2
asyms_name = 'sgasyms'
asym_idx = 0
cosine_sine_names = ['cos(theta_p1_pipim)', 'sin(theta_p1_pipim)']
xs_ul, depols_ul, asyms_ul, asym_formulas_ul = get_xs_ul(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)
asym_idx = len(asyms_ul)
xs_ll, depols_ll, asyms_ll, asym_formulas_ll = get_xs_ll(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)

# Test the UL formula
print("xs_ul = ",xs_ul)
print("depols_ul = [")
for depol in depols_ul:
    print(f"    {depol}")
print("]")
print("asyms_ul = [")
for asym in asyms_ul:
    print(f"    {asym}")
print("]")
print("asym_formulas_ul = {")
for key in asym_formulas_ul:
    print("\t"+key+" : [")
    for el in asym_formulas_ul[key]:
        print("\t\t"+el+",")
    print("]")
print("}")

# Test the LL formula
print("xs_ll = ",xs_ll)
print("depols_ll = [")
for depol in depols_ll:
    print(f"    {depol}")
print("]")
print("asyms_ll = [")
for asym in asyms_ll:
    print(f"    {asym}")
print("]")
print("asym_formulas_ll = {")
for key in asym_formulas_ll:
    print("\t"+key+" : [")
    for el in asym_formulas_ll[key]:
        print("\t\t"+el+",")
    print("]")
print("}")

#---------- Get the RGC pi+pi- FIT formulas for UL and LU ----------#
nfitvars_rgc = 2
e = f'x[{len(asyms_ul)+len(asyms_ll)+nfitvars_rgc}]' #epsilon #epsilon_mc
print("DEBUGGING: e = ",e)
y = 'y' #y #y_mc
costheta = 'cos(theta_p1_pipim)' #'cos(x[0])'
phi_h = 'x[0]' # phi_h_pipim
phi_r = 'x[1]' # phi_rt_pipim
phi_s = '' # phi_s
lmax = 2
asyms_name = 'x'
asym_idx = nfitvars_rgc
cosine_sine_names = ['cos(theta_p1_pipim)', 'sin(theta_p1_pipim)'] #['cos(x[0])', 'sin(x[0])']
xs_ul, depols_ul, asyms_ul, asym_formulas_ul = get_xs_ul(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)
asym_idx = len(asyms_ul) + nfitvars_rgc
xs_ll, depols_ll, asyms_ll, asym_formulas_ll = get_xs_ll(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)

# Print the UL and LL formulas
print("xs_ul = ",xs_ul)
print()
print("xs_ll = ",xs_ll)

#---------- Get the RGH pi+pi- INJECTION formulas for UT and LT ----------#

e = '' #epsilon #epsilon_mc
y = '' #y #y_mc
costheta = 'cos(theta_p1_pipim)'
phi_h = 'phi_h_pipim'
phi_r = 'phi_rt_pipim'
phi_s = 'phi_s_up'
lmax = 2
asyms_name = 'sgasyms'
asym_idx = 0
cosine_sine_names = ['cos(theta_p1_pipim)', 'sin(theta_p1_pipim)']
xs_ut, depols_ut, asyms_ut, asym_formulas_ut = get_xs_ut(e, y, costheta, phi_h, phi_r, phi_s, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)
asym_idx = len(asyms_ut)
xs_lt, depols_lt, asyms_lt, asym_formulas_lt = get_xs_lt(e, y, costheta, phi_h, phi_r, phi_s, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)

# Test the UT formula
print("xs_ut = ",xs_ut)
print("depols_ut = [")
for depol in depols_ut:
    print(f"    {depol}")
print("]")
print("asyms_ut = [")
for asym in asyms_ut:
    print(f"    {asym}")
print("]")
print("asym_formulas_ut = {")
for key in asym_formulas_ut:
    print("\t"+key+" : [")
    for el in asym_formulas_ut[key]:
        print("\t\t"+el+",")
    print("]")
print("}")

# Test the LT formula
print("xs_lt = ",xs_lt)
print("depols_lt = [")
for depol in depols_lt:
    print(f"    {depol}")
print("]")
print("asyms_lt = [")
for asym in asyms_lt:
    print(f"    {asym}")
print("]")
print("asym_formulas_lt = {")
for key in asym_formulas_lt:
    print("\t"+key+" : [")
    for el in asym_formulas_lt[key]:
        print("\t\t"+el+",")
    print("]")
print("}")

#---------- Get the RGH pi+pi- FIT formulas for UT and LT ----------#
nfitvars_rgh = 3
e = f'x[{len(asyms_ul)+len(asyms_ll)+nfitvars_rgh}]' #epsilon #epsilon_mc
y = 'y' #y #y_mc
costheta = 'cos(theta_p1_pipim)' #'cos(x[0])'
phi_h = 'x[0]' # phi_h_pipim
phi_r = 'x[1]' # phi_rt_pipim
phi_s = 'x[2]' # phi_s
lmax = 2
asyms_name = 'x'
asym_idx = nfitvars_rgh
cosine_sine_names = ['cos(theta_p1_pipim)','sin(theta_p1_pipim)'] #['cos(x[0])', 'sin(x[0])']
xs_ut, depols_ut, asyms_ut, asym_formulas_ut = get_xs_ut(e, y, costheta, phi_h, phi_r, phi_s, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)
asym_idx = len(asyms_ut) + nfitvars_rgh
xs_lt, depols_lt, asyms_lt, asym_formulas_lt = get_xs_lt(e, y, costheta, phi_h, phi_r, phi_s, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)

# Print the UT and LT formulas
print("xs_ut = ",xs_ut)
print()
print("xs_lt = ",xs_lt)
