package services;

import models.Activite;

import java.util.List;

public class ActivityService {
    private List<Activite> activityList;
    public ActivityService(List<Activite> activityList)
    {
        this.activityList = activityList;
    }

    public Activite findByNumeroAndGroupe(int numero, String groupe) throws Exception {
        for (Activite activite: activityList)
        {
            if(activite.getGroupe().equals(groupe) && activite.getNumero() == numero)
            {
                return activite;
            }
        }
        throw new Exception("activite n'existe pas");
    }

    public List<Activite> getActivityList() {
        return activityList;
    }

    public void setActivityList(List<Activite> activiteList)
    {
        activityList = activiteList;
    }

    public String displayListActivities()
    {
        StringBuilder output = new StringBuilder();
        for(Activite activite: activityList)
        {
            output.append(activite.toString()).append("\n");
        }
        return output.toString();
    }
}
