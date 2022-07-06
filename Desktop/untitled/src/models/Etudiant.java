package models;

import java.util.LinkedList;

public class Etudiant {
    private String numero;
    private String nom;
    private LinkedList<Activite> activites = new LinkedList<>();

    public Etudiant(String numero, String nom) {
        this.numero = numero;
        this.nom = nom;
    }

    public Etudiant(String numero, String nom, LinkedList<Activite> activites) {
        this.numero = numero;
        this.nom = nom;
        this.activites = activites;
    }

    public String getNumero() {
        return numero;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public LinkedList<Activite> getActivites() {
        return activites;
    }

    public void setActivites(LinkedList<Activite> activites) {
        this.activites = activites;
    }

    @Override
    public String toString() {
        return numero + " "+ nom;
    }

    public String displayActivities()
    {
        StringBuilder listActivities = new StringBuilder();
        for(Activite activite: activites)
        {
            listActivities.append(activite.toString());
        }
        return listActivities.toString();
    }
}
