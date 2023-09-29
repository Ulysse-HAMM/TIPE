# Créé par erwan, le 31/07/2023 en Python 3.7
from random import randint
def trier (liste):
    """
    Trie une liste de couples par ordre alphabetique (methodde tri bulle)
    ---------
    Entrée :
        liste au format [[2,4],[4,5],[2,4],[1,2],[2,5]]
    Sortie :
        liste_triee [[1,2],[2,4],[2,4],[2,5],[4,5]]
    """
    n=len(liste)
    for i in range (n):
        for j in range (i):
            if liste[i][0]<liste[j][0]:
                liste[i],liste[j]=liste[j],liste[i]
            elif liste[i][0]==liste[j][0] and liste[i][1]<liste[j][1]:
                liste[i],liste[j]=liste[j],liste[i]
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
    Renvoie True si la bille est possible (cad dans le terrain et pas sur une case deja visitée)
    """
    return (not appartient(bille,dejaclear)) and 0<bille[0]<largeur-1 and 0<bille[1]<longueur-1
def supprimerlesdoubles(liste):
    """
    Supprime les doubles d'une liste
    on traverse la liste à l'envers pour ne pas modifier des positions de doubles en supprimant les éléments au début.
    """
    for i in range (len(liste)-1,-1,-1):
        if appartient(liste[i],liste[:i]):
            liste.pop(i)
def nettoyer(liste,longueur,largeur):
    """
    Trie la liste sur la base du tri bulle (flemme de faire un des algos relou à implémenter)
    et supprime tous les elements en double ou inutiles car en dehors de boite

    Fonction utile pour nettoyer tout le monde et vérifier si 2 listes sont egales plus facilement
    """

    supprimerlesdoubles(liste)
    trier (liste)
    for i in range(len(liste)-1,-1,-1) :
        if not(billepossible(liste[i],[],longueur,largeur)):
            liste.pop(i)
def crea_billes (nb,longueur,largeur,L=[]):

    """
    Crée une liste de nb billes reparties dans longueur en x ,largeur en y
    Attention: Appel récursif pour crée nb-1 bille (taille de L majorée par nb et croissante à chaque appel)
    ------------
    Entrées :
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
        trier(L)
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

    R=crea_billes(nb,longueur,largeur,R)
    return R
def deplacement_unitaire (rayon,billes=[]):
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
    pos=deplacement_unitaire(pos0,billes)
    if pos==0 :                     #Cas d'absorption directe
        return 0
    if pos[0]==0 or pos[0]==largeur-1 or pos[1]==0 or pos[1]==longueur-1 :  #Cas de reflexion en bord de boite : apres 1 coup on est tjr pas entré
        return 1
    while pos!=0 and pos[0]!=0 and pos[0]!=largeur-1 and pos[1]!=0 and pos[1]!=longueur-1 : #tant qu'on est pas sorti ou absorbé on se deplace
        pos=deplacement_unitaire(pos,billes)

    if pos!=0 and pos[:2]==pos0[:2]: #Si la sortie vaut l'entree c'est une reflexion
        return 1
    return pos   #Sinon on retourne juste la sortie


