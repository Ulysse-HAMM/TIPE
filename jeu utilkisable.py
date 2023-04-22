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
def est_une_bille(billes,point):
    """
    test si le point est une des billes
    -----------
    Entree :
        billes la liste des billes
    Sortie :
        True si c'en est une False sinon
    """
    for i in billes :
        if point==i:
            return True
    return False
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
    if est_une_bille(billes,[x+movx,y+movy]): #cas d'bsorption
        return 0
    if movx==0: #cas de déviation 1
        if est_une_bille(billes,[x+1,y+movy]):
            return [x,y,[-1,0]]
        elif est_une_bille(billes,[x-1,y+movy]):
            return [x,y,[1,0]]
    elif movy==0: #cas de déviation 2
        if est_une_bille(billes,[x+movx,y+1]):
            return [x,y,[0,-1]]
        elif est_une_bille(billes,[x+movx,y-1]):
            return [x,y,[0,1]]

    return [x+movx,y+movy,[movx,movy]]  #cas de déplacement sans gène
def traduction (longueur,largeur,entree):
    """
    Pas sur de garder cette fonction
    Traduit une entree au format "sens,signe,valeur" en format [x,y,[1,0]]
    ----------
    exemple d'entree :
        "x-4" -> entree sur l'axe x de sens opposé et de valeur 4
    sortie :
        [0,4,[1,0]]
    """
    if entree[0]=="y":
        if entree[1]=="-":
            val=int(entree[2:])
            return [longueur-1,val,[-1,0]]
        else :
            val=int(entree[1:])
            return [0,val,[1,0]]
    else :
        if entree[1]=="-":
            val=int(entree[2:])
            return [val,largeur-1,[0,-1]]
        else :
            val=int(entree[1:])
            return [val,0,[0,1]]
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
    #pos0=traduction(longueur,largeur,entree) #?
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

def sauvegarde (liste1,liste2):
    """
    Fonction permettant de socker liste2 dans liste1 sans impact (genre pb de mémoire et tt)
    """
    liste1.append([])
    if liste2!=0:
        for elt in liste2:
            if type(elt)!=list :
                liste1[-1].append(elt)
            else:
                sauvegarde(liste1[-1],elt)

def billepossible(bille,dejaclear,longueur,largeur):
    """
    Renvoie True si la bille est possible
    """
    return (not appartient(bille,dejaclear)) and (not(bille[0]==0 or bille[0]==longueur-1 or bille[1]==0 or bille[1]==largeur-1))

def calculespaces (billes,rayon,dejaclear,sortie,longueur,largeur,nbbilles,demitour=0):
    """
    ATTENTION si reflexion il faut mettre en valeur de "sortie" la position de la reflexion
    ---------
    Sortie :
        si un seul cas possible:
            0 si mauvaise sortie
            les billes qui la permettent si bonne sortie
        sinon :
            liste des positions de billes qui rendent un jeu possible
    """
    #Cas de bases :Sortie ou utilisation de toutes les billes.
    if rayon==0 or rayon[0]==0 or rayon[0]==longueur-1 or rayon[1]==0 or rayon[1]==largeur-1 : #Si on est sorti on regarde si c'est la bonne sortie (cas de base)

        if rayon==sortie :
            return [billes,dejaclear]
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
            if sortie==0:
                dejaclear.pop(-1)
                dejaclear.pop(-1)
            return [billes,dejaclear]
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
        sauvegarde(L,[billes+[[x+movx,y+movy]],dejaclear+[[x+movx,y+movy]]])
    if demitour==1:
        demitourpossible=1 #on compte ici si la bille gauche et droite sont possibles (et si il y a bien eu demitour)
    else:
        demitourpossible=0

    if movx==0 :
        nouvbille=[x+1,y+movy]      #Si la nouvelle bille est à gauche
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour)
            if cas!=0:
                for elt in cas:
                    sauvegarde(L,elt)

            billes.pop(-1)
            demitourpossible+=1


        nouvbille=[x-1,y+movy] #Si à droite

        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour) #Attention ici on a ajouté le cas de la bille gauche dans déjà fait car las cas où les 2 existent est deja fait
            if cas!=0:
                for elt in cas:
                    sauvegarde(L,elt)
            billes.pop(-1)
            demitourpossible+=1

        cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles,demitour)
        if cas!=0:
            for elt in cas:
                sauvegarde(L,elt)
        if demitourpossible==3:
            bille1=[x+1,y+movy]
            bille2=[x-1,y+movy]
            if billepossible(bille1,dejaclear,longueur,largeur) and billepossible(bille2,dejaclear,longueur,largeur)and len(billes)<nbbilles-1:
                sauvegarde(L,[billes+[bille1,bille2],dejaclear+[[x,y+movy],bille1,bille2]])

    else : #movy=0
        nouvbille=[x+movx,y+1]      #Si la nouvelle bille est à gauche
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles,demitour)
            if cas!=0:
                for elt in cas:
                    sauvegarde(L,elt)
            billes.pop(-1)
            demitourpossible+=1
        nouvbille=[x+movx,y-1]
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles,demitour) #Attention ici on a ajouté le cas de la bille gauche dans déjà fait car las cas où les 2 existent est deja fait
            if cas!=0:
                for elt in cas:
                    sauvegarde(L,elt)
            billes.pop(-1)
            demitourpossible+=1
        cas=calculespaces(billes,deplacement_unitaire(billes,rayon),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles,demitour)
        if cas!=0:
            for elt in cas:
                sauvegarde(L,elt)
        if demitourpossible==3 :
            bille1=[x+movx,y+1]
            bille2=[x+movx,y-1]
            if billepossible(bille1,dejaclear,longueur,largeur) and billepossible(bille2,dejaclear,longueur,largeur) and len(billes)<nbbilles-1:
                sauvegarde(L,[billes+[bille1,bille2],dejaclear+[[x+movx,y],bille1,bille2]])
    if L==[]: #Si la liste est toujours vide cela veut dire que tous les cas sont impossibles.
        L=0
    return L
