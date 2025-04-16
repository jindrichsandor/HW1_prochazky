##### Knihovny #####
import math
import numpy as np
import random as rand
import time
import os # zmena pracovniho adresare; vytvoreni slozky pro ukladani dat

##### Nastaveni simulace #####
d=1 # velikost kroku
N=10000 # pocet nezavislych nahodnych prochazek (pro kazdy pocet kroku n), ktery chceme nasimulovat
grid=1 # vyber gridu: 1 = ctvercova mrizka, 2 = trojuhelnikova mrizka, 3 = hexagonalni mrizka
n_list=[i+1 for i in range(0,50)]

### -------------------- ###
### Nastaveni, pro ktere jsem simuloval vystup k odevzdani
#grid=1
#n_list=[i+1 for i in range(0,84)] 

#grid=2
#n_list=[i+1 for i in range(0,56)] 

#grid=3
#n_list=[i+1 for i in range(0,111)] 
### -------------------- ###

save_folder="data" # nazev slozky, do ktere se budou ukladat data ze simulace


##### Definice funkci - nahodne prochazky bez prekrizeni ##### 
### N.B.: prvni krok vzdy provadime do libovolneho smeru; pri vyberu dalsich kroku automaticky z nahodneho vyberu vyrazujeme kroky, ktere by nas navratili do predchozi pozice
### Ctvercova mrizka (4 mozne smery)
def RandomWalk_SelfAvoiding_SquareGrid(n,d):
    nx,ny = 0,0
    path=[[0,0] for i in range(n+1)] # tabulka pro zaznam trajektorie, pro n kroku potrebujeme tabulku velikosti n+1 (kvuli zahrnuti pocatku)
    
    dir=rand.randint(1,4)
    for i in range (1,n+1):
        if dir == 1:
            nx += 1 
            dir = rand.choice([1,2,4])
        elif dir == 2:
            ny += 1
            dir = rand.choice([1,2,3])
        elif dir == 3:
            nx -= 1
            dir = rand.choice([2,3,4])
        elif dir == 4:
            ny -= 1
            dir = rand.choice([1,3,4])  
        path[i]=[nx,ny] # ulozeni nove polohy do tabulky

    return path # funkce vrati trajektorii

### Trojuhelnikova mrizka (6 moznych smeru)
def RandomWalk_SelfAvoiding_TriangularGrid(n,d):    
    nx, ny = 0,0
    path=[[0,0] for i in range(n+1)] # tabulka pro zaznam trajektorie, pro n kroku potrebujeme tabulku velikosti n+1 (kvuli zahrnuti pocatku)
    
    dir=rand.randint(1,6)
    for i in range (1,n+1):
        if dir == 1:
            nx += 1
            ny += 1 
            dir = rand.choice([1,2,3,5,6])
        elif dir == 2:
            ny += 2
            dir = rand.choice([1,2,3,4,6])
        elif dir == 3:
            nx -= 1
            ny += 1
            dir = rand.choice([1,2,3,4,5])
        elif dir == 4:
            nx -= 1
            ny -= 1
            dir = rand.choice([2,3,4,5,6])
        elif dir == 5:
            ny -= 2 
            dir = rand.choice([1,3,4,5,6])
        elif dir == 6:
            nx += 1
            ny -= 1
            dir = rand.choice([1,2,4,5,6])
        path[i]=[nx,ny] # ulozeni nove polohy do tabulky
    
    return path # funkce vrati trajektorii

### Hexagonalni mrizka (3 mozne smery, 2 podmrize)
def RandomWalk_SelfAvoiding_HexagonalGrid(n,d):  
    nx, ny = 0,0
    path=[[0,0] for i in range(n+1)] # tabulka pro zaznam trajektorie, pro n kroku potrebujeme tabulku velikosti n+1 (kvuli zahrnuti pocatku)
    
    dir=rand.randint(1,3)
    for i in range (1,n+1):
        if i%2==1: # cislujeme od jednicky, tak i=1,3,5,... odpovida lichemu kroku
            if dir == 1:
                nx += 1
                ny += 1 
                dir = rand.choice([1,3])
            elif dir == 2:
                nx -= 1
                ny += 1 
                dir = rand.choice([1,2])
            elif dir == 3:
                ny -= 2 
                dir = rand.choice([2,3])
        else:
            if dir == 1:
                ny += 2   
                dir = rand.choice([1,2])
            elif dir == 2:
                nx -= 1
                ny -= 1 
                dir = rand.choice([2,3])
            elif dir == 3:
                nx += 1   
                ny -= 1 
                dir = rand.choice([1,3])
        path[i]=[nx,ny] # ulozeni nove polohy do tabulky
    
    return path # funkce vrati trajektorii

##### Funkce pro statisticke zpracovani - vypocet prumerne vzdalenosti od pocatku a smerodatne odchylky sigma ##### 
def MeanAndStdDeviation(SampleData): 
    N=len(SampleData)
    
    R_Mean=np.sum(SampleData)/N # prumerna vzdalenost od pocatu
    x2=np.sum(np.square(SampleData))/N
    sigma=np.sqrt(x2-R_Mean**2) # smerodatna odchylka
    
    return [float(R_Mean),float(sigma)]

