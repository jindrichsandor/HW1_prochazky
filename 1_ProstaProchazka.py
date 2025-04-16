##### Knihovny #####
import math
import numpy as np
import random as rand
import time
import os # zmena pracovniho adresare; vytvoreni slozky pro ukladani dat

##### Nastaveni simulace #####
d=1 # velikost kroku
N=50000 # pocet nezavislych nahodnych prochazek (pro kazdy pocet kroku n), ktery chceme nasimulovat
grid=1 # vyber gridu: 1 = ctvercova mrizka, 2 = trojuhelnikova mrizka, 3 = hexagonalni mrizka

# pole s pocty kroku, pro ktere chceme provest simulaci
n_list=[i+1 for i in range(0,100)] 
n_list.extend([100+(i+1)*10 for i in range (0,90)])
n_list.extend([1000+(i+1)*100 for i in range (0,90)])


save_folder="data" # nazev slozky, do ktere se budou ukladat data ze simulace


##### Definice funkci - proste nahodne prochazky ##### 
### N.B.: v pripade proste nahodne prochazky nezavisi na poradi jednotlivych kroku, takze vsechny kroky muzeme vygenerovat soucasne
### Ctvercova mrizka (4 mozne smery)
def RandomWalk_Simple_SquareGrid(n,d):
    walk=rand.choices([1,2,3,4],k=n) # vygenerovani seznamu nahodnych cisel 1,2,3,4; delka seznamu=n

    n1=walk.count(1) # pocet kroku ve smeru "1" odpovida poctu nahodne vygenerovanych cislic "1" v seznamu
    n2=walk.count(2) # pocet kroku ve smeru "2"
    n3=walk.count(3) # pocet kroku ve smeru "3"
    n4=walk.count(4) # pocet kroku ve smeru "4"
    
    nx=n1-n3
    ny=n2-n4
    
    return d*math.sqrt(nx**2+ny**2) # funkce vraci euklidovskou vzdalenost od pocatku

### Trojuhelnikova mrizka (6 moznych smeru)
def RandomWalk_Simple_TriangularGrid(n,d):
    walk=rand.choices([1,2,3,4,5,6],k=n)
    # pocty kroku ve smerech 1,2,3,4,5,6
    n1=walk.count(1)
    n2=walk.count(2)
    n3=walk.count(3)
    n4=walk.count(4)
    n5=walk.count(5)
    n6=walk.count(6)
    
    nx=n1-n3-n4+n6
    ny=n1+2*n2+n3-n4-2*n5-n6
    
    return d*math.sqrt(3*nx**2+ny**2)/2 # euklidovska vzdalenost od pocatku

### Hexagonalni mrizka (3 mozne smery, 2 podmrize)
def RandomWalk_Simple_HexagonalGrid(n,d):  
    # Hexagonalni mrizka je slozena ze dvou podmrizi -> toto je nutne pri prochazce zohlednit
    if n%2==0: # pripad sudeho poctu kroku -> na kazde podmrizi vykoname stejny pocet (=n/2) kroku
        walk_subgrid1=rand.choices([1,2,3],k=int(n/2))
        walk_subgrid2=rand.choices([1,2,3],k=int(n/2))
    else: # pripad licheho poctu kroku
        walk_subgrid1=rand.choices([1,2,3],k=int((n+1)/2)) # na prvni podmrizi vykoname n+1 kroku
        walk_subgrid2=rand.choices([1,2,3],k=int((n-1)/2)) # na druhe podmrizi vykoname n-1 kroku
    
    # pocty kroku ve smerech 1,2,3 vykonanych na prvni podmrizi
    n1=walk_subgrid1.count(1)
    n2=walk_subgrid1.count(2)
    n3=walk_subgrid1.count(3)
    # pocty kroku ve smerech 1,2,3 vykonanych na druhe podmrizi
    m1=walk_subgrid2.count(1)
    m2=walk_subgrid2.count(2)
    m3=walk_subgrid2.count(3)
    
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
    if grid == 1: R_list=[RandomWalk_Simple_SquareGrid(n_list[i],d) for _ in range(N)]  # prochazka na ctvercove mrizce
    elif grid == 2: R_list=[RandomWalk_Simple_TriangularGrid(n_list[i],d) for _ in range(N)] 
    elif grid == 3:  R_list=[RandomWalk_Simple_HexagonalGrid(n_list[i],d) for _ in range(N)] # prochazka na hexagonalni mrizce
    
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
if grid == 1: file_name=save_folder+"/1_ProstaProchazka_CtvercovyGrid.dat"
elif grid == 2: file_name=save_folder+"/1_ProstaProchazka_TrojuhelnikovyGrid.dat"
elif grid == 3: file_name=save_folder+"/1_ProstaProchazka_HexGrid.dat"
np.savetxt(file_name,result,fmt="%1.30s",delimiter="  ", header="n R sigma", comments="")

# Ulozeni logu ze simulace do datoveho souboru #####
if grid == 1: file_name=save_folder+"/1_ProstaProchazka_CtvercovyGrid_log.dat"
elif grid == 2: file_name=save_folder+"/1_ProstaProchazka_TrojuhelnikovyGrid_log.dat"
elif grid == 3: file_name=save_folder+"/1_ProstaProchazka_HexGrid_log.dat"
log_file=open(file_name, "w")
log_file.write("N = " + str(N) + " ; pocet vygenerovanych nezavislych nahodnych prochazek pro kazde n\n")
log_file.write("t = " + str(end_time-start_time) + " s ; celkovy cas behu programu\n")
log_file.close()