def calculespaces (billes,rayon,dejaclear,sortie,longueur,largeur,nbbilles):
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
        #demitour: vaut 1 si la sortie vaut 1 cad qu'on a fait un demitour (car on ne peut pas mettre 1 dans la valeur sortie car on oublierai la valeur de l'ntree dans les appels récursifs)
    Sortie :
        0 si mauvaise sortie/ cas impossible
        L la liste des différents cas possibles :
            format L=[cas1,cas2,...]
            avec
            cas=[[billes du cas],[cases où il ne peut y avoir de billes]]
    """
    #Cas de bases :Sortie ou utilisation de toutes les billes.
    if rayon==0 or rayon[0]==0 or rayon[0]==largeur-1 or rayon[1]==0 or rayon[1]==longueur-1 : #Si on est sorti(sur le bord et pas en train d'entrer) on regarde si c'est la bonne sortie
        if rayon==sortie :
            return [[billes,dejaclear]]
        else :
            return []
    if nbbilles == len(billes): #Si on a déjà fait une suppostion qui utilise toutes les billes, on continue jusqu'au bout et voit si on est bon.
        while rayon!=0 and rayon[0]!=0 and rayon[0]!=largeur-1 and rayon[1]!=0 and rayon[1]!=longueur-1 : #tant qu'on est pas sorti ou absorbé on se deplace et on ajoute à la liste dejaclear
            x,y,[movx,movy]=rayon
            if movx==0:
                dejaclear+=[x,y+movy],[x+1,y+movy],[x-1,y+movy]
            else:
                dejaclear+=[x+movx,y],[x+movx,y+1],[x+movx,y-1]
            rayon=deplacement_unitaire(rayon,billes)

        if rayon == sortie:
            if sortie==0:   #si la sortie est une absorption on a enfait pas dejaclear ces 2 cases
                dejaclear.pop(-1)
                dejaclear.pop(-1)
            return [[billes,dejaclear]]
        else:
            return []


    #Récursif :
    #Si on est pas sorti on va faire les 4 suppositions : une a gauche, une a droite,une en face (si sortie= absorption) ou rien
    L=[]  #Liste des différents univers
    x,y,[movx,movy]=rayon

    """
    Ordre des if :
        Si en face (seulement dans le cas d'une sortie absorption)
        Si sur les cotes (cas ou on bouge selon y) Attention vu que la gauche est verifiee en 1er la doite peut aussi etre une bille
        Si sur les cotes (cas ou on bouge selon x)
        Si rien du tout

    """
    if sortie==0 and billepossible([x+movx,y+movy],dejaclear,longueur,largeur):
        ajout(L,[billes+[[x+movx,y+movy]],dejaclear+[[x+movx,y+movy]]])


    #Si le deplacement est horizontal (on ne bouge pas selon x)
    if movx==0 :
        nouvbille=[x+1,y+movy]        #Si la nouvelle bille est en bas
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que la bille qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            liste_cas=calculespaces(billes,deplacement_unitaire(rayon,billes),dejaclear+[[x+movx,y+movy],[x+1,y+movy]],sortie,longueur,largeur,nbbilles)

            for cas in liste_cas:
                ajout(L,cas)
            billes.pop(-1)  #on enlève la supposition qu'on vient de faire

        nouvbille=[x-1,y+movy]        #Si la nouvelle bille est en haut
        if billepossible(nouvbille,dejaclear,longueur,largeur): #il faut que le chemin qu'on crée soit possible: (on ne peut pas avoir une bille sur un chemin ou on est deja passé)
            billes+=[nouvbille]
            liste_cas=calculespaces(billes,deplacement_unitaire(rayon,billes),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles)
            for cas in liste_cas:
                ajout(L,cas)
            billes.pop(-1)

                                  #Si la nouvelle bille est tout droit (horizontalement)
        liste_cas=calculespaces(billes,deplacement_unitaire(rayon,billes),dejaclear+[[x+movx,y+movy],[x+1,y+movy],[x-1,y+movy]],sortie,longueur,largeur,nbbilles)
        for cas in liste_cas:
            ajout(L,cas)


    #exactement pareil mais pour un deplacement vertical
    else : #movy=0
        nouvbille=[x+movx,y+1]      #Si la nouvelle bille est à droite
        if billepossible(nouvbille,dejaclear,longueur,largeur):
            billes+=[nouvbille]
            liste_cas=calculespaces(billes,deplacement_unitaire(rayon,billes),dejaclear+[[x+movx,y+movy],[x+movx,y+1]],sortie,longueur,largeur,nbbilles)
            for cas in liste_cas:
                ajout(L,cas)
            billes.pop(-1)

        nouvbille=[x+movx,y-1]      #Si la nouvelle bille est à gauche
        if billepossible(nouvbille,dejaclear,longueur,largeur):
            billes+=[nouvbille]
            liste_cas=calculespaces(billes,deplacement_unitaire(rayon,billes),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles)
            for cas in liste_cas:
                ajout(L,cas)
            billes.pop(-1)
                                  #Si la nouvelle bille est tout droit (verticalement)
        liste_cas=calculespaces(billes,deplacement_unitaire(rayon,billes),dejaclear+[[x+movx,y+movy],[x+movx,y+1],[x+movx,y-1]],sortie,longueur,largeur,nbbilles)
        for cas in liste_cas:
            ajout(L,cas)

    #Si la liste est toujours vide cela veut dire que tous les cas sont impossibles.
    return L

def chercheur (nbbilles,longueur,largeur,billesréelles,strategie):
    """
    BOB est notre joueur qui calcule toutes les possibilités et s'arrete dès qu'il trouve une unicité des cas possibles (qui comportent le bon nb de billes)
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
    #On initialise la liste des entrees possibles dont les elements seront supprimés dès qu'on a testé l'entree



    ###coup initial:(à part car il evite des tests de coup initial dans le cas général pour les cas particuliers)
    entree=strategie(liste_coups,entreespossibles)
    sortie=deplacement(entree,billesréelles,longueur,largeur)

    if sortie!=0 and sortie !=1: #Si la sortie est un autre endroit, on la supprime aussi (par retour inverse de la lumière ce test est inutile)
        for i in range (4):
            for elt in range (len(entreespossibles[i])-1,-1,-1):
                if entreespossibles[i][elt][:2]==sortie[:2]:
                    entreespossibles[i].pop(elt)

    #print('entree',entree,sortie,entreespossibles)
    x,y,[movx,movy]=entree
    ajout(liste_coups,[entree,sortie])
    depart=[]  #Met dans dejafait les premières cases environnantes. Opération obligatoire on va appliquer calculespaces sur le rayon qui est deja entré dans la boite les cas de reflexion en bord de boite sont traités a part.
    for i in range (-1,2):
        for j in  range (-1,2):
            depart.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave elles seront nettoyées plus tard

    if sortie==0:
        liste_cas=calculespaces([],deplacement_unitaire(entree),depart,sortie,longueur,largeur,nbbilles)

        for cas in liste_cas:
                ajout(liste_des_univers,cas)
        ajout(liste_des_univers,[[[x+movx,y+movy]],[[x+movx,y+movy]]]) #cas à part si c'est la bille en tout premier qui fait une telle sortie

    elif sortie==1:

        #cas de sortie=entree
        liste_cas=calculespaces([],deplacement_unitaire(entree),depart,[x,y,[-movx,-movy]],longueur,largeur,nbbilles)

        for cas in liste_cas:
            ajout(liste_des_univers,cas)

        #Cas de reflexion en bord de boite
        comptage=0   #si une bille a gauche et une bille a droite sont possibles alors les 2 ensembre le sont aussi
        for i in range(-1,3,2):
            for j in range (-1,3,2):
                if billepossible([x+i,y+j],[],longueur,largeur) : #contrairement a depart on ne veut surtout pas compter de billes en dehors du plateau
                    ajout(liste_des_univers,[[[x+i,y+j]],[[x+i,y+j],[x+movx,y+movy]]])
                    comptage+=1
        if comptage==2 and nbbilles>1:
            ajout(liste_des_univers,[liste_des_univers[-1][0]+liste_des_univers[-2][0],liste_des_univers[-1][1]+[liste_des_univers[-2][1][0]]])

    else :
        liste_cas=calculespaces([],deplacement_unitaire(entree),depart,sortie,longueur,largeur,nbbilles)
        for cas in liste_cas:
            ajout(liste_des_univers,cas)
    for cas in liste_des_univers:
        billes,dejafait=cas
        trier(billes)
        nettoyer(dejafait,longueur,largeur)






    #cas général
    while (not(len (liste_des_univers)==1 and len(liste_des_univers[0][0])==nbbilles)) and entreespossibles!=[[],[],[],[]]:
        #tant qu'on a pas unicité d'une solution valide et qu'on a pas testé toutes les entrées
        entree=strategie(liste_coups,entreespossibles)
        """if appartient( [[0, 4, [1, 0]], [1, 6, [0, 1]]],liste_coups):
            entree=selection(moyenne,liste_coups)
        else:
            entree=[0, 4, [1, 0]]"""
        sortie=deplacement(entree,billesréelles,longueur,largeur)
        if sortie!=0 and sortie !=1: #Si la sortie est un autre endroit, on la supprime aussi (par retour inverse de la lumière ce test est inutile)
            for i in range (4):
                for elt in range (len(entreespossibles[i])-1,-1,-1):
                    if entreespossibles[i][elt][:2]==sortie[:2]:
                        entreespossibles[i].pop(elt)
        x,y,[movx,movy]=entree
        ajout(liste_coups,[entree,sortie])
        #print("coup:",liste_coups[-1])


        for cas_traite in range (len(liste_des_univers)-1,-1,-1):
            #Maintenant on va tester chaque cas possible et verifier qu'il correspond avec le nouveau coup qu'on vient de jouer et si c'est bien le cas on ajoute a listedesunivers tous les nouveaux cas possibles.


            #print(liste_des_univers)
            #print(cas_traite)
            billes,dejafait=liste_des_univers[cas_traite]
            nouveaux_cas=[] #On stock ici les nouveaux cas, ils seront triés et nettoyés après

            depart=[] #Les cases qui sont deja analysées par le départ
            for i in range (-1,2):
                for j in  range (-1,2):
                    depart.append([x+i,y+j]) #on met trop de cases dans déja fait mais pas grave c'est des cases en dehors du terrain


            #Si il n'y a aucune des billes déjà trouvées n'est autour du départ (cela induirait une contradiction et un  cas impossible)
            test0=False #Test si la sortie devrait etre 0
            test1=False #Test si la sortie devrait etre 1
            sauvegarde=[] #compte si les 2 cotés sont deja occupés et retiens leur position (compte avec sa longueur)
            for i in range (-1,2):
                for j in range (-1,2):
                    if appartient([x+i,y+j],billes) and (i==0 or j==0):
                        test0=True
                    elif appartient([x+i,y+j],billes):#i==+-1 or j=+-1
                        test1=True
                        sauvegarde.append([x+i,y+j])

            if test0 and sortie==0:
                ajout(liste_des_univers,liste_des_univers[cas_traite])
            if (not test0) and test1 and sortie==1:
                ajout(nouveaux_cas,[billes,dejafait+[[x+movx,y+movy]]])

                if len(sauvegarde)==1 :#si on savait une bille à gauche on peut aussi supposer qu'il y en a une à droite(par exemple)
                    for i in range (-1,2,2):
                        for j in range(-1,2,2):
                            if [[x+i,y+j]]!=sauvegarde and billepossible([x+i,y+j],dejafait,longueur,largeur) and len(billes)<nbbilles:
                                ajout(nouveaux_cas,[billes+[[x+i,y+j]],dejafait+[[x+i,y+j],[x+movx,y+movy]]])
            if test1 and sortie==0 and len(billes)<nbbilles and billepossible([x+movx,y+movy],dejafait,longueur,largeur):
                ajout(nouveaux_cas,[billes+[[x+movx,y+movy]],dejafait+[[x+movx,y+movy]]])


            #Cas des sans problèmes au départ


            if (not test0) and (not test1) and sortie==0:
                liste_cas=calculespaces(billes,deplacement_unitaire(entree),dejafait+depart,sortie,longueur,largeur,nbbilles)

                for cas in liste_cas:
                    ajout(nouveaux_cas,cas)
                """if appartient([x+movx,y+movy],billes):
                    ajout(nouveaux_cas,[billes,dejafait])"""
                if billepossible([x+movx,y+movy],dejafait,longueur,largeur) and len(billes)<nbbilles:
                    ajout(nouveaux_cas,[billes+[[x+movx,y+movy]],dejafait+[[x+movx,y+movy]]]) #cas à part si c'est la bille en tout premier qui fait bugger

            elif (not test0) and (not test1) and sortie==1:
                #cas de sortie=entree

                liste_cas=calculespaces(billes,deplacement_unitaire(entree),dejafait+depart,[x,y,[-movx,-movy]],longueur,largeur,nbbilles)
                for cas in liste_cas:
                    ajout(nouveaux_cas,cas)
                #Cas de reflexion en bord de boite
                if len(billes)<nbbilles: #Si on peut en rajouter une nouvelle
                    comptage=0   #si une bille a gauche et une bille a droite sont possibles alors les 2 ensemble le sont aussi
                    for i in range(-1,3,2):
                        for j in range (-1,3,2):
                            if billepossible([x+i,y+j],dejafait,longueur,largeur) : #contrairement a depart on ne veut surtout pas compter de billes en dehors du plateau
                                ajout(nouveaux_cas,[billes+[[x+i,y+j]],dejafait+[[x+movx,y+movy],[x+i,y+j]]]) #De plus ces cases ne sont forcément pas déjà des billes sinon on aurait test1=True
                                comptage+=1

                    if comptage==2 and len(billes)<nbbilles-1:
                        ajout(nouveaux_cas,[billes+[nouveaux_cas[-1][0][-1]]+[nouveaux_cas[-2][0][-1]] , dejafait+[[x+movx,y+movy]]])

            elif (not test0) and (not test1) :
                liste_cas=calculespaces(billes,deplacement_unitaire(entree),dejafait+depart,sortie,longueur,largeur,nbbilles)

                for cas in liste_cas:
                    ajout(nouveaux_cas,cas)


            for cas in nouveaux_cas:#On nettoie tous les nouveaux cas et on les ajoutes à la grosse liste (pour les comparaisons et supprimer les possibles doubles)
                billes,dejafait=cas
                trier(billes)
                nettoyer(dejafait,longueur,largeur)
                ajout(liste_des_univers,cas)


            liste_des_univers.pop(cas_traite) #On supprime le cas qu'on vient d'analyser qui a été remplacé on simplement supprimé s'il ne correspondait pas à la nouvelle entrée

        supprimerlesdoubles(liste_des_univers)

    #Si le bon résultat n'a pas ete trouve a ce moment
    if (not(len (liste_des_univers)==1 and len(liste_des_univers[0][0])==nbbilles)):


        #Cas ou la solution est sure ET le nombre de billes manquantes est celui des cases non visitées
        if len (liste_des_univers)==1:
            n=0
            sauvegarde=[]
            for i in range (1,largeur-1):
                for j in range (1,longueur-1):
                    if [i,j]!=liste_des_univers[0][1][n]:
                        sauvegarde.append([i,j])
                        n-=1
                    n+=1
            if len(sauvegarde)+len(liste_des_univers[0][0])==nbbilles:
                return liste_des_univers[0][0]+sauvegarde,liste_coups
            elif len(sauvegarde)+len(liste_des_univers[0][0])<nbbilles:
                print ('probleme: unicite de la solution mais pas trouvée',liste_des_univers,liste_coups)
                print(bloblablu)
                return liste_des_univers[0][0]+sauvegarde,liste_coups
            else:
                print('gros gros probleme: plus de billes que de place restante pour une unicité de solution',liste_des_univers,liste_coups)
                print(bloblablu)


        #Cas ou l'on va etre obligé de faire une moyenne
        #print('cas a problemes \n',liste_des_univers,"prb\n",liste_coups)
        moyenne =[[0 for i in range (longueur)]for j in range (largeur)]
        nbcas=len(liste_des_univers)
        for cas in range(nbcas-1,-1,-1):
            n=0
            sauvegarde=[]
            for i in range (1,largeur-1):
                for j in range (1,longueur-1):
                    if [i,j]!=liste_des_univers[cas][1][n]:
                        sauvegarde.append([i,j])
                        n-=1
                    n+=1
            if len(sauvegarde)+len(liste_des_univers[cas][0])<nbbilles:#Si la solution proposée n'utilise pas assez de billes
                liste_des_univers.pop(cas)
            else:
                for i in range (len(liste_des_univers[cas][0])):
                    moyenne[liste_des_univers[cas][0][i][0]][liste_des_univers[cas][0][i][1]]+=1
                nb=len (sauvegarde)
                for i in range (nb):
                    moyenne[sauvegarde[i][0]][sauvegarde[i][1]]+=1/nb
        nbcas=len(liste_des_univers)
        if nbcas==1 and len(liste_des_univers[0][0])==nbbilles:
            return liste_des_univers[0][0],liste_coups
        for i in range (1,largeur-1):
                for j in range (1,longueur-1):
                    moyenne[i][j]/=nbcas
        print("ok ben c'est la merde mais on teste")
        """,liste_des_univers,liste_coups"""
        printt(moyenne)
        print(bloblablu)
    return liste_des_univers[0][0],liste_coups

def selection_aleatoire (liste_coups,entreespossibles):
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
    test=entreespossibles[a][x]
    entreespossibles[a].pop(x)
    return test

def printt (tab):
    """pour les tests"""
    for i in tab :
        print(i)



longueur=10
largeur=10
nbbilles=5
tests=10
tab=[[0 for i in range (longueur)]for j in range (largeur)]
printt(tab)
compteur=0
for i in range (tests):
    billes=crea_billes(nbbilles,longueur,largeur)
    #billes=[[1, 8], [5, 5], [6, 7], [7, 7]]
    print('billes',billes)
    billes_trouvées,coups=chercheur(nbbilles,longueur,largeur,billes,selection_aleatoire)
    print('resultat',billes_trouvées,len(coups))
    if billes_trouvées==billes :
        print('end of the game')
    else :
        print('aleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed',coups)


