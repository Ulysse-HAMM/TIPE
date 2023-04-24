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
    """
    #met les billes dans l'ordre (ordre alphabetique :[[1, 1], [1, 2], [2, 1], [2, 2]])(peut etre pas utile)
    i=0
    while i<len(L) and (L[i][0]<a or (L[i][0]==a and L[i][1]<b)):
        R.append(L[i])
        i+=1
    R.append([a,b])
    while i<len(L) :
        R.append(L[i])
        i+=1
    """
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
    Déplace d'une case
    ----------
    Entrée: la position des vraies billes
    Sortie:
        Prochaine position si pas de pb
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
    Note: je sais pas encore comment on va lui mettre les entrees donc on se laisse le choix d'une possible fonction de traduction
    -------
    Sortie de type :
        [x,y,[deplacement x,deplacement y]] si sortie effective
        1 si reflexion en bord de boite ou demi tour et sortie a la meme case qu'entree
        0 si absorption
    """
    pos0=entree
    pos=deplacement_unitaire(billes,pos0)
    if pos==0 :
        return 0
    if pos[0]==0 or pos[0]==longueur-1 or pos[1]==0 or pos[1]==largeur-1 :  #Cas de reflexion en bord de boite : apres 1 coup on est tjr pas entré
        return 1
    while pos!=0 and pos[0]!=0 and pos[0]!=longueur-1 and pos[1]!=0 and pos[1]!=largeur-1 : #tant qu'on est pas sorti ou absorbé on se deplace
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
    Renvoie True si la bille est possible
    """
    return (not appartient(bille,dejaclear)) and (not(bille[0]<=0 or bille[0]>=longueur-1 or bille[1]<=0 or bille[1]>=largeur-1))
def calculespaces (billes,rayon,dejaclear,sortie,longueur,largeur,nbbilles,demitour=0):
    """
    ATTENTION si reflexion il faut mettre en valeur de "sortie" la position de la reflexion
    ---------
    Sortie :
        si un seul cas possible:
            0 si mauvaise sortie
            les billes qui la permettent si bonne sortie,1 car cas de base
        sinon :
            liste des positions de billes qui rendent un jeu possible,0 car pas cas de base
    """
    #Cas de bases :Sortie ou utilisation de toutes les billes.
    if rayon==0 or rayon[0]==0 or rayon[0]==longueur-1 or rayon[1]==0 or rayon[1]==largeur-1 : #Si on est sorti on regarde si c'est la bonne sortie

        if rayon==sortie :
            return [[billes,dejaclear]]
        else :
            return 0
    if nbbilles == len(billes): #Si on a déjà fait une suppostion qui utilise toutes les billes, on continue jusqu'au bout et voit si on est bon.
        while rayon!=0 and rayon[0]!=0 and rayon[0]!=longueur-1 and rayon[1]!=0 and rayon[1]!=largeur-1 : #tant qu'on est pas sorti ou absorbé on se deplace
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
    #Si on est pas sorti on va faire les 4 suppositions : Une bille en face, une a gauvhe, une a droite, ou rien (test d'en face seulement si absorption)
    L=[]  #Liste des différents univers
    x,y,[movx,movy]=rayon

    """
    Ordre des if :
        Si en face (seulement dans le cas d'une sortie absorption
        Si sur les cotes (cas ou on bouge selon y)
        Si sur les cotes (cas ou on bouge selon x)
        Si rien du tout

    """
    if sortie==0 and billepossible([x+movx,y+movy],dejaclear,longueur,largeur):
        ajout(L,[billes+[[x+movx,y+movy]],dejaclear+[[x+movx,y+movy]]])

    if demitour==1:
        demitourpossible=1 #on compte ici si la bille gauche et droite sont possibles (et si il y a bien eu demitour)
    else:
        demitourpossible=0

    if movx==0 :
        nouvbille=[x+1,y+movy]      #Si la nouvelle bille est à gauche
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que la bille qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour)
            if cas!=0:
                for elt in cas:
                    ajout(L,elt)

            billes.pop(-1)
            demitourpossible+=1


        nouvbille=[x-1,y+movy] #Si à droite

        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour) #Attention ici on a ajouté le cas de la bille gauche dans déjà fait car las cas où les 2 existent est deja fait
            if cas!=0:
                for elt in cas:
                    ajout(L,elt)
            billes.pop(-1)
            demitourpossible+=1

        cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour)
        if cas!=0:
                for elt in cas:
                    ajout(L,elt)

        if demitourpossible==3:
            bille1=[x+1,y+movy]
            bille2=[x-1,y+movy]
            if billepossible(bille1,dejaclear,longueur,largeur) and billepossible(bille2,dejaclear,longueur,largeur)and len(billes)<nbbilles-1:
                ajout(L,[billes+[bille1,bille2],dejaclear+[[x,y+movy],bille1,bille2]])

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
    if L==[]: #Si la liste est toujours vide cela veut dire que tous les cas sont impossibles.
        L=0
    return L
