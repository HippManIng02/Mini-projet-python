from datetime import datetime
import sqlite3


class Etudiant:

    def __init__(self, numero: int = 0, nom: str = "", prenom: str = "", date_naissance: datetime = None,
                 annee: str = "", niveau: str = "", moyenne: int = 0,
                 absence: int = 0):
        self.numero = numero
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.moyenne = moyenne
        self.absence = absence
        self.annee = annee
        self.niveau = niveau
        self.connection = Connection()
        self.students = self.get_students()

    @property
    def numero(self):
        return self.__numero

    @property
    def nom(self):
        return self.__nom

    @property
    def prenom(self):
        return self.__prenom

    @property
    def date_naissance(self):
        return self.__date_naissance


    @property
    def moyenne(self):
        return self.__moyenne

    @property
    def absence(self):
        return self.__absence

    @property
    def annee(self):
        return self.__annee

    @property
    def niveau(self):
        return self.__niveau

    @numero.setter
    def numero(self, numero: int):
        assert isinstance(numero, int), "numero must be an int"
        self.__numero = numero

    @nom.setter
    def nom(self, nom: str):
        assert isinstance(nom, str), "nom must be an str"
        self.__nom = nom

    @prenom.setter
    def prenom(self, prenom: str):
        assert isinstance(prenom, str), "prenom must be an str"
        self.__prenom = prenom

    @date_naissance.setter
    def date_naissance(self, date_naissance):
        # assert isinstance(date_naissance, datetime), "date of birthday must be an date"
        self.__date_naissance = date_naissance

    @moyenne.setter
    def moyenne(self, moyenne: int):
        self.__moyenne = moyenne

    @absence.setter
    def absence(self, absence: int):
        self.__absence = absence

    @annee.setter
    def annee(self, annee):
        self.__annee = annee

    @niveau.setter
    def niveau(self, niveau):
        self.__niveau = niveau

    def __str__(self):
        return "Numero : {}, Nom : {},Prenom: {}, DateNaissance: {}, Moyenne: {}, Absence:{}".format(
            self.numero,
            self.nom,
            self.prenom,
            self.date_naissance, self.moyenne, self.absence
        )

    def get_students(self):
        return self.connection.get_all_students()

    def verify_numero(self):
        existe = False
        for element in self.students:
            if element[0] == self.numero:
                existe = True
                break
        return existe

    def get_one_student(self):
        for element in self.students:
            if element[0] == self.numero:
                return element
        return None

    def update_students_liste(self, student):
        for element in self.students:
            if element[0] == self.numero:
                self.students.remove(element)
                break
        self.students.append(student)

    def delete_student_from_liste(self, numero):
        for element in self.students:
            if element[0] == numero:
                self.students.remove(element)
                break


class Scolarite:
    def __init__(self, annee_scolaire: str = "", classe: str = "", commentaire: str = "", semestre: int = 0,
                 ):
        self.annee_scolaire = annee_scolaire
        self.classe = classe
        self.commentaire = commentaire
        self.semestre = semestre
        self.connection = Connection()
        self.scolarites = self.get_scols()

    @property
    def annee_scolaire(self):
        return self.__annee_scolaire

    @property
    def classe(self):
        return self.__classe

    @property
    def commentaire(self):
        return self.__commentaire

    @property
    def semestre(self):
        return self.__semestre

    @annee_scolaire.setter
    def annee_scolaire(self, annee_scolaire: str):
        assert isinstance(annee_scolaire, str), "annee scolaire must be an str"
        self.__annee_scolaire = annee_scolaire

    @classe.setter
    def classe(self, classe: str):
        assert isinstance(classe, str), "Classe must be an str"
        self.__classe = classe

    @commentaire.setter
    def commentaire(self, commentaire: str):
        assert isinstance(commentaire, str), "Commentaire must be an str"
        self.__commentaire = commentaire

    @semestre.setter
    def semestre(self, semestre: int):
        self.__semestre = semestre

    def __str__(self):
        return "Annee Scolaire: {}, Classe: {}, Commentaire: {}, Semestre :{}".format(
            self.annee_scolaire,
            self.classe,
            self.commentaire,
            self.semestre)

    def get_scols(self):
        return self.connection.get_all_scolarite()

    def verify_scol(self):
        for element in self.scolarites:
            if (self.annee_scolaire == element[0]) and (self.classe == element[1]):
                return True
        return False

    def get_one_scol(self):
        for element in self.scolarites:
            if (self.annee_scolaire == element[0]) and (self.classe == element[1]):
                return element
        return None

    def update_scol_liste(self, scol):
        for element in self.scolarites:
            if (self.annee_scolaire == element[0]) and (self.classe == element[1]):
                self.scolarites.remove(element)
                break
        self.scolarites.append(scol)