##### Funkce pro urceni toho, zda doslo k prekrizeni
def PathIntersectionTest(path):
    n=len(path)
    path_sorted=path.copy()    
    path_sorted.sort()  # serazeni tabulky; 
    # N.B.: format tabulky je [[nx,ny],....]
    # 1) jednotliva pole se v tabulce se seradi od nejmensiho nx po nejvetsi nx, 
    # 2) pokud maji pole stejne hodnoty nx, tak se seradi od nejmensiho ny po nejvtsi ny
    # z toho plyne, ze pokud v tabulce existuji pole, ktere maji shodne souradnice nx, ny (tzn. doslo k prekrizeni), budou tyto pole serazeny za sebou 
    
    test_var=path_sorted[0] # testovaci pole
    
    intersection=False # promenna s informaci, zda doslo k prekrizeni
    for i in range(1,n): # cyklus, ktery projde jednotlive prvky tabulky a zjisti, zda doslo k prekrizeni
        if test_var==path_sorted[i]:  # srovnani souradnic dvou po sobe jdoucich poli
            intersection=True  # doslo k prekrizeni
            break
        else: test_var=path_sorted[i] # pokud nedoslo k prekrizeni, zmen testovaci pole na nadchazejici pole v tabulce
        
    return intersection # vrati True nebo False podle toho, zda doslo ci nedoslo k prekrizeni




##### Zmena pracovniho adresare a vytvoreni souboru pro ukladani dat #####
file_directory=os.path.dirname(os.path.abspath(__file__)) # absolutni cesta k adresari obsahujici python skript
os.chdir(file_directory) # zmena pracovniho adresare

# vytvoreni slozky pro ukladani dat (pokud jiz neexistuje)
if os.path.exists(save_folder)==False:
    os.mkdir(save_folder)
    
# Vytvoreni souboru pro ukladani vysledku #####
if grid == 1: file_name=save_folder+"/3_BezPrekrizeni_CtvercovyGrid.dat"
elif grid == 2: file_name=save_folder+"/3_BezPrekrizeni_TrojuhelnikovyGrid.dat"
elif grid == 3: file_name=save_folder+"/3_BezPrekrizeni_HexGrid.dat"
result_file=open(file_name, "w")
result_file.write("n    R   sigma N_total   N_success  N_success/N_total   time(s) \n")
result_file.close()

# vytvoreni log souboru
if grid == 1: log_file_name=save_folder+"/3_BezPrekrizeni_CtvercovyGrid_log.dat"
elif grid == 2: log_file_name=save_folder+"/3_BezPrekrizeni_TrojuhelnikovyGrid_log.dat"
elif grid == 3: log_file_name=save_folder+"/3_BezPrekrizeni_HexGrid_log.dat"
log_file=open(log_file_name, "w")
log_file.write("N = " + str(N) + " ; pocet vygenerovanych nezavislych nahodnych prochazek pro kazde n\n")
log_file.close()

 
##### Simulace #####
start_time = time.time() # zaznam casu spusteni behu simulace

R_list=[0]*N # pomocna promenna - seznam pro ukladani euklidovskych vzdalenosti jednotlivych prochazek

for i in range (len(n_list)): # cyklus pres pocty kroku
    t0=time.time()
    n=n_list[i]
    N_total,N_success = 0,0 # celkovy vygenerovanych prochazek, celkovy pocet prochazek bez prekrizeni

    while N_success < N: # simuluj prochazky dokud  pocet prochazek bez prekrizeni je N, tj. N_success=N
        # vygenerovani trajektorie prochazky
        if grid == 1: path = RandomWalk_SelfAvoiding_SquareGrid(n,d) # prochazka na ctvercove mrizce
        elif grid == 2: path = RandomWalk_SelfAvoiding_TriangularGrid(n,d) # prochazka na trojuhelnikove mrizce
        elif grid == 3: path = RandomWalk_SelfAvoiding_HexagonalGrid(n,d) # prochazka na hexagonalni mrizce

        if PathIntersectionTest(path) == False:  # pokud nedoslo k prekrizeni
            # vypocet euklidovske vzdalenosti
            if grid == 1: R_list[N_success]=d*math.sqrt(path[-1][0]**2 + path[-1][1]**2)
            elif grid == 2: R_list[N_success]=d*math.sqrt(3*path[-1][0]**2+path[-1][1]**2)/2
            elif grid == 3: R_list[N_success]=d*math.sqrt(3*path[-1][0]**2+path[-1][1]**2)/2
            N_success+=1  

        N_total+=1
        
    t1=time.time()
    
    temp=MeanAndStdDeviation(R_list)
    result_file=open(file_name,"a")
    result_file.write(str(n) + "    " + str(temp[0]) + "    " + str(temp[1]) + "   " + str(N_total) + "  " +str(N_success) + "   " + str(N_success/N_total) + "  " + str(t1-t0) + "\n")
    result_file.close()      


end_time = time.time() # zaznam casu ukonceni behu simulace

# doplneni udaje o celkovem casu trvani simulace do log souboru
log_file=open(log_file_name, "a")
log_file.write("t = " + str(end_time-start_time) + " s ; celkovy cas behu programu\n")
log_file.close()