def selection (univers,liste_coups):
    """
    C'est cette fonction qui détermine ou tirer lorque l'on sait un univers
    """
    a=randint(1,4)
    n=len(univers)
    m=len(univers[0])
    liste_entrees=[]
    for i in liste_coups:
        liste_entrees.append(i[0])
    if a==1:
        test=[0,randint(1,m-2),[1,0]]
        if appartient(test,liste_coups):
            return selection(univers,liste_coups)
        else:
            return test
    if a==2:
        test= [n-1,randint(1,m-2),[-1,0]]
        if appartient(test,liste_coups):
            return selection(univers,liste_coups)
        else:
            return test
    if a==3:
        test= [randint(1,n-2),0,[0,1]]
        if appartient(test,liste_coups):
            return selection(univers,liste_coups)
        else:
            return test

    if a==4:
        test=[randint(1,n-2),m-1,[0,-1]]
        if appartient(test,liste_coups):
            return selection(univers,liste_coups)
        else:
            return test
def supprimerlesdoubles(liste):
    """
    Supprime les doubles d'une liste
    """
    for i in range (len(liste)-1,-1,-1): #on traverse la liste à l'envers pour ne pas modifier la position des doubles en supprimant les éléments du début.
        if appartient(liste[i],liste[:i]):
            liste.pop(i)
