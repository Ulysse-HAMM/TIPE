# Créé par erwan, le 19/04/2023 en Python 3.7
from random import randint
def printt (tab):
    """pour les tests"""
    for i in tab :
        print(i)
def crea_billes (nb,longueur,largeur,L=[]):
    """
    Crée une liste de nb billes reparties dans longueur en x ,largeur en y
    Attention: Appel récursif pour crée nb-1 bille (taille de L majorée par nb et croissante à chaque appel)
    ------------
    Entrée :
        Attention: ne pas demamder de placer plus de billes qu'il n'y a de place sinon: tourne en boucle
        nb le nombre de billes à créer,
        Longueur et largeur du tableau utilisé
        Liste des billes (initialement vide)
    Sortie :
        R la liste des nb billes (non confondues) (triées ?)
    Exemples :
        crea_billes (4,4,4)
        >>>[[1, 1], [1, 2], [2, 1], [2, 2]]
        4 billes dans la matrice [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        Elles sont forcées d'etre au milieu
    """
    if nb==0: #Si on demande 0 billes balec
        return []
    if len(L)==0:    #Si aucune bille n'est crée on en fait une sans conditions
        return crea_billes(nb,longueur,largeur,[[randint(1,largeur-2),randint(1,longueur-2)]])
    if len(L)==nb:
        return L

    deja=True
    while deja==True:   #Boucle qui tire au hasard une bille qui n'existe pas déjà
        a=randint(1,largeur-2)
        b=randint(1,longueur-2)
        deja=False
        for i in L :
            if [a,b]==i:
                deja=True

    R=[]

    for i in range (len(L)):
        R.append(L[i])
    R.append([a,b])
    if len(R)==nb:
        return R
    else:
        R=crea_billes(nb,longueur,largeur,R)
        return R
def deplacement_unitaire (billes,rayon):
    """
    Déplace d'une case ou
    ----------
    Entrée:
        la position des billes: liste type[[a1,b1],[a2,b2],...]
        la position actuelle: type [x,y,[movx,movy]]
    Sortie:
        Prochaine position si pas de pb (juste tourner de 90° est un deplacement)
        0 si absorption
    """
    x=rayon[0]
    y=rayon[1]
    movx,movy=rayon[2]
    if appartient([x+movx,y+movy],billes): #cas d'bsorption
        return 0
    if movx==0: #cas de déviation 1
        if appartient([x+1,y+movy],billes):
            return [x,y,[-1,0]]
        elif appartient([x-1,y+movy],billes):
            return [x,y,[1,0]]
    elif movy==0: #cas de déviation 2
        if appartient([x+movx,y+1],billes):
            return [x,y,[0,-1]]
        elif appartient([x+movx,y-1],billes):
            return [x,y,[0,1]]

    return [x+movx,y+movy,[movx,movy]]  #cas de déplacement sans gène
def deplacement (entree,billes,longueur,largeur):
    """
    Permet de rendre la sortie d'un rayon sachant l'entree
    -------
    Entree:
        entree :type [x,y,[movx,movy]]
        billes :[[a1,b1],[a2,b2],...]
        longueur,largeur du terrain
    Sortie :
        [x,y,[deplacement x,deplacement y]] si sortie effective
        1 si reflexion en bord de boite ou demi tour (sortie a la meme case qu'entree)
        0 si absorption
    """
    pos0=entree
    pos=deplacement_unitaire(billes,pos0)
    if pos==0 :
        return 0
    if pos[0]==0 or pos[0]==largeur-1 or pos[1]==0 or pos[1]==longueur-1 :  #Cas de reflexion en bord de boite : apres 1 coup on est tjr pas entré
        return 1
    while pos!=0 and pos[0]!=0 and pos[0]!=largeur-1 and pos[1]!=0 and pos[1]!=longueur-1 : #tant qu'on est pas sorti ou absorbé on se deplace
        pos=deplacement_unitaire(billes,pos)

    if pos!=0 and pos[:2]==pos0[:2]: #Si la sortie vaut l'entree c'est une reflexion
        return 1
    return pos   #Sinon on retourne juste la sortie
def appartient (elt,liste):
    """
    Teste une appartenance de elt dans la liste
    """
    for elts in liste :
        if elts==elt:
            return True
    return False
