package models;

public class Activite {
    private Matiere matiere;
    private String groupe;
    private int numero;
    private String jour;
    private int debut;
    private int duree;
    private String salle;
    private int capacite;
    private int inscrits;

    public Activite() {
    }

    public Matiere getMatiere() {
        return matiere;
    }

    public void setMatiere(Matiere matiere) {
        this.matiere = matiere;
    }

    public String getGroupe() {
        return groupe;
    }

    public void setGroupe(String groupe) {
        this.groupe = groupe;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }

    public String getJour() {
        return jour;
    }

    public void setJour(String jour) {
        this.jour = jour;
    }

    public int getDebut() {
        return debut;
    }

    public void setDebut(int debut) {
        this.debut = debut;
    }

    public int getDuree() {
        return duree;
    }

    public void setDuree(int duree) {
        this.duree = duree;
    }

    public String getSalle() {
        return salle;
    }

    public void setSalle(String salle) {
        this.salle = salle;
    }

    public int getCapacite() {
        return capacite;
    }

    public void setCapacite(int capacite) {
        this.capacite = capacite;
    }

    public int getInscrits() {
        return inscrits;
    }

    public void setInscrits(int inscrits) {
        this.inscrits = inscrits;
    }

    public Activite(Matiere matiere, String groupe, int numero, String jour, int debut, int duree, String salle, int capacite, int inscrits) {
        this.matiere = matiere;
        this.groupe = groupe;
        this.numero = numero;
        this.jour = jour;
        this.debut = debut;
        this.duree = duree;
        this.salle = salle;
        this.capacite = capacite;
        this.inscrits = inscrits;
    }

    public String toString()
    {
        return this.matiere+" "+this.groupe+" "+this.numero+" "+this.jour+" "+this.debut+":00 "+this.debut+"h "+this.inscrits+"/"+this.capacite;
    }
}
