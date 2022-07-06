import models.Activite;
import models.Etudiant;
import models.Matiere;
import services.EtudiantService;

import java.util.LinkedList;

public class Universite {
    private static final String choixUnivesiteMessage = "Choix (a/s/v/l/x) : ";
    private static final String lettersUnivesity = "avcxs";
    private static final String optionsUniversiteMessage = "Options du menu Université\n" + "a = ajouter un étudiant\n" + "s = supprimer un étudiant\n" + "v = voir tous les étudiants\n" + "c = connexion\n" + "x = sortie";
    private static final String getChoixEtudiantMessage = "Choix (v/i/d/x) : ";
    private static final String lettersEtudiants = "vidx";
    private static final String optionsEtudiantMessage = "Options du menu étudiant\n" + "v = voir mes activités\n" + "i = s'inscrire à une activité\n" + "d = se désinscrire d'une activité\n" + "x = sortie";
    private final LinkedList<Matiere> matieres = new LinkedList<>();
    private final LinkedList<Etudiant> etudiants = new LinkedList<>();
    private final EtudiantService etudiantService;
    private Etudiant etudiant;

    Universite() {
        Matiere m1 = new Matiere(48024, "Développement des applications");
        Matiere m2 = new Matiere(31284, "Développement des web services");
        m1.getActivites().add(new Activite(m1, "cours1", 1, "mercredi", 18, 1, "S405", 200, 0));
        m1.getActivites().add(new Activite(m1, "TP1", 1, "mercredi", 19, 2, "S403", 2, 0));
        m1.getActivites().add(new Activite(m1, "TP1", 2, "mercredi", 19, 2, "S401", 2, 0));
        m1.getActivites().add(new Activite(m1, "TP1", 3, "mercredi", 19, 2, "S402", 2, 0));
        m2.getActivites().add(new Activite(m2, "cours1", 1, "mardi", 16, 1, "S002", 160, 0));
        m2.getActivites().add(new Activite(m2, "TP1", 2, "mardi", 9, 2, "S102", 30, 0));
        m2.getActivites().add(new Activite(m2, "TP1", 3, "mardi", 9, 2, "S103", 30, 0));
        m2.getActivites().add(new Activite(m2, "TP1", 3, "mardi", 14, 2, "S102", 30, 0));
        m2.getActivites().add(new Activite(m2, "TP1", 3, "mardi", 14, 2, "S103", 30, 0));
        matieres.add(m1);
        matieres.add(m2);
        this.etudiantService = new EtudiantService(etudiants);
    }

    public void addEtudiant() {
        String numero = EntreeUtilisateur.getValue("Numéro : ");
        String nom = EntreeUtilisateur.getValue("Nom : ");
        try {
            etudiants.add(etudiantService.create(numero, nom));
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }


    public void afficherListeEtudiants() {
        System.out.println(etudiants);
        for (Etudiant etudiant : etudiants) {
            System.out.println(etudiant);
        }
    }

    public boolean connection() {
        String numero = EntreeUtilisateur.getValue("Numéro : ");
        try {
            etudiant = etudiantService.connection(numero);
            return true;
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return false;
    }

    public void deleteEtudiant() {
        String numero = EntreeUtilisateur.getValue("Numéro : ");
        try {
            etudiantService.delete(numero);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public void inscrireActivite() {
        int option = Integer.parseInt(EntreeUtilisateur.getValue("Numéro de sujet : "));
        for (Matiere matiere : matieres) {
            if (matiere.getNumero() == option) {

                etudiantService.setActivityList(matiere.getActivites());
                System.out.println("Sélectionnez une activité :");
                etudiantService.getListActivities();
                try {
                    String activityString = EntreeUtilisateur.getValue("Code d'activité (groupe:numéro): ");
                    String[] data = activityString.split(":");
                    etudiantService.iscrireActivite(etudiant, Integer.parseInt(data[1]), data[0]);
                    etudiantService.setActivityList(etudiant.getActivites());
                    return;
                } catch (Exception e) {
                    System.out.println(e.getMessage());
                    return;
                }
            } else {
                return;
            }
        }
    }

    public static void main(String[] args) {
        Universite universite = new Universite();
        String input = EntreeUtilisateur.readInput(choixUnivesiteMessage, lettersUnivesity, optionsUniversiteMessage);
        while ("asvcx".contains(input)) {
            switch (input) {
                case "v":
                    universite.afficherListeEtudiants();
                    break;
                case "a":
                    universite.addEtudiant();
                    break;
                case "s":
                    universite.deleteEtudiant();
                    break;
                case "c":
                    boolean isConnected = universite.connection();
                    if (isConnected) {
                        do {
                            input = EntreeUtilisateur.readInput(getChoixEtudiantMessage, lettersEtudiants, optionsEtudiantMessage);
                            switch (input) {
                                case "v":
                                    universite.etudiantService.getListActivities();
                                    break;
                                case "i":
                                    for (Matiere matiere : universite.matieres) {
                                        System.out.println(matiere);
                                    }
                                    universite.inscrireActivite();
                                    break;
                                case "d":
                                    universite.etudiant = null;
                                    isConnected = false;
                                    break;
                            }
                        } while (isConnected);
                    }
            }
            input = EntreeUtilisateur.readInput(choixUnivesiteMessage, lettersUnivesity, optionsUniversiteMessage);
        }
    }
}
