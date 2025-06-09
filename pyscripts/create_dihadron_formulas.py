
from math import factorial

#----- Set the associated legendre polynomial function -----#




#NOTE JUST NEED LEGENDREE HERE
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


#----- Set the cross section functions -----#

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
            p_lm = get_associated_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            asym_idx += 1
            if xs_uu_a != "":
                xs_uu_a += "+"
            asym_formula = f"{p_lm}*cos({m}*({phi_h}-{phi_r}))*{asyms_name}[{asym_idx}]"
            print("DEBUGGING: adding ",asym_formula)
            xs_uu_a += asym_formula
            asym_formulas[depol_a].append(asym_formula)
            asyms.append(f"A^[ P_({l},{m}) cos({m}({phi_h}-{phi_r})) ]")

    # Set the xs value
    xs_uu_a = f"{depol_a}*({xs_uu_a})"

    #----- Set second set of asymmetries -----#
    # Loop l values
    xs_uu_b = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_associated_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            asym_idx += 1
            if xs_uu_b != "":
                xs_uu_b += "+"
            asym_formula = f"{p_lm}*cos({2-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            print("DEBUGGING: adding ",asym_formula)
            xs_uu_b += asym_formula
            asym_formulas[depol_b].append(asym_formula)
            asyms.append(f"A^[ P_({l},{m}) cos({2-m}*{phi_h}+{m}*{phi_r}) ]")

    # Set the xs value
    xs_uu_b = f"{depol_b}*({xs_uu_b})"

    #----- Set third set of asymmetries -----#
    # Loop l values
    xs_uu_v = ""
    for l in range(0,lmax+1):

        # Loop m values
        for m in range(-l, l+1):
            p_lm = get_associated_legendre_polynomial(costheta, l, m, cosine_sine_names=cosine_sine_names)
            asym_idx += 1
            if xs_uu_v != "":
                xs_uu_v += "+"
            asym_formula = f"{p_lm}*cos({1-m}*{phi_h}+{m}*{phi_r})*{asyms_name}[{asym_idx}]"
            print("DEBUGGING: adding ",asym_formula)
            xs_uu_v += asym_formula
            asym_formulas[depol_v].append(asym_formula)
            asyms.append(f"A^[ P_({l},{m}) cos({1-m}*{phi_h}+{m}*{phi_r}) ]")

    # Set the xs formula
    xs_uu_v = f"{depol_v}*({xs_uu_v})"

    # Set the full XS formula
    xs_uu = f"{xs_uu_a} + {xs_uu_b} + {xs_uu_v}"

    return xs_uu, depols, asyms, asym_formulas

# Test the unpolarized formula
e = 'e'
y = 'y'
costheta = 'cos(theta)'
phi_h = 'phi_h'
phi_r = 'phi_r'
lmax = 2
asyms_name = 'sgasyms'
asym_idx = 0
cosine_sine_names = ['cos(theta)', 'sin(theta)']
xs_uu, depols_uu, asyms_uu, asym_formulas_uu = get_xs_uu(e, y, costheta, phi_h, phi_r, lmax=lmax, asyms_name=asyms_name, asym_idx=asym_idx, cosine_sine_names=cosine_sine_names)


print("DEBUGGING: xs_uu = ",xs_uu)
print("DEBUGGING: depols_uu = [")
for depol in depols_uu:
    print(f"DEBUGGING:     {depol}")
print("DEBUGGING: ]")
print("DEBUGGING: asyms_uu = [")
for asym in asyms_uu:
    print(f"DEBUGGING:     {asym}")
print("DEBUGGING: ]")
print("DEBUGGING: asym_formulas_uu = {")
for key in asym_formulas_uu:
    print("DEBUGGING: \t"+key+" : [")
    for el in asym_formulas_uu[key]:
        print("DEBUGGING: \t\t"+el+",")
    print("DEBUGGING: ]")
print("DEBUGGING: }")