def BOB (nbbilles,longueur,largeur,billesréelles):
    """
    BOB est notre joueur qui calcule toutes les possibilités et fait une moyenne de tous les univers possibles pour placer une bille s'il y a une proba de 1 et tirer un rayon passant par la plus grosse valeur de probas
    -----
    Entrées :
        le tableau réel
    Sorties :
        la position des billes
    Attention cas particulier de la possibilité des reflexions en bord de boite a implementer
    """
    nbbilles_sur=0
    moyenne=[[1/(longueur*largeur) for i in range (largeur)]for j in range (longueur)]
    liste_coups=[]
    liste_des_univers=[]
    #coup initial:
    entree=selection(moyenne,liste_coups)
    sortie=deplacement(entree,billesréelles,longueur,largeur)

    x,y,[movx,movy]=entree
    ajout(liste_coups,[entree,sortie])
    #print(liste_coups[-1])
    depart=[]  #Opération obligatoire on va appliquer calculespaces sur le rayon qui est deja entré dans la boite les cas de reflexion en bord de boite sont traités a part.
    for i in range (-1,2):
        for j in  range (-1,2):
            depart.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave c'est des cases en dehors du terrain

    if sortie==0:
        cas=calculespaces([],deplacement_unitaire([],entree),depart,sortie,longueur,largeur,nbbilles)
        if cas !=0:
            for elt in cas:
                ajout(liste_des_univers,elt)
        ajout(liste_des_univers,[[[x+movx,y+movy]],[[x+movx,y+movy]]]) #cas à part si c'est la bille en tout premier qui fait bugger

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
                if 0<x+i<longueur-1 and 0<y+j<largeur-1 : #contrairement a depart on ne veut surtout pas compter de billes en dehors du plateau
                    ajout(liste_des_univers,[[[x+i,y+j]],[[x+i,y+j],[x+movx,y+movy]]])
                    comptage+=1
        if comptage==2 and nbbilles>1:
            ajout(liste_des_univers,[liste_des_univers[-1][0]+liste_des_univers[-2][0],liste_des_univers[-1][1]+[liste_des_univers[-2][1][0]]])

    else :
        for elt in calculespaces([],deplacement_unitaire([],entree),depart,sortie,longueur,largeur,nbbilles):
            ajout(liste_des_univers,elt)

    #print(liste_des_univers)
    #cas général
    while (len (liste_des_univers)!=1 or len(liste_des_univers[0][0])!=nbbilles) and len(liste_coups)<2*(longueur+largeur-6):
        entree=selection(moyenne,liste_coups)
        """if appartient( [[0, 4, [1, 0]], [1, 6, [0, 1]]],liste_coups):
            entree=selection(moyenne,liste_coups)
        else:
            entree=[0, 4, [1, 0]]"""
        sortie=deplacement(entree,billesréelles,longueur,largeur)

        x,y,[movx,movy]=entree
        ajout(liste_coups,[entree,sortie])
        #print("coup:",liste_coups[-1])


        for cas_traite in range (len(liste_des_univers)-1,-1,-1):
            #print(liste_des_univers)
            #print(cas_traite)
            billes,dejafait=liste_des_univers[cas_traite]

            depart=[] #Les cases qui sont deja analysées par le départ
            for i in range (-1,2):
                for j in  range (-1,2):
                    depart.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave c'est des cases en dehors du terrain
            supprimerlesdoubles(dejafait)
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
            #Cas des sans problèmes au départ
            if (not test0) and (not test1) and sortie==0:
                cas=calculespaces(billes,deplacement_unitaire([],entree),dejafait+depart,sortie,longueur,largeur,nbbilles)
                if cas !=0:
                    for elt in cas:
                        ajout(liste_des_univers,elt)
                if appartient([x+movx,y+movy],billes):
                    ajout(liste_des_univers,[billes,dejafait])
                if billepossible([x+movx,y+movy],dejafait,longueur,largeur) and len(billes)<nbbilles:
                    ajout(liste_des_univers,[billes+[[x+movx,y+movy]],dejafait+[[x+movx,y+movy]]]) #cas à part si c'est la bille en tout premier qui fait bugger

            elif (not test0) and (not test1) and sortie==1:
                #cas de sortie=entree

                cas=calculespaces(billes,deplacement_unitaire([],entree),dejafait+depart,[x,y,[-movx,-movy]],longueur,largeur,nbbilles,1)
                if cas !=0:
                    for elt in cas:
                        ajout(liste_des_univers,elt)
                #Cas de reflexion en bord de boite
                if len(billes)<nbbilles: #Si on peut en rajouter une nouvelle
                    comptage1=0   #si une bille a gauche et une bille a droite sont possibles alors les 2 ensembre le sont aussi
                    comptage2=0
                    for i in range(-1,3,2):
                        for j in range (-1,3,2):
                            if billepossible([x+i,y+j],dejafait,longueur,largeur) : #contrairement a depart on ne veut surtout pas compter de billes en dehors du plateau
                                ajout(liste_des_univers,[billes+[[x+i,y+j]],dejafait+[[x+movx,y+movy],[x+i,y+j]]])
                                comptage1+=1
                            if appartient([x+i,y+j],billes):
                                ajout(liste_des_univers,[billes,dejafait+[[x+movx,y+movy]]])
                                comptage2+=1
                    if comptage1==2 and len(billes)<nbbilles-1:
                        ajout(liste_des_univers,[billes+[liste_des_univers[-1][0][-1]]+[liste_des_univers[-2][0][-1]] , dejafait+[[x+movx,y+movy]]])
                    if comptage2==2:
                        ajout(liste_des_univers,[billes,dejafait+[[x+movx,y+movy]]])
            elif (not test0) and (not test1) :
                #print('ok2')


                cas=calculespaces(billes,deplacement_unitaire([],entree),dejafait+depart,sortie,longueur,largeur,nbbilles)
                #print('ok3')
                if cas!=0:
                    for elt in cas:
                        ajout(liste_des_univers,elt)
            #print(cas)

            liste_des_univers.pop(cas_traite)
        #print("fini",liste_des_univers)
    if len(liste_coups)==2*(longueur+largeur-6):
        return"stop"
    return liste_des_univers[0][0]

longueur=7
largeur=7
nbbilles=2
tab=[[0 for i in range (longueur)]for j in range (largeur)]
billes=crea_billes(nbbilles,longueur,largeur)
#billes=[[5, 3], [2, 1]]
for i in billes :
    tab[i[0]][i[1]]=1

printt(tab)
print(billes)
a=BOB(nbbilles,longueur,largeur,billes)
print(a)
print(billes)
printt(tab)
compteur=0
for i in range (10):
    billes=crea_billes(nbbilles,longueur,largeur)

    a=BOB(nbbilles,longueur,largeur,billes)
    print('end of the game',billes,a)
    if appartient(a[0],billes) and appartient(a[1],billes)and a[0]!=a[1]:
        compteur+=1
print(compteur)