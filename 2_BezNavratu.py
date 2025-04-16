##### Knihovny #####
import math
import numpy as np
import random as rand
import time
import os # zmena pracovniho adresare; vytvoreni slozky pro ukladani dat

##### Nastaveni simulace #####
d=1 # velikost kroku
N=25000 # pocet nezavislych nahodnych prochazek (pro kazdy pocet kroku n), ktery chceme nasimulovat
grid=1 # vyber gridu: 1 = ctvercova mrizka, 2 = trojuhelnikova mrizka, 3 = hexagonalni mrizka

# pole s pocty kroku, pro ktere chceme provest simulaci
n_list=[i+1 for i in range(0,100)] 
n_list.extend([100+(i+1)*10 for i in range (0,90)])
n_list.extend([1000+(i+1)*100 for i in range (0,90)])


save_folder="data" # nazev slozky, do ktere se budou ukladat data ze simulace


##### Definice funkci - nahodne prochazky bez navratu ##### 
### N.B.: prvni krok vzdy provadime do libovolneho smeru; pri vyberu dalsich kroku automaticky z nahodneho vyberu vyrazujeme kroky, ktere by nas navratili do predchozi pozice
### Ctvercova mrizka (4 mozne smery)
def RandomWalk_NoReturn_SquareGrid(n,d):
    n1, n2, n3, n4 = 0,0,0,0 # pocty kroku ve smerech 1,2,3,4
    
    dir=rand.randint(1,4) # prvni krok je do libovolneho smeru (dalsi kroky jiz budou )
    for i in range (n): # cyklus provadejici jednotlive kroky prochazky
        if dir == 1:
            n1 += 1 
            dir = rand.choice([1,2,4]) # dir != 3 (dir = 3 byodpovidalo navratu, proto jsme jej vyradili)
        elif dir == 2:
            n2 += 1
            dir = rand.choice([1,2,3]) # dir != 4
        elif dir == 3:
            n3 += 1
            dir = rand.choice([2,3,4]) # dir != 1
        elif dir == 4:
            n4 += 1
            dir = rand.choice([1,3,4]) # dir != 2
    
    nx=n1-n3
    ny=n2-n4
    
    return d*math.sqrt(nx**2+ny**2) # funkce vraci euklidovskou vzdalenost od pocatku

### Trojuhelnikova mrizka (6 moznych smeru)
def RandomWalk_NoReturn_TriangularGrid(n,d):    
    n1, n2, n3, n4, n5, n6 = 0,0,0,0,0,0 # pocty kroku ve smerech 1,2,3,4,5,6
    
    dir=rand.randint(1,6) # prvni krok je do libovolneho smeru
    for i in range (n): # cyklus provadejici jednotlive kroky prochazky
        if dir == 1:
            n1 += 1 
            dir = rand.choice([1,2,3,5,6]) # dir != 4
        elif dir == 2:
            n2 += 1
            dir = rand.choice([1,2,3,4,6]) # dir != 5
        elif dir == 3:
            n3 += 1
            dir = rand.choice([1,2,3,4,5]) # dir != 6
        elif dir == 4:
            n4 += 1
            dir = rand.choice([2,3,4,5,6]) # dir != 1
        elif dir == 5:
            n5 += 1 
            dir = rand.choice([1,3,4,5,6]) # dir != 2
        elif dir == 6:
            n6 += 1
            dir = rand.choice([1,2,4,5,6]) # dir != 3
    
    nx=n1-n3-n4+n6
    ny=n1+2*n2+n3-n4-2*n5-n6
    
    return d*math.sqrt(3*nx**2+ny**2)/2 # euklidovska vzdalenost od pocatku