def ajout (liste1,liste2):
    """
    Fonction permettant de socker liste2 dans liste1 sans impact (genre pb de mémoire et tt)
    --------
    Entree:
        liste1 [[...],[...]]
        liste2:[...]
    Sortie:
        [[...],[...],[...]]
    """

    if liste2!=0:
        liste1.append([])
        for elt in liste2:
            if type(elt)!=list :
                liste1[-1].append(elt)
            else:
                ajout(liste1[-1],elt)
def billepossible(bille,dejaclear,longueur,largeur):
    """
    Renvoie True si la bille est possible (cad dans le terrain et pas sur une case deja visitée
    """
    return (not appartient(bille,dejaclear)) and (not(bille[0]<=0 or bille[0]>=largeur-1 or bille[1]<=0 or bille[1]>=longueur-1))
def calculespaces (billes,rayon,dejaclear,sortie,longueur,largeur,nbbilles,demitour=0):
    """
    ATTENTION si reflexion il faut mettre en valeur de "sortie" la position de la reflexion
    ---------
    Entrees:
        billes: billes qu'on suppose déjà placées
        rayon: position actuelle
        dejaclear: les cases par lesquelles on est déja passé (des billes ne peuvent par conséquent pas être placées ici)
        sortie: la vraie sortie qu'on a eu
        longueur,largeur du terrain comme d'hab
        nbbilles: le nombre de billes qu'il ne faut pas dépasser
        demitour: vaut 1 si la sortie vaut 1 cad qu'on a fait un demitour (car on ne peut pas mettre 1 dans la valeur sortie car on oublierai la valeur de l'ntree dans les appels récursifs)
    Sortie :
        0 si mauvaise sortie/ cas impossible
        L la liste des différents cas possibles :
            format L=[cas1,cas2,...]
            avec
            cas=[[billes du cas],[cases où il ne peut y avoir de billes]]
    """
    #Cas de bases :Sortie ou utilisation de toutes les billes.
    if rayon==0 or rayon[0]==0 or rayon[0]==largeur-1 or rayon[1]==0 or rayon[1]==longueur-1 : #Si on est sorti on regarde si c'est la bonne sortie

        if rayon==sortie :
            return [[billes,dejaclear]]
        else :
            return 0
    if nbbilles == len(billes): #Si on a déjà fait une suppostion qui utilise toutes les billes, on continue jusqu'au bout et voit si on est bon.
        while rayon!=0 and rayon[0]!=0 and rayon[0]!=largeur-1 and rayon[1]!=0 and rayon[1]!=longueur-1 : #tant qu'on est pas sorti ou absorbé on se deplace et on ajoute à la liste dejaclear
            x,y,[movx,movy]=rayon
            if movx==0:
                dejaclear+=[x,y+movy],[x+1,y+movy],[x-1,y+movy]
            else:
                dejaclear+=[x+movx,y],[x+movx,y+1],[x+movx,y-1]
            rayon=deplacement_unitaire(billes,rayon)

        if rayon == sortie:
            if sortie==0:   #si la sortie est une absorption on a enfait pas dejaclear ces 2 cases
                dejaclear.pop(-1)
                dejaclear.pop(-1)
            return [[billes,dejaclear]]
        else:
            return 0


    #Récursif :
    #Si on est pas sorti on va faire les 4 suppositions : une a gauche, une a droite,une en face (si sortie= absorption) ou rien
    L=[]  #Liste des différents univers
    x,y,[movx,movy]=rayon

    """
    Ordre des if :
        Si en face (seulement dans le cas d'une sortie absorption)
        Si sur les cotes (cas ou on bouge selon y)
        Si sur les cotes (cas ou on bouge selon x)
        Si rien du tout

    """
    if sortie==0 and billepossible([x+movx,y+movy],dejaclear,longueur,largeur):
        ajout(L,[billes+[[x+movx,y+movy]],dejaclear+[[x+movx,y+movy]]])

    #on compte ici si la bille gauche(+1) et droite(+1) sont possibles (et si il y a bien eu demitour +1)
    #les tests gauche et droite sont faits plus tard pour éviter les répétitions
    if demitour==1:
        demitourpossible=1
    else:
        demitourpossible=0

    #Si le deplacement est vertical (on ne bouge pas selon x)
    if movx==0 :
        #Si la nouvelle bille est à gauche
        nouvbille=[x+1,y+movy]
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que la bille qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour)
            if cas!=0: #si ce n'est pas un cas impossible
                for elt in cas:
                    ajout(L,elt)

            billes.pop(-1)  #on enlève la supposition qu'on vient de faire
            demitourpossible+=1 #et on ajoute 1 ici car la bille de gauche etait possible

        #Si à droite
        nouvbille=[x-1,y+movy]
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour) #Attention ici on a ajouté le cas de la bille gauche dans déjà fait car las cas où les 2 existent est deja fait
            if cas!=0:
                for elt in cas:
                    ajout(L,elt)
            billes.pop(-1)
            demitourpossible+=1
        #cas où il ne se passe rien (ni gauche ni droite)
        cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour)
        if cas!=0:
                for elt in cas:
                    ajout(L,elt)
        #enfin si toutes les conditions du demi tour sont remplies on ajoute ce cas
        if demitourpossible==3:
            bille1=[x+1,y+movy]
            bille2=[x-1,y+movy]
            if billepossible(bille1,dejaclear,longueur,largeur) and billepossible(bille2,dejaclear,longueur,largeur)and len(billes)<nbbilles-1:
                ajout(L,[billes+[bille1,bille2],dejaclear+[[x,y+movy],bille1,bille2]])

    #exactement pareil mais pour un deplacement horizontal
    else : #movy=0
        nouvbille=[x+movx,y+1]      #Si la nouvelle bille est à gauche
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles,demitour)

            if cas!=0:
                for elt in cas:
                    ajout(L,elt)
            billes.pop(-1)
            demitourpossible+=1

        nouvbille=[x+movx,y-1]
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles,demitour) #Attention ici on a ajouté le cas de la bille gauche dans déjà fait car las cas où les 2 existent est deja fait
            if cas!=0:
                for elt in cas:
                    ajout(L,elt)

            billes.pop(-1)
            demitourpossible+=1

        cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles,demitour)
        if cas!=0:
                for elt in cas:
                    ajout(L,elt)

        if demitourpossible==3 :
            bille1=[x+movx,y+1]
            bille2=[x+movx,y-1]
            if billepossible(bille1,dejaclear,longueur,largeur) and billepossible(bille2,dejaclear,longueur,largeur) and len(billes)<nbbilles-1:
                ajout(L,[billes+[bille1,bille2],dejaclear+[[x+movx,y],bille1,bille2]])
    #Si la liste est toujours vide cela veut dire que tous les cas sont impossibles.
    if L==[]:
        L=0
    return L