def selection (univers):
    """
    C'est cette fonction qui détermine ou tirer lorque l'on sait un univers
    """
    a=randint(1,4)
    n=len(univers)
    m=len(univers[0])
    if a==1:
        return [0,randint(1,m-2),[1,0]]
    if a==2:
        return [n-1,randint(1,m-2),[-1,0]]
    if a==3:
        return [randint(1,n-2),0,[0,1]]
    if a==4:
        return [randint(1,n-2),m-1,[0,-1]]

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
    L=[]
    #coup initial:
    entree=selection(moyenne)
    x,y,[movx,movy]=entree
    sortie=deplacement(entree,billesréelles,longueur,largeur)
    print(entree,sortie)
    dejafait=[]  #Opération obligatoire on va appliquer calculespaces sur le rayon qui est deja entré dans la boite les cas de reflexion en bord de boite sont traités a part.
    for i in range (-1,2):
        for j in  range (-1,2):
            dejafait.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave c'est des cases en dehors du terrain

    if sortie==0:
        liste_des_univers=calculespaces([],deplacement_unitaire([],entree),dejafait,sortie,longueur,largeur,nbbilles)
        liste_des_univers.append([[deplacement_unitaire([],entree)[:2]],[deplacement_unitaire([],entree)[:2]]]) #cas à part si c'est la bille en tout premier qui fait bugger

    elif sortie==1:
        liste_des_univers=calculespaces([],deplacement_unitaire([],entree),dejafait,[x,y,[-movx,-movy]],longueur,largeur,nbbilles,1)
        if liste_des_univers==0:
            liste_des_univers=[]
        comptage=0   #si une bille a gauche et une bille a droite sont possibles alors les 2 ensembre le sont aussi
        for i in range(-1,3,2): #contrairement a dejafait on ne veut surtout pas compter de billes en dehors du plateau
            for j in range (-1,3,2):
                if 0<x+i<longueur-1 and 0<y+j<largeur-1 :
                    liste_des_univers.append([[[x+i,y+j]],[[x+i,y+j],[x+movx,y+movy]]])
                    comptage+=1
        if comptage==2:
            liste_des_univers.append([[liste_des_univers[-1][0]+liste_des_univers[-2][0]],liste_des_univers[-1][1]+[liste_des_univers[-2][1][0]]])
    else :
        liste_des_univers=calculespaces([],deplacement_unitaire([],entree),dejafait,sortie,longueur,largeur,nbbilles)
        BBBBBBOOOOOOOOOOOOOOOOBBBBBBBBBBBBBBBB

    return liste_des_univers

longueur=7
largeur=7
nbbilles=2
tab=[[0 for i in range (longueur)]for j in range (largeur)]
billes=crea_billes(nbbilles,longueur,largeur)
for i in billes :
    tab[i[0]][i[1]]=1
printt(tab)
print("")
print(BOB(nbbilles,longueur,largeur,billes))
[[[[4, 3]], [[3, 4], [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6], [4, 3]]], [[[4, 2]], [[3, 4], [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6], [4, 3], [5, 3], [3, 3], [4, 2]]], [[[4, 1]], [[3, 4], [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6], [4, 3], [5, 3], [3, 3], [4, 2], [5, 2], [3, 2], [4, 1]]], [[[4, 4]], [[4, 4]]]]