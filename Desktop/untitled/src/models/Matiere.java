package models;

import java.util.LinkedList;

public class Matiere {
    private int numero;
    private String nom;
    private LinkedList<Activite> activites = new LinkedList<>();

    public Matiere(int numero, String nom) {
        this.numero = numero;
        this.nom = nom;
    }

    public Matiere() {
    }

    public LinkedList<Activite> getActivites() {
        return activites;
    }

    public void setActivites(LinkedList<Activite> activites) {
        this.activites = activites;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    @Override
    public String toString() {
        return numero + " "+nom;
    }
}