def selection_aleatoire (univers,liste_coups,entreespossibles):
    """
    C'est cette fonction qui détermine où tirer lorque l'on sait un univers pour l'instant elle est en aléatoire
    """
    a=randint(0,3) # a représente le côté d'entree (N,S,O,E)
    i=0 # variable qui fait crash si on est dans un while infini
    if entreespossibles==[[],[],[],[]]:
        #normalement on entre pas ici c'est juste pour eviter un while infini en faisant crash (pour les tests)
        print(houla_ya_un_probleme)

    while entreespossibles[a]==[] and i<100:
        a=randint(0,3)
        i+=1
    if i==100:
        print(bloblabla)

    #On choisi une entree parmi celles qui sont possibles(qui n'ont pas ete supprimees de entreepossibles)
    if a==0 or a==1:
        x=randint(0,len(entreespossibles[a])-1)
    else:
        x=randint(0,len(entreespossibles[a])-1)
    """
    LA SUITE EST A SUPPRIMER (enfin si tout marche sans lui)
    il faut juste mettre un

    return entreepossible[a][x]

    liste_entrees=[]
    for i in liste_coups:
        liste_entrees.append(i[0])

    test=entreespossibles[a][x]
    if appartient(test,liste_entrees):
        return selection(univers,liste_coups,entreespossibles)
    else:"""
    test=entreespossibles[a][x]
    entreespossibles[a].pop(x)
    return test
