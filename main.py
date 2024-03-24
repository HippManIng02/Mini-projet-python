from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

from etudiant import Scolarite, Etudiant, Connection


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.entrer_absence_u = None
        self.entrer_numero = None
        self.entrer_nom = None
        self.entrer_prenom = None
        self.entrer_date = None
        self.entrer_annee = None
        self.entrer_classe = None
        self.entrer_commentaire = None
        self.table = None
        self.entrer_recherche = None
        self.entrer_numero_m = None
        self.entrer_moyenne = None
        self.etudiant = Etudiant()
        self.scolarite = Scolarite()
        self.create_menu_bar()
        self.create_home_frame()
        self.geometry("1400x700")
        self.title("Gestion Scolarité V1.0")
        self.connection = Connection()

    def create_menu_bar(self):
        menu_bar = Menu(self)
        menu_bar.add_command(label="Recherche", command=self.recherche_window)
        menu_bar.add_command(label="Moyenne", command=self.moyenne_window)
        menu_bar.add_command(label="Absence", command=self.absence_window)

        self.config(menu=menu_bar)

    def create_home_frame(self):
        lbl_titre = Label(self, bd=15, relief=RIDGE, text="GESTION DE LA SCOLARITÉ", font=("Arial", 30),
                          bg="#293133", fg="white")
        lbl_titre.place(x=0, y=0, width=1365)

        # Liste des étudiants
        lbl_liste_etu = Label(self, text="LISTES DES ETUDIANTS ", font=("Arial", 16), bg="darkblue", fg="white")
        lbl_liste_etu.place(x=500, y=100, width=760)

        # text numéro
        lbl_numero = Label(self, text="Numéro", font=("Arial", 16), bg="#293133", fg="white")
        lbl_numero.place(x=0, y=100, width=200)
        self.entrer_numero = Entry(self)
        self.entrer_numero.place(x=200, y=100, width=160, height=30)

        # text nom
        lbl_nom = Label(self, text="Nom ", font=("Arial", 16), bg="#293133", fg="white")
        lbl_nom.place(x=0, y=150, width=200)
        self.entrer_nom = Entry(self)
        self.entrer_nom.place(x=200, y=150, width=200, height=30)

        # text prenom
        lbl_prenom = Label(self, text="Prenom", font=("Arial", 16), bg="#293133", fg="white")
        lbl_prenom.place(x=0, y=200, width=200)
        self.entrer_prenom = Entry(self)
        self.entrer_prenom.place(x=200, y=200, width=200, height=30)

        # text age
        lbl_date = Label(self, text="Date Naissance", font=("Arial", 16), bg="#293133", fg="white")
        lbl_date.place(x=0, y=250, width=200)
        self.entrer_date = DateEntry(self)
        self.entrer_date.place(x=200, y=250, width=100, height=30)

        # text année scolaire
        lbl_annee = Label(self, text="Année Scolaire", font=("Arial", 16), bg="#293133", fg="white")
        lbl_annee.place(x=0, y=300, width=200)
        self.entrer_annee = Entry(self)
        self.entrer_annee.place(x=200, y=300, width="300", height=30)

        # text classe
        lbl_classe = Label(self, text="Classe", font=("Arial", 16), bg="#293133", fg="white")
        lbl_classe.place(x=0, y=350, width=200)
        self.entrer_classe = Entry(self)
        self.entrer_classe.place(x=200, y=350, width=200, height=30)

        # text commentaire
        lbl_commentaire = Label(self, text="Commentaire", font=("Arial", 16), bg="#293133", fg="white")
        lbl_commentaire.place(x=0, y=400, width=200)
        self.entrer_commentaire = Entry(self)
        self.entrer_commentaire.place(x=200, y=400, width=300, height=30)

        # Enregistrer
        btn_enregistrer = Button(self, text="Enregistrer", font=("Arial", 16), bg="#4FC031", fg="white",
                                 command=self.validate)
        btn_enregistrer.place(x=30, y=450, width=200)

        # modifier
        btn_modofier = Button(self, text="Modifier", font=("Arial", 16), bg="#005C96", fg="white",
                              command=self.modification)
        btn_modofier.place(x=270, y=450, width=200)

        # Supprimer
        btn_supprimer = Button(self, text="Supprimer", font=("Arial", 16), bg="red", fg="white",
                               command=self.delete)
        btn_supprimer.place(x=150, y=500, width=200)

        self.table = ttk.Treeview(self,
                                  columns=('numero', 'firstname', 'lastname', 'date', 'annee', 'class', 'moy', 'abs'),
                                  show="headings")
        self.table.place(x=500, y=150, width=760, height=450)

        self.table.heading('numero', text="Numéro")
        self.table.heading('firstname', text="Nom")
        self.table.heading('lastname', text="Prénom")
        self.table.heading('date', text="Date Naissance")
        self.table.heading('annee', text="Année")
        self.table.heading('class', text="Classe")
        self.table.heading('moy', text="Moyenne")
        self.table.heading('abs', text="Absence")

        self.table.column('numero', width=50)
        self.table.column('firstname', width=80)
        self.table.column('lastname', width=80)
        self.table.column('date', width=150)
        self.table.column('annee', width=60)
        self.table.column('class', width=50)
        self.table.column('moy', width=50)
        self.table.column('abs', width=50)
        results = self.etudiant.get_students()
        for item in results:
            self.table.insert('', END, values=item)
        self.table.bind("<Double-1>", self.on_double_click)

    def validate(self):
        scolarite = Scolarite(self.entrer_annee.get(),
                              self.entrer_classe.get().upper(), self.entrer_commentaire.get(), 2)
        etudiant = Etudiant(int(self.entrer_numero.get()), self.entrer_nom.get(), self.entrer_prenom.get(),
                            datetime.combine(self.entrer_date.get_date(), datetime.min.time()),
                            scolarite.annee_scolaire,
                            scolarite.classe, 0, 0)
        if etudiant.verify_numero():
            messagebox.showwarning(title="Notification", message="Numéro du dossier existe déjà")
        else:
            if not scolarite.verify_scol():
                self.connection.add_scolarite(scolarite)
            self.connection.add_student(etudiant)
            messagebox.showinfo(title="Notification", message="Création d'étudiant avec succès")
            etu = (
                etudiant.numero, etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.annee,
                etudiant.niveau,
                etudiant.moyenne, etudiant.absence)
            self.table.insert('', END, values=etu)
            self.cancel()

    def modification(self):
        scolarite = Scolarite(self.entrer_annee.get(),
                              self.entrer_classe.get().upper(), self.entrer_commentaire.get(), 2)
        etudiant = Etudiant(int(self.entrer_numero.get()), self.entrer_nom.get(), self.entrer_prenom.get(),
                            datetime.combine(self.entrer_date.get_date(), datetime.min.time()),
                            scolarite.annee_scolaire,
                            scolarite.classe, 0, 0)
        if etudiant.verify_numero():
            if scolarite.verify_scol():
                self.connection.update_scolarite(scolarite)
            else:
                messagebox.showwarning(title="Notification", message="L'année scolaire et la classe n'existe pas!!!")
            self.connection.update_student(etudiant)
            messagebox.showinfo(title="Notification", message="Modification d'étudiant avec succès")
            etu = (
                etudiant.numero, etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.annee,
                etudiant.niveau, etudiant.moyenne, etudiant.absence)
            selected_item = self.table.selection()[0]
            self.table.delete(selected_item)
            self.table.insert('', END, values=etu)
            self.cancel()
        else:
            messagebox.showwarning(title="Notification", message="Numéro du dossier n'existe pas!!!")

    def delete(self):
        scolarite = Scolarite(self.entrer_annee.get(),
                              self.entrer_classe.get().upper(), self.entrer_commentaire.get(), 2)
        etudiant = Etudiant(int(self.entrer_numero.get()), self.entrer_nom.get(), self.entrer_prenom.get(),
                            datetime.combine(self.entrer_date.get_date(), datetime.min.time()),
                            scolarite.annee_scolaire,
                            scolarite.classe, 0, 0)
        if etudiant.verify_numero():
            if messagebox.askyesno(title="Suppression d'un étudiant",
                                   message="Êtes-vous sûre de supprimer l'étudiant {} {}?".format(etudiant.nom,
                                                                                                  etudiant.prenom)):
                self.connection.delete_student(etudiant.numero)
                messagebox.showinfo(title="Notification", message="Suppression d'étudiant avec succès")
                selected_item = self.table.selection()[0]
                self.table.delete(selected_item)
                self.cancel()

        else:
            messagebox.showwarning(title="Notification", message="Numéro du dossier n'existe pas!!!")

    def recherche_window(self):
        r_window = Tk()
        r_window.title("Fenêtre de Recherche")
        r_window.geometry("400x400")
        r_frame = Frame(r_window, bg="#293133")
        r_frame.pack(fill="both", expand=True)
        lbl_recherche = Label(r_frame, text="Recherche")
        self.entrer_recherche = Entry(r_frame)
        b = Button(r_frame, text="Valider", command=self.recherche)
        lbl_recherche.place(x=100, y=100, width=200)
        self.entrer_recherche.place(x=100, y=140, width=200)
        b.place(x=140, y=190, width=120)
        r_window.mainloop()

    def moyenne_window(self):
        r_window = Tk()
        r_window.title("Mise à jour de la Moyenne")
        r_window.geometry("400x400")
        r_frame = Frame(r_window, bg="#293133")
        r_frame.pack(fill="both", expand=True)
        lbl_numero = Label(r_frame, text="Numéro")
        self.entrer_numero_m = Entry(r_frame)
        lbl_moyenne = Label(r_frame, text="Moyenne")
        self.entrer_moyenne = Entry(r_frame)
        b = Button(r_frame, text="Enrégistrer", command=self.valide_moyenne)
        lbl_numero.place(x=100, y=100, width=200)
        self.entrer_numero_m.place(x=100, y=120, width=200)
        lbl_moyenne.place(x=100, y=150, width=200)
        self.entrer_moyenne.place(x=100, y=170, width=200)
        b.place(x=140, y=200, width=120)
        r_window.mainloop()

    def absence_window(self):
        r_window = Tk()
        r_window.title("Fenêtre de gestion d'absence")
        r_window.geometry("400x400")
        r_frame = Frame(r_window, bg="#293133")
        r_frame.pack(fill="both", expand=True)
        lbl_absence_u = Label(r_frame, text="Numéro")
        self.entrer_absence_u = Entry(r_frame)
        b = Button(r_frame, text="Valider", command=self.save_absence)
        lbl_absence_u.place(x=100, y=100, width=200)
        self.entrer_absence_u.place(x=100, y=140, width=200)
        b.place(x=140, y=190, width=120)
        r_window.mainloop()

    def recherche(self):
        if self.entrer_recherche.get() is not None:
            results = self.connection.search_students(self.entrer_recherche.get())
            if results is None:
                messagebox.showwarning(title="Recherche", message="Aucun donnée ne correspond à votre recherche!!!")
            else:
                for item in self.table.get_children():
                    self.table.delete(item)
                if isinstance(results, tuple):
                    self.table.insert('', END, values=results)
                else:
                    for item in results:
                        self.table.insert('', END, values=item)

    def actualise_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        etudiant = Etudiant()
        results = etudiant.get_students()
        for item in results:
            self.table.insert('', END, values=item)

    def valide_moyenne(self):
        if self.entrer_numero_m.get() is not None:
            etudiant = Etudiant(numero=int(self.entrer_numero_m.get()), moyenne=int(self.entrer_moyenne.get()))
            if etudiant.verify_numero():
                etu = etudiant.get_one_student()
                new = Etudiant(etu[0], etu[1], etu[2], etu[3], etu[4], etu[5],
                               etudiant.moyenne, etu[7])
                self.connection.update_student(new)
                messagebox.showinfo(title="Information", message="Moyenne mise à jour avec succès")
                self.actualise_table()
            else:
                messagebox.showwarning(title="Information", message="Entrer un numéro correct!!!")

    def save_absence(self):
        if self.entrer_absence_u.get() is not None:
            etudiant = Etudiant(numero=int(self.entrer_absence_u.get()))
            new = etudiant.get_one_student()
            if new is not None:
                absence = 1
                if new[-1] is not None:
                    absence = absence + new[-1]
                e = Etudiant(new[0], new[1], new[2], new[3], new[4], new[5], new[6], absence)
                self.connection.update_student(e)
                messagebox.showinfo(title="Information", message="Absence mise à jour avec succès")
                self.actualise_table()
            else:
                messagebox.showwarning(title="Information", message="Entrer un numéro correct!!!")

    def cancel(self):
        self.entrer_commentaire.delete(first=0, last=len(self.entrer_commentaire.get()))
        self.entrer_classe.delete(first=0, last=len(self.entrer_classe.get()))
        self.entrer_annee.delete(first=0, last=len(self.entrer_annee.get()))
        self.entrer_date.delete(first=0, last=len(self.entrer_date.get()))
        self.entrer_prenom.delete(first=0, last=len(self.entrer_prenom.get()))
        self.entrer_nom.delete(first=0, last=len(self.entrer_nom.get()))
        self.entrer_numero.delete(first=0, last=len(str(self.entrer_numero.get())))

    def on_double_click(self, event):
        item = self.table.selection()[0]
        data = self.table.item(item)['values']
        scolarite = Scolarite(data[4], data[5])
        scol = scolarite.get_one_scol()

        if data is not None:
            self.cancel()
            self.entrer_numero.insert(0, data[0])
            self.entrer_nom.insert(0, data[1])
            self.entrer_prenom.insert(0, data[2])
            self.entrer_date.insert(0, data[3])
            self.entrer_annee.insert(0, data[4])
            self.entrer_classe.insert(0, data[5])
            if scol[2] is not None:
                self.entrer_commentaire.insert(0, scol[2])


if __name__ == "__main__":
    connection = Connection()
    connection.create_table()
    root = App()
    root.mainloop()
