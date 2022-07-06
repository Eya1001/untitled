package services;

import models.Activite;
import models.Etudiant;

import java.util.List;

public class EtudiantService
{
    private final List<Etudiant> etudiants;
    private ActivityService activityService;
    public EtudiantService(List<Etudiant> etudiants)
    {
        activityService = new ActivityService(null);
        this.etudiants = etudiants;
    }

    public ActivityService getActivityService() {
        return activityService;
    }

    public void setActivityService(ActivityService activiteService) {
        activityService = activiteService;
    }

    public void setActivityList(List<Activite> activityList)
    {
        activityService.setActivityList(activityList);
    }

    public Etudiant create(String numero, String nom) throws Exception {
        for (Etudiant etudiant : etudiants) {
            if (etudiant.getNumero().equals(numero)) {
                throw new Exception("Le numéro d'étudiant existe déjà");
            }
        }
        return new Etudiant(numero, nom);
    }
    public void delete(String numero) throws Exception {
        for(Etudiant etudiant: etudiants)
        {
            if(etudiant.getNumero().equals(numero))
            {
                etudiants.remove(etudiant);
                return;
            }
        }
        throw new Exception("Pas d’étudiants avec ce numéro");
    }

    public Etudiant connection(String numero) throws Exception {
        for (Etudiant etudiant: etudiants)
        {
            if(etudiant.getNumero().equals(numero))
            {
                activityService = new ActivityService(etudiant.getActivites());
                return etudiant;
            }
        }
        throw new Exception("Pas d’étudiants avec ce numéro");
    }

    public void iscrireActivite(Etudiant etudiant,int numeroActivite, String groupeNumero) throws Exception {
        for (Activite activite1 : etudiant.getActivites()) {
            if (activite1 != null && activite1.getGroupe().equals(groupeNumero)) {
                throw new Exception("");
            }
        }
        etudiant.getActivites().add(activityService.findByNumeroAndGroupe(numeroActivite, groupeNumero));
    }

    public List<Etudiant> getEtudiants() {
        return etudiants;
    }

    public void getListActivities()
    {
        System.out.println(activityService.displayListActivities());
    }

    public static void desinscrireActivite(Etudiant etudiant, Activite activite)
    {

    }
}