def supprimerlesdoubles(liste):
    """
    Supprime les doubles d'une liste
    on traverse la liste à l'envers pour ne pas modifier des positions de doubles en supprimant les éléments au début.
    """
    for i in range (len(liste)-1,-1,-1):
        if appartient(liste[i],liste[:i]):
            liste.pop(i)
def billeplusgrande (elt1,elt2):
    """
    compare si un elt1 est plus grand qu'un elt2 au sens alphabétique
    format: elt_=[a,b]
    """
    x1,y1=elt1
    x2,y2=elt2
    if x1>x2:
        return True
    elif x1<x2:
        return False
    else:
        if y1>=y2:
            return True
        else:
            return False

def nettoyer(liste,longueur,largeur):
    """
    Trie la liste sur la base du tri bulle (flemme de faire un des algos relou à implémenter)
    et supprime tous les elements en double ou inutiles car en dehors de boite

    Fonction utile pour nettoyer tout le monde et vérifier si 2 listes sont egales plus facilement
    """

    supprimerlesdoubles(liste)
    n=len(liste)

    for i in range (n-1,-1,-1):
        mini=i

        for j in range (0,i+1):
            if not(billeplusgrande(liste[j],liste[mini])):
                mini=j
        if not(0<liste[mini][0]<largeur-1 and 0<liste[mini][1]<longueur-1) :
            liste.pop(mini)
        else:
            liste[mini],liste[i]=liste[i],liste[mini]