class Connection:
    def __init__(self):
        self.conn = self.db_connect()

    def db_connect(self):
        conn = sqlite3.connect('./BD/Ecole.db')
        return conn

    def create_table(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS etudiant (numero INT PRIMARY KEY, nom VARCHAR(255), prenom VARCHAR("
            "255), date_naissance DATE, annee VARCHAR(255),niveau VARCHAR(255),moyenne INT, absence INT, FOREIGN KEY(annee, niveau) REFERENCES "
            "scolarite(annee, niveau))")

        self.conn.execute("CREATE TABLE IF NOT EXISTS scolarite (annee_scolaire "
                          "VARCHAR(20), classe VARCHAR(255),"
                          "commentaire VARCHAR(255),semestre INT, PRIMARY KEY("
                          "annee_scolaire, classe))")
        self.conn.commit()

    def add_student(self, etudiant):
        sql = "INSERT INTO etudiant (numero, nom, prenom, date_naissance, annee, niveau) VALUES ({}, '{}', '{}', " \
              "'{}', '{}', '{}')".format(
            etudiant.numero, etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.annee, etudiant.niveau
        )
        self.conn.execute(sql)
        self.conn.commit()
        etu = (etudiant.numero, etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.annee, etudiant.niveau, etudiant.moyenne, etudiant.absence)
        etudiant.students.append(etu)

    def update_student(self, etudiant):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE etudiant SET nom = ?, prenom = ?, date_naissance= ?, annee = ?, niveau = ?, moyenne= ?, absence = ? WHERE numero = ? ",
            (etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.annee, etudiant.niveau, etudiant.moyenne,etudiant.absence,
             etudiant.numero)
        )
        self.conn.commit()
        cur.close()
        etu = (etudiant.numero, etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.annee, etudiant.niveau, etudiant.moyenne, etudiant.absence)
        etudiant.update_students_liste(etu)

    def search_students(self, term):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM etudiant WHERE numero LIKE ? OR nom LIKE ? OR prenom LIKE ? OR annee=? OR niveau = ?",
            ('%' + term + '%', '%' + term + '%', '%' + term + '%', '%' + term + '%', '%' + term + '%',))
        result = cur.fetchall()
        cur.close()
        return result

    def get_all_students(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM etudiant")
        result = cur.fetchall()
        cur.close()
        return result

    def get_student_by_numero(self, numero):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM etudiant WHERE numero = ?", (numero,))
        result = cur.fetchone()
        cur.close()
        return result

    def delete_student(self, numero):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM etudiant WHERE numero = ?", (numero,))
        self.conn.commit()
        cur.close()
        etudiant = Etudiant()
        etudiant.delete_student_from_liste(numero)

    # Request from controle table
    def add_scolarite(self, scolarite: Scolarite):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO scolarite(annee_scolaire, classe, commentaire,semestre) VALUES(?,?,?,?)",
            (
                scolarite.annee_scolaire, scolarite.classe, scolarite.commentaire, scolarite.semestre))
        self.conn.commit()
        cur.close()
        scol = (
            scolarite.annee_scolaire, scolarite.classe, scolarite.commentaire, scolarite.semestre)
        scolarite.scolarites.append(scol)

    def update_scolarite(self, scolarite: Scolarite):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE scolarite SET commentaire= ?, semestre= ? WHERE annee_scolaire=? AND classe=?",
            (scolarite.commentaire, scolarite.semestre, scolarite.annee_scolaire,
             scolarite.classe))
        self.conn.commit()
        cur.close()
        scol = (
            scolarite.annee_scolaire, scolarite.classe, scolarite.commentaire, scolarite.semestre)
        scolarite.update_scol_liste(scol)

    def get_all_scolarite(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM scolarite")
        result = cur.fetchall()
        cur.close()
        return result

