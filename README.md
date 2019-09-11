nutella - Mangez moins gras
===========================

La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. 

Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que le gras c’est la vie).

Ce site utilisera l'API Open Food Facts pour rechercher les produits moins gras et dans la même catégorie.

Les différentes étapes à respecter
----------------------------------

### Fonctionnalités

* Affichage du champ de recherche dès la page d’accueil
* La recherche ne doit pas s’effectuer en AJAX
* Interface responsive
* Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de passe pour le moment.

### Étapes

1. Planifier votre projet

Découpez votre projet en étapes et sous-étapes en suivant une méthodologie de projet agile que vous adapterez à vos besoins. 

Remplissez un tableau Trello ou Pivotal Tracker.

Avant de coder, initialisez un repo Github et faites votre premier push.

 
2. Créer un nouveau projet Django

Créez votre projet, modifiez les réglages par défaut et commencez à le développer  fonctionnalité par fonctionnalité. 

Vous trouverez des indications supplémentaires dans les étapes suivantes sur certaines des fonctionnalités à réaliser.

 
3. La page d’accueil des héros

Intéressez-vous à la page d’accueil de la plateforme. 

Vous aurez besoin d’intégrer une librairie externe, Bootstrap, ainsi que jQuery. Structurez bien vos assets !

Puis créez le contenu HTML et mettez en forme l’ensemble grâce à CSS et ses librairies.

 
4. Ça c'est mon espace

Codez donc la page de création de compte ainsi que le formulaire associé.

Mettez à jour la barre de menu pour qu’elle affiche une icône “Mon compte” quand l’utilisateur est connecté et une icône “Créer un compte” quand il ne l’est pas.

Puis créez la page “Mon compte”.


5. Search but don't destroy

Commencez par parcourir la documentation de l’API Open Food Facts et trouvez comment récupérer les informations de l’aliment recherché.

Puis construisez votre base de données en y intégrant uniquement les éléments nécessaires (le score nutritionnel par exemple).

Enfin, inventez un algorithme qui va chercher dans votre base de données l’aliment qui a un meilleur score nutritionnel à l’aliment demandé mais qui reste dans la même catégorie.

Mettez à jour la page d’accueil et le menu pour que le formulaire de recherche soit effectivement fonctionnel.

Créez la page qui affiche les résultats de recherche.

Puis créez la page détaillant les caractéristiques de l’aliment de substitution.

À la fin, fêtez cette première fonctionnalité en faisant une pause qui vous fait plaisir (c’est important !).


6. Des aliments sains dans un corps sain

À présent, plongez dans la fonctionnalité qui permet à l’utilisateur d’enregistrer un produit de substitution en favoris. 

Mettez à jour la page qui affiche les résultats de recherche en ajoutant un bouton sous chaque produit. 

Puis ajoutez une nouvelle fonctionnalité à Django.

Créez la page Mes Produits, accessible en cliquant sur la carotte dans le menu.


7. Finitions et mise en ligne

Créez la page Mentions Légales et mettez en ligne votre site en utilisant Heroku.