def BOB (nbbilles,longueur,largeur,billesréelles,strategie):
    """
    BOB est notre joueur qui calcule toutes les possibilités et s'arrete dés qu'il trouve une unicité des cas possibles (qui comportent le bon nb de billes)
    pour l'instant il marche pour 1 et 2 billes à 100% du temps et dans quelques modifs (qu'on sait deja commment les implementer) il marcher pour 3 et 4
    Cependant vu qu'on ne peut pas toujours trouver toutes les billes à partir de >4,on lui fera return les différentes cases qui sont possibles (pour les billes toujours inconnues)
    -----
    Entrées :
        nbbilles: le nombre de billes qu'il doit trouver
        longueur,largeur du terrain
        billesréelles: la position des vraies billes (evidemment on les retourne pas elles memes mais on en a besoin pour avoir la sortie effective à partir d'une entree)
        strategie:la strategie employee
    Sorties :
        la position des billes trouvées

    """
    liste_coups=[] #Normalement on devrait pouvoir s'en passer mtn
    liste_des_univers=[] #liste de tous les cas (univers) possibles

    entreespossibles=[[],[],[],[]]
    for i in range (1,longueur-1):
        entreespossibles[0].append([0,i,[1,0]])
        entreespossibles[1].append([largeur-1,i,[-1,0]])
    for j in range (1,largeur-1):
        entreespossibles[2].append([j,0,[0,1]])
        entreespossibles[3].append([j,longueur-1,[0,-1]])
    #print('entree :',entreespossibles)
    #On initialise la liste des entrees possibles dont les elements seront supprimés dès qu'on a testé l'entree



    ###coup initial:(à part car il evite des tests de coup initial dans le cas général pour les cas particuliers)
    moyenne=0 #inutile
    entree=strategie(moyenne,liste_coups,entreespossibles)
    sortie=deplacement(entree,billesréelles,longueur,largeur)

    x,y,[movx,movy]=entree
    ajout(liste_coups,[entree,sortie])
    #print('coup:',liste_coups[-1])
    depart=[]  #Met dans dejafait les premiéres cases environnantes. Opération obligatoire on va appliquer calculespaces sur le rayon qui est deja entré dans la boite les cas de reflexion en bord de boite sont traités a part.
    for i in range (-1,2):
        for j in  range (-1,2):
            depart.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave elles seront nettoyées plus tard

    if sortie==0:
        cas=calculespaces([],deplacement_unitaire([],entree),depart,sortie,longueur,largeur,nbbilles)
        if cas !=0:
            for elt in cas:
                ajout(liste_des_univers,elt)
        ajout(liste_des_univers,[[[x+movx,y+movy]],[[x+movx,y+movy]]]) #cas à part si c'est la bille en tout premier qui fait une telle sortie

    elif sortie==1:

        #cas de sortie=entree
        cas=calculespaces([],deplacement_unitaire([],entree),depart,[x,y,[-movx,-movy]],longueur,largeur,nbbilles,1)
        if cas !=0:
            for elt in cas:
                ajout(liste_des_univers,elt)

        #Cas de reflexion en bord de boite
        comptage=0   #si une bille a gauche et une bille a droite sont possibles alors les 2 ensembre le sont aussi
        for i in range(-1,3,2):
            for j in range (-1,3,2):
                if 0<x+i<largeur-1 and 0<y+j<longueur-1 : #contrairement a depart on ne veut surtout pas compter de billes en dehors du plateau
                    ajout(liste_des_univers,[[[x+i,y+j]],[[x+i,y+j],[x+movx,y+movy]]])
                    comptage+=1
        if comptage==2 and nbbilles>1:
            ajout(liste_des_univers,[liste_des_univers[-1][0]+liste_des_univers[-2][0],liste_des_univers[-1][1]+[liste_des_univers[-2][1][0]]])

    else :
        for elt in calculespaces([],deplacement_unitaire([],entree),depart,sortie,longueur,largeur,nbbilles):
            ajout(liste_des_univers,elt)
    for elt in liste_des_univers:
        billes,dejafait=elt
        nettoyer(billes,longueur,largeur)
        nettoyer(dejafait,longueur,largeur)






    #cas général
    while (len (liste_des_univers)!=1 or len(liste_des_univers[0][0])!=nbbilles) and len(liste_coups)<2*(longueur+largeur-4):
        #tant qu'on a pas unicité d'une solution valide et qu'on a pas testé toutes les entrées
        entree=strategie(moyenne,liste_coups,entreespossibles)
        """if appartient( [[0, 4, [1, 0]], [1, 6, [0, 1]]],liste_coups):
            entree=selection(moyenne,liste_coups)
        else:
            entree=[0, 4, [1, 0]]"""
        sortie=deplacement(entree,billesréelles,longueur,largeur)

        x,y,[movx,movy]=entree
        ajout(liste_coups,[entree,sortie])
        #print("coup:",liste_coups[-1])


        for cas_traite in range (len(liste_des_univers)-1,-1,-1):
            #Maintenant on va tester chaque cas possible et verifier qu'il correspond avec le nouveau coup qu'on vient de jouer et si c'est bien le cas on ajoute a listedesunivers tous les nouveaux cas possibles.


            #print(liste_des_univers)
            #print(cas_traite)
            billes,dejafait=liste_des_univers[cas_traite]
            nouveaux_cas=[]
            """nettoyer(billes,longueur,largeur) #Il faut deplacer ca plus loin mais ca implique pas mal de modifs à faire plus tard...
            nettoyer(dejafait,longueur,largeur)"""

            depart=[] #Les cases qui sont deja analysées par le départ
            for i in range (-1,2):
                for j in  range (-1,2):
                    depart.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave c'est des cases en dehors du terrain
            #print('ok1')


            #Si il n'y a aucune des billes autour du départ (cela induirait une contradiction et un  cas impossible)
            test0=False #Test si la sortie devrait etre 0
            test1=False #Test si la sortie devrait etre 1
            for i in range (-1,2):
                for j in range (-1,2):
                    if appartient([x+i,y+j],billes) and (i==0 or j==0):
                        test0=True
                    elif appartient([x+i,y+j],billes):
                        test1=True

            if test0 and sortie==0:
                ajout(liste_des_univers,liste_des_univers[cas_traite])
            if (not test0) and test1 and sortie==1:
                ajout(liste_des_univers,liste_des_univers[cas_traite])
            if test1 and sortie==0 and len(billes)<nbbilles:
                ajout(liste_des_univers,[billes+[[x+movx,y+movy]],dejafait+[[x+movx,y+movy]]])


            #Cas des sans problèmes au départ


            if (not test0) and (not test1) and sortie==0:
                cas=calculespaces(billes,deplacement_unitaire([],entree),dejafait+depart,sortie,longueur,largeur,nbbilles)
                if cas !=0:
                    for elt in cas:
                        ajout(nouveaux_cas,elt)
                if appartient([x+movx,y+movy],billes):
                    ajout(nouveaux_cas,[billes,dejafait])
                if billepossible([x+movx,y+movy],dejafait,longueur,largeur) and len(billes)<nbbilles:
                    ajout(nouveaux_cas,[billes+[[x+movx,y+movy]],dejafait+[[x+movx,y+movy]]]) #cas à part si c'est la bille en tout premier qui fait bugger

            elif (not test0) and (not test1) and sortie==1:
                #cas de sortie=entree

                cas=calculespaces(billes,deplacement_unitaire([],entree),dejafait+depart,[x,y,[-movx,-movy]],longueur,largeur,nbbilles,1)
                if cas !=0:
                    for elt in cas:
                        ajout(nouveaux_cas,elt)
                #Cas de reflexion en bord de boite
                if len(billes)<nbbilles: #Si on peut en rajouter une nouvelle
                    comptage1=0   #si une bille a gauche et une bille a droite sont possibles alors les 2 ensembre le sont aussi
                    comptage2=0
                    for i in range(-1,3,2):
                        for j in range (-1,3,2):
                            if billepossible([x+i,y+j],dejafait,longueur,largeur) : #contrairement a depart on ne veut surtout pas compter de billes en dehors du plateau
                                ajout(nouveaux_cas,[billes+[[x+i,y+j]],dejafait+[[x+movx,y+movy],[x+i,y+j]]])
                                comptage1+=1
                            if appartient([x+i,y+j],billes):
                                ajout(nouveaux_cas,[billes,dejafait+[[x+movx,y+movy]]])
                                comptage2+=1
                    if comptage1==2 and len(billes)<nbbilles-1:
                        ajout(nouveaux_cas,[billes+[nouveaux_cas[-1][0][-1]]+[nouveaux_cas[-2][0][-1]] , dejafait+[[x+movx,y+movy]]])
                    if comptage2==2:
                        ajout(nouveaux_cas,[billes,dejafait+[[x+movx,y+movy]]])
            elif (not test0) and (not test1) :
                #print('ok2')
                cas=calculespaces(billes,deplacement_unitaire([],entree),dejafait+depart,sortie,longueur,largeur,nbbilles)
                #print('ok3')
                if cas!=0:
                    for elt in cas:
                        ajout(nouveaux_cas,elt)
            #print(cas)
            #print(nouveaux_cas)
            if nouveaux_cas !=[]:
                for elt in nouveaux_cas:
                    billes,dejafait=elt
                    nettoyer(billes,longueur,largeur)
                    nettoyer(dejafait,longueur,largeur)
                    ajout(liste_des_univers,elt)


            liste_des_univers.pop(cas_traite)
            #print("ok2",liste_des_univers)
        supprimerlesdoubles(liste_des_univers)
        #print("fini",liste_des_univers)


    if len(liste_coups)==2*(longueur+largeur-4):
        if len (liste_des_univers)==1:
            comptage_des_deja_vus=0
            n=0
            sauvegarde=[]
            for i in range (largeur-2,0,-1):
                for j in range (longueur-2,0,-1):
                    if [i,j]==liste_des_univers[0][1][n]:
                        comptage_des_deja_vus+=1
                        sauvegarde.append([i,j])
                    n+=1
            if comptage_des_deja_vus+len(liste_des_univers[0][0])==nbbilles:
                return liste_des_univers[0][0]+sauvegarde ,len(liste_coups)
        return 'stop',liste_des_univers,liste_coups
    return liste_des_univers[0][0],len(liste_coups)

longueur=10
largeur=10
nbbilles=4

tab=[[0 for i in range (longueur)]for j in range (largeur)]
printt(tab)



compteur=0
nombredetests=635376####### Modifie ici pour faire le nb de tests que tu veux
for i in range (nombredetests):
    billes=crea_billes(nbbilles,longueur,largeur)
    #billes=[[3, 4], [5, 3]]
    a,nbcoups=BOB(nbbilles,longueur,largeur,billes,selection_aleatoire)
    print('end of the game',billes,a,nbcoups)
    test=True
    for j in range (nbbilles) :
        if not(appartient(a[j],billes)) or  appartient (a[j],a[:j]):
            test=False
            print(billes)
            print(lets_carsh_psq_ya_un_bug)
    if test:
        compteur+=1
if compteur==nombredetests:
    print("Youpi c'est gagné")