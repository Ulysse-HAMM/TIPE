# Créé par erwan, le 28/06/2023 en Python 3.7
from numpy import log
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

longueur=7
largeur=7
entreespossibles=[]
for i in range (1,longueur-1):
    entreespossibles.append([0,i,[1,0]])
    entreespossibles.append([largeur-1,i,[-1,0]])
for j in range (1,largeur-1):
    entreespossibles.append([j,0,[0,1]])
    entreespossibles.append([j,longueur-1,[0,-1]])

loi={}
config=0
for b1x in range(1,longueur-1):
    for b1y in range (1,largeur-1):
        for b2x in range (1,longueur-1):
            for b2y in range(1,largeur-1):
                for b3x in range (1,longueur-1):
                    for b3y in range (1,largeur-1):
                        for b4x in range (1,longueur-1):
                            for b4y in range (1,largeur-1):
                                for b5x in range (1,longueur-1):
                                    for b5y in range (1,largeur-1):
                                        b1=[b1x,b1y]
                                        b2=[b2x,b2y]
                                        b3=[b3x,b3y]
                                        b4=[b4x,b4y]
                                        b5=[b5x,b5y]
                                        if (b1!=b2) and (b1!=b3) and (b1!=b4) and (b1!=b5) and (b2!=b3) and (b2!=b4) and (b2!=b5)and (b3!=b4)and (b3!=b5)and (b4!=b5):
                                            config+=1
                                            for etr in range(len(entreespossibles)):
                                                elt=str([entreespossibles[etr],deplacement(entreespossibles[etr],[b1,b2,b3,b4,b5],longueur,largeur)])
                                                if elt in loi:
                                                    loi[elt]+=1
                                                else:
                                                    loi[elt]=1

def transfo (string):
    x=0
    y=0
    if string[3]==',':
        x=int(string[2])
        if string[6]==',':
            y=int(string[5])
        else:
            y=int(string[5:7])
    else :
        x=int(string[2:4])
        if string[7]==',':
            y=int(string[6])
        else:
            y=int(string[6:8])
    return [x,y]


    return 2
print(loi)
tot=config/6
somme=0
information={}
for i in loi.keys():
    loi[i]=loi[i]/6
    a=str(transfo(i))
    if a in information:

        information[a]-=loi[i]*log(loi[i]/tot)/tot
    else:

        information[a]=-loi[i]*log(loi[i]/tot)/tot

for i in information.keys():

    print(i,information[i])
