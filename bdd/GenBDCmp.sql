set datestyle to "ISO , DMY";

drop table  RESERVATIONS;
drop table DEFCLASSES;
drop table  VOLS;
drop table CLIENTS;
drop table AVIONS;
drop table PILOTES;


create Table AVIONS(
NumAv integer primary key,
NomAv varchar(20) , 
CapAv integer,
VilleAv varchar(15)  );

create Table PILOTES
(	NumPil integer primary Key,
	NomPil Varchar(20) ,
	NaisPil integer,
	VillePil varchar(15)   );

Create Table CLIENTS
(	NumCl integer primary Key,
	NomCl varchar(20) ,
	NumRueCl integer ,
	NomRueCl varchar(50),
	CodePosteCl integer,
	VilleCl varchar(15)  );

Create Table VOLS
(	NumVol varchar(5) primary Key,
	VilleD varchar(15),
	VilleA varchar(15),
	DateD Date,
	   HD time,
	DateA Date,
	   HA time,
	NumPil integer  references PILOTES,
	NumAv integer references AVIONS );

Create Table DEFCLASSES
(	NumVol varchar(5) references VOLS,
	Classe varchar(12),
	CoeffPrix integer,
	 primary Key (NumVol,Classe) );

Create Table RESERVATIONS
(	NumCl integer  references CLIENTS,
	NumVol varchar(5),
	Classe varchar(12),
	NbPlaces integer,
	 primary Key (NumCl, NumVol, Classe),
  foreign key (NumVol,Classe) references DEFCLASSES(NumVol,Classe)  );
  
 \copy AVIONS from AVIONS.txt
\copy PILOTES from PILOTES.txt
\copy CLIENTS from CLIENTS.txt
\copy VOLS from VOLS.txt
\copy DEFCLASSES from DEFCLASSES.txt
\copy RESERVATIONS from RESERVATIONS.txt



