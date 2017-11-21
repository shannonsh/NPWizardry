import random
import string
nums = [20, 35, 50]
fname = 'input_{}'

def gen_names(n):
    names = ['Tink', 'Ghost_Saw', 'Carrier', 'Draegan_Monroe', 'Steelkill', 'Soren_Wolf', 'Gomra__Eater_Of_Sheep', 'Zephyrus', 'Essential_Data_Destruction_Robot', 'Thanatos', 'Eoin_Dread', 'Goldenmark', 'Chamory__Champion_Of_The_Blue', 'Zumed__The_Powerful_One', 'Shasta', 'Zeus', 'Ziku__The_Gentle', 'Bazag__The_Dark', 'Lennix_Wright', 'Kill_Kill', 'Gail_Lovelace', 'Solarplume', 'Combot', 'Okl', 'Self-Aware_War_Domination_Device', 'Chomper', 'Lanky_Zombie', 'The_Rapid_Mask', 'Tyndorth__The_White', 'The_Muffled_Shadow', 'Mechanized_Animal_Protection_Technology', 'Romran__The_Powerful_One', 'Thornfluff', 'Higher', 'Ratcher', 'Dosisda__Champion_Of_The_White', 'Babbage_Trevil', 'Zephyr', 'Artificial_Network_Defense_Device', 'Sloucher', 'Bloodscar', 'Stryker_Christian', 'Yagers', 'Amaranth_Knotley', 'Dulzrocres__The_Mysterious_One', 'Cryer', 'Adeis__The_Jealous_One', 'Godfrey_Periculum', 'Dissolver', 'Cannibal', 'The_Unheard_Flame', 'Drizzler', 'The_Falling_Hawk', 'Egn', 'Gage', 'Rosebill', 'Marshfeathers', 'Tickler', 'Karayan_Ash', 'The_Hidden_Mime']
    return names[:n]

def gen_prob(n):
    constraints = []
    seen = []
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if i == j or j == k or i == k:
                    continue
                if (k > i and k < j) or (k > j and k < i):
                    continue
                tuples = (i,j),(j,i),(j,k),(k,j),(i,k),(k,i)
                duplicate = any([t in seen for t in tuples])
                if not duplicate:
                    constraints.append((i,j,k))
                    constraints.append((j,i,k))
                    seen += list(tuples)
    return constraints

for n in nums:
    name = fname.format(n)
    f = open(name, 'w')
    f.write(str(n) + '\n')
    wizard_names = gen_names(n)
    name_str = ' '.join(wizard_names)
    f.write(name_str + '\n')
    constraints = gen_prob(n)
    random.shuffle(constraints)
    constraints = constraints[:500]
    f.write(str(len(constraints)) + '\n')
    for constraint in constraints:
        i, j, k = constraint
        n1, n2, n3 = wizard_names[i], wizard_names[j], wizard_names[k]
        constraint_str = n1 + ' ' + n2 + ' ' + n3
        f.write(constraint_str + '\n')
    f.close()