### Hexagonalni mrizka (3 mozne smery, 2 podmrize)
def RandomWalk_NoReturn_HexagonalGrid(n,d):  
    n1, n2, n3, m1, m2, m3 = 0,0,0,0,0,0 # pocty kroku ve smerech 1,2,3 na dvou ruznych podmrizich
    
    dir=rand.randint(1,3) # prvni krok je do libovolneho smeru
    for i in range (n): # cyklus provadejici jednotlive kroky prochazky
        if i%2==0: # cislujeme od nuly, tudiz i=0,2,4,... odpovida lichym krokum
            if dir == 1:
                n1 += 1 
                dir = rand.choice([1,3]) # dir != 2
            elif dir == 2:
                n2 += 1
                dir = rand.choice([1,2]) # dir != 3
            elif dir == 3:
                n3 += 1
                dir = rand.choice([2,3]) # dir != 1
        else:
            if dir == 1:
                m1 += 1 
                dir = rand.choice([1,2]) # dir != 3
            elif dir == 2:
                m2 += 1
                dir = rand.choice([2,3]) # dir != 1
            elif dir == 3:
                m3 += 1
                dir = rand.choice([1,3]) # dir != 2
    
    nx=n1-n2-m2+m3
    ny=n1+n2-2*n3+2*m1-m2-m3
    
    return d*math.sqrt(3*nx**2+ny**2)/2 # euklidovska vzdalenost od pocatku

##### Funkce pro statisticke zpracovani - vypocet prumerne vzdalenosti od pocatku a smerodatne odchylky sigma ##### 
def MeanAndStdDeviation(SampleData): 
    N=len(SampleData)
    
    R_Mean=np.sum(SampleData)/N # prumerna vzdalenost od pocatu
    x2=np.sum(np.square(SampleData))/N
    sigma=np.sqrt(x2-R_Mean**2) # smerodatna odchylka
    
    return [float(R_Mean),float(sigma)]

    
##### Simulace ##### 
start_time = time.time() # zaznam casu spusteni behu simulace

result = [[0,0,0] for i in range(len(n_list))] # priprava tabulky pro ukladani vysledku

for i in range (len(n_list)): # cyklus pres pocty kroku
    # vygenerovani N nezavislych nahodnych prochazek
    if grid == 1: R_list=[RandomWalk_NoReturn_SquareGrid(n_list[i],d) for _ in range(N)] # prochazka na ctvercove mrizce
    elif grid == 2:  R_list=[RandomWalk_NoReturn_TriangularGrid(n_list[i],d) for _ in range(N)] # prochazka na trojuhelnikove mrizce
    elif grid == 3: R_list=[RandomWalk_NoReturn_HexagonalGrid(n_list[i],d) for _ in range(N)] # prochazka na hexagonalni mrizce
    
    temp=MeanAndStdDeviation(R_list)
    result[i]=[n_list[i],temp[0],temp[1]] # ulozeni vysledku simulace ve tvaru [pocet kroku, prumerne R od pocatku, sigma]

end_time = time.time() # zaznam casu ukonceni behu simulace


##### Ulozeni dat ze simulace #####
file_directory=os.path.dirname(os.path.abspath(__file__)) # absolutni cesta k adresari obsahujici python skript
os.chdir(file_directory) # zmena pracovniho adresare

# vytvoreni slozky pro ukladani dat (pokud jiz neexistuje)
if os.path.exists(save_folder)==False:
    os.mkdir(save_folder)
    
# Ulozeni vysledku simulace do datoveho souboru #####
if grid == 1: file_name=save_folder+"/2_BezNavratu_CtvercovyGrid.dat"
elif grid == 2: file_name=save_folder+"/2_BezNavratu_TrojuhelnikovyGrid.dat"
elif grid == 3: file_name=save_folder+"/2_BezNavratu_HexGrid.dat"
np.savetxt(file_name,result,fmt="%1.30s",delimiter="  ", header="n R sigma", comments="")

# Ulozeni logu ze simulace do datoveho souboru #####
if grid == 1: file_name=save_folder+"/2_BezNavratu_CtvercovyGrid_log.dat"
elif grid == 2: file_name=save_folder+"/2_BezNavratu_TrojuhelnikovyGrid_log.dat"
elif grid == 3: file_name=save_folder+"/2_BezNavratu_HexGrid_log.dat"
log_file=open(file_name, "w")
log_file.write("N = " + str(N) + " ; pocet vygenerovanych nezavislych nahodnych prochazek pro kazde n\n")
log_file.write("t = " + str(end_time-start_time) + " s ; celkovy cas behu programu\n")
log_file.close